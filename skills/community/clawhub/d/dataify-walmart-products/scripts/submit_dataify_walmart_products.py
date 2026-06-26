#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder?platform=1"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
LOGIN_URL = "https://dashboard.dataify.com/login?utm_source=skill"
MIN_PYTHON = (3, 6)

MODE_URL = "url"
MODE_CATEGORY_URL = "category-url"
MODE_SKU = "sku"
MODE_KEYWORDS = "keywords"
SPIDER_IDS = {
    MODE_URL: "walmart_product_by-url",
    MODE_CATEGORY_URL: "walmart_product_by-category-url",
    MODE_SKU: "walmart_product_by-sku",
    MODE_KEYWORDS: "walmart_product_by-keywords",
}
DEFAULT_URL = "https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true"
DEFAULT_CATEGORY_URL = "https://www.walmart.com/shop/deals/food/"
DEFAULT_SKU = "439179861"
DEFAULT_KEYWORD = "leggins"
DEFAULT_DOMAIN = "https://www.walmart.com/"
DEFAULT_ALL_VARIATIONS = "false"
DEFAULT_CATEGORY_PAGE_TURNING = "1"
DEFAULT_KEYWORD_PAGE_TURNING = "2"
DEFAULT_FILE_NAME = "{{TasksID}}"
BOOL_VALUES = ("true", "false")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_walmart_products.py --mode sku --sku \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_SKU,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url, category-url, sku, or keywords.".format(value))
    return clean


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_walmart_url(value, field_name):
    clean = normalize_text(value, field_name)
    if not clean.startswith("https://www.walmart.com/"):
        raise ValueError("{} must start with https://www.walmart.com/".format(field_name))
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean or not clean.isdigit():
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return clean


def normalize_boolean(value, field_name):
    clean = str(value).strip().lower()
    if clean not in BOOL_VALUES:
        raise ValueError("{} must be true or false".format(field_name))
    return clean


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_url_group(group):
    return {
        "url": normalize_walmart_url(group.get("url", DEFAULT_URL), "url"),
        "all_variations": normalize_boolean(group.get("all_variations", DEFAULT_ALL_VARIATIONS), "all_variations"),
    }


def normalize_category_url_group(group):
    return {
        "category_url": normalize_walmart_url(group.get("category_url", DEFAULT_CATEGORY_URL), "category_url"),
        "all_variations": normalize_boolean(group.get("all_variations", DEFAULT_ALL_VARIATIONS), "all_variations"),
        "page_turning": normalize_non_negative_integer(group.get("page_turning", DEFAULT_CATEGORY_PAGE_TURNING), "page_turning"),
    }


def normalize_sku_group(group):
    return {
        "sku": normalize_text(group.get("sku", DEFAULT_SKU), "sku"),
        "all_variations": normalize_boolean(group.get("all_variations", DEFAULT_ALL_VARIATIONS), "all_variations"),
    }


def normalize_keywords_group(group):
    return {
        "keyword": normalize_text(group.get("keyword", DEFAULT_KEYWORD), "keyword"),
        "domain": normalize_walmart_url(group.get("domain", DEFAULT_DOMAIN), "domain"),
        "all_variations": normalize_boolean(group.get("all_variations", DEFAULT_ALL_VARIATIONS), "all_variations"),
        "page_turning": normalize_non_negative_integer(group.get("page_turning", DEFAULT_KEYWORD_PAGE_TURNING), "page_turning"),
    }


def normalize_group(group, mode):
    if mode == MODE_URL:
        return normalize_url_group(group)
    if mode == MODE_CATEGORY_URL:
        return normalize_category_url_group(group)
    if mode == MODE_SKU:
        return normalize_sku_group(group)
    return normalize_keywords_group(group)


def load_groups_from_json(raw, mode):
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise ValueError("params-json must be valid JSON: {}".format(exc))
    if not isinstance(payload, list) or not payload:
        raise ValueError("params-json must be a non-empty JSON array")
    groups = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Each params-json item must be an object")
        groups.append(normalize_group(item, mode))
    return groups


