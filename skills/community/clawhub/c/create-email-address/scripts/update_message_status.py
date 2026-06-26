#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a message status.")
    add_common_args(parser, require_auth=True)
    parser.add_argument("message_id", help="Message public id (UUID)")
    parser.add_argument("action", choices=["read", "unread", "archive", "unarchive"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)
        result = api_request("POST", args.api_base, f"/messages/{args.message_id}/{args.action}", token=token, payload={})
        if not result["ok"]:
            raise SkillError(extract_api_error(result))

        body = result["body"]
        if args.json:
            print_json(body)
            return 0

        msg = body.get("data", {})
        print_human_summary(
            "Message status updated",
            [
                ("message_id", msg.get("id")),
                ("new_status", msg.get("status")),
                ("subject", msg.get("subject")),
            ],
        )
        return 0
    except SkillError as exc:
        print(f"Status update failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
