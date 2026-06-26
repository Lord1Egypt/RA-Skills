#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, parse_json_arg, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Send an outbound message.")
    add_common_args(parser, require_auth=True)
    parser.add_argument("--to", required=True, help='JSON array of recipients, e.g. ["alice@example.com"]')
    parser.add_argument("--cc", help='JSON array, e.g. ["cc@example.com"]')
    parser.add_argument("--bcc", help='JSON array, e.g. ["bcc@example.com"]')
    parser.add_argument("--from-name", help='Optional sender display name, e.g. "Claw Agent Email"')
    parser.add_argument("--subject", default="")
    parser.add_argument("--body-text", default="")
    parser.add_argument("--body-html", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)
        payload = {
            "to": parse_json_arg(args.to),
            "cc": parse_json_arg(args.cc) if args.cc else [],
            "bcc": parse_json_arg(args.bcc) if args.bcc else [],
            "subject": args.subject,
            "body_text": args.body_text,
            "body_html": args.body_html,
        }

        if args.from_name is not None:
            payload["from_name"] = args.from_name

        if not isinstance(payload["to"], list) or len(payload["to"]) == 0:
            raise SkillError("--to must be a non-empty JSON array of email addresses.")
        if not payload["body_text"].strip() and not payload["body_html"].strip():
            raise SkillError("Either --body-text or --body-html must be provided.")

        result = api_request("POST", args.api_base, "/send", token=token, payload=payload)
        if not result["ok"]:
            raise SkillError(extract_api_error(result))

        body = result["body"]
        if args.json:
            print_json(body)
            return 0

        msg = body.get("data", {})
        print_human_summary(
            "Outbound message queued",
            [
                ("id", msg.get("id")),
                ("status", msg.get("status")),
                ("from_name", msg.get("from_name")),
                ("subject", msg.get("subject")),
                ("to", ", ".join(msg.get("to_addresses") or [])),
            ],
        )
        return 0
    except SkillError as exc:
        print(f"Send failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
