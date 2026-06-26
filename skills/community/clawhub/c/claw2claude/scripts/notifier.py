#!/usr/bin/env python3
"""
notifier.py — Polls for Claude's completion and sends chunked results back to the user.

Spawned by launch.sh before Claude starts. Polls every 2 seconds for a notify
JSON file written by parse_stream.py. When found, chunks the summary by section
and sends each piece individually, then exits.

Delivery strategy (in priority order):
  1. openclaw 'message' tool via gateway — works for all platforms (discord, whatsapp, telegram, …)
  2. Discord bot API directly            — Discord-only fallback when gateway is unreachable
  3. macOS notification                  — last-resort local fallback

Usage:
  notifier.py --notify-file <path> --project <name>
              [--watcher-pid <pid>]
              [--session-key <key>]
              [--config <path>]
              [--max-wait <seconds>]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

MAX_CHUNK     = 500
POLL_INTERVAL = 2  # seconds

DISCORD_API = "https://discord.com/api/v10"

parser = argparse.ArgumentParser()
parser.add_argument("--notify-file",  required=True)
parser.add_argument("--project",      required=True)
parser.add_argument("--watcher-pid",  type=int, default=0,
                    help="PID of launch.sh. When it exits, notifier knows Claude finished.")
parser.add_argument("--session-key",  default="main")
parser.add_argument("--config",
    default=str(Path.home() / ".openclaw" / "openclaw.json"))
parser.add_argument("--max-wait",     type=int, default=2100,
                    help="Max seconds to wait before giving up (default: 35 min)")
args = parser.parse_args()

NOTIFY_FILE = Path(args.notify_file)


# ── Config loader ─────────────────────────────────────────────────

def load_config(config_path: str) -> dict:
    try:
        return json.loads(Path(config_path).read_text(encoding="utf-8"))
    except Exception:
        return {}

_cfg_cache: dict = {}

def cfg() -> dict:
    global _cfg_cache
    if not _cfg_cache:
        _cfg_cache = load_config(args.config)
    return _cfg_cache


# ── Session key parser ────────────────────────────────────────────

def parse_session_key(key: str) -> dict:
    """
    Parse keys like:
      agent:main:discord:channel:1490483473645965342
      agent:main:whatsapp:direct:+818045624604
    Returns dict with 'platform', 'chat_type', 'id' (or empty strings).
    """
    parts = key.split(":")
    # Expected: agent:<agent>:<platform>:<chat_type>:<id>
    if len(parts) >= 5:
        return {"platform": parts[2], "chat_type": parts[3], "id": parts[4]}
    return {"platform": "", "chat_type": "", "id": ""}


# ── Discord direct delivery ───────────────────────────────────────

def discord_send(channel_id: str, text: str) -> bool:
    token = cfg().get("channels", {}).get("discord", {}).get("token", "")
    if not token:
        print("[notifier] ⚠️  No Discord token in config", flush=True)
        return False

    payload = json.dumps({"content": text}).encode()
    req = urllib.request.Request(
        f"{DISCORD_API}/channels/{channel_id}/messages",
        data=payload,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/openclaw, 1.0)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
            msg_id = resp.get("id", "")
            print(f"[notifier] ✅ Discord sent (msg_id={msg_id})", flush=True)
            return True
    except urllib.error.HTTPError as e:
        body = e.read(300).decode(errors="replace")
        print(f"[notifier] ⚠️  Discord HTTP {e.code}: {body}", flush=True)
        return False
    except Exception as e:
        print(f"[notifier] ⚠️  Discord send failed: {e}", flush=True)
        return False


# ── Gateway tool caller ───────────────────────────────────────────

def gateway_invoke(tool: str, tool_args: dict) -> tuple[bool, dict]:
    """Call any allowed tool via the openclaw gateway. Returns (ok, result_dict)."""
    c     = cfg()
    port  = c.get("gateway", {}).get("port", 18789)
    token = c.get("gateway", {}).get("auth", {}).get("token", "")
    url   = f"http://127.0.0.1:{port}"

    payload = json.dumps({"tool": tool, "args": tool_args}).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{url}/tools/invoke",
                                 data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
        return resp.get("ok", False), resp
    except Exception as e:
        print(f"[notifier] ⚠️  gateway_invoke({tool}) failed: {e}", flush=True)
        return False, {}


def message_send(platform: str, target: str, text: str) -> bool:
    """
    Send via openclaw 'message' tool — works for all platforms.
    Uses 'target' (not the legacy 'to') for correct routing.
    """
    ok, resp = gateway_invoke("message", {
        "action":  "send",
        "channel": platform,
        "target":  target,
        "text":    text,
    })
    if ok:
        print(f"[notifier] ✅ message sent via gateway ({platform}→{target})", flush=True)
    else:
        err = resp.get("error", {})
        print(f"[notifier] ⚠️  message tool error: {err}", flush=True)
    return ok


# ── macOS notification fallback ───────────────────────────────────

def macos_notify(title: str, body: str):
    try:
        safe_title = title.replace('"', "'")
        safe_body  = body[:200].replace('"', "'").replace("\n", " ")
        script = f'display notification "{safe_body}" with title "{safe_title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", script], check=False, timeout=5)
        print("[notifier] 🔔 macOS notification sent", flush=True)
    except Exception as e:
        print(f"[notifier] ⚠️  macOS notification failed: {e}", flush=True)


# ── Unified send ──────────────────────────────────────────────────

# Platforms supported by the openclaw message tool
SUPPORTED_PLATFORMS = {
    "discord", "whatsapp", "telegram", "slack",
    "signal", "line", "matrix", "mattermost",
    "irc", "zalo", "feishu",
}

def send_one(text: str) -> bool:
    """
    Send a single chunk to the user. Delivery priority:
      1. openclaw 'message' tool via gateway  — works for all supported platforms
      2. Discord bot API directly             — Discord-only fallback if gateway is down
      3. macOS notification                   — handled by caller as last resort
    """
    sk   = parse_session_key(args.session_key)
    plat = sk["platform"]
    cid  = sk["id"]

    if not plat or not cid:
        print(f"[notifier] ⚠️  Cannot parse session key: {args.session_key}", flush=True)
        return False

    if plat not in SUPPORTED_PLATFORMS:
        print(f"[notifier] ⚠️  Unknown platform '{plat}' — skipping", flush=True)
        return False

    # 1. openclaw message tool (universal)
    if message_send(plat, cid, text):
        return True

    # 2. Discord-only direct API fallback (when gateway is unreachable)
    if plat == "discord":
        print("[notifier] Falling back to Discord bot API …", flush=True)
        return discord_send(cid, text)

    return False


# ── Chunking ─────────────────────────────────────────────────────

def split_chunks(text: str, max_chars: int = MAX_CHUNK) -> list:
    """
    Split text into chunks ≤ max_chars.
    Primary split: markdown section headings (# / ## / ###).
    Secondary split: sentence boundaries for oversized sections.
    Hard split as last resort.
    """
    # Split keeping the heading at the start of each section
    sections = re.split(r'(?=^#{1,3} )', text, flags=re.MULTILINE)
    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        if len(section) <= max_chars:
            chunks.append(section)
            continue

        # Section too long — split at sentence boundaries
        buf = ""
        # Split on ". ", "! ", "? ", or newlines
        for piece in re.split(r'(?<=[\.\!\?])\s+|\n{2,}', section):
            piece = piece.strip()
            if not piece:
                continue
            candidate = (buf + "\n" + piece).strip() if buf else piece
            if len(candidate) <= max_chars:
                buf = candidate
            else:
                if buf:
                    chunks.append(buf)
                # Single piece still too long — hard split
                while len(piece) > max_chars:
                    chunks.append(piece[:max_chars])
                    piece = piece[max_chars:].strip()
                buf = piece
        if buf:
            chunks.append(buf)

    return chunks


# ── Delivery ─────────────────────────────────────────────────────

def deliver(data: dict):
    project  = args.project
    mode     = data.get("mode", "execute")
    if mode not in ("discuss", "execute"):
        print(f"[notifier] ⚠️  Unknown mode '{mode}' — assuming execute", flush=True)
        mode = "execute"
    summary  = data.get("summary", "").strip()
    status   = data.get("status", "done")
    log_path = data.get("log_path", "")

    def send(msg: str):
        ok = send_one(msg)
        time.sleep(0.4)
        return ok

    # ── 1. Header ─────────────────────────────────────────────────
    if status == "error":
        send(f"❌ Claude Code error · {project}")
    else:
        label = "Discussion complete" if mode == "discuss" else "Execution complete"
        send(f"✅ {label} · {project}")

    # ── 2. Summary chunks ─────────────────────────────────────────
    if summary:
        chunks = split_chunks(summary)
        print(f"[notifier] Sending {len(chunks)} chunk(s) …", flush=True)
        for i, chunk in enumerate(chunks, 1):
            print(f"[notifier] chunk {i}/{len(chunks)} ({len(chunk)} chars)", flush=True)
            send(chunk)
    else:
        send("(no summary available)")

    # ── 3. Footer / call to action ────────────────────────────────
    if status == "error":
        footer = "⚠️ Claude Code exited unexpectedly. Check the log for details."
    elif mode == "discuss":
        footer = "Ready to start building? Reply and I'll kick off implementation."
    else:
        footer = "Please verify the result in your project directory."

    if log_path:
        footer += f"\n📄 Full log: {log_path}"

    if not send(footer):
        # All delivery methods failed — fall back to macOS notification
        macos_notify(
            title=f"{'✅' if status == 'done' else '❌'} Claude Code · {project}",
            body=summary[:200] if summary else "Task complete.",
        )


# ── Process helper ────────────────────────────────────────────────

def is_running(pid: int) -> bool:
    """Return True if the process is still alive (or if pid <= 0 = unknown)."""
    if pid <= 0:
        return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


# ── Main poll loop ────────────────────────────────────────────────

print(f"[notifier] Started — project={args.project} session={args.session_key} "
      f"pid_watch={args.watcher_pid}", flush=True)

deadline = time.time() + args.max_wait
last_pid_alive = True

while time.time() < deadline:
    # Check for completion file first
    if NOTIFY_FILE.exists():
        try:
            data = json.loads(NOTIFY_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[notifier] Failed to parse notify file: {e} — retrying", flush=True)
            time.sleep(POLL_INTERVAL)
            continue

        print("[notifier] Notify file found — delivering chunks", flush=True)
        deliver(data)
        # Clean up notify file
        try:
            NOTIFY_FILE.unlink()
        except OSError:
            pass
        print("[notifier] Done — exiting", flush=True)
        sys.exit(0)

    # Check if the watcher process (launch.sh) has exited
    pid_alive = is_running(args.watcher_pid)
    if last_pid_alive and not pid_alive:
        # Launcher just died. parse_stream.py may still be writing the notify
        # file (it runs inside the pipe, so it outlives launch.sh by a moment).
        # Keep polling for up to 30 seconds before giving up.
        print(f"[notifier] Watcher PID={args.watcher_pid} exited — waiting up to 30s for notify file", flush=True)
        grace_deadline = time.time() + 30
        while time.time() < grace_deadline:
            if NOTIFY_FILE.exists():
                break
            time.sleep(POLL_INTERVAL)
        if NOTIFY_FILE.exists():
            # Let the main loop handle it on the next iteration
            last_pid_alive = pid_alive
            continue
        # File never appeared — treat as crash
        print("[notifier] No notify file after 30s grace — sending error notice", flush=True)
        deliver({
            "status":  "error",
            "mode":    "execute",
            "summary": "Claude Code exited without producing a result (timeout or crash).",
        })
        sys.exit(1)

    last_pid_alive = pid_alive
    time.sleep(POLL_INTERVAL)

# Deadline reached
print("[notifier] Max wait exceeded — giving up", flush=True)
deliver({
    "status":  "error",
    "mode":    "execute",
    "summary": "Claude Code did not complete within the maximum wait period.",
})
sys.exit(1)
