#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch outbox list or a specific outbound message.")
    add_common_args(parser, require_auth=True)
    parser.add_argument("--message-id", help="If set, fetch one outbound message by public message id (UUID)")
    parser.add_argument("--per-page", type=int, default=25)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)

        if args.message_id:
            endpoint = f"/outbox/{args.message_id}"
        else:
            endpoint = f"/outbox?per_page={args.per_page}&page={args.page}"

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
                f"Outbound message {args.message_id}",
                [
                    ("status", msg.get("status")),
                    ("subject", msg.get("subject")),
                    ("provider_message_id", msg.get("provider_message_id")),
                    ("sent_at", msg.get("sent_at")),
                    ("failed_at", msg.get("failed_at")),
                    ("error_code", msg.get("error_code")),
                    ("queue_reason", msg.get("queue_reason")),
                    ("next_eligible_at", msg.get("next_eligible_at")),
                ],
            )
        else:
            messages = body.get("data", [])
            meta = body.get("meta", {})
            print_human_summary(
                "Outbox",
                [
                    ("count_returned", len(messages)),
                    ("current_page", meta.get("current_page")),
                    ("total", meta.get("total")),
                ],
            )
            for msg in messages[:10]:
                print(
                    "  - #{} [{}] {}".format(
                        msg.get("id"),
                        msg.get("status"),
                        msg.get("subject") or "(no subject)",
                    )
                )
        return 0
    except SkillError as exc:
        print(f"Outbox request failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
