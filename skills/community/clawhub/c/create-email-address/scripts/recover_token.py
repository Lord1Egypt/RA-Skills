#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from common import (
    SkillError,
    add_common_args,
    api_request,
    extract_api_error,
    load_identity,
    print_human_summary,
    print_json,
    save_token,
    sign_challenge_message,
    solve_pow,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recover mailbox token using OpenClaw identity.")
    add_common_args(parser)
    parser.add_argument("--json", action="store_true", help="Print raw JSON response")
    args = parser.parse_args()

    try:
        identity = load_identity(args.identity_path)

        challenge_result = api_request(
            "POST",
            args.api_base,
            "/challenge",
            payload={"instance_id": identity.instance_id},
        )
        if not challenge_result["ok"]:
            raise SkillError(extract_api_error(challenge_result))

        challenge_data = challenge_result["body"].get("data", {})
        challenge_nonce = challenge_data.get("challenge_nonce")
        difficulty = challenge_data.get("challenge", {}).get("difficulty", 1)

        if not challenge_nonce:
            raise SkillError("Challenge response missing challenge_nonce.")

        pow_value = solve_pow(identity.instance_id, challenge_nonce, int(difficulty))
        signature_b64 = sign_challenge_message(identity.instance_id, challenge_nonce, identity.private_key_pem)

        recover_payload = {
            "instance_id": identity.instance_id,
            "challenge_nonce": challenge_nonce,
            "proof": {
                "signature": signature_b64,
                "pow": pow_value,
            },
        }

        recover_result = api_request("POST", args.api_base, "/recover", payload=recover_payload)
        if not recover_result["ok"]:
            raise SkillError(extract_api_error(recover_result))

        data = recover_result["body"].get("data", {})
        token = data.get("token")
        mailbox = data.get("mailbox", {})

        if not token:
            raise SkillError("Recover response missing token.")

        token_record = {
            "token": token,
            "api_base": args.api_base,
            "instance_id": identity.instance_id,
            "mailbox_id": mailbox.get("id"),
            "mailbox_address": mailbox.get("address"),
            "token_expires_at": data.get("expires_at"),
            "identity_path": args.identity_path,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        save_token(args.token_path, token_record)

        if args.json:
            print_json({"challenge": challenge_result["body"], "recover": recover_result["body"], "saved_token": token_record})
            return 0

        print_human_summary(
            "Mailbox token recovered successfully.",
            [
                ("instance_id", identity.instance_id),
                ("mailbox", mailbox.get("address", "(unknown)")),
                ("status", mailbox.get("status", "(unknown)")),
                ("token_saved_to", args.token_path),
            ],
        )
        return 0

    except SkillError as exc:
        print(f"Token recovery failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
