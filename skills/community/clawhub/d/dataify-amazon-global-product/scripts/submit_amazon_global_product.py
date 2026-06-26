#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_FILE_NAME = "{{TasksID}}"
MIN_PYTHON = (3, 6)
DATAIFY_URL = "https://dashboard.dataify.com?utm_source=skill"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
DEFAULT_PRODUCT_URL = "https://www.amazon.com/dp/B0CHHSFMRL/"
DEFAULT_CATEGORY_URL = "https://www.amazon.com/s?i=luggage-intl-ship"
DEFAULT_DOMAIN = "https://www.amazon.com"
BUILDER_URLS = {
    "product-url": "https://scraperapi.dataify.com/builder",
    "category-url": "https://scraperapi.dataify.com/builder?platform=1",
    "keyword": "https://scraperapi.dataify.com/builder?platform=1",
    "keyword-brand": "https://scraperapi.dataify.com/builder?platform=1",
}
SPIDER_IDS = {
    "product-url": "amazon_global-product_by-url",
    "category-url": "amazon_global-product_by-category-url",
    "keyword": "amazon_global-product_by-keywords",
    "keyword-brand": "amazon_global-product_by-keywords-brand",
}


def ensure_utf8_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_amazon_global_product.py product-url".format(
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
    print("Missing Dataify API TOKEN. Get one from {}.".format(DATAIFY_URL), file=sys.stderr)
    return False


def normalize_file_name(value):
    file_name = value.strip() if value else ""
    if not file_name:
        raise ValueError("File name cannot be empty.")
    return file_name


