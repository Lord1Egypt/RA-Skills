#!/usr/bin/env python3
"""Call the Bana Taobao search API with reusable saved credentials."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://wxpub.aibana.art"
SKILL_CENTER_URL = "https://wxpub.aibana.art"
SORT_ALIASES = {
    "default": "",
    "sale": "_sale",
    "销量": "_sale",
    "_sale": "_sale",
    "price_asc": "_price_asc",
    "低价": "_price_asc",
    "价格从低到高": "_price_asc",
    "_price_asc": "_price_asc",
    "price_desc": "_price_desc",
    "高价": "_price_desc",
    "价格从高到低": "_price_desc",
    "_price_desc": "_price_desc",
    "total": "_total",
    "总价": "_total",
    "_total": "_total",
    "popular": "_popular",
    "人气": "_popular",
    "_popular": "_popular",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Bana Taobao search API and print its JSON response."
    )
    parser.add_argument("--keyword", required=True, help="Taobao search keyword.")
    parser.add_argument(
        "--sort",
        default="default",
        help="Sort: default, sale, price_asc, price_desc, total, or popular.",
    )
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


def credentials_path() -> Path:
    configured = os.environ.get("BANA_TAOBAO_CREDENTIALS_FILE")
    if configured:
        return Path(configured).expanduser()
    config_home = os.environ.get("XDG_CONFIG_HOME")
    root = Path(config_home).expanduser() if config_home else Path.home() / ".config"
    return root / "bana-taobao" / "credentials.json"


def load_saved_credentials() -> tuple[str, str]:
    path = credentials_path()
    if not path.exists():
        return "", ""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return (
            str(value.get("app_id", "")).strip(),
            str(value.get("secure_key", "")).strip(),
        )
    except (OSError, ValueError, AttributeError) as exc:
        print(f"警告：无法读取已保存的凭证：{exc}", file=sys.stderr)
        return "", ""


def save_credentials(app_id: str, secure_key: str) -> None:
    path = credentials_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump({"app_id": app_id, "secure_key": secure_key}, handle)
            handle.write("\n")
        path.chmod(0o600)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def get_credentials(args: argparse.Namespace) -> tuple[str, str]:
    saved_app_id, saved_secure_key = load_saved_credentials()
    app_id = (args.app_id or saved_app_id or os.environ.get("BANA_TAOBAO_APP_ID", "")).strip()
    secure_key = (
        args.secure_key
        or saved_secure_key
        or os.environ.get("BANA_TAOBAO_SECURE_KEY", "")
    ).strip()
    if not app_id or not secure_key:
        raise ValueError(
            "没有已保存的 AppID 和 SecureKey。请直接在对话中请用户提供；"
            "如果用户还没有凭证，请引导其前往巴娜技能中心注册并生成："
            f"{SKILL_CENTER_URL}"
        )

    supplied = args.app_id is not None or args.secure_key is not None
    if supplied and not args.no_save_credentials:
        try:
            save_credentials(app_id, secure_key)
            print("凭证已保存，后续查询将自动使用。", file=sys.stderr)
        except OSError as exc:
            print(f"警告：凭证无法保存（{exc}），将继续完成本次查询。", file=sys.stderr)
    return app_id, secure_key


def build_payload(args: argparse.Namespace) -> dict[str, str]:
    keyword = args.keyword.strip()
    sort_input = args.sort.strip()
    if not keyword:
        raise ValueError("--keyword must not be empty.")
    if sort_input not in SORT_ALIASES:
        raise ValueError(
            "--sort must be one of: " + ", ".join(sorted(SORT_ALIASES))
        )
    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than zero.")

    app_id, secure_key = get_credentials(args)
    return {
        "app_id": app_id,
        "secure_key": secure_key,
        "keyword": keyword,
        "sort": SORT_ALIASES[sort_input],
    }


def parse_error_body(body: str) -> str:
    try:
        value = json.loads(body)
    except json.JSONDecodeError:
        return body[:500] or "empty response"
    if isinstance(value, dict) and isinstance(value.get("error"), str):
        return value["error"]
    return json.dumps(value, ensure_ascii=False)[:500]


def call_api(payload: dict[str, str], timeout: float) -> Any:
    base_url = os.environ.get("BANA_TAOBAO_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    request = urllib.request.Request(
        f"{base_url}/taobao/search",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {parse_error_body(body)}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from None
    except TimeoutError:
        raise RuntimeError("Request timed out.") from None

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise RuntimeError("API returned a non-JSON response.") from None


def main() -> int:
    args = parse_args()
    try:
        payload = build_payload(args)
        print("费用提示：淘宝商品搜索公测期间限时免费，本次调用不扣费。", file=sys.stderr)
        result = call_api(payload, args.timeout)
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
