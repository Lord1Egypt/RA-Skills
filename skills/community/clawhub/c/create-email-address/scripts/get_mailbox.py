#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import SkillError, add_common_args, api_request, extract_api_error, print_human_summary, print_json, require_token


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch mailbox details.")
    add_common_args(parser, require_auth=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        token, _ = require_token(args)
        result = api_request("GET", args.api_base, "/mailbox", token=token)
        if not result["ok"]:
            raise SkillError(extract_api_error(result))

        mailbox = result["body"].get("data", {})
        if args.json:
            print_json(result["body"])
            return 0

        print_human_summary(
            "Mailbox",
            [
                ("id", mailbox.get("id")),
                ("address", mailbox.get("address")),
                ("instance_id", mailbox.get("instance_id")),
                ("status", mailbox.get("status")),
                ("provisioned_at", mailbox.get("provisioned_at")),
            ],
        )
        return 0
    except SkillError as exc:
        print(f"Mailbox lookup failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
