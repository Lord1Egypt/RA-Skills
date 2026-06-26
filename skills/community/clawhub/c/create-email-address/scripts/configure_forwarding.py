#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Get or update mailbox forwarding settings.")
    add_common_args(parser, require_auth=True)

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--enable", action="store_true", help="Enable forwarding to --forward-to-email.")
    mode.add_argument("--disable", action="store_true", help="Disable forwarding and clear destination.")

    parser.add_argument("--forward-to-email", help="Forwarding destination email address.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)

        if args.enable and not args.forward_to_email:
            raise SkillError("--enable requires --forward-to-email.")
        if args.disable and args.forward_to_email:
            raise SkillError("--disable cannot be combined with --forward-to-email.")

        if args.enable or args.disable:
            payload = {
                "forwarding_enabled": bool(args.enable),
                "forward_to_email": args.forward_to_email if args.enable else None,
            }
            result = api_request("POST", args.api_base, "/mailbox/forwarding", token=token, payload=payload)
            action = "Mailbox forwarding updated"
        else:
            result = api_request("GET", args.api_base, "/mailbox/forwarding", token=token)
            action = "Mailbox forwarding"

        if not result["ok"]:
            raise SkillError(extract_api_error(result))

        body = result["body"]
        if args.json:
            print_json(body)
            return 0

        data = body.get("data", {})
        print_human_summary(
            action,
            [
                ("forwarding_enabled", data.get("forwarding_enabled")),
                ("forward_to_email", data.get("forward_to_email") or "(none)"),
            ],
        )
        return 0
    except SkillError as exc:
        print(f"Forwarding configuration failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
