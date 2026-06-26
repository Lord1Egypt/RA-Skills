#!/usr/bin/env python3
"""Build Costco inventory monitoring config for one or many products.

Examples:
  Single product (legacy mode):
    build_monitor_config.py --product-url ... --product-id 123 --zip 03051

  Batch mode:
    build_monitor_config.py --product "4000362984|TCL 55 Q77K|https://www.costco.com/p/..." \
      --product "777|Another Item|https://www.costco.com/p/..." --zip 03051 --zip 97230
"""

from __future__ import annotations

import argparse
import json
import random
import re
import uuid
from datetime import datetime, timezone
from typing import Iterable

ZIP_RE = re.compile(r"^\d{5}$")
PRODUCT_SPEC_RE = re.compile(r"^([^|]+)\|([^|]+)\|(.+)$")


def str_to_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {raw}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)

    # Legacy single-product flags
    parser.add_argument("--product-url")
    parser.add_argument("--product-id")
    parser.add_argument("--product-name", default="")

    # Batch mode flags
    parser.add_argument(
        "--product",
        action="append",
        default=[],
        help="Format: <id>|<name>|<url>. Repeat this flag for multiple products.",
    )

    parser.add_argument("--zip", action="append", dest="zip_codes", required=True)
    parser.add_argument("--interval", type=int, default=60, dest="interval_minutes")
    parser.add_argument("--timezone", default="America/Los_Angeles")
    parser.add_argument("--channel", action="append", dest="channels", default=[])
    parser.add_argument(
        "--fingerprint-mode",
        choices=["none", "stable", "random"],
        default="random",
        help="random=每次运行生成不同指纹；stable=基于输入生成固定指纹；none=不生成",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "pretty"],
        default="pretty",
        help="pretty 会先输出摘要表格，再输出 JSON。",
    )

    parser.add_argument(
        "--network-path",
        choices=["direct", "residential_proxy"],
        default="direct",
        help="direct=服务器直连；residential_proxy=通过家宽代理访问。",
    )
    parser.add_argument(
        "--proxy-url",
        help="完整代理 URL，例如 http://user:pass@gw.dataimpulse.com:823",
    )
    parser.add_argument(
        "--proxy-host",
        default="gw.dataimpulse.com",
        help="当不提供 --proxy-url 时生效。",
    )
    parser.add_argument("--proxy-port", type=int, default=823)
    parser.add_argument("--proxy-username")
    parser.add_argument("--proxy-password")
    parser.add_argument(
        "--proxy-session-id",
        help="sticky 会话标识，可用于把多次请求绑定到同一出口 IP。",
    )
    parser.add_argument(
        "--proxy-rotate-per-request",
        type=str_to_bool,
        default=True,
        help="true=每次请求轮换出口，false=复用 session（sticky）。默认 true。",
    )
    parser.add_argument(
        "--proxy-country",
        help="可选国家代码（例如 US）。",
    )
    parser.add_argument("--proxy-state", help="可选州/省。")
    parser.add_argument("--proxy-city", help="可选城市。")
    parser.add_argument("--proxy-zip", help="可选代理出口邮编。")
    return parser.parse_args()


def normalize_zip_codes(zip_codes: list[str]) -> list[str]:
    normalized = []
    for code in zip_codes:
        if not ZIP_RE.match(code):
            raise ValueError(f"Invalid ZIP code: {code}")
        normalized.append(code)
    return sorted(set(normalized))


def parse_batch_products(specs: Iterable[str]) -> list[dict[str, str]]:
    products: list[dict[str, str]] = []
    for spec in specs:
        match = PRODUCT_SPEC_RE.match(spec)
        if not match:
            raise ValueError(
                f"Invalid --product value: {spec}. Expected '<id>|<name>|<url>'."
            )
        pid, name, url = match.groups()
        products.append({"id": pid.strip(), "name": name.strip(), "url": url.strip()})
    return products


def resolve_products(args: argparse.Namespace) -> list[dict[str, str]]:
    products = parse_batch_products(args.product)

    has_legacy = bool(args.product_id or args.product_url)
    if has_legacy:
        if not (args.product_id and args.product_url):
            raise ValueError("Legacy mode requires both --product-id and --product-url")
        products.append(
            {
                "id": str(args.product_id).strip(),
                "name": args.product_name.strip() or f"product-{args.product_id}",
                "url": args.product_url.strip(),
            }
        )

    if not products:
        raise ValueError(
            "Provide at least one product via --product '<id>|<name>|<url>' or legacy flags"
        )

    dedup: dict[str, dict[str, str]] = {}
    for item in products:
        dedup[item["id"]] = item
    return [dedup[key] for key in sorted(dedup.keys())]


