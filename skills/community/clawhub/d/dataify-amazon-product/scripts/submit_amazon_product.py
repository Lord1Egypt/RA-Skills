#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
DATAIFY_URL = "https://dashboard.dataify.com?utm_source=skill"
DEFAULT_FILE_NAME = "{{TasksID}}"
MIN_PYTHON = (3, 6)


def ensure_utf8_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_amazon_product.py asin B0BZYCJK89".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
            ),
            file=sys.stderr,
        )
        return False
    return True


def require_token(api_token):
    if api_token:
        return True
    print(
        "Missing Dataify API TOKEN. Get one from {}.".format(DATAIFY_URL),
        file=sys.stderr,
    )
    return False


def normalize_file_name(value):
    file_name = value.strip() if value else ""
    if not file_name:
        raise ValueError("File name cannot be empty.")
    return file_name


def extract_asin(value):
    text = value.strip()
    if not text:
        return None

    patterns = [
        r"/dp/([A-Z0-9]{10})(?:[/?#]|$)",
        r"/gp/product/([A-Z0-9]{10})(?:[/?#]|$)",
        r"(?:^|[?&])asin=([A-Z0-9]{10})(?:&|$)",
    ]
    upper = text.upper()
    for pattern in patterns:
        match = re.search(pattern, upper)
        if match:
            return match.group(1)

    if re.fullmatch(r"[A-Z0-9]{10}", upper):
        return upper
    return None


def normalize_urls(values):
    urls = []
    for value in values:
        clean = value.strip()
        if clean and clean not in urls:
            urls.append(clean)
    return urls


def sort_options():
    return {
        "best sellers": "Best Sellers",
        "Best Sellers": "Best Sellers",
        "newest arrivals": "Newest Arrivals",
        "Newest Arrivals": "Newest Arrivals",
        "average customer review": "Avg. Customer Review",
        "Avg. Customer Review": "Avg. Customer Review",
        "price high to low": "Price: High to Low",
        "Price: High to Low": "Price: High to Low",
        "price low to high": "Price: Low to High",
        "Price: Low to High": "Price: Low to High",
        "featured recommendations": "Featured",
        "Featured": "Featured",
    }


def normalize_sort_by(value):
    sort_by = value.strip() if value else ""
    options = sort_options()
    if sort_by in options:
        return options[sort_by]
    raise ValueError("Unsupported sort_by '{}'. Use one of: Best Sellers, Newest Arrivals, Avg. Customer Review, Price: High to Low, Price: Low to High, Featured.".format(value))


