#!/usr/bin/env python3
"""
Unlink a previously paired iOS device by resetting write-token binding via challenge signing.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib import error, request
from config import load_effective_config, resolve_state_dir, resolve_user_paths, write_user_config
from sync_cryptography import public_key_base64_from_pem, sign_legacy_challenge, sign_v5_challenge


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_public_key_base64(value: str) -> str:
    return "".join(str(value).split())


def http_post_json(url: str, payload: Dict[str, Any], timeout: int, apikey: str, region: str) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-region": region,
            "apikey": apikey,
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            return json.loads(raw.decode("utf-8"))
    except error.HTTPError as http_error:
        detail = http_error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {http_error.code} from function: {detail}") from http_error
    except error.URLError as url_error:
        raise RuntimeError(f"Cannot reach function: {url_error}") from url_error

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unlink a paired iOS device for HealthSync.")
    parser.add_argument("--state-dir", default="", help=argparse.SUPPRESS)
    parser.add_argument("--user-id", default="")
    parser.add_argument("--record-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--private-key-path", default="")
    parser.add_argument("--public-key", default="")
    parser.add_argument("--timeout-seconds", type=int, default=20)
    return parser.parse_args()


def resolve_runtime(
    args: argparse.Namespace,
    config: Dict[str, Any],
    paths: Dict[str, Path],
) -> Dict[str, Any]:
    function_url = str(config.get("supabase_unlink_device_url", "")).strip()
    user_id = args.user_id or args.record_id or config.get("user_id", "") or config.get("record_id", "")
    protocol_version = int(config.get("protocol_version", 4) or 4)
    if protocol_version == 5:
        private_key_path = Path(
            args.private_key_path or config.get("signing_private_key_path", paths["secrets_dir"] / "signing_private_key_v5.pem")
        ).expanduser()
        public_key_base64 = normalize_public_key_base64(
            args.public_key or config.get("signing_public_key_base64", "")
        )
    else:
        private_key_path = Path(
            args.private_key_path or config.get("private_key_path", paths["secrets_dir"] / "private_key.pem")
        ).expanduser()
        public_key_base64 = normalize_public_key_base64(args.public_key or config.get("public_key_base64", ""))

        if not public_key_base64:
            public_key_path = Path(config.get("public_key_path", paths["config_dir"] / "public_key.pem")).expanduser()
            if public_key_path.exists():
                public_key_base64 = public_key_base64_from_pem(public_key_path.read_text(encoding="utf-8"))
            else:
                raise RuntimeError(
                    "Missing public key. Set --public-key or config.public_key_base64/public_key_path."
                )

    if not user_id:
        raise RuntimeError("Missing user ID. Set --user-id or config.user_id.")
    if not function_url:
        raise RuntimeError("Missing app-owned unlink-device URL in scripts/config.py.")
    if not private_key_path.exists():
        raise RuntimeError(f"Missing private key file: {private_key_path}")
    return {
        "function_url": function_url,
        "user_id": user_id,
        "private_key_path": private_key_path,
        "public_key_base64": public_key_base64,
        "algorithm": str(config.get("algorithm", "RSA-2048")),
        "protocol_version": protocol_version,
    }


def main() -> int:
    args = parse_args()
    state_dir = resolve_state_dir(args.state_dir)
    paths = resolve_user_paths(state_dir)
    user_config: Dict[str, Any] = {}
    config: Dict[str, Any] = {}

    try:
        user_config, config = load_effective_config(state_dir)
        runtime = resolve_runtime(args, config, paths)
        publishable_key = str(config.get("supabase_publishable_key", "")).strip()
        region = str(config.get("supabase_region", "")).strip()
        if not publishable_key:
            raise RuntimeError("Missing app-owned publishable key in scripts/config.py or --apikey.")
        if not region:
            raise RuntimeError("Missing app-owned Supabase region in scripts/config.py.")

        challenge_response = http_post_json(
            str(runtime["function_url"]),
            {
                "action": "issue_challenge",
                "id": runtime["user_id"],
                "protocol_version": runtime["protocol_version"],
            },
            args.timeout_seconds,
            publishable_key,
            region,
        )
        challenge = challenge_response["challenge"]
        challenge_id = challenge_response["challengeId"]
        if int(runtime["protocol_version"]) == 5:
            signature = sign_v5_challenge(Path(runtime["private_key_path"]), challenge)
        else:
            signature = sign_legacy_challenge(Path(runtime["private_key_path"]), challenge, str(runtime["algorithm"]))

        unlink_payload: Dict[str, Any] = {
            "action": "unlink_device",
            "id": runtime["user_id"],
            "challengeId": challenge_id,
            "signature": signature,
        }
        if int(runtime["protocol_version"]) == 5:
            unlink_payload["protocol_version"] = 5
            unlink_payload["signing_public_key"] = runtime["public_key_base64"]
        else:
            unlink_payload["public_key"] = runtime["public_key_base64"]

        unlink_response = http_post_json(
            str(runtime["function_url"]),
            unlink_payload,
            args.timeout_seconds,
            publishable_key,
            region,
        )
        if not unlink_response.get("ok"):
            raise RuntimeError(f"Unexpected unlink response: {unlink_response}")

        unlinked_at = unlink_response.get("unlinkedAt") or now_iso()
        user_config["last_unlink_at"] = unlinked_at
        user_config["last_unlink_status"] = "ok"
        write_user_config(user_config, state_dir)
        print(
            f"Unlink successful: user_id={runtime['user_id']}, "
            f"protocol=v{runtime['protocol_version']}, unlinked_at={unlinked_at}"
        )
        return 0
    except Exception as runtime_error:
        print(f"Error: {runtime_error}", file=sys.stderr)
        try:
            if user_config:
                user_config["last_unlink_at"] = now_iso()
                user_config["last_unlink_status"] = "error"
                user_config["last_unlink_error"] = str(runtime_error)
                write_user_config(user_config, state_dir)
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