def normalize_sort_by(value):
    options = {
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
    clean = value.strip() if value else ""
    if clean in options:
        return options[clean]
    raise ValueError("Unsupported sort_by '{}'. Use one of: Best Sellers, Newest Arrivals, Avg. Customer Review, Price: High to Low, Price: Low to High, Featured.".format(value))


def normalize_get_sponsored(value):
    clean = value.strip().lower() if value else ""
    if clean in ("true", "false"):
        return clean
    raise ValueError("get_sponsored must be true or false.")


def submit_builder(builder_url, spider_id, api_token, spider_parameters, file_name):
    form = {
        "spider_name": "amazon.com",
        "spider_id": spider_id,
        "spider_parameters": json.dumps(spider_parameters, separators=(",", ":"), ensure_ascii=False),
        "spider_errors": "true",
        "file_name": file_name,
    }
    body = urllib.parse.urlencode(form).encode("utf-8")
    request = urllib.request.Request(
        builder_url,
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


def handle_product_url(args):
    url = args.url.strip()
    if not url:
        raise ValueError("URL cannot be empty.")
    file_name = normalize_file_name(args.file_name)
    parameters = [{"url": url}]
    summary = {"url": url, "file_name": file_name}
    return BUILDER_URLS["product-url"], SPIDER_IDS["product-url"], parameters, file_name, summary


def handle_category_url(args):
    url = args.url.strip()
    if not url:
        raise ValueError("URL cannot be empty.")
    if args.maximum < 0:
        raise ValueError("Maximum must be greater than or equal to 0.")
    sort_by = normalize_sort_by(args.sort_by)
    get_sponsored = normalize_get_sponsored(args.get_sponsored)
    file_name = normalize_file_name(args.file_name)
    parameters = [{
        "url": url,
        "maximum": str(args.maximum),
        "sort_by": sort_by,
        "get_sponsored": get_sponsored,
    }]
    summary = {
        "url": url,
        "maximum": str(args.maximum),
        "sort_by": sort_by,
        "get_sponsored": get_sponsored,
        "file_name": file_name,
    }
    return BUILDER_URLS["category-url"], SPIDER_IDS["category-url"], parameters, file_name, summary


def handle_keyword(args):
    keyword = args.keyword.strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")
    domain = args.domain.strip()
    if not domain:
        raise ValueError("Domain cannot be empty.")
    if args.lowest_price < 0:
        raise ValueError("Lowest price must be greater than or equal to 0.")
    if args.highest_price < 0:
        raise ValueError("Highest price must be greater than or equal to 0.")
    if args.highest_price < args.lowest_price:
        raise ValueError("Highest price cannot be less than lowest price.")
    if args.page_turning < 0:
        raise ValueError("Page turning must be greater than or equal to 0.")
    file_name = normalize_file_name(args.file_name)
    parameters = [{
        "keyword": keyword,
        "domain": domain,
        "lowest_price": str(args.lowest_price),
        "highest_price": str(args.highest_price),
        "page_turning": str(args.page_turning),
    }]
    summary = {
        "keyword": keyword,
        "domain": domain,
        "lowest_price": str(args.lowest_price),
        "highest_price": str(args.highest_price),
        "page_turning": str(args.page_turning),
        "file_name": file_name,
    }
    return BUILDER_URLS["keyword"], SPIDER_IDS["keyword"], parameters, file_name, summary


def handle_keyword_brand(args):
    keyword = args.keyword.strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")
    brands = args.brands.strip()
    if not brands:
        raise ValueError("Brands cannot be empty.")
    if args.page_turning < 0:
        raise ValueError("Page turning must be greater than or equal to 0.")
    file_name = normalize_file_name(args.file_name)
    parameters = [{
        "keyword": keyword,
        "brands": brands,
        "page_turning": str(args.page_turning),
    }]
    summary = {
        "keyword": keyword,
        "brands": brands,
        "page_turning": str(args.page_turning),
        "file_name": file_name,
    }
    return BUILDER_URLS["keyword-brand"], SPIDER_IDS["keyword-brand"], parameters, file_name, summary


def build_parser():
    parser = argparse.ArgumentParser(description="Submit Dataify Amazon global product Builder tasks.")
    subparsers = parser.add_subparsers(dest="mode")
    subparsers.required = True

    product_url = subparsers.add_parser("product-url", help="Collect global product details by product URL.")
    product_url.add_argument("--url", default=DEFAULT_PRODUCT_URL, help="Amazon product URL.")
    add_common_args(product_url)
    product_url.set_defaults(handler=handle_product_url)

    category_url = subparsers.add_parser("category-url", help="Collect global product details from a category URL.")
    category_url.add_argument("--url", default=DEFAULT_CATEGORY_URL, help="Amazon category URL.")
    category_url.add_argument("--maximum", default=5, type=int, help="Maximum number of products to collect. Defaults to 5.")
    category_url.add_argument("--sort-by", default="Best Sellers", help="Sort option. Defaults to Best Sellers.")
    category_url.add_argument("--get-sponsored", default="true", help="Whether to include sponsored products: true or false. Defaults to true.")
    add_common_args(category_url)
    category_url.set_defaults(handler=handle_category_url)

    keyword = subparsers.add_parser("keyword", help="Collect global product details from a keyword search.")
    keyword.add_argument("--keyword", default="coffee", help="Amazon search keyword. Defaults to coffee.")
    keyword.add_argument("--domain", default=DEFAULT_DOMAIN, help="Amazon domain. Defaults to https://www.amazon.com.")
    keyword.add_argument("--lowest-price", default=20, type=int, help="Lowest price. Defaults to 20.")
    keyword.add_argument("--highest-price", default=50, type=int, help="Highest price. Defaults to 50.")
    keyword.add_argument("--page-turning", default=2, type=int, help="Number of pages to collect. Defaults to 2.")
    add_common_args(keyword)
    keyword.set_defaults(handler=handle_keyword)

    keyword_brand = subparsers.add_parser("keyword-brand", help="Collect global product details from a keyword and brand filter.")
    keyword_brand.add_argument("--keyword", default="shirts", help="Amazon search keyword. Defaults to shirts.")
    keyword_brand.add_argument("--brands", default="Adidas", help="Brand filter. Defaults to Adidas.")
    keyword_brand.add_argument("--page-turning", default=2, type=int, help="Number of pages to collect. Defaults to 2.")
    add_common_args(keyword_brand)
    keyword_brand.set_defaults(handler=handle_keyword_brand)

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
        builder_url, spider_id, spider_parameters, file_name, summary = args.handler(args)
        task_id = submit_builder(builder_url, spider_id, args.api_token, spider_parameters, file_name)
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
