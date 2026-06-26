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
MODE_KEYWORDS = "keywords"
MODE_LISTURL = "listurl"
SPIDER_IDS = {
    MODE_URL: "ebay_ebay_by-url",
    MODE_CATEGORY_URL: "ebay_ebay_by-category-url",
    MODE_KEYWORDS: "ebay_ebay_by-keywords",
    MODE_LISTURL: "ebay_ebay_by-listurl",
}
DEFAULT_URL = "https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"
DEFAULT_CATEGORY_URL = "https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829"
DEFAULT_KEYWORDS = "baby toys"
DEFAULT_LISTURL = "https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086"
DEFAULT_COUNT = "60"
DEFAULT_FILE_NAME = "{{TasksID}}"


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_ebay_products.py --mode keywords --keywords \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_KEYWORDS,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url, category-url, keywords, or listurl.".format(value))
    return clean


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_ebay_url(value):
    clean = normalize_text(value, "url")
    if not clean.startswith("https://www.ebay.com/"):
        raise ValueError("url must start with https://www.ebay.com/")
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean or not clean.isdigit():
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
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
        "url": normalize_ebay_url(group.get("url", DEFAULT_URL)),
    }


def normalize_category_url_group(group):
    count_value = normalize_non_negative_integer(group.get("count", DEFAULT_COUNT), "count")
    count_upper = normalize_non_negative_integer(group.get("Count", count_value), "Count")
    return {
        "url": normalize_ebay_url(group.get("url", DEFAULT_CATEGORY_URL)),
        "Count": count_upper,
        "count": count_value,
    }


def normalize_keywords_group(group):
    return {
        "keywords": normalize_text(group.get("keywords", DEFAULT_KEYWORDS), "keywords"),
        "count": normalize_non_negative_integer(group.get("count", DEFAULT_COUNT), "count"),
    }


def normalize_listurl_group(group):
    return {
        "url": normalize_ebay_url(group.get("url", DEFAULT_LISTURL)),
        "count": normalize_non_negative_integer(group.get("count", DEFAULT_COUNT), "count"),
    }


def normalize_group(group, mode):
    if mode == MODE_URL:
        return normalize_url_group(group)
    if mode == MODE_CATEGORY_URL:
        return normalize_category_url_group(group)
    if mode == MODE_KEYWORDS:
        return normalize_keywords_group(group)
    return normalize_listurl_group(group)


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
        return [normalize_group({"url": url}, mode) for url in urls]
    if mode == MODE_CATEGORY_URL:
        urls = args.url or [DEFAULT_CATEGORY_URL]
        return [normalize_group({"url": url, "Count": args.count, "count": args.count}, mode) for url in urls]
    if mode == MODE_KEYWORDS:
        keywords = args.keywords or [DEFAULT_KEYWORDS]
        return [normalize_group({"keywords": keyword, "count": args.count}, mode) for keyword in keywords]
    urls = args.url or [DEFAULT_LISTURL]
    return [normalize_group({"url": url, "count": args.count}, mode) for url in urls]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "ebay.com",
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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify eBay Products Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: url, category-url, keywords, listurl.")
    parser.add_argument("--url", action="append", help="Product URL, category URL, or store URL. Repeat for multiple URLs.")
    parser.add_argument("--keywords", action="append", help="Keyword mode only. Repeat for multiple keywords.")
    parser.add_argument("--count", default=DEFAULT_COUNT, help="Integer greater than or equal to 0. Default: 60.")
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
