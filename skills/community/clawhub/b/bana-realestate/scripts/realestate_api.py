#!/usr/bin/env python3
"""Call the Bana real-estate API with reusable saved credentials."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://wxpub.aibana.art"
SKILL_CENTER_URL = "https://wxpub.aibana.art"


@dataclass(frozen=True)
class MethodSpec:
    required: tuple[str, ...] = ()
    optional: tuple[str, ...] = ()
    paid: bool = True


METHODS = {
    "getCities": MethodSpec(paid=False),
    "getCommunityList": MethodSpec(("city",), ("page",), paid=False),
    "getCity": MethodSpec(("city",)),
    "getCommunityListByDistrict": MethodSpec(
        ("city", "district"), ("page",)
    ),
    "getErshoufangList": MethodSpec(("city",), ("page",)),
    "getErshoufangListByDistrict": MethodSpec(
        ("city", "district"), ("page",)
    ),
    "getErshoufangListByBizcircle": MethodSpec(
        ("city", "bizcircle"), ("page",)
    ),
    "searchErshoufang": MethodSpec(("city", "keyword"), ("page",)),
    "getRentalList": MethodSpec(("city",)),
    "searchRental": MethodSpec(("city", "keyword"), ("page",)),
    "searchCommunity": MethodSpec(("city", "keyword"), ("page",)),
    "getNewHouseList": MethodSpec(("city",)),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Bana real-estate API and print its JSON response."
    )
    parser.add_argument("method", choices=METHODS)
    parser.add_argument("--city")
    parser.add_argument("--page", type=int)
    parser.add_argument("--district")
    parser.add_argument("--bizcircle")
    parser.add_argument("--keyword")
    parser.add_argument("--app-id", help="Bana Skill Center AppID.")
    parser.add_argument("--secure-key", help="Bana Skill Center SecureKey.")
    parser.add_argument(
        "--no-save-credentials",
        action="store_true",
        help="Use supplied credentials once instead of saving them.",
    )
    parser.add_argument(
        "--compact", action="store_true", help="Print compact JSON output."
    )
    parser.add_argument(
        "--timeout", type=float, default=180.0, help="Request timeout in seconds."
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    app_id, secure_key = get_credentials(args)

    spec = METHODS[args.method]
    payload: dict[str, Any] = {"app_id": app_id, "secure_key": secure_key}
    for name in spec.required:
        value = getattr(args, name)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"--{name} is required for {args.method}.")
        payload[name] = value.strip() if isinstance(value, str) else value

    for name in spec.optional:
        value = getattr(args, name)
        if value is not None:
            payload[name] = value.strip() if isinstance(value, str) else value

    if "page" in payload and payload["page"] < 1:
        raise ValueError("--page must be a positive integer.")
    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than zero.")
    return payload


def credentials_path() -> Path:
    configured = os.environ.get("BANA_REALESTATE_CREDENTIALS_FILE")
    if configured:
        return Path(configured).expanduser()
    config_home = os.environ.get("XDG_CONFIG_HOME")
    root = Path(config_home).expanduser() if config_home else Path.home() / ".config"
    return root / "bana-real-estate" / "credentials.json"


def load_saved_credentials() -> tuple[str, str]:
    path = credentials_path()
    if not path.exists():
        return "", ""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        app_id = str(value.get("app_id", "")).strip()
        secure_key = str(value.get("secure_key", "")).strip()
        return app_id, secure_key
    except (OSError, ValueError, AttributeError) as exc:
        print(f"警告：无法读取已保存的凭证：{exc}", file=sys.stderr)
        return "", ""


def save_credentials(app_id: str, secure_key: str) -> None:
    path = credentials_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(
                {"app_id": app_id, "secure_key": secure_key},
                handle,
                ensure_ascii=False,
            )
            handle.write("\n")
        path.chmod(0o600)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def get_credentials(args: argparse.Namespace) -> tuple[str, str]:
    """Prefer supplied values, then saved values, then automation injection."""
    saved_app_id, saved_secure_key = load_saved_credentials()
    app_id = (args.app_id or saved_app_id or os.environ.get("BANA_REALESTATE_APP_ID", "")).strip()
    secure_key = (
        args.secure_key
        or saved_secure_key
        or os.environ.get("BANA_REALESTATE_SECURE_KEY", "")
    ).strip()

    if not app_id or not secure_key:
        raise ValueError(
            "没有已保存的 AppID 和 SecureKey。请直接在对话中请用户提供；"
            "如果用户还没有凭证，请引导其前往巴娜 Skill 技能中心注册并生成："
            f"{SKILL_CENTER_URL}"
        )

    supplied = args.app_id is not None or args.secure_key is not None
    if supplied and not args.no_save_credentials:
        try:
            save_credentials(app_id, secure_key)
            print("凭证已保存，后续查询将自动使用。", file=sys.stderr)
        except OSError as exc:
            print(
                f"警告：凭证无法保存（{exc}），将继续完成本次查询。",
                file=sys.stderr,
            )
    return app_id, secure_key


def call_api(method: str, payload: dict[str, Any], timeout: float) -> Any:
    base_url = os.environ.get("BANA_REALESTATE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}/realestate/{method}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        detail = parse_error_body(body)
        if exc.code == 402:
            raise RuntimeError(
                "余额不足，请前往巴娜 Skill 技能中心充值："
                f"{SKILL_CENTER_URL}"
            ) from None
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from None
    except TimeoutError:
        raise RuntimeError("Request timed out.") from None

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise RuntimeError("API returned a non-JSON response.") from None


def parse_error_body(body: str) -> str:
    try:
        value = json.loads(body)
    except json.JSONDecodeError:
        return body[:500] or "empty response"
    if isinstance(value, dict) and isinstance(value.get("error"), str):
        return value["error"]
    return json.dumps(value, ensure_ascii=False)[:500]


def main() -> int:
    args = parse_args()
    try:
        payload = build_payload(args)
        if METHODS[args.method].paid:
            print(
                "费用提示：本接口成功调用一次收费 0.4 元。",
                file=sys.stderr,
            )
        result = call_api(args.method, payload, args.timeout)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.compact:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
