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
MODE_EVENTLIST_URL = "eventlist-url"
MODE_SEARCH_URL = "search-url"
MODE_EVENTS_URL = "events-url"
SPIDER_IDS = {
    MODE_EVENTLIST_URL: "facebook_event_by-eventlist-url",
    MODE_SEARCH_URL: "facebook_event_by-search-url",
    MODE_EVENTS_URL: "facebook_event_by-events-url",
}
DEFAULT_URLS = {
    MODE_EVENTLIST_URL: "https://www.facebook.com/nohoclub/events",
    MODE_SEARCH_URL: "https://www.facebook.com/events/explore/us-atlanta/107991659233606",
    MODE_EVENTS_URL: "https://www.facebook.com/events/1546764716269782",
}
DEFAULT_FILE_NAME = "{{TasksID}}"


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_facebook_events.py --mode events-url --url \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_URLS[MODE_EVENTS_URL],
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use eventlist-url, search-url, or events-url.".format(value))
    return clean


def normalize_url(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("url cannot be empty")
    if not clean.startswith("https://www.facebook.com/"):
        raise ValueError("url must start with https://www.facebook.com/")
    return clean


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_group(group, mode):
    return {
        "url": normalize_url(group.get("url", DEFAULT_URLS[mode])),
    }


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
    urls = args.url or [DEFAULT_URLS[mode]]
    return [normalize_group({"url": url}, mode) for url in urls]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "facebook.com",
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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify Facebook Events Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: eventlist-url, search-url, events-url.")
    parser.add_argument("--url", action="append", help="Facebook URL. Repeat for multiple URLs.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of url parameter objects for the selected mode.")
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
