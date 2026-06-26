#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://gamemarket.yy.com"
APP_ID = "market_app"
IDENTIFY = "ixlOJVDwdOm5rGdudhEywwK6"
DEFAULT_PAGE_SIZE = 20
DEFAULT_MAX_PAGES = 1
DEFAULT_PAGES_PER_SORT = 2

SORT_PROFILES = {
    "baseline": {"label": "综合排序", "sortField": None, "sortType": None},
    "recent": {"label": "最新发布", "sortField": "CREATE_TIME", "sortType": "DESC"},
    "high_price": {"label": "价格最高", "sortField": "PRICE", "sortType": "DESC"},
}

TARGET_GAME_NAMES = [
    "王者荣耀",
    "英雄联盟",
    "三角洲行动",
    "和平精英",
    "穿越火线",
    "无畏契约",
    "绝地求生",
    "逆战未来",
    "崩坏:星穹铁道",
    "王者荣耀世界",
    "暗黑破坏神",
    "CSGO",
    "天龙八部",
    "原神",
    "异环",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch public mall.yy.com trade listing data as JSON.")
    parser.add_argument("--page-size", type=positive_int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--max-pages", type=positive_int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--pages-per-sort", type=positive_int, default=DEFAULT_PAGES_PER_SORT)
    parser.add_argument("--request-source", default="SECLIST")
    parser.add_argument(
        "--sort-profile",
        choices=["all", *SORT_PROFILES.keys()],
        default="all",
        help="排序视角：all/baseline/recent/high_price，默认 all",
    )
    parser.add_argument("--game", action="append", help="只查询指定游戏名；可重复传多个，例如 --game 王者荣耀 --game 原神")
    return parser.parse_args()


def positive_int(value):
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def trace_time(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y%m%d%H%M%S")


def selected_sort_profiles(sort_profile):
    if sort_profile == "all":
        return list(SORT_PROFILES.items())
    return [(sort_profile, SORT_PROFILES[sort_profile])]


def signature_headers(path):
    nonce = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    raw = f"appId={APP_ID}&nonce={nonce}&timestamp={timestamp}&uri={path}&secret={IDENTIFY}"
    signature = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return {
        "accept": "application/json, text/plain, */*",
        "origin": "https://mall.yy.com",
        "referer": "https://mall.yy.com/",
        "x-appid": APP_ID,
        "x-nonce": nonce,
        "x-timestamp": timestamp,
        "x-signature": signature,
        "x-traceid": f"{uuid.uuid4().hex}-{trace_time(int(timestamp))}",
    }


def build_url(path, params):
    filtered = {key: value for key, value in params.items() if value is not None and value != ""}
    query = urlencode(filtered, doseq=True)
    return f"{API_BASE}{path}" + (f"?{query}" if query else "")


def fetch_json(path, params):
    url = build_url(path, params)
    request = Request(url, headers=signature_headers(path), method="GET")
    try:
        with urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8")
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {body[:300]}") from error
    except URLError as error:
        raise RuntimeError(f"Request failed: {error.reason}") from error

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON: {text[:300]}") from error

    if payload.get("code") != 0:
        raise RuntimeError(f"API {payload.get('code')}: {payload.get('message') or text[:300]}")

    return payload


def fetch_categories():
    payload = fetch_json("/category/queryShowCategories", {"sid": ""})
    data = payload.get("data")
    return data if isinstance(data, list) else []


def build_target_games(categories, selected_names=None):
    categories_by_name = {category.get("name"): category for category in categories}
    games = []
    target_names = selected_names or TARGET_GAME_NAMES

    for name in target_names:
        category = categories_by_name.get(name)
        sub_categories = category.get("subCategories", []) if category else []
        account_sub_category = next((item for item in sub_categories if item.get("name") == "账号"), None)
        fallback_sub_category = sub_categories[0] if sub_categories else None
        selected_sub_category = account_sub_category or fallback_sub_category

        games.append(
            {
                "name": name,
                "categoryId": category.get("id") if category else None,
                "categoryName": category.get("name") if category else None,
                "subCategoryId": selected_sub_category.get("id") if selected_sub_category else None,
                "subCategoryName": selected_sub_category.get("name") if selected_sub_category else None,
                "categorySource": "category/queryShowCategories" if category else "unresolved",
                "accountCategoryAvailable": bool(account_sub_category),
            }
        )

    return games


def fetch_listing_page(game, page_num, page_size, request_source, sort_config):
    params = {
        "pageNum": page_num,
        "pageSize": page_size,
        "requestSource": request_source,
        "withRegionServer": "true",
        "categoryId": game.get("categoryId"),
        "subCategoryId": game.get("subCategoryId"),
        "sortField": sort_config.get("sortField"),
        "sortType": sort_config.get("sortType"),
        "searchDistChannelGoods": "false",
    }
    payload = fetch_json("/goods/v2/search", params)
    data = payload.get("data") or {}
    items = data.get("goodsList") if isinstance(data.get("goodsList"), list) else []
    return {
        "request": {"path": "/goods/v2/search", "params": params},
        "token": data.get("token"),
        "hasMore": bool(data.get("hasMore")),
        "source": data.get("source"),
        "serverTime": data.get("serverTime"),
        "items": items,
    }


def merge_unique_items(profile_results):
    seen = set()
    merged = []
    for profile in profile_results:
        for item in profile.get("items", []):
            goods_id = item.get("goodsId")
            key = goods_id if goods_id is not None else id(item)
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return merged


def fetch_game_profile(game, profile_name, sort_config, args):
    items = []
    pages = []
    has_more = False

    for page_num in range(1, args.pages_per_sort + 1):
        page = fetch_listing_page(
            game,
            page_num,
            args.page_size,
            args.request_source,
            sort_config,
        )
        pages.append(
            {
                "pageNum": page_num,
                "itemCount": len(page["items"]),
                "hasMore": page["hasMore"],
            }
        )
        items.extend(page["items"])
        has_more = page["hasMore"]
        if not page["hasMore"] or len(page["items"]) < args.page_size:
            break

    return {
        "name": profile_name,
        "label": sort_config.get("label", profile_name),
        "sortField": sort_config.get("sortField"),
        "sortType": sort_config.get("sortType"),
        "pagination": {
            "pageSize": args.page_size,
            "maxPages": args.pages_per_sort,
            "fetchedPages": len(pages),
            "hasMore": has_more,
            "itemCount": len(items),
            "pages": pages,
        },
        "items": items,
    }


def fetch_game_goods(game, args):
    if not game.get("categoryId") or not game.get("subCategoryId"):
        return {
            "name": game["name"],
            "categoryId": game.get("categoryId"),
            "subCategoryId": game.get("subCategoryId"),
            "subCategoryName": game.get("subCategoryName"),
            "sortProfiles": [],
            "pagination": {
                "pageSize": args.page_size,
                "pagesPerSort": args.pages_per_sort,
                "profileCount": 0,
                "hasMore": False,
                "itemCount": 0,
                "rawItemCount": 0,
            },
            "items": [],
            "error": "categoryId or subCategoryId not resolved",
        }

    profile_results = []
    for profile_name, sort_config in selected_sort_profiles(args.sort_profile):
        profile_results.append(fetch_game_profile(game, profile_name, sort_config, args))

    items = merge_unique_items(profile_results)
    return {
        "name": game["name"],
        "categoryId": game.get("categoryId"),
        "subCategoryId": game.get("subCategoryId"),
        "subCategoryName": game.get("subCategoryName"),
        "sortProfiles": profile_results,
        "pagination": {
            "pageSize": args.page_size,
            "pagesPerSort": args.pages_per_sort,
            "profileCount": len(profile_results),
            "hasMore": any(profile["pagination"].get("hasMore") for profile in profile_results),
            "itemCount": len(items),
            "rawItemCount": sum(profile["pagination"].get("itemCount", 0) for profile in profile_results),
        },
        "items": items,
    }


def main():
    args = parse_args()
    output = {
        "generatedAt": now_iso(),
        "source": "gamemarket.yy.com",
        "sampling": {
            "pageSize": args.page_size,
            "pagesPerSort": args.pages_per_sort,
            "requestSource": args.request_source,
            "sortProfile": args.sort_profile,
            "sortProfiles": [name for name, _ in selected_sort_profiles(args.sort_profile)],
        },
        "games": [],
    }

    try:
        categories = fetch_categories()
        games = build_target_games(categories, args.game)
    except Exception as error:
        games = [
            {
                "name": name,
                "categoryId": None,
                "categoryName": None,
                "subCategoryId": None,
                "subCategoryName": None,
                "categorySource": "error",
                "accountCategoryAvailable": False,
                "categoryError": str(error),
            }
            for name in (args.game or TARGET_GAME_NAMES)
        ]
        output["error"] = str(error)

    for game in games:
        try:
            output["games"].append(fetch_game_goods(game, args))
        except Exception as error:
            output["games"].append(
                {
                    "name": game["name"],
                    "categoryId": game.get("categoryId"),
                    "subCategoryId": game.get("subCategoryId"),
                    "subCategoryName": game.get("subCategoryName"),
                    "sortProfiles": [],
                    "pagination": {
                        "pageSize": args.page_size,
                        "pagesPerSort": args.pages_per_sort,
                        "profileCount": 0,
                        "hasMore": False,
                        "itemCount": 0,
                        "rawItemCount": 0,
                    },
                    "items": [],
                    "error": str(error),
                }
            )

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
