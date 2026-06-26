#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder?platform=1"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
LOGIN_URL = "https://dashboard.dataify.com/login?utm_source=skill"
MIN_PYTHON = (3, 6)

MODE_DETAIL_URL = "detail-url"
MODE_ALLREEL_URL = "allreel-url"
MODE_LISTURL = "listurl"
SPIDER_IDS = {
    MODE_DETAIL_URL: "ins_reel_by-url",
    MODE_ALLREEL_URL: "ins_allreel_by-url",
    MODE_LISTURL: "ins_reel_by-listurl",
}
DEFAULT_URLS = {
    MODE_DETAIL_URL: "https://www.instagram.com/reel/C5Rdyj_q7YN/",
    MODE_ALLREEL_URL: "https://www.instagram.com/billieeilish",
    MODE_LISTURL: "https://www.instagram.com/espn",
}
DEFAULT_NUM_OF_POSTS = "10"
DEFAULT_POSTS_TO_NOT_INCLUDE = "DP861NijuwE"
DEFAULT_START_DATE = "01-28-2025"
DEFAULT_END_DATE = "01-28-2026"
DEFAULT_FILE_NAME = "{{TasksID}}"
DATE_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_instagram_reels.py --mode detail-url --url \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_URLS[MODE_DETAIL_URL],
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use detail-url, allreel-url, or listurl.".format(value))
    return clean


def normalize_url(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("url cannot be empty")
    if not clean.startswith("https://www.instagram.com/"):
        raise ValueError("url must start with https://www.instagram.com/")
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean or not clean.isdigit():
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return clean


def normalize_date(value, field_name):
    clean = str(value).strip()
    if not DATE_RE.match(clean):
        raise ValueError("{} must use mm-dd-yyyy format".format(field_name))
    try:
        parsed = datetime.datetime.strptime(clean, "%m-%d-%Y").date()
    except ValueError:
        raise ValueError("{} must use mm-dd-yyyy format".format(field_name))
    return clean, parsed


def normalize_optional_text(value, default):
    if value is None:
        return default
    return str(value).strip()


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_detail_group(group):
    return {
        "url": normalize_url(group.get("url", DEFAULT_URLS[MODE_DETAIL_URL])),
    }


def normalize_list_group(group, mode):
    start_date, start_parsed = normalize_date(group.get("start_date", DEFAULT_START_DATE), "start_date")
    end_date, end_parsed = normalize_date(group.get("end_date", DEFAULT_END_DATE), "end_date")
    if start_parsed > end_parsed:
        raise ValueError("start_date must be on or before end_date")
    return {
        "url": normalize_url(group.get("url", DEFAULT_URLS[mode])),
        "num_of_posts": normalize_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
        "posts_to_not_include": normalize_optional_text(group.get("posts_to_not_include"), DEFAULT_POSTS_TO_NOT_INCLUDE),
        "start_date": start_date,
        "end_date": end_date,
    }


def normalize_group(group, mode):
    if mode == MODE_DETAIL_URL:
        return normalize_detail_group(group)
    return normalize_list_group(group, mode)


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
    groups = []
    for url in urls:
        group = {"url": url}
        if mode != MODE_DETAIL_URL:
            group.update({
                "num_of_posts": args.num_of_posts,
                "posts_to_not_include": args.posts_to_not_include,
                "start_date": args.start_date,
                "end_date": args.end_date,
            })
        groups.append(normalize_group(group, mode))
    return groups


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "instagram.com",
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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify Instagram Reels Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: detail-url, allreel-url, listurl.")
    parser.add_argument("--url", action="append", help="Instagram URL. Repeat for multiple URLs.")
    parser.add_argument("--num-of-posts", default=DEFAULT_NUM_OF_POSTS, help="List modes only. Integer greater than or equal to 0.")
    parser.add_argument("--posts-to-not-include", default=DEFAULT_POSTS_TO_NOT_INCLUDE, help="List modes only. Reel post IDs or PK values to exclude.")
    parser.add_argument("--start-date", default=DEFAULT_START_DATE, help="List modes only. Start date in mm-dd-yyyy format.")
    parser.add_argument("--end-date", default=DEFAULT_END_DATE, help="List modes only. End date in mm-dd-yyyy format.")
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
