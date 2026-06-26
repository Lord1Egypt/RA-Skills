#!/usr/bin/env python3
"""Send a Feishu message via Open API.

Usage:
    python3 send.py --to <open_id|chat_id> --text "message"
    python3 send.py --to <open_id|chat_id> --text "message" --id-type <open_id|chat_id|user_id|union_id>
    python3 send.py --list-contacts
    python3 send.py --to "林智峰" --text "message"   # lookup by label in dms config

Reads app_id/app_secret from ~/.openclaw/openclaw.json automatically.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
FEISHU_API = "https://open.feishu.cn/open-apis"


def load_feishu_credentials():
    """Load appId and appSecret from openclaw.json."""
    with open(OPENCLAW_CONFIG, "r") as f:
        config = json.load(f)
    account = config["channels"]["feishu"]["accounts"]["default"]
    return account["appId"], account["appSecret"]


def load_dms_mapping():
    """Load DM contact mapping from openclaw.json."""
    with open(OPENCLAW_CONFIG, "r") as f:
        config = json.load(f)
    account = config["channels"]["feishu"]["accounts"]["default"]
    return account.get("dms", {})


def get_tenant_access_token(app_id, app_secret):
    """Get tenant_access_token from Feishu."""
    url = f"{FEISHU_API}/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code", -1) != 0:
        raise RuntimeError(f"Failed to get token: {result.get('msg', 'unknown error')}")
    return result["tenant_access_token"]


def resolve_recipient(to_value, dms_mapping):
    """Resolve a recipient: if it matches a label in dms, return the open_id."""
    # Direct open_id / chat_id / user_id
    if to_value.startswith(("ou_", "oc_", "on_", "cli_")):
        return to_value, None

    # Lookup by label
    for open_id, info in dms_mapping.items():
        label = info.get("label", "")
        if to_value == label or to_value in label:
            return open_id, label

    # Might be a raw ID without prefix
    return to_value, None


def detect_id_type(receive_id):
    """Auto-detect receive_id_type from ID prefix."""
    if receive_id.startswith("ou_"):
        return "open_id"
    elif receive_id.startswith("oc_"):
        return "chat_id"
    elif receive_id.startswith("on_"):
        return "union_id"
    else:
        return "open_id"  # default


def send_message(token, receive_id, receive_id_type, text):
    """Send a text message via Feishu API."""
    url = f"{FEISHU_API}/im/v1/messages?receive_id_type={receive_id_type}"
    payload = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            result = {"code": e.code, "msg": body}

    return result


def main():
    parser = argparse.ArgumentParser(description="Send Feishu message")
    parser.add_argument("--to", help="Recipient: open_id, chat_id, or contact label")
    parser.add_argument("--text", help="Message text to send")
    parser.add_argument("--id-type", dest="id_type",
                        choices=["open_id", "chat_id", "user_id", "union_id"],
                        help="Override receive_id_type (auto-detected by default)")
    parser.add_argument("--list-contacts", action="store_true",
                        help="List configured DM contacts")
    args = parser.parse_args()

    dms = load_dms_mapping()

    if args.list_contacts:
        if not dms:
            print(json.dumps({"contacts": [], "message": "No DM contacts configured"}))
        else:
            contacts = [{"open_id": k, "label": v.get("label", "")} for k, v in dms.items()]
            print(json.dumps({"contacts": contacts}, ensure_ascii=False))
        return

    if not args.to or not args.text:
        parser.error("--to and --text are required (or use --list-contacts)")

    receive_id, matched_label = resolve_recipient(args.to, dms)
    id_type = args.id_type or detect_id_type(receive_id)

    app_id, app_secret = load_feishu_credentials()
    token = get_tenant_access_token(app_id, app_secret)
    result = send_message(token, receive_id, id_type, args.text)

    if result.get("code", -1) == 0:
        output = {
            "success": True,
            "to": receive_id,
            "to_label": matched_label,
            "message_id": result.get("data", {}).get("message_id"),
            "chat_id": result.get("data", {}).get("chat_id"),
        }
    else:
        output = {
            "success": False,
            "to": receive_id,
            "to_label": matched_label,
            "error_code": result.get("code"),
            "error_msg": result.get("msg"),
        }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0 if output["success"] else 1)


if __name__ == "__main__":
    main()