def build_groups(args, mode):
    if args.params_json:
        return load_groups_from_json(args.params_json, mode)
    if mode == MODE_URL:
        urls = args.url or [DEFAULT_URL]
        return [normalize_group({"url": url, "all_variations": args.all_variations}, mode) for url in urls]
    if mode == MODE_CATEGORY_URL:
        category_urls = args.category_url or [DEFAULT_CATEGORY_URL]
        return [
            normalize_group(
                {
                    "category_url": category_url,
                    "all_variations": args.all_variations,
                    "page_turning": args.page_turning,
                },
                mode,
            )
            for category_url in category_urls
        ]
    if mode == MODE_SKU:
        skus = args.sku or [DEFAULT_SKU]
        return [normalize_group({"sku": sku, "all_variations": args.all_variations}, mode) for sku in skus]
    keywords = args.keyword or [DEFAULT_KEYWORD]
    return [
        normalize_group(
            {
                "keyword": keyword,
                "domain": args.domain,
                "all_variations": args.all_variations,
                "page_turning": args.page_turning,
            },
            mode,
        )
        for keyword in keywords
    ]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "walmart.com",
        "spider_id": spider_id,
        "spider_parameters": json.dumps(groups, ensure_ascii=False, separators=(",", ":")),
        "spider_errors": "true",
        "file_name": file_name,
    }
    body = urllib.parse.urlencode(form).encode("utf-8")
    request = urllib.request.Request(
        BUILDER_URL,
        data=body,
        headers={
            "Authorization": "Bearer {}".format(api_token),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError("Builder request failed with HTTP {}: {}".format(exc.code, detail))
    except urllib.error.URLError as exc:
        raise RuntimeError("Builder request failed: {}".format(exc.reason))

    try:
        payload = json.loads(raw)
    except ValueError:
        raise RuntimeError("Builder returned non-JSON response: {}".format(raw))

    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError("Builder did not return task_id. Response: {}".format(json.dumps(payload, ensure_ascii=False)))
    status = data.get("status") or payload.get("status") or payload.get("message") or "submitted"
    return spider_id, task_id, status


def main():
    if not ensure_python_version():
        return 2

    parser = argparse.ArgumentParser(description="Submit a guided Dataify Walmart Products Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: url, category-url, sku, keywords.")
    parser.add_argument("--url", action="append", help="Product URL mode only. Repeat for multiple product URLs.")
    parser.add_argument("--category-url", action="append", help="Category URL mode only. Repeat for multiple category URLs.")
    parser.add_argument("--sku", action="append", help="SKU mode only. Repeat for multiple SKUs.")
    parser.add_argument("--keyword", action="append", help="Keyword mode only. Repeat for multiple keywords.")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="Keyword mode only. Default: https://www.walmart.com/.")
    parser.add_argument("--all-variations", default=DEFAULT_ALL_VARIATIONS, help="Allowed values: true, false. Default: false.")
    parser.add_argument("--page-turning", default=None, help="Category or keyword mode only. Integer greater than or equal to 0.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of parameter objects for the selected mode.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if not args.api_token:
        print(
            "Missing Dataify API TOKEN. Enter your Dataify API TOKEN to continue. If you want to reuse it later, save it as DATAIFY_API_TOKEN. If you do not have one, log in at {} to get one.".format(LOGIN_URL),
            file=sys.stderr,
        )
        return 2

    try:
        mode = normalize_mode(args.mode)
        if args.page_turning is None:
            args.page_turning = DEFAULT_CATEGORY_PAGE_TURNING if mode == MODE_CATEGORY_URL else DEFAULT_KEYWORD_PAGE_TURNING
        groups = build_groups(args, mode)
        file_name = normalize_file_name(args.file_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        spider_id, task_id, status = submit_builder(args.api_token, mode, groups, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(
        {
            "mode": mode,
            "spider_id": spider_id,
            "task_id": task_id,
            "status": status,
            "parameters": groups,
            "file_name": file_name,
            "dashboard_url": DASHBOARD_URL,
            "message": "Task submitted. Visit {} to view results.".format(DASHBOARD_URL),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
