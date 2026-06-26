#!/usr/bin/env python3
"""
Bootstrap secure identity material for Apple Health sync. Not required to just onboard a new iOS device.
"""

import argparse
import json
import os
import secrets
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib import error, request
from config import (
    APP_CONFIG,
    load_defaults_config,
    load_existing_user_config,
    resolve_state_dir,
    resolve_user_paths,
    write_user_config,
)
from sync_cryptography import (
    V5_BOX_ALGORITHM,
    V5_ENCRYPTION_ALGORITHM,
    V5_PROTOCOL_VERSION,
    V5_SIGNING_ALGORITHM,
    build_legacy_onboarding_payload,
    build_v5_onboarding_payload,
    ed25519_public_key_base64_from_private_key,
    generate_legacy_rsa_keys,
    generate_v5_keys,
    public_key_base64_from_pem,
    resolve_v5_key_paths,
    sign_legacy_challenge,
    sign_v5_challenge,
    x25519_public_key_base64_from_private_key,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def secure_json_write(path: Path, value: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.chmod(tmp_path, 0o600)
    tmp_path.replace(path)


def secure_binary_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_bytes(value)
    os.chmod(tmp_path, 0o600)
    tmp_path.replace(path)


def resolve_mutable_string_setting(existing_config: Dict[str, Any], defaults: Dict[str, Any], key: str) -> str:
    existing_value = str(existing_config.get(key, "")).strip()
    if existing_value:
        return existing_value
    return str(defaults.get(key, ""))


def generate_user_id() -> str:
    return "ahs_" + secrets.token_urlsafe(16).rstrip("=")


def ensure_binary(binary_name: str) -> None:
    if shutil.which(binary_name) is None:
        raise RuntimeError(f"Missing required binary: {binary_name}")


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


def http_post_binary(url: str, payload: Dict[str, Any], timeout: int, apikey: str, region: str) -> Tuple[bytes, str]:
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
            content_type = response.headers.get("Content-Type", "")
            return raw, content_type
    except error.HTTPError as http_error:
        detail = http_error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {http_error.code} from function: {detail}") from http_error
    except error.URLError as url_error:
        raise RuntimeError(f"Cannot reach function: {url_error}") from url_error

def ensure_sqlite_schema(sqlite_path: Path) -> None:
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(sqlite_path)
    try:
        conn.execute(
            """
            create table if not exists health_data (
              id integer primary key autoincrement,
              user_id text not null,
              date text not null,
              data text not null,
              created_at text not null,
              updated_at text not null
            );
            """
        )
        conn.execute(
            "create unique index if not exists health_data_user_date_idx "
            "on health_data (user_id, date);"
        )
        conn.commit()
    finally:
        conn.close()


def render_qr_via_supabase(
    payload: str,
    config_dir: Path,
    function_url: str,
    apikey: str,
    region: str,
    user_id: str,
    private_key_path: Path,
    algorithm: str,
    public_key_base64: str,
    protocol_version: int = 4,
) -> Path:
    challenge_response = http_post_json(
        function_url,
        {
            "action": "issue_challenge",
            "id": user_id,
            "protocol_version": protocol_version,
        },
        10,
        apikey,
        region,
    )
    challenge = str(challenge_response["challenge"])
    challenge_id = str(challenge_response["challengeId"])
    signature = sign_v5_challenge(private_key_path, challenge) if protocol_version == 5 else sign_legacy_challenge(private_key_path, challenge, algorithm)

    request_payload: Dict[str, Any] = {
        "action": "render_onboarding_qr",
        "id": user_id,
        "payload": payload,
        "challengeId": challenge_id,
        "signature": signature,
    }
    if protocol_version == 5:
        request_payload["protocol_version"] = 5
        request_payload["signing_public_key"] = public_key_base64
    else:
        request_payload["public_key"] = public_key_base64

    raw_png, content_type = http_post_binary(
        function_url,
        request_payload,
        10,
        apikey,
        region,
    )
    if "image/png" not in content_type.lower():
        raise RuntimeError(f"Function response has unexpected content type: {content_type or 'unknown'}")
    if not raw_png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Function response is not a valid PNG payload.")

    qr_png_path = config_dir / "registration-qr.png"
    secure_binary_write(qr_png_path, raw_png)
    return qr_png_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize keypair and config for HealthSync.")
    parser.add_argument(
        "--state-dir",
        default="",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--storage",
        choices=("auto", "sqlite", "json"),
        default="auto",
        help="Default local storage backend for fetch script.",
    )
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="Rotate keys if key files already exist.",
    )
    parser.add_argument(
        "--protocol",
        choices=("v4", "v5"),
        default="v5",
        help="Onboarding protocol version to generate. v5 uses Ed25519/X25519, v4 keeps the RSA fallback.",
    )
    return parser.parse_args()


def main() -> int:
    os.umask(0o077)
    args = parse_args()
    state_dir = resolve_state_dir(args.state_dir)
    paths = resolve_user_paths(state_dir)
    config_dir = paths["config_dir"]
    secrets_dir = paths["secrets_dir"]
    state_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    secrets_dir.mkdir(parents=True, exist_ok=True)

    try:
        ensure_binary("openssl")
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    private_key_path = secrets_dir / "private_key.pem"
    public_key_path = config_dir / "public_key.pem"
    v5_key_paths = resolve_v5_key_paths(secrets_dir, config_dir)
    qr_payload_path = config_dir / "registration-qr.json"

    try:
        config_defaults = load_defaults_config()
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    existing_config = load_existing_user_config(state_dir)

    user_id = existing_config.get("user_id") or generate_user_id()
    resolved_ios_app_link = str(APP_CONFIG["ios_app_link"])
    resolved_storage = (
        args.storage
        if args.storage != "auto"
        else resolve_mutable_string_setting(existing_config, config_defaults, "storage")
    )
    resolved_onboarding_version = int(APP_CONFIG["onboarding_version"])
    resolved_supabase_region = str(APP_CONFIG.get("supabase_region", "")).strip()
    resolved_qr_function_url = str(APP_CONFIG.get("supabase_qr_code_generator_url", "")).strip()
    resolved_publishable_key = str(APP_CONFIG.get("supabase_publishable_key", "")).strip()

    protocol_version = 4 if args.protocol == "v4" else 5
    active_public_key_path = public_key_path
    onboarding_payload: Dict[str, Any]
    active_public_key_base64 = ""
    active_private_key_path = private_key_path
    algorithm = "RSA-2048"

    if protocol_version == 4:
        try:
            generate_legacy_rsa_keys(private_key_path, public_key_path, rotate=args.rotate)
        except RuntimeError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        except subprocess.CalledProcessError as error:
            print(error.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
            return 1

        public_key_pem = public_key_path.read_text(encoding="utf-8")
        active_public_key_base64 = public_key_base64_from_pem(public_key_pem)
        onboarding_payload = build_legacy_onboarding_payload(
            user_id,
            resolved_onboarding_version,
            algorithm,
            active_public_key_base64,
        )
    else:
        try:
            generate_v5_keys(
                v5_key_paths["signing_private_key_path"],
                v5_key_paths["signing_public_key_path"],
                v5_key_paths["encryption_private_key_path"],
                v5_key_paths["encryption_public_key_path"],
                rotate=args.rotate,
            )
        except RuntimeError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

        signing_public_key_base64 = ed25519_public_key_base64_from_private_key(v5_key_paths["signing_private_key_path"])
        encryption_public_key_base64 = x25519_public_key_base64_from_private_key(
            v5_key_paths["encryption_private_key_path"]
        )
        onboarding_payload = build_v5_onboarding_payload(
            user_id,
            signing_public_key_base64,
            encryption_public_key_base64,
        )
        active_public_key_base64 = signing_public_key_base64
        active_private_key_path = v5_key_paths["signing_private_key_path"]
        active_public_key_path = v5_key_paths["signing_public_key_path"]
        algorithm = V5_SIGNING_ALGORITHM

    onboarding_payload_compact = json.dumps(onboarding_payload, separators=(",", ":"), sort_keys=True)
    onboarding_payload_hex = onboarding_payload_compact.encode("utf-8").hex()
    secure_json_write(qr_payload_path, onboarding_payload)

    qr_png_path = None
    if resolved_qr_function_url and resolved_publishable_key and resolved_supabase_region:
        try:
            qr_png_path = render_qr_via_supabase(
                onboarding_payload_compact,
                config_dir,
                resolved_qr_function_url,
                resolved_publishable_key,
                resolved_supabase_region,
                user_id,
                active_private_key_path,
                algorithm,
                active_public_key_base64,
                protocol_version=protocol_version,
            )
        except RuntimeError as error:
            print(f"QR rendering via Supabase failed: {error}")
    else:
        print("QR rendering via Supabase is unavailable: missing function configuration.")

    sqlite_path = state_dir / "health_data.db"
    ensure_sqlite_schema(sqlite_path)

    user_config = dict(existing_config)
    user_config.pop("qr_svg_path", None)
    user_config.update(
        {
        "user_id": user_id,
        "protocol_version": protocol_version,
        "algorithm": algorithm,
        "state_dir": str(state_dir),
        "config_dir": str(config_dir),
        "secrets_dir": str(secrets_dir),
        "private_key_path": str(private_key_path),
        "public_key_path": str(public_key_path),
        "public_key_base64": existing_config.get("public_key_base64", ""),
        "onboarding_fingerprint": onboarding_payload["fingerprint"],
        "onboarding_payload_json": onboarding_payload_compact,
        "onboarding_payload_hex": onboarding_payload_hex,
        "storage": resolved_storage,
        "sqlite_path": str(sqlite_path),
        "json_path": str(config_dir / "health_data.ndjson"),
        "qr_payload_path": str(qr_payload_path),
        "qr_png_path": str(qr_png_path) if qr_png_path else "",
        "updated_at": now_iso(),
        }
    )
    if protocol_version == 4:
        user_config["public_key_base64"] = active_public_key_base64
        user_config["private_key_path"] = str(private_key_path)
        user_config["public_key_path"] = str(public_key_path)
        user_config["algorithm"] = "RSA-2048"
    else:
        encryption_public_key_base64 = x25519_public_key_base64_from_private_key(v5_key_paths["encryption_private_key_path"])
        user_config["signing_algorithm"] = V5_SIGNING_ALGORITHM
        user_config["signing_private_key_path"] = str(v5_key_paths["signing_private_key_path"])
        user_config["signing_public_key_path"] = str(v5_key_paths["signing_public_key_path"])
        user_config["signing_public_key_base64"] = active_public_key_base64
        user_config["encryption_algorithm"] = V5_ENCRYPTION_ALGORITHM
        user_config["box_algorithm"] = V5_BOX_ALGORITHM
        user_config["encryption_private_key_path"] = str(v5_key_paths["encryption_private_key_path"])
        user_config["encryption_public_key_path"] = str(v5_key_paths["encryption_public_key_path"])
        user_config["encryption_public_key_base64"] = encryption_public_key_base64
    write_user_config(user_config, state_dir)

    print("\nInitialization complete.")
    print(f"State dir: {state_dir}")
    print(f"Config dir: {config_dir}")
    print(f"User ID: {user_id}")
    print(f"Protocol: v{protocol_version}")
    print(f"Public key: {active_public_key_path}")
    if protocol_version == 5:
        print(f"Encryption public key: {v5_key_paths['encryption_public_key_path']}")
    if qr_png_path:
        print(f"QR PNG: {qr_png_path}")
    if not qr_png_path:
        print("QR unavailable: use the Hex onboarding payload.")
    print(f"iOS app link: {resolved_ios_app_link}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