def build_fingerprint(seed_payload: dict, mode: str) -> str | None:
    if mode == "none":
        return None
    if mode == "stable":
        stable_seed = json.dumps(seed_payload, sort_keys=True, ensure_ascii=False)
        return str(uuid.uuid5(uuid.NAMESPACE_URL, stable_seed))

    # random mode: 每次运行随机指纹，适合模拟浏览器轮换
    return f"run-{uuid.uuid4()}-{random.randint(1000, 9999)}"


def build_proxy_config(args: argparse.Namespace) -> dict:
    if args.network_path == "direct":
        return {
            "enabled": False,
            "mode": "direct",
            "reason": "default_direct_path",
        }

    if args.proxy_url:
        endpoint = args.proxy_url.strip()
    else:
        if not (args.proxy_username and args.proxy_password):
            raise ValueError(
                "residential_proxy 模式下，若未提供 --proxy-url，则必须提供 --proxy-username 和 --proxy-password"
            )
        endpoint = (
            f"http://{args.proxy_username}:{args.proxy_password}@"
            f"{args.proxy_host}:{args.proxy_port}"
        )

    return {
        "enabled": True,
        "mode": "residential_proxy",
        "endpoint": endpoint,
        "host": args.proxy_host,
        "port": args.proxy_port,
        "rotate_per_request": args.proxy_rotate_per_request,
        "session_id": args.proxy_session_id,
        "geo": {
            "country": args.proxy_country,
            "state": args.proxy_state,
            "city": args.proxy_city,
            "zip": args.proxy_zip,
        },
    }


def render_pretty(payload: dict) -> str:
    lines: list[str] = []
    lines.append("=== Inventory Monitor Plan ===")
    lines.append(
        f"Run ID: {payload['run']['fingerprint'] or 'N/A'} | Generated: {payload['generated_at_utc']}"
    )
    lines.append(
        f"Products: {len(payload['products'])} | ZIPs: {len(payload['zip_codes'])} | Interval: {payload['schedule']['interval_minutes']} min"
    )
    lines.append("")
    lines.append("Products")
    lines.append("-" * 80)
    for idx, product in enumerate(payload["products"], start=1):
        lines.append(f"{idx:02d}. [{product['id']}] {product['name']}")
        lines.append(f"    {product['url']}")

    lines.append("")
    lines.append(f"ZIP Targets: {', '.join(payload['zip_codes'])}")
    lines.append(f"Alert Channels: {', '.join(payload['alerts']['channels']) or 'none'}")
    lines.append("=" * 80)
    lines.append(json.dumps(payload, ensure_ascii=False, indent=2))
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    if args.interval_minutes <= 0:
        raise ValueError("--interval must be a positive integer")

    zip_codes = normalize_zip_codes(args.zip_codes)
    products = resolve_products(args)

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "run": {
            "fingerprint_mode": args.fingerprint_mode,
        },
        "products": products,
        "zip_codes": zip_codes,
        "schedule": {
            "interval_minutes": args.interval_minutes,
            "timezone": args.timezone,
        },
        "alerts": {
            "channels": sorted(set(args.channels)),
            "suppress_minutes": 30,
        },
        "network": {
            "path": args.network_path,
            "proxy": build_proxy_config(args),
            "akamai_block_recovery": {
                "enabled": args.network_path == "residential_proxy",
                "notes": [
                    "If direct path returns HTTP 403 Access Denied, switch to residential proxy.",
                    "Use sticky session when product page requires multi-step render and cart checks.",
                ],
            },
        },
        "status_values": ["in_stock", "limited_stock", "out_of_stock", "unknown"],
    }
    fingerprint_seed = {
        "products": payload["products"],
        "zip_codes": payload["zip_codes"],
        "schedule": payload["schedule"],
        "alerts": payload["alerts"],
    }
    payload["run"]["fingerprint"] = build_fingerprint(fingerprint_seed, args.fingerprint_mode)

    if args.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(render_pretty(payload))


if __name__ == "__main__":
    main()
