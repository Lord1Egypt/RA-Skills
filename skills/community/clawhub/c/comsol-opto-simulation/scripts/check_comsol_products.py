#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check COMSOL installation, product availability, and model requirements.

Default product keys target optoelectronic detector workflows:
COMSOL, SEMICONDUCTOR, RF, WAVEOPTICS, HEATTRANSFER.
Use --skip-start for a fast environment-only check that does not consume a
COMSOL license.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VENDOR_SITE = SKILL_DIR / "vendor" / "site-packages"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if VENDOR_SITE.exists() and str(VENDOR_SITE) not in sys.path:
    sys.path.insert(0, str(VENDOR_SITE))

from discover_comsol_environment import discover  # noqa: E402


DEFAULT_PRODUCTS = ("COMSOL", "SEMICONDUCTOR", "RF", "WAVEOPTICS", "HEATTRANSFER")


def normalize_products(values: list[str]) -> list[str]:
    products: list[str] = []
    for value in values:
        for part in value.replace(",", " ").split():
            token = part.strip().upper()
            if token:
                products.append(token)
    return products


def start_and_check(products: list[str], model_path: Path | None, cores: int) -> dict[str, object]:
    import mph

    client = mph.start(cores=cores)
    java = client.java

    product_status: dict[str, object] = {}
    for product in products:
        try:
            product_status[product] = bool(java.hasProduct(product))
        except Exception as exc:
            product_status[product] = {"error": str(exc)}

    model_status: dict[str, object] | None = None
    if model_path:
        model_status = {"path": str(model_path), "exists": model_path.exists()}
        if model_path.exists():
            try:
                model_status["has_products_for_file"] = bool(java.hasProductForFile(str(model_path)))
            except Exception as exc:
                model_status["has_products_for_file_error"] = str(exc)
            try:
                model = client.load(str(model_path))
                model_status["used_products"] = model.modules()
                try:
                    client.remove(model)
                except Exception:
                    pass
            except Exception as exc:
                model_status["load_error"] = str(exc)

    return {
        "status": "checked",
        "products": product_status,
        "model": model_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="Override COMSOL installation root.")
    parser.add_argument("--products", nargs="*", default=list(DEFAULT_PRODUCTS), help="COMSOL product keys to check.")
    parser.add_argument("--model", type=Path, help="Optional .mph file to inspect.")
    parser.add_argument("--cores", type=int, default=2, help="COMSOL cores for mph.start.")
    parser.add_argument("--skip-start", action="store_true", help="Only discover paths; do not start COMSOL.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    args = parser.parse_args()

    products = normalize_products(args.products)
    env = discover(args.root)
    result: dict[str, object] = {
        "environment_status": env.get("status"),
        "install_root": env.get("install_root"),
        "products_requested": products,
        "skip_start": args.skip_start,
    }
    if env.get("status") != "found":
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 1
    if args.skip_start:
        result["status"] = "environment_only"
        result["note"] = "Run without --skip-start to query ModelUtil.hasProduct and model file requirements."
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 0

    try:
        result.update(start_and_check(products, args.model, args.cores))
    except Exception as exc:
        result["status"] = "error"
        result["message"] = str(exc)
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 1

    failed = [
        key for key, value in result.get("products", {}).items()
        if value is not True
    ]
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
