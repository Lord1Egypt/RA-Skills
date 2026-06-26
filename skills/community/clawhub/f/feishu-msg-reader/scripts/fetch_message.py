#!/usr/bin/env python3
"""
Fetch Feishu message content by message_id, with thread context support.

Usage:
    python3 fetch_message.py <message_id> [--thread] [--raw]

Supports all msg_types: text, post, interactive, image, merge_forward, etc.
For interactive cards, body.content only contains fallback text (Feishu API limitation).
Use --thread to also fetch thread context (root + siblings) for richer content.

Auth: reads credentials from OpenClaw config (~/.openclaw/openclaw.json) automatically,
or set FEISHU_APP_ID + FEISHU_APP_SECRET env vars, or pass --token.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

FEISHU_BASE = "https://open.feishu.cn/open-apis"


def get_openclaw_feishu_creds():
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        return None, None
    with open(config_path) as f:
        config = json.load(f)
    feishu = config.get("channels", {}).get("feishu", {})
    app_id = feishu.get("appId")
    app_secret = feishu.get("appSecret")
    if not app_id or not app_secret:
        for acc in feishu.get("accounts", {}).values():
            if acc.get("appId") and acc.get("appSecret"):
                app_id = acc["appId"]
                app_secret = acc["appSecret"]
                break
    return app_id, app_secret


def get_tenant_token(app_id, app_secret):
    url = f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code", -1) != 0:
        raise RuntimeError(f"Failed to get token: {result}")
    return result["tenant_access_token"]


def feishu_get(token, path):
    url = f"{FEISHU_BASE}{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def fetch_message(token, message_id):
    return feishu_get(token, f"/im/v1/messages/{message_id}")


def fetch_chat_messages(token, chat_id, start_time, end_time, page_size=50):
    path = (f"/im/v1/messages?container_id_type=chat&container_id={chat_id}"
            f"&start_time={start_time}&end_time={end_time}"
            f"&page_size={page_size}&sort_type=ByCreateTimeAsc")
    return feishu_get(token, path)


def parse_content(body_content, msg_type):
    """Parse body.content JSON string into structured data."""
    try:
        parsed = json.loads(body_content)
    except (json.JSONDecodeError, TypeError):
        return body_content

    if msg_type == "text":
        return parsed.get("text", parsed) if isinstance(parsed, dict) else parsed
    return parsed


def format_message(item):
    """Format a single message item."""
    msg_type = item.get("msg_type", "unknown")
    body_content = item.get("body", {}).get("content", "")
    sender = item.get("sender", {})

    result = {
        "message_id": item.get("message_id"),
        "msg_type": msg_type,
        "sender_id": sender.get("id"),
        "sender_type": sender.get("sender_type"),
        "chat_id": item.get("chat_id"),
        "create_time": item.get("create_time"),
        "root_id": item.get("root_id") or None,
        "parent_id": item.get("parent_id") or None,
        "content": parse_content(body_content, msg_type),
    }

    if msg_type == "interactive":
        result["_note"] = (
            "Feishu API limitation: interactive card body.content only contains "
            "fallback/degraded text, not the full card JSON. Use --thread to get "
            "surrounding context for more information."
        )

    return result


def get_thread_messages(token, item):
    """Fetch thread context: root message + all replies."""
    root_id = item.get("root_id")
    chat_id = item.get("chat_id")
    if not root_id or not chat_id:
        return []

    # Fetch root message
    root_resp = fetch_message(token, root_id)
    root_items = root_resp.get("data", {}).get("items", [])
    root_create = None
    if root_items:
        root_create = root_items[0].get("create_time")

    # Fetch messages in a time window around the thread
    create_time = item.get("create_time", "0")
    # Use root create time as start, current message + buffer as end
    start_ts = int(root_create or create_time) // 1000 - 1
    end_ts = int(create_time) // 1000 + 60

    chat_resp = fetch_chat_messages(token, chat_id, start_ts, end_ts, 50)
    all_items = chat_resp.get("data", {}).get("items", [])

    # Filter to same thread
    thread_items = [m for m in all_items
                    if m.get("root_id") == root_id or m.get("message_id") == root_id]

    # Sort by create_time
    thread_items.sort(key=lambda m: int(m.get("create_time", "0")))
    return thread_items


def resolve_token(args):
    if args.token:
        return args.token
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        app_id, app_secret = get_openclaw_feishu_creds()
    if not app_id or not app_secret:
        print("Error: Provide --token, set FEISHU_APP_ID/FEISHU_APP_SECRET, "
              "or have OpenClaw config at ~/.openclaw/openclaw.json", file=sys.stderr)
        sys.exit(1)
    return get_tenant_token(app_id, app_secret)


def main():
    parser = argparse.ArgumentParser(description="Fetch Feishu message content by message_id")
    parser.add_argument("message_id", help="Message ID (om_xxx)")
    parser.add_argument("--token", help="tenant_access_token (auto if not provided)")
    parser.add_argument("--thread", action="store_true",
                        help="Also fetch thread context (root + replies)")
    parser.add_argument("--raw", action="store_true", help="Print raw API response")
    args = parser.parse_args()

    token = resolve_token(args)
    response = fetch_message(token, args.message_id)

    if args.raw:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return

    if response.get("code") != 0:
        print(json.dumps(response, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    items = response.get("data", {}).get("items", [])
    if not items:
        print("No message found", file=sys.stderr)
        sys.exit(1)

    target = items[0]
    result = format_message(target)

    if args.thread and (target.get("root_id") or target.get("parent_id")):
        thread_items = get_thread_messages(token, target)
        result["thread"] = [format_message(m) for m in thread_items]
        result["thread_count"] = len(thread_items)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
