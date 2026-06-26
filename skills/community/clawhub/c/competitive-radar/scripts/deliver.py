#!/usr/bin/env python3
"""
deliver.py — Routes the weekly digest to configured channels.

Supports: Slack (webhook or bot token), Telegram, WhatsApp (via WhatsApp Business API
or Twilio), Discord webhook.

Reads delivery config from competitors.json -> notify_channels per competitor,
or from DELIVER_CONFIG env var (JSON string) for global override.

Usage:
  python3 deliver.py <digest_md_path> [--channels slack:#general telegram discord]
  python3 deliver.py --latest                  # deliver today's saved digest
"""

from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
DIGESTS_DIR = DATA_DIR / "digests"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

TODAY = date.today().isoformat()

# Max message length by platform
PLATFORM_LIMITS = {
    "telegram": 4096,
    "slack": 3000,
    "discord": 2000,
    "whatsapp": 1600,
}


# ---------------------------------------------------------------------------
# Message formatters (platform-specific)
# ---------------------------------------------------------------------------

def format_for_telegram(md: str) -> str:
    """Telegram supports basic Markdown. Strip unsupported elements."""
    # Escape special chars that aren't part of formatting
    text = md.replace("━", "—").replace("═", "=").replace("⚪", "○")
    # Telegram MarkdownV2 doesn't like bare underscores
    text = re.sub(r"(?<!\*)\*(?!\*)", "", text)
    return text


def format_for_slack(md: str) -> str:
    """Slack uses mrkdwn — convert Markdown to Slack-flavored text."""
    text = md
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    # Strip bare #hashtag headers — Slack doesn't render them
    text = re.sub(r"^#{1,3} (.+)$", r"*\1*", text, flags=re.MULTILINE)
    return text


def format_for_discord(md: str) -> str:
    """Discord supports standard Markdown."""
    return md


def format_for_whatsapp(md: str) -> str:
    """WhatsApp has very limited formatting. Strip most markdown."""
    text = re.sub(r"[*_~`#]", "", md)
    text = md.replace("━", "-").replace("═", "=")
    # Shorten aggressively for WhatsApp's 1600 char limit per message
    return text


def chunk_message(text: str, max_len: int) -> list[str]:
    """Split message into chunks at paragraph boundaries."""
    if len(text) <= max_len:
        return [text]
    chunks = []
    current = ""
    for para in text.split("\n\n"):
        candidate = current + "\n\n" + para if current else para
        if len(candidate) > max_len:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current = candidate
    if current:
        chunks.append(current.strip())
    return chunks or [text[:max_len]]


# ---------------------------------------------------------------------------
# Platform senders
# ---------------------------------------------------------------------------

