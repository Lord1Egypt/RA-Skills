"""Step1: query Dianxiaobao user info."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import DXB_BASE, dump, env, post


def public_store_view(store: dict) -> dict:
    raw = store.get("raw") or {}
    extend_data = raw.get("extend_data") if isinstance(raw.get("extend_data"), dict) else {}
    marketplaces = []
    marketplace_participation = raw.get("marketplaceParticipationList") or extend_data.get("marketplaceParticipationList") or []
    for marketplace in marketplace_participation:
        marketplace_info = marketplace.get("marketplace") or {}
        marketplaces.append(
            {
                "name": marketplace_info.get("name") or "",
                "countryCode": marketplace_info.get("countryCode") or "",
                "marketplaceId": marketplace_info.get("marketplaceId") or marketplace_info.get("id") or "",
            }
        )
    return {
        "storeName": store.get("storeName") or "",
        "marketplaces": marketplaces,
    }


def get_user_info(user_id: str | None = None, store_name: str | None = None) -> dict:
    user_id = user_id or env("DXB_USER_ID")
    if not user_id:
        raise RuntimeError("Missing DXB_USER_ID")
    data = post(f"{DXB_BASE}/shop/queryDxbInfoById", {"userId": user_id}, timeout=20)
    encrypted_code = data["encryptedCode"]
    amazon_stores = (data.get("shopInfo") or {}).get("amazon") or []
    resolved_store = store_name or env("AMAZON_STORE_NAME")
    if not resolved_store and amazon_stores:
        resolved_store = amazon_stores[0].get("shop_name") or amazon_stores[0].get("storeName")
    if not resolved_store:
        raise RuntimeError("Missing Amazon storeName; set AMAZON_STORE_NAME")
    return {"encryptedCode": encrypted_code, "storeName": resolved_store, "raw": data}


def list_amazon_stores(user_id: str | None = None) -> list[dict]:
    user_id = user_id or env("DXB_USER_ID")
    if not user_id:
        raise RuntimeError("Missing DXB_USER_ID")
    data = post(f"{DXB_BASE}/shop/queryDxbInfoById", {"userId": user_id}, timeout=20)
    encrypted_code = data["encryptedCode"]
    amazon_stores = (data.get("shopInfo") or {}).get("amazon") or []
    return [
        {
            "encryptedCode": encrypted_code,
            "storeName": store.get("shop_name") or store.get("storeName") or "",
            "raw": store,
        }
        for store in amazon_stores
    ]


if __name__ == "__main__":
    stores = list_amazon_stores()
    if not stores:
        print(dump({"error": "no_store", "message": "当前用户未绑定 Amazon 店铺"}))
        sys.exit(1)
    print(dump([public_store_view(store) for store in stores]))
