#!/usr/bin/env python3
"""Small Crisp API helper for the crisp-grocery skill.

Standard library only. It does not store secrets unless the user explicitly
passes --token-file for login commands.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE = "https://crispapp.nl/v1"
DEFAULT_UA = "crisp/app/android/634"


def token_from_env_or_file(args: argparse.Namespace) -> str:
    token = getattr(args, "token", None) or os.environ.get("CRISP_BEARER_TOKEN")
    token_file = getattr(args, "token_file", None) or os.environ.get("CRISP_TOKEN_FILE")
    if not token and token_file:
        token = Path(token_file).read_text(encoding="utf-8").strip()
    if not token:
        raise SystemExit("Missing token. Set CRISP_BEARER_TOKEN or CRISP_TOKEN_FILE, or pass --token/--token-file.")
    return token


def api_base(args: argparse.Namespace) -> str:
    return (getattr(args, "base", None) or os.environ.get("CRISP_API_BASE") or DEFAULT_BASE).rstrip("/")


def user_agent(args: argparse.Namespace) -> str:
    return getattr(args, "user_agent", None) or os.environ.get("CRISP_USER_AGENT") or DEFAULT_UA


def request_json(
    args: argparse.Namespace,
    method: str,
    endpoint: str,
    body: dict[str, Any] | None = None,
    token: str | None = None,
) -> Any:
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        url = endpoint
    else:
        url = api_base(args) + "/" + endpoint.lstrip("/")

    data = None
    headers = {
        "User-Agent": user_agent(args),
        "Accept": "application/json",
    }
    if token is None:
        token = token_from_env_or_file(args)
    headers["Authorization"] = f"bearer {token}"
    if body is not None:
        data = json.dumps(body, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            if not raw:
                return None
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} for {method} {url}: {text[:500]}")


def write_output(args: argparse.Namespace, payload: Any) -> None:
    save = getattr(args, "save", None)
    if save:
        out_dir = Path(os.environ.get("CRISP_OUTPUT_DIR", "artifacts/api"))
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / save
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(path)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def money(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def summarize(kind: str, payload: Any) -> None:
    if kind == "client":
        print(json.dumps({
            "id_present": bool(payload.get("id")),
            "outdated": payload.get("outdated"),
        }, ensure_ascii=False, indent=2))
    elif kind == "basket":
        products = payload.get("products") or {}
        print(json.dumps({
            "basket_id_present": bool(payload.get("id")),
            "product_count": len(products),
            "products_total": payload.get("productsTotalPrice"),
            "pay_price": payload.get("payPrice"),
            "minimum_order_value": payload.get("mov"),
            "needed_for_minimum": payload.get("neededForMOV"),
            "selected_delivery_slot": payload.get("deliverySlot"),
            "base_delivery_slot": payload.get("baseDeliverySlot"),
        }, ensure_ascii=False, indent=2))
    elif kind == "delivery":
        days = []
        for day in payload.get("deliveryDays") or []:
            slots = day.get("slots") or []
            cheapest = min(slots, key=lambda s: money(s.get("price")), default=None)
            if cheapest:
                days.append({
                    "date": day.get("date"),
                    "day": day.get("day"),
                    "slot_count": len(slots),
                    "cheapest_price": cheapest.get("price"),
                    "cheapest_start": cheapest.get("start"),
                    "cheapest_end": cheapest.get("end"),
                    "cheapest_type": cheapest.get("type"),
                    "cutoff_message": day.get("cutoffMessage"),
                })
        print(json.dumps(days, ensure_ascii=False, indent=2))
    elif kind == "promos":
        products = [b.get("product") for b in payload.get("promo", {}).get("blocks", []) if b.get("type") == "product"]
        rows = []
        for p in products:
            if not p:
                continue
            base = money(p.get("basePrice"))
            price = money(p.get("price"))
            save = round(base - price, 2)
            rows.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "price": p.get("price"),
                "basePrice": p.get("basePrice"),
                "saves": f"{save:.2f}",
                "percent": round((save / base) * 100, 1) if base else None,
                "promotion": (p.get("promotion") or {}).get("descr"),
                "lactoseFree": (p.get("tags") or {}).get("lactoseFree"),
            })
        rows.sort(key=lambda r: (r["percent"] or 0, money(r["saves"])), reverse=True)
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif kind == "orders":
        rows = []
        for wrapper in payload.get("data") or []:
            order = wrapper.get("item") or {}
            rows.append({
                "deliveryAt": order.get("deliveryAt"),
                "finalPrice": order.get("finalPrice"),
                "fulfillStatus": order.get("fulfillStatus"),
                "payStatus": order.get("payStatus"),
                "productCount": len(order.get("products") or []),
                "recipeCount": len(order.get("recipes") or []),
            })
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif kind == "your-shop":
        cats = []
        for cat in payload.get("categories") or []:
            if cat.get("showAsHeader") or cat.get("l2CategoryId") is not None:
                cats.append({
                    "key": cat.get("key"),
                    "title": cat.get("header") or cat.get("outboundTitle"),
                    "momentId": cat.get("momentId"),
                    "l2CategoryId": cat.get("l2CategoryId"),
                })
        print(json.dumps({
            "hasSavedItems": payload.get("hasSavedItems"),
            "hasGroups": payload.get("hasGroups"),
            "itemCount": len(payload.get("items") or []),
            "categories": cats,
        }, ensure_ascii=False, indent=2))
    else:
        raise SystemExit(f"Unknown summary kind: {kind}")


def cmd_get(args: argparse.Namespace) -> None:
    payload = request_json(args, "GET", args.endpoint)
    if args.summary:
        summarize(args.summary, payload)
    else:
        write_output(args, payload)


def random_token() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(20))


def cmd_login_start(args: argparse.Namespace) -> None:
    token = args.token or random_token()
    payload = request_json(args, "POST", "/user/login", {"email": args.email, "country": args.country}, token=token)
    if args.token_file:
        path = Path(args.token_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(token, encoding="utf-8")
    print(json.dumps({"sent": payload, "token_saved": bool(args.token_file)}, ensure_ascii=False, indent=2))


def cmd_login_code(args: argparse.Namespace) -> None:
    token = token_from_env_or_file(args)
    payload = request_json(args, "POST", "/user/login", {"email": args.email, "code": args.code, "country": args.country}, token=token)
    print(json.dumps({"login": payload}, ensure_ascii=False, indent=2))


def cmd_basket_add_product(args: argparse.Namespace) -> None:
    expected = f"add product {args.product_id} quantity {args.quantity}"
    if args.confirm != expected:
        raise SystemExit(f"Refusing mutation. Pass --confirm {expected!r}")
    body = {
        "products": {
            str(args.product_id): {
                "count": args.quantity,
                "from": {
                    "screenName": args.from_screen,
                    "screenUrl": args.from_url,
                    "scroller": args.from_scroller,
                },
            }
        }
    }
    payload = request_json(args, "PUT", "/basket/main", body)
    summarize("basket", payload)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--base", default=None)
    common.add_argument("--user-agent", default=None)
    common.add_argument("--token", default=None)
    common.add_argument("--token-file", default=None)

    parser = argparse.ArgumentParser(description="Crisp API helper", parents=[common])
    sub = parser.add_subparsers(required=True)

    get = sub.add_parser("get", parents=[common])
    get.add_argument("endpoint")
    get.add_argument("--save")
    get.add_argument("--summary", choices=["client", "basket", "delivery", "promos", "orders", "your-shop"])
    get.set_defaults(func=cmd_get)

    login_start = sub.add_parser("login-start", parents=[common])
    login_start.add_argument("email")
    login_start.add_argument("--country", default="nl")
    login_start.set_defaults(func=cmd_login_start)

    login_code = sub.add_parser("login-code", parents=[common])
    login_code.add_argument("email")
    login_code.add_argument("code")
    login_code.add_argument("--country", default="nl")
    login_code.set_defaults(func=cmd_login_code)

    add = sub.add_parser("basket-add-product", parents=[common])
    add.add_argument("product_id", type=int)
    add.add_argument("quantity", type=int)
    add.add_argument("--from-screen", default="YourShop")
    add.add_argument("--from-url", default="/yourShop")
    add.add_argument("--from-scroller", default="Eerder gekocht en bewaard")
    add.add_argument("--confirm", required=True)
    add.set_defaults(func=cmd_basket_add_product)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
