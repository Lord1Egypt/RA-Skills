"""Step2: query and normalize 1688 offer details."""
from __future__ import annotations

import os
import re
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import ALPHA_BASE, alpha_headers, dump, post

OFFER_URL = f"{ALPHA_BASE}/alphashop.openclaw.offer.detail.query/1.0"


def _fmt(value) -> str:
    return f"{Decimal(str(value)):.2f}" if value is not None else ""


def query_offer(offer_id: int | str) -> dict:
    data = post(OFFER_URL, {"productId": str(offer_id)}, headers=alpha_headers(), timeout=30)
    if data.get("resultCode") != "SUCCESS":
        raise RuntimeError(f"1688 offer query failed: {data}")
    return data["result"]["result"]


def extract_offer_info(raw: dict) -> dict:
    sale_info = raw.get("productSaleInfo", {})
    price_ranges = sale_info.get("priceRanges", [])
    sku_infos = raw.get("productSkuInfos", [])
    sku_shipping = raw.get("productShippingInfo", {}).get("skuShippingInfos", [])
    min_price = _fmt(price_ranges[0]["price"]) if price_ranges else ""
    prices = [Decimal(str(sku["price"])) for sku in sku_infos if sku.get("price") is not None]
    max_price = _fmt(max(prices)) if prices else min_price

    sku_list = []
    for sku in sku_infos:
        specs = [
            {
                "name": attr.get("attributeName", ""),
                "value": attr.get("value", ""),
                "nameTrans": attr.get("attributeNameTrans", ""),
                "valueTrans": attr.get("valueTrans", ""),
                "attributeId": attr.get("attributeId", ""),
                "valueId": attr.get("valueId", ""),
            }
            for attr in sku.get("skuAttributes", [])
        ]
        image = next(
            (attr.get("skuImageUrl", "") for attr in sku.get("skuAttributes", []) if attr.get("skuImageUrl")),
            "",
        )
        sku_list.append(
            {
                "skuId": str(sku.get("skuId", "")),
                "price": _fmt(sku.get("price")),
                "cargoNumber": sku.get("cargoNumber", ""),
                "stock": sku.get("amountOnSale") or 0,
                "specs": specs,
                "image": image,
            }
        )

    detail_html = raw.get("description", "") or ""
    detail_images = re.findall(r'src=["\'](https?://[^"\']+)["\']', detail_html)
    attributes = [
        {"name": attr.get("attributeName", ""), "value": attr.get("value", "")}
        for attr in raw.get("productAttribute", [])
        if attr.get("attributeName")
    ]

    return {
        "offerId": raw.get("offerId"),
        "subject": raw.get("subject", ""),
        "mainImages": raw.get("productImage", {}).get("images", []),
        "detailImages": detail_images,
        "detailHtml": detail_html,
        "minPrice": min_price,
        "maxPrice": max_price,
        "skuList": sku_list,
        "attributes": attributes,
        "weightKg": sku_shipping[0].get("skuWeight") if sku_shipping else None,
        "category": {
            "firstCategoryId": str(raw.get("topCategoryId") or ""),
            "secondCategoryId": str(raw.get("secondCategoryId") or ""),
            "thirdCategoryId": str(raw.get("thirdCategoryId") or ""),
        },
    }


def get_offer(offer_id: int | str) -> dict:
    return extract_offer_info(query_offer(offer_id))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/query_offer.py <session_dir|offerId>", file=sys.stderr)
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        from scripts.common import read_session, write_session

        session_dir = sys.argv[1]
        run_input = read_session(session_dir, "input.json", required_keys=["offer_id"])
        result = get_offer(run_input["offer_id"])
        write_session(session_dir, "query_offer.json", result)
        print(dump(result))
    else:
        print(dump(get_offer(sys.argv[1])))