def send_slack(text: str, channel_config: str) -> bool:
    """
    channel_config: 'slack:#channel-name' or a full webhook URL.
    Uses SLACK_BOT_TOKEN env var if available, otherwise SLACK_WEBHOOK_URL.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    bot_token = os.environ.get("SLACK_BOT_TOKEN", "")

    # Parse channel name
    channel = channel_config.replace("slack:", "").strip()
    if channel.startswith("https://"):
        webhook_url = channel
        channel = ""

    formatted = format_for_slack(text)
    chunks = chunk_message(formatted, PLATFORM_LIMITS["slack"])

    for i, chunk in enumerate(chunks):
        payload: dict = {}
        if bot_token and channel:
            payload = {"channel": channel, "text": chunk, "mrkdwn": True}
            cmd = [
                "curl", "-sS", "-X", "POST",
                "https://slack.com/api/chat.postMessage",
                "-H", f"Authorization: Bearer {bot_token}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload),
            ]
        elif webhook_url:
            payload = {"text": chunk}
            cmd = [
                "curl", "-sS", "-X", "POST", webhook_url,
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload),
            ]
        else:
            print("[deliver/slack] No SLACK_BOT_TOKEN or SLACK_WEBHOOK_URL set",
                  file=sys.stderr)
            return False

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            resp = result.stdout
            if '"ok":false' in resp or '"error"' in resp:
                print(f"[deliver/slack] API error: {resp[:200]}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"[deliver/slack] Error: {e}", file=sys.stderr)
            return False

    print(f"[deliver/slack] Sent {len(chunks)} message(s) to {channel or 'webhook'}")
    return True


def send_telegram(text: str, _config: str = "") -> bool:
    """
    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("[deliver/telegram] TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID required",
              file=sys.stderr)
        return False

    formatted = format_for_telegram(text)
    chunks = chunk_message(formatted, PLATFORM_LIMITS["telegram"])

    for chunk in chunks:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        cmd = [
            "curl", "-sS", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            resp = json.loads(result.stdout) if result.stdout else {}
            if not resp.get("ok"):
                print(f"[deliver/telegram] Error: {resp.get('description', result.stdout[:200])}",
                      file=sys.stderr)
                return False
        except Exception as e:
            print(f"[deliver/telegram] Error: {e}", file=sys.stderr)
            return False

    print(f"[deliver/telegram] Sent {len(chunks)} message(s)")
    return True


def send_discord(text: str, config: str = "") -> bool:
    """
    config: 'discord' or a webhook URL.
    Requires DISCORD_WEBHOOK_URL env var if not passed in config.
    """
    webhook_url = (
        config if config.startswith("https://") else
        os.environ.get("DISCORD_WEBHOOK_URL", "")
    )
    if not webhook_url:
        print("[deliver/discord] DISCORD_WEBHOOK_URL required", file=sys.stderr)
        return False

    formatted = format_for_discord(text)
    chunks = chunk_message(formatted, PLATFORM_LIMITS["discord"])

    for chunk in chunks:
        payload = {"content": chunk}
        cmd = [
            "curl", "-sS", "-X", "POST", webhook_url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode != 0:
                print(f"[deliver/discord] curl failed: {result.stderr[:100]}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"[deliver/discord] Error: {e}", file=sys.stderr)
            return False

    print(f"[deliver/discord] Sent {len(chunks)} message(s)")
    return True


def send_whatsapp(text: str, _config: str = "") -> bool:
    """
    Sends via Twilio WhatsApp API.
    Requires: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_WHATSAPP, TWILIO_TO_WHATSAPP
    """
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    from_num = os.environ.get("TWILIO_FROM_WHATSAPP", "")
    to_num = os.environ.get("TWILIO_TO_WHATSAPP", "")

    if not all([sid, token, from_num, to_num]):
        print("[deliver/whatsapp] Twilio env vars required: "
              "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, "
              "TWILIO_FROM_WHATSAPP, TWILIO_TO_WHATSAPP", file=sys.stderr)
        return False

    formatted = format_for_whatsapp(text)
    chunks = chunk_message(formatted, PLATFORM_LIMITS["whatsapp"])
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"

    for chunk in chunks:
        cmd = [
            "curl", "-sS", "-X", "POST", url,
            "-u", f"{sid}:{token}",
            "--data-urlencode", f"From=whatsapp:{from_num}",
            "--data-urlencode", f"To=whatsapp:{to_num}",
            "--data-urlencode", f"Body={chunk}",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            resp = json.loads(result.stdout) if result.stdout else {}
            if resp.get("status") == 400 or "error" in str(resp.get("message", "")).lower():
                print(f"[deliver/whatsapp] Error: {resp}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"[deliver/whatsapp] Error: {e}", file=sys.stderr)
            return False

    print(f"[deliver/whatsapp] Sent {len(chunks)} message(s)")
    return True


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

PLATFORM_SENDERS = {
    "slack": send_slack,
    "telegram": send_telegram,
    "discord": send_discord,
    "whatsapp": send_whatsapp,
}


def deliver(text: str, channels: list[str]) -> dict[str, bool]:
    """
    Deliver text to all specified channels.
    channels: list of strings like ['slack:#intel', 'telegram', 'discord']
    Returns: dict of channel -> success bool
    """
    results = {}
    for channel in channels:
        platform = channel.split(":")[0].lower()
        sender = PLATFORM_SENDERS.get(platform)
        if not sender:
            print(f"[deliver] Unknown platform: {platform}", file=sys.stderr)
            results[channel] = False
            continue
        results[channel] = sender(text, channel)
    return results


def get_all_channels() -> list[str]:
    """Collect all unique notify_channels from all active competitors."""
    if not COMPETITORS_FILE.exists():
        return []
    data = json.loads(COMPETITORS_FILE.read_text())
    channels: set[str] = set()
    for c in data.get("competitors", []):
        if c.get("active", True):
            channels.update(c.get("notify_channels", []))
    return list(channels)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar delivery")
    parser.add_argument("digest_path", nargs="?", help="Path to digest Markdown file")
    parser.add_argument("--latest", action="store_true",
                        help="Deliver today's saved digest")
    parser.add_argument("--channels", nargs="*",
                        help="Override channels (e.g. slack:#intel telegram)")
    args = parser.parse_args()

    # Resolve digest file
    if args.latest:
        digest_file = DIGESTS_DIR / f"{TODAY}.md"
    elif args.digest_path:
        digest_file = Path(args.digest_path)
    else:
        parser.print_help()
        sys.exit(1)

    if not digest_file.exists():
        print(f"[deliver] Digest file not found: {digest_file}", file=sys.stderr)
        sys.exit(1)

    digest_text = digest_file.read_text(encoding="utf-8")

    # Resolve channels
    channels = args.channels if args.channels else get_all_channels()
    if not channels:
        print("[deliver] No channels configured. Set notify_channels in competitors.json "
              "or pass --channels", file=sys.stderr)
        sys.exit(1)

    print(f"[deliver] Delivering to: {channels}")
    results = deliver(digest_text, channels)

    for channel, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {channel}")

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
