#!/usr/bin/env python3
"""Query the Dataify scraper task-status endpoint without exposing the API key."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


ENDPOINT = "https://scraperapi.dataify.com/task_status"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
SUCCESS_STATUS = "成功"


def configure_utf8_output():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")


def normalize_task_id(value):
    task_id = str(value).strip()
    if not task_id:
        raise ValueError("task-id cannot be empty")
    return task_id


def build_url(task_id, api_key):
    query = urllib.parse.urlencode({"api_key": api_key, "task_id": task_id})
    return "{}?{}".format(ENDPOINT, query)


def build_download_url(task_id, api_key):
    endpoint = "{}/download".format(ENDPOINT.rsplit("/", 1)[0])
    query = urllib.parse.urlencode({"api_key": api_key, "task_id": task_id, "type": "json"})
    return "{}?{}".format(endpoint, query)


def redact_api_key(value, api_key):
    return value.replace(api_key, "<redacted>") if api_key else value


def is_successful_status(response_text):
    try:
        payload = json.loads(response_text)
    except ValueError:
        return False
    data = payload.get("data")
    return isinstance(data, dict) and data.get("status") == SUCCESS_STATUS


def download_task_result(task_id, api_key):
    request = urllib.request.Request(build_download_url(task_id, api_key), method="GET")
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return content.decode(charset, errors="replace")


def main():
    configure_utf8_output()
    parser = argparse.ArgumentParser(description="Query a Dataify scraper task by task ID.")
    parser.add_argument("--task-id", required=True, help="Task ID returned by a Dataify scraper submission.")
    parser.add_argument("--dry-run", action="store_true", help="Preview the request with the API key redacted.")
    args = parser.parse_args()

    try:
        task_id = normalize_task_id(args.task_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    api_key = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    if args.dry_run:
        print(json.dumps({
            "method": "GET",
            "url": build_url(task_id, "<redacted>"),
        }, ensure_ascii=False, indent=2))
        return 0

    if not api_key:
        print(
            "DATAIFY_API_TOKEN is not set. Sign in at {} to obtain an API key. New accounts receive 50 free credits.".format(DASHBOARD_URL),
            file=sys.stderr,
        )
        return 2

    request = urllib.request.Request(build_url(task_id, api_key), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            response_text = content.decode(charset, errors="replace")
            print(redact_api_key(response_text, api_key))
            if is_successful_status(response_text):
                print(redact_api_key(download_task_result(task_id, api_key), api_key))
            return 0
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(redact_api_key(detail, api_key) or "HTTP {}".format(exc.code), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print("Request failed: {}".format(exc.reason), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
