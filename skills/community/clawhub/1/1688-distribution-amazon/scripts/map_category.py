"""Step3: map 1688 category IDs to Amazon category metadata."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import ALPHA_PRE_BASE, alpha_headers, dump, post

CATEGORY_MAP_URL = f"{ALPHA_PRE_BASE}/global.1688.cbu.category.mapping.query/1.0"


def query_amazon_category(first_id: str, second_id: str, third_id: str) -> dict:
    payload = {
        "platform": "amazon",
        "firstCategoryId": first_id,
        "secondCategoryId": second_id,
        "thirdCategoryId": third_id,
    }
    response = post(CATEGORY_MAP_URL, payload, headers=alpha_headers(), timeout=10)
    if response.get("resultCode") != "SUCCESS" or not response.get("result"):
        raise RuntimeError(f"Amazon category mapping failed: {response}")
    data = response["result"].get("data") or response["result"]
    return {
        "categoryId": data.get("categoryId", ""),
        "categoryName": data.get("categoryName", ""),
        "fullCategoryId": data.get("fullCategoryId", ""),
        "fullCategoryName": data.get("fullCategoryName", ""),
        "productType": data.get("productType") or data.get("ptType") or data.get("categoryName", ""),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/map_category.py <session_dir> OR <firstId> <secondId> <thirdId>", file=sys.stderr)
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        from scripts.common import read_session, write_session

        session_dir = sys.argv[1]
        offer = read_session(session_dir, "query_offer.json", required_keys=["category"])
        cat = offer["category"]
        result = query_amazon_category(cat["firstCategoryId"], cat["secondCategoryId"], cat["thirdCategoryId"])
        write_session(session_dir, "map_category.json", result)
        print(dump(result))
    else:
        if len(sys.argv) < 4:
            print("Usage: python scripts/map_category.py <firstId> <secondId> <thirdId>", file=sys.stderr)
            sys.exit(1)
        print(dump(query_amazon_category(sys.argv[1], sys.argv[2], sys.argv[3])))