def submit_builder(api_token, spider_id, spider_parameters, file_name):
    form = {
        "spider_name": "amazon.com",
        "spider_id": spider_id,
        "spider_parameters": json.dumps(spider_parameters, separators=(",", ":"), ensure_ascii=False),
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
    except json.JSONDecodeError:
        raise RuntimeError("Builder returned non-JSON response: {}".format(raw))

    task_id = payload.get("data", {}).get("task_id")
    if not task_id:
        raise RuntimeError("Builder did not return task_id. Response: {}".format(json.dumps(payload, ensure_ascii=False)))
    return task_id


def add_common_args(parser):
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name value. Defaults to {{TasksID}}.")


def handle_asin(args):
    asins = []
    for value in args.asins:
        asin = extract_asin(value)
        if asin and asin not in asins:
            asins.append(asin)
    if not asins:
        raise ValueError("No valid ASINs were provided.")

    file_name = normalize_file_name(args.file_name)
    parameters = [{"asin": asin} for asin in asins]
    return "amazon_product_by-asin", parameters, file_name, {"asins": asins, "file_name": file_name}


def handle_url(args):
    zip_code = args.zip_code.strip()
    if not zip_code:
        raise ValueError("Zip code cannot be empty.")

    urls = normalize_urls(args.urls)
    if not urls:
        raise ValueError("No valid URLs were provided.")

    file_name = normalize_file_name(args.file_name)
    parameters = [{"url": url, "zip_code": zip_code} for url in urls]
    return "amazon_product_by-url", parameters, file_name, {"urls": urls, "zip_code": zip_code, "file_name": file_name}


def handle_keyword(args):
    keyword = args.keyword.strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")
    if args.page_turning < 1:
        raise ValueError("Page turning must be greater than or equal to 1.")
    if args.lowest_price > args.highest_price:
        raise ValueError("Lowest price cannot be greater than highest price.")

    file_name = normalize_file_name(args.file_name)
    parameters = [
        {
            "keyword": keyword,
            "page_turning": args.page_turning,
            "lowest_price": args.lowest_price,
            "highest_price": args.highest_price,
        }
    ]
    return "amazon_product_by-keywords", parameters, file_name, {
        "keyword": keyword,
        "page_turning": args.page_turning,
        "lowest_price": args.lowest_price,
        "highest_price": args.highest_price,
        "file_name": file_name,
    }


def handle_category_url(args):
    url = args.url.strip()
    if not url:
        raise ValueError("URL cannot be empty.")
    if args.page_turning < 1:
        raise ValueError("Page turning must be greater than or equal to 1.")

    sort_by = normalize_sort_by(args.sort_by)
    file_name = normalize_file_name(args.file_name)
    parameters = [{"url": url, "page_turning": args.page_turning, "sort_by": sort_by}]
    return "amazon_product_by-category-url", parameters, file_name, {
        "url": url,
        "page_turning": args.page_turning,
        "sort_by": sort_by,
        "file_name": file_name,
    }


def handle_best_sellers_url(args):
    url = args.url.strip()
    if not url:
        raise ValueError("URL cannot be empty.")
    if args.page_turning < 1:
        raise ValueError("Page turning must be greater than or equal to 1.")

    file_name = normalize_file_name(args.file_name)
    parameters = [{"url": url, "page_turning": args.page_turning}]
    return "amazon_product_by-best-sellers", parameters, file_name, {
        "url": url,
        "page_turning": args.page_turning,
        "file_name": file_name,
    }


def build_parser():
    parser = argparse.ArgumentParser(description="Submit Dataify Amazon product Builder tasks.")
    subparsers = parser.add_subparsers(dest="mode")
    subparsers.required = True

    asin = subparsers.add_parser("asin", help="Collect product details by ASIN.")
    asin.add_argument("asins", nargs="+", help="ASINs or Amazon product URLs.")
    add_common_args(asin)
    asin.set_defaults(handler=handle_asin)

    url = subparsers.add_parser("url", help="Collect product details by product URL and zip code.")
    url.add_argument("urls", nargs="+", help="Amazon product URLs.")
    url.add_argument("--zip-code", required=True, help="Zip code to use for each Amazon URL.")
    add_common_args(url)
    url.set_defaults(handler=handle_url)

    keyword = subparsers.add_parser("keyword", help="Collect Amazon keyword search results.")
    keyword.add_argument("--keyword", required=True, help="Amazon search keyword.")
    keyword.add_argument("--page-turning", default=2, type=int, help="Number of search result pages to collect. Defaults to 2.")
    keyword.add_argument("--lowest-price", default=10, type=float, help="Lowest price filter. Defaults to 10.")
    keyword.add_argument("--highest-price", default=50, type=float, help="Highest price filter. Defaults to 50.")
    add_common_args(keyword)
    keyword.set_defaults(handler=handle_keyword)

    category_url = subparsers.add_parser("category-url", help="Collect Amazon category listing results.")
    category_url.add_argument("--url", required=True, help="Amazon category URL.")
    category_url.add_argument("--page-turning", required=True, type=int, help="Number of category pages to collect.")
    category_url.add_argument("--sort-by", default="Best Sellers", help="Sort option. Defaults to Best Sellers.")
    add_common_args(category_url)
    category_url.set_defaults(handler=handle_category_url)

    best_sellers_url = subparsers.add_parser("best-sellers-url", help="Collect Amazon Best Sellers listing results.")
    best_sellers_url.add_argument("--url", required=True, help="Amazon Best Sellers category URL.")
    best_sellers_url.add_argument("--page-turning", required=True, type=int, help="Number of Best Sellers pages to collect.")
    add_common_args(best_sellers_url)
    best_sellers_url.set_defaults(handler=handle_best_sellers_url)

    return parser


def main():
    ensure_utf8_output()
    if not ensure_python_version():
        return 2

    parser = build_parser()
    args = parser.parse_args()

    if not require_token(args.api_token):
        return 2

    try:
        spider_id, spider_parameters, file_name, summary = args.handler(args)
        task_id = submit_builder(args.api_token, spider_id, spider_parameters, file_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output = {
        "task_id": task_id,
        "mode": args.mode,
        "spider_id": spider_id,
        "dashboard_url": DASHBOARD_URL,
        "message": "Task submitted. Visit {} to view results.".format(DASHBOARD_URL),
    }
    output.update(summary)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
