#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch inbox list or a specific message.")
    add_common_args(parser, require_auth=True)
    parser.add_argument("--message-id", help="If set, fetch one message by public message id (UUID)")
    parser.add_argument("--status", choices=["unread", "read", "archived"])
    parser.add_argument("--per-page", type=int, default=25)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)

        if args.message_id:
            endpoint = f"/messages/{args.message_id}"
        else:
            query = {"per_page": args.per_page, "page": args.page}
            if args.status:
                query["status"] = args.status
            qs = "&".join(f"{k}={v}" for k, v in query.items())
            endpoint = f"/inbox?{qs}"

        result = api_request("GET", args.api_base, endpoint, token=token)
        if not result["ok"]:
            raise SkillError(extract_api_error(result))

        body = result["body"]
        if args.json:
            print_json(body)
            return 0

        if args.message_id:
            msg = body.get("data", {})
            print_human_summary(
                f"Message {args.message_id}",
                [
                    ("status", msg.get("status")),
                    ("subject", msg.get("subject")),
                    ("from", msg.get("from_address")),
                    ("received_at", msg.get("received_at")),
                    ("body_text_preview", (msg.get("body_text") or "")[:120]),
                ],
            )
        else:
            messages = body.get("data", [])
            meta = body.get("meta", {})
            print_human_summary(
                "Inbox",
                [
                    ("count_returned", len(messages)),
                    ("current_page", meta.get("current_page")),
                    ("total", meta.get("total")),
                ],
            )
            for msg in messages[:10]:
                print(f"  - #{msg.get('id')} [{msg.get('status')}] {msg.get('subject') or '(no subject)'}")
        return 0
    except SkillError as exc:
        print(f"Inbox request failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
