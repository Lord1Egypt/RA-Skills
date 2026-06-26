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
DATAIFY_URL = "https://dashboard.dataify.com?utm_source=skill"
MIN_PYTHON = (3, 6)
MODE_URL = "url"
MODE_KEYWORD = "keyword"
SPIDER_IDS = {
    MODE_URL: "youtube_profiles_by-url",
    MODE_KEYWORD: "youtube_profiles_by-keyword",
}
DEFAULT_URL = "https://www.youtube.com/@mrbeast"
DEFAULT_KEYWORD = "MrBeast"
DEFAULT_PAGE_TURNING = "1"
DEFAULT_FILE_NAME = "{{TasksID}}"


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_youtube_profiles.py --mode url --url \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_URL,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url or keyword.".format(value))
    return clean


def validate_youtube_url(value):
    clean = str(value).strip()
    parsed = urllib.parse.urlparse(clean)
    if parsed.scheme != "https" or parsed.netloc != "www.youtube.com":
        raise ValueError("URL must use https://www.youtube.com: {}".format(clean))
    return clean


def normalize_keyword(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("keyword cannot be empty")
    return clean


def validate_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    try:
        number = int(clean, 10)
    except ValueError:
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    if number < 0:
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return str(number)


def normalize_file_name(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_url_group(group):
    return {
        "url": validate_youtube_url(group.get("url", DEFAULT_URL)),
    }


def normalize_keyword_group(group):
    return {
        "keyword": normalize_keyword(group.get("keyword", DEFAULT_KEYWORD)),
        "page_turning": validate_non_negative_integer(group.get("page_turning", DEFAULT_PAGE_TURNING), "page_turning"),
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
        if mode == MODE_URL:
            groups.append(normalize_url_group(item))
        else:
            groups.append(normalize_keyword_group(item))
    return groups


def build_groups(args, mode):
    if args.params_json:
        return load_groups_from_json(args.params_json, mode)
    if mode == MODE_URL:
        urls = args.url or [DEFAULT_URL]
        return [normalize_url_group({"url": url}) for url in urls]
    keywords = args.keyword or [DEFAULT_KEYWORD]
    return [
        normalize_keyword_group({
            "keyword": keyword,
            "page_turning": args.page_turning,
        })
        for keyword in keywords
    ]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "youtube.com",
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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify YouTube Profiles Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: url, keyword.")
    parser.add_argument("--url", action="append", help="URL mode only. YouTube channel URL. Repeat for multiple URLs.")
    parser.add_argument("--keyword", action="append", help="Keyword mode only. YouTube channel/profile search keyword. Repeat for multiple keywords.")
    parser.add_argument("--page-turning", default=DEFAULT_PAGE_TURNING, help="Keyword mode only. Number of result pages, integer >= 0. Default: 1.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of parameter objects for the selected mode.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if not args.api_token:
        print(
            "Missing Dataify API TOKEN. Get one from {}.".format(DATAIFY_URL),
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
