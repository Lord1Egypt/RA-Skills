#!/usr/bin/env python3
"""Forward a Feishu thread (话题) to a user or group.

Usage:
    python3 forward_thread.py --thread-id omt_xxx --receive-id oc_xxx --receive-id-type chat_id
    python3 forward_thread.py --message-id om_xxx --receive-id ou_xxx --receive-id-type open_id

If --thread-id is not provided but --message-id is, the script will first
fetch the message to extract its thread_id.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def get_token(config_path="/root/.openclaw/openclaw.json"):
    with open(config_path) as f:
        cfg = json.load(f)
    app_id = cfg["channels"]["feishu"]["appId"]
    app_secret = cfg["channels"]["feishu"]["appSecret"]

    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get("code", -1) != 0:
        print(f"ERROR: Failed to get token: {resp}", file=sys.stderr)
        sys.exit(1)
    return resp["tenant_access_token"]


def get_thread_id_from_message(token, message_id):
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get("code", -1) != 0:
        print(f"ERROR: Failed to get message: {resp}", file=sys.stderr)
        sys.exit(1)
    items = resp.get("data", {}).get("items", [])
    if not items:
        print("ERROR: Message not found", file=sys.stderr)
        sys.exit(1)
    thread_id = items[0].get("thread_id")
    if not thread_id:
        print("ERROR: Message has no thread_id (not a topic message)", file=sys.stderr)
        sys.exit(1)
    return thread_id


def forward_thread(token, thread_id, receive_id, receive_id_type, uuid=None):
    url = f"https://open.feishu.cn/open-apis/im/v1/threads/{thread_id}/forward?receive_id_type={receive_id_type}"
    if uuid:
        url += f"&uuid={uuid}"

    req = urllib.request.Request(
        url,
        data=json.dumps({"receive_id": receive_id}).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        resp = json.loads(e.read().decode())

    return resp


def main():
    parser = argparse.ArgumentParser(description="Forward a Feishu thread")
    parser.add_argument("--thread-id", help="Thread ID (omt_xxx)")
    parser.add_argument("--message-id", help="Message ID to extract thread_id from")
    parser.add_argument("--receive-id", required=True, help="Target ID")
    parser.add_argument(
        "--receive-id-type",
        required=True,
        choices=["open_id", "chat_id", "user_id", "union_id", "email", "thread_id"],
        help="Target ID type",
    )
    parser.add_argument("--uuid", help="Idempotency key (max 50 chars)")
    parser.add_argument("--config", default="/root/.openclaw/openclaw.json")
    args = parser.parse_args()

    if not args.thread_id and not args.message_id:
        parser.error("Either --thread-id or --message-id is required")

    token = get_token(args.config)

    thread_id = args.thread_id
    if not thread_id:
        thread_id = get_thread_id_from_message(token, args.message_id)
        print(f"Resolved thread_id: {thread_id}", file=sys.stderr)

    result = forward_thread(
        token, thread_id, args.receive_id, args.receive_id_type, args.uuid
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("code", -1) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
