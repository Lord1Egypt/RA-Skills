"""Step7: release Amazon listing through Dianxiaobao."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import DXB_BASE, dump, env, post, redact_sensitive


DRAFT_ONLY_MESSAGE = (
    "This skill version only supports saving Amazon listings as Dianxiaobao localSave drafts. "
    "Use the Dianxiaobao Amazon pending-products page for later publishing."
)
VALID_RELEASE_TYPES = {"localSave"}


def release_type(default: str = "localSave") -> str:
    return "localSave"


def validate_release_type(value: str) -> str:
    if value not in VALID_RELEASE_TYPES:
        raise ValueError(f"Online release types are not supported. Expected localSave. {DRAFT_ONLY_MESSAGE}")
    return value


def _json_field(product_data: dict, section: str, field: str):
    raw = ((product_data.get(section) or {}).get(field))
    if isinstance(raw, str):
        return json.loads(raw)
    return raw


def _positive_inventory(value: object) -> bool:
    if value in (None, ""):
        return False
    try:
        return int(str(value).strip()) >= 1
    except (TypeError, ValueError):
        return False


def build_release_payload(
    encrypted_code: str,
    store_name: str,
    product_data: dict | None = None,
    *,
    release_type_value: str | None = None,
    local_id: str | None = None,
) -> dict:
    mode = validate_release_type(release_type_value or release_type())
    payload = {
        "ptName": "amazon",
        "userCode": encrypted_code,
        "storeName": store_name,
        "type": mode,
    }
    if product_data is None:
        raise ValueError(f"{mode} requires product data")
    payload["data"] = json.dumps(product_data, ensure_ascii=False)
    return payload


def release_product(
    encrypted_code: str,
    store_name: str,
    product_data: dict | None = None,
    *,
    release_type_value: str | None = None,
    local_id: str | None = None,
) -> dict:
    payload = build_release_payload(
        encrypted_code,
        store_name,
        product_data,
        release_type_value=release_type_value,
        local_id=local_id,
    )
    return post(f"{DXB_BASE}/api-goods/product/releaseProductToOut", payload, timeout=30)


def is_success_value(value: object) -> bool:
    return value in (1, "1", True)


def is_failure_value(value: object) -> bool:
    return value in (0, "0", False)


def release_success(result: dict, release_type_value: str = "localSave") -> bool:
    mode = validate_release_type(release_type_value)
    inner = result.get("data") if isinstance(result.get("data"), dict) else result
    if result.get("success") is False or inner.get("success") is False:
        return False
    if is_failure_value(inner.get("isSuccess")):
        return False
    if is_success_value(inner.get("isSuccess")):
        return True
    if mode == "localSave":
        return bool(inner.get("localId"))
    return False


def parse_cli_options(argv: list[str]) -> tuple[str, str]:
    selected_type = "localSave"
    selected_local_id = ""
    for idx, arg in enumerate(argv):
        if arg == "--release-type":
            if idx + 1 >= len(argv):
                raise ValueError("--release-type requires a value")
            selected_type = argv[idx + 1]
        if arg == "--local-id":
            if idx + 1 >= len(argv):
                raise ValueError("--local-id requires a value")
            selected_local_id = argv[idx + 1]
    return validate_release_type(selected_type), selected_local_id


def main_with_args(argv: list[str]) -> int:
    if len(argv) < 1:
        print(
            "Usage: python scripts/release_product.py <session_dir> [--release-type localSave] [--dry-run]",
            file=sys.stderr,
        )
        return 1
    try:
        selected_type, selected_local_id = parse_cli_options(argv[1:])
    except ValueError as exc:
        print(f"[GUARD] {exc}", file=sys.stderr)
        return 2
    if os.path.isdir(argv[0]):
        from scripts.common import read_session, write_session

        session_dir = argv[0]
        user = read_session(session_dir, "query_user_info.json", required_keys=["encryptedCode", "storeName"])
        product = read_session(session_dir, "build_product.json", required_keys=["subject", "categoryId"])
        try:
            payload = build_release_payload(
                user["encryptedCode"],
                user["storeName"],
                product,
                release_type_value=selected_type,
                local_id=selected_local_id,
            )
        except ValueError as exc:
            print(f"[GUARD] {exc}", file=sys.stderr)
            return 2
        if "--dry-run" in argv:
            safe_payload = redact_sensitive(payload)
            write_session(session_dir, "release_payload_dry_run.json", safe_payload)
            print(dump(safe_payload))
            return 0
        result = post(f"{DXB_BASE}/api-goods/product/releaseProductToOut", payload, timeout=30)
        write_session(session_dir, "release_product.json", result)
        print(dump(result))
        return 0 if release_success(result, selected_type) else 2

    print(
        "[GUARD] Direct credential CLI mode is disabled to avoid leaking encryptedCode in shell history. "
        "Use a session_dir created by init_session.py.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main_with_args(sys.argv[1:]))
