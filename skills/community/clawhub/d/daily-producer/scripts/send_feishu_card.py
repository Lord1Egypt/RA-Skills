#!/usr/bin/env python3
"""
Send a Feishu interactive card (or plain text) to a group chat.

Usage:
    # Send a link card for the daily report:
    python3 send_feishu_card.py <report_url> [<chat_id>]

    # Send a plain text missing-reminder:
    python3 send_feishu_card.py --text "今日日报尚未产出，请检查生成链路。" [<chat_id>]

If chat_id is omitted, defaults to oc_fbfb0a5e15e2487bac8ec64edd3443c9.
Reads Feishu app credentials from ~/.openclaw/openclaw.json.
"""
from __future__ import annotations
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

OPENCLAW_CFG = Path.home() / ".openclaw" / "openclaw.json"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

# Skill root: parent of scripts/
SKILL_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = SKILL_ROOT / "config" / "profile.yaml"


def _grep_profile(key_path: str) -> str:
    """
    Extract a scalar value from profile.yaml by dot-separated key path
    (e.g. 'feishu.notification.chat_id').  Returns empty string if not found.
    Uses pyyaml when available, otherwise falls back to a line-scan heuristic.
    """
    if not PROFILE_PATH.exists():
        return ""
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
        for part in key_path.split("."):
            if not isinstance(data, dict):
                return ""
            data = data.get(part, "")
        return str(data) if data else ""
    except Exception:
        pass
    # Fallback: scan lines for the last component of the key path
    target_key = key_path.split(".")[-1]
    for line in PROFILE_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, _, rest = stripped.partition(":")
        if key.strip() != target_key:
            continue
        # Strip inline comment
        val = rest.split("#")[0].strip().strip('"').strip("'")
        if val:
            return val
    return ""


def _profile_chat_id() -> str:
    """Return chat_id from profile.yaml feishu.notification.chat_id, or empty string."""
    v = _grep_profile("feishu.notification.chat_id")
    if not v:
        v = _grep_profile("feishu.group_id")
    return v


def _profile_public_url() -> str:
    """Return server.public_url from profile.yaml."""
    return _grep_profile("server.public_url")


def _post(url: str, payload: dict, headers: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


def get_tenant_token(app_id: str, app_secret: str) -> str:
    resp = _post(
        f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if resp.get("code") != 0:
        raise RuntimeError(f"get_token failed: {resp}")
    return resp["tenant_access_token"]


_PRIORITY_ICON = {"major": "🔥", "notable": "🚀", "normal": "📌", "minor": "💡"}


def _load_top_articles(date_str: str) -> list[dict]:
    """
    Load the top 3 articles from output/daily/{date}.json.
    Returns list of dicts with 'title', 'priority', 'source'.
    """
    json_path = SKILL_ROOT / "output" / "daily" / f"{date_str}.json"
    if not json_path.exists():
        return []
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        articles = data.get("articles", [])
        # Sort: major first, then notable, then normal
        order = {"major": 0, "notable": 1, "normal": 2, "minor": 3}
        articles = sorted(articles, key=lambda a: order.get(a.get("priority", "minor"), 3))
        return articles[:3]
    except Exception:
        return []


def build_card(report_url: str, date_str: str) -> dict:
    """Build a Feishu interactive card with real article headlines from the JSON."""
    articles = _load_top_articles(date_str)

    elements: list[dict] = []

    if articles:
        # Build preview lines: icon + title for each top article
        lines = []
        for a in articles:
            icon = _PRIORITY_ICON.get(a.get("priority", "normal"), "📌")
            title = a.get("title", "").strip()
            if title:
                lines.append(f"{icon} {title}")
        if lines:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "\n".join(lines),
                },
            })
        # Divider
        elements.append({"tag": "hr"})
    else:
        # Fallback when JSON not available
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "今日 AI 情报已生成，点击下方按钮查看完整日报。",
            },
        })

    # Action button
    elements.append({
        "tag": "action",
        "actions": [
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "打开今日日报"},
                "url": report_url,
                "type": "primary",
            }
        ],
    })

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "blue",
            "title": {"tag": "plain_text", "content": f"📰 AI 日报 · {date_str}"},
        },
        "elements": elements,
    }


def send_card(token: str, chat_id: str, report_url: str, date_str: str) -> dict:
    card = build_card(report_url, date_str)
    payload = {
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False),
    }
    resp = _post(
        f"{FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id",
        payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp


def send_text(token: str, chat_id: str, text: str) -> dict:
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }
    resp = _post(
        f"{FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id",
        payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp


def _load_credentials() -> tuple[str, str]:
    """Return (app_id, app_secret) from openclaw.json.

    Account priority:
      1. feishu.notification.account_id in profile.yaml
      2. channels.feishu.defaultAccount in openclaw.json
      3. first account in openclaw.json
    """
    cfg = json.loads(OPENCLAW_CFG.read_text())
    feishu_cfg = cfg.get("channels", {}).get("feishu", {})
    accounts = feishu_cfg.get("accounts", {})

    # Prefer the account explicitly set in profile.yaml for notifications
    profile_acct_id = _grep_profile("feishu.notification.account_id")
    if profile_acct_id and profile_acct_id in accounts:
        acct_id = profile_acct_id
    else:
        acct_id = feishu_cfg.get("defaultAccount", "")
        if acct_id not in accounts:
            acct_id = next(iter(accounts))

    acct = accounts[acct_id]
    return acct["appId"], acct["appSecret"]


def main() -> None:
    args = sys.argv[1:]

    # Resolve default chat_id from profile.yaml
    default_chat_id = _profile_chat_id()
    if not default_chat_id:
        default_chat_id = "oc_fbfb0a5e15e2487bac8ec64edd3443c9"

    # --text mode: send plain text missing reminder
    if args and args[0] == "--text":
        if len(args) < 2:
            print("Usage: send_feishu_card.py --text <message> [<chat_id>]", file=sys.stderr)
            sys.exit(1)
        text = args[1]
        chat_id = args[2] if len(args) > 2 else default_chat_id
        app_id, app_secret = _load_credentials()
        token = get_tenant_token(app_id, app_secret)
        result = send_text(token, chat_id, text)
        if result.get("code") == 0:
            msg_id = result.get("data", {}).get("message_id", "")
            print(f"OK: message_id={msg_id}")
        else:
            print(f"ERROR: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
            sys.exit(1)
        return

    # Default mode: send interactive card with report URL
    if not args:
        print("Usage: send_feishu_card.py <report_url> [<chat_id>]", file=sys.stderr)
        sys.exit(1)

    report_url = args[0]
    chat_id = args[1] if len(args) > 1 else default_chat_id

    # Extract date from URL filename (e.g. 2026-04-14.html → 2026-04-14)
    filename = report_url.rstrip("/").split("/")[-1]
    date_str = filename.replace(".html", "")

    app_id, app_secret = _load_credentials()
    token = get_tenant_token(app_id, app_secret)
    result = send_card(token, chat_id, report_url, date_str)

    if result.get("code") == 0:
        msg_id = result.get("data", {}).get("message_id", "")
        print(f"OK: message_id={msg_id}")
    else:
        print(f"ERROR: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
