#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
DATAIFY_URL = "https://dashboard.dataify.com?utm_source=skill"
DEFAULT_URL = "https://www.amazon.com/HISDERN-Checkered-Handkerchief-Classic-Necktie/dp/B0BRXPR726"
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


def submit_builder(api_token, url, file_name):
    form = {
        "spider_name": "amazon.com",
        "spider_id": "amazon_comment_by-url",
        "spider_parameters": json.dumps([{"url": url}], separators=(",", ":"), ensure_ascii=False),
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


def main():
    ensure_utf8_output()
    if not ensure_python_version():
        return 2

    parser = argparse.ArgumentParser(description="Submit a Dataify Amazon comment Builder task.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Amazon product URL. Defaults to the sample product URL.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name value. Defaults to {{TasksID}}.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if not args.api_token:
        print("Missing Dataify API TOKEN. Get one from {}.".format(DATAIFY_URL), file=sys.stderr)
        return 2

    url = args.url.strip()
    if not url:
        print("URL cannot be empty.", file=sys.stderr)
        return 2
    file_name = args.file_name.strip()
    if not file_name:
        print("File name cannot be empty.", file=sys.stderr)
        return 2

    try:
        task_id = submit_builder(args.api_token, url, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps({
        "task_id": task_id,
        "url": url,
        "file_name": file_name,
        "dashboard_url": DASHBOARD_URL,
        "message": "Task submitted. Visit {} to view results.".format(DASHBOARD_URL),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
