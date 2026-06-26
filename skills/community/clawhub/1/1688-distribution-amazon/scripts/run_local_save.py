"""Run the default 1688 -> Amazon localSave flow in one Newton-safe command."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts import check_env
from scripts.common import DEFAULT_MARKETPLACE_ID, dump, read_session
from scripts.init_session import create_session
from scripts.query_user_info import list_amazon_stores, public_store_view
from scripts.release_product import release_success


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DRAFT_MANAGEMENT_URL = "https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer"


class StepFailure(RuntimeError):
    pass


def _positive_inventory_quantity(raw: str) -> str:
    try:
        quantity = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"--inventory-quantity must be a positive integer, got {raw!r}") from exc
    if quantity < 1:
        raise argparse.ArgumentTypeError(f"--inventory-quantity must be >= 1, got {quantity}")
    return str(quantity)


def _redact(text: str) -> str:
    text = re.sub(r"DXB[A-Za-z0-9_+=/-]{12,}", "<DXB_ENCRYPTED_CODE>", text)
    text = re.sub(r'"encryptedCode"\s*:\s*"[^"]+"', '"encryptedCode": "<DXB_ENCRYPTED_CODE>"', text)
    text = re.sub(r'"encrypted_code"\s*:\s*"[^"]+"', '"encrypted_code": "<DXB_ENCRYPTED_CODE>"', text)
    return text


def _tail(text: str, max_chars: int = 2000) -> str:
    text = _redact(text.strip())
    if len(text) <= max_chars:
        return text
    return text[-max_chars:]


def _run_script(label: str, script_name: str, *args: str, timeout: int = 180) -> None:
    command = [sys.executable, str(SCRIPTS / script_name), *args]
    result = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        print(f"[FAIL] {label}: exit={result.returncode}", file=sys.stderr)
        if result.stdout.strip():
            print(_tail(result.stdout), file=sys.stderr)
        if result.stderr.strip():
            print(_tail(result.stderr), file=sys.stderr)
        raise StepFailure(label)
    print(f"[OK] {label}", file=sys.stderr)


def _select_store(store_name: str) -> dict[str, Any]:
    stores = list_amazon_stores()
    for store in stores:
        if store.get("storeName") == store_name:
            return store
    visible = [public_store_view(store) for store in stores]
    raise StepFailure(f"未找到 Amazon 店铺 {store_name}，可用店铺: {dump(visible)}")


def _inner_release_result(result: dict[str, Any]) -> dict[str, Any]:
    return result.get("data") if isinstance(result.get("data"), dict) else result


def _inventory_quantity_from_product(product: dict[str, Any]) -> str:
    trade_info = product.get("tradeInfo") if isinstance(product.get("tradeInfo"), dict) else {}
    raw_sku_prices = trade_info.get("skuAndPrice", "[]")
    try:
        sku_prices = json.loads(raw_sku_prices) if isinstance(raw_sku_prices, str) else raw_sku_prices
    except json.JSONDecodeError:
        sku_prices = []
    if isinstance(sku_prices, list):
        for row in sku_prices:
            if isinstance(row, dict) and row.get("inventory") not in (None, ""):
                return str(row["inventory"])
    attr_info = product.get("attrInfo") if isinstance(product.get("attrInfo"), dict) else {}
    raw_cat_prop = attr_info.get("catProp", "{}")
    try:
        cat_prop = json.loads(raw_cat_prop) if isinstance(raw_cat_prop, str) else raw_cat_prop
    except json.JSONDecodeError:
        cat_prop = {}
    values = cat_prop.get("fulfillment_availability") if isinstance(cat_prop, dict) else []
    if isinstance(values, list):
        for row in values:
            if isinstance(row, dict) and row.get("quantity") not in (None, ""):
                return str(row["quantity"])
    return ""


def run(args: argparse.Namespace) -> int:
    env_status = check_env.main()
    if env_status != 0:
        return env_status

    store = _select_store(args.store_name)
    session_dir = create_session(
        args.offer_id,
        store["encryptedCode"],
        store["storeName"],
        args.marketplace_id,
    )

    _run_script("query 1688 offer", "query_offer.py", session_dir, timeout=60)
    _run_script("map Amazon category", "map_category.py", session_dir, timeout=60)
    _run_script("process Amazon images", "process_images.py", session_dir, timeout=180)
    _run_script("query Amazon attributes", "map_amazon_attrs.py", session_dir, timeout=180)
    _run_script("map Amazon CPV attributes", "map_pv_attrs.py", session_dir, timeout=180)

    build_args = [session_dir]
    if args.price_multiplier:
        build_args.extend(["--price-multiplier", args.price_multiplier])
    if args.inventory_quantity:
        build_args.extend(["--inventory-quantity", args.inventory_quantity])
    _run_script("build Amazon product payload", "build_product.py", *build_args, timeout=60)
    _run_script("save Dianxiaobao local draft", "release_product.py", session_dir, timeout=60)

    product = read_session(session_dir, "build_product.json")
    release_result = read_session(session_dir, "release_product.json")
    inner = _inner_release_result(release_result)
    ok = release_success(release_result, "localSave")
    summary = {
        "ok": ok,
        "releaseType": "localSave",
        "sessionDir": session_dir,
        "offerId": int(args.offer_id),
        "storeName": store["storeName"],
        "marketplaceId": args.marketplace_id,
        "localId": inner.get("localId", ""),
        "isSuccess": inner.get("isSuccess", ""),
        "inventoryQuantity": _inventory_quantity_from_product(product),
        "nextStep": "Open the Dianxiaobao Amazon pending-products page to review and publish the draft.",
        "draftManagementUrl": DRAFT_MANAGEMENT_URL,
        "files": [
            "input.json",
            "query_user_info.json",
            "query_offer.json",
            "map_category.json",
            "image_processing.json",
            "map_amazon_attrs.json",
            "map_pv_attrs.json",
            "build_product.json",
            "release_product.json",
        ],
    }
    print(dump(summary))
    return 0 if ok else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Amazon localSave listing flow in one command.")
    parser.add_argument("offer_id", type=int, help="1688 offerId")
    parser.add_argument("--store-name", required=True, help="Amazon store name")
    parser.add_argument("--marketplace-id", default=DEFAULT_MARKETPLACE_ID, help="Amazon marketplaceId")
    parser.add_argument("--price-multiplier", help="Optional listing price multiplier")
    parser.add_argument(
        "--inventory-quantity",
        type=_positive_inventory_quantity,
        help="Optional positive Amazon draft inventory quantity. Use this when the user explicitly provides inventory.",
    )
    args = parser.parse_args(argv)
    try:
        return run(args)
    except StepFailure as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
