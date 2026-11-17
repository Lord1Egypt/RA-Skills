#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

TASK_RUNTIME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "dataify-task-operations", "scripts"))
if TASK_RUNTIME_DIR not in sys.path:
    sys.path.insert(0, TASK_RUNTIME_DIR)
from task_runtime import complete_task, extract_task_id


BUILDER_URL = "https://scraperapi.dataify.com/builder"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
DATAIFY_URL = "https://dashboard.dataify.com?utm_source=skill"
DEFAULT_KEYWORD = "https://www.amazon.com/sp?ie=UTF8&seller=ADZ7LD48GVFQJ&asin=B07H56J7K1&ref_=dp_merchant_link&isAmazonFulfilled=1"
DEFAULT_DOMAIN = "https://www.amazon.com/"
DEFAULT_FILE_NAME = "{{TasksID}}"
MIN_PYTHON = (3, 6)


def ensure_utf8_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print("Python {}.{} or newer is required. Run this script with a Python 3 interpreter.".format(MIN_PYTHON[0], MIN_PYTHON[1]), file=sys.stderr)
        return False
    return True


def submit_builder(api_token, keyword, domain, page_turning, file_name):
    form = {
        "spider_name": "amazon.com",
        "spider_id": "amazon_product-list_by-keywords-domain",
        "spider_parameters": json.dumps([{
            "keyword": keyword,
            "domain": domain,
            "page_turning": str(page_turning),
        }], separators=(",", ":"), ensure_ascii=False),
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
    task_id = extract_task_id(payload)
    if not task_id:
        raise RuntimeError("Builder did not return task_id. Response: {}".format(json.dumps(payload, ensure_ascii=False)))
    return task_id


def main():
    ensure_utf8_output()
    if not ensure_python_version():
        return 2

    parser = argparse.ArgumentParser(description="Submit a Dataify Amazon product list Builder task.")
    parser.add_argument("--keyword", required=True, help="Amazon product-list keyword query.")
    parser.add_argument("--domain", help="Amazon domain. Defaults to https://www.amazon.com/.")
    parser.add_argument("--page-turning", default=1, type=int, help="Number of pages to collect. Defaults to 1.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name value. Defaults to {{TasksID}}.")
    parser.add_argument("--no-wait", action="store_true", help="Return after submission without waiting for the final result.")
    parser.add_argument("--wait-timeout", type=float, default=600, help="Maximum final-result wait in seconds.")
    args = parser.parse_args()
    api_token = os.environ.get("DATAIFY_API_TOKEN", "").strip()

    if not api_token:
        print("Missing Dataify API TOKEN. Get one from {}. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.".format(DATAIFY_URL), file=sys.stderr)
        return 2

    keyword = args.keyword.strip()
    if not keyword:
        print("Keyword cannot be empty.", file=sys.stderr)
        return 2
    domain = (args.domain or DEFAULT_DOMAIN).strip()
    if not domain:
        print("Domain cannot be empty.", file=sys.stderr)
        return 2
    if args.page_turning < 0:
        print("Page turning must be greater than or equal to 0.", file=sys.stderr)
        return 2
    file_name = args.file_name.strip()
    if not file_name:
        print("File name cannot be empty.", file=sys.stderr)
        return 2

    try:
        task_id = submit_builder(api_token, keyword, domain, args.page_turning, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps({
        "task_id": task_id,
        "keyword": keyword,
        "domain": domain,
        "page_turning": str(args.page_turning),
        "file_name": file_name,
        "message": "Task submitted. Continue monitoring the returned task_id.",
    }, ensure_ascii=False, indent=2))
    if not args.no_wait:
        try:
            final_result = complete_task(task_id, api_token, args.wait_timeout)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps(final_result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
