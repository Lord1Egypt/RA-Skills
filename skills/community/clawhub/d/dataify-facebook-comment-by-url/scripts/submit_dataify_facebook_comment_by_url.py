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
SPIDER_ID = "facebook_comment_by-comments-url"
DEFAULT_URL = "https://www.facebook.com/share/p/1K6xfHFkrK/"
DEFAULT_GET_ALL_REPLIES = "True"
DEFAULT_LIMIT_RECORDS = "10"
DEFAULT_COMMENTS_SORT = "All comments"
DEFAULT_FILE_NAME = "{{TasksID}}"

GET_ALL_REPLIES_OPTIONS = [("True", "True"), ("Flase", "Flase")]
COMMENTS_SORT_OPTIONS = [("最相关", "Most Relevent"), ("由新到旧", "Newest"), ("所有评论", "All comments")]


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_facebook_comment_by_url.py --url \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_URL,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_url(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("url cannot be empty")
    if not clean.startswith("https://www.facebook.com/"):
        raise ValueError("url must start with https://www.facebook.com/")
    return clean


def normalize_choice(value, options, field_name):
    clean = str(value).strip()
    allowed = {option_value for _, option_value in options}
    if clean not in allowed:
        raise ValueError("Unsupported {}: {}. Use an allowed dropdown value.".format(field_name, clean))
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean:
        return DEFAULT_LIMIT_RECORDS
    try:
        number = int(clean, 10)
    except ValueError:
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    if number < 0:
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return str(number)


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_group(group):
    return {
        "url": normalize_url(group.get("url", DEFAULT_URL)),
        "get_all_replies": normalize_choice(group.get("get_all_replies", DEFAULT_GET_ALL_REPLIES), GET_ALL_REPLIES_OPTIONS, "get_all_replies"),
        "limit_records": normalize_non_negative_integer(group.get("limit_records", DEFAULT_LIMIT_RECORDS), "limit_records"),
        "comments_sort": normalize_choice(group.get("comments_sort", DEFAULT_COMMENTS_SORT), COMMENTS_SORT_OPTIONS, "comments_sort"),
    }


def load_groups_from_json(raw):
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
        groups.append(normalize_group(item))
    return groups


def build_groups(args):
    if args.params_json:
        return load_groups_from_json(args.params_json)
    urls = args.url or [DEFAULT_URL]
    return [
        normalize_group({
            "url": url,
            "get_all_replies": args.get_all_replies,
            "limit_records": args.limit_records,
            "comments_sort": args.comments_sort,
        })
        for url in urls
    ]


def submit_builder(api_token, groups, file_name):
    form = {
        "spider_name": "facebook.com",
        "spider_id": SPIDER_ID,
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
    return task_id, status


def main():
    if not ensure_python_version():
        return 2

    parser = argparse.ArgumentParser(description="Submit a Dataify Facebook post comment by URL Builder task.")
    parser.add_argument("--url", action="append", help="Facebook post URL. Repeat for multiple URLs.")
    parser.add_argument("--get-all-replies", default=DEFAULT_GET_ALL_REPLIES, help="get_all_replies value. Default: True.")
    parser.add_argument("--limit-records", default=DEFAULT_LIMIT_RECORDS, help="limit_records value, integer >= 0. Default: 10.")
    parser.add_argument("--comments-sort", default=DEFAULT_COMMENTS_SORT, help="comments_sort value. Default: All comments.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of comment parameter objects.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if not args.api_token:
        print(
            "Missing Dataify API TOKEN. Enter your Dataify API TOKEN to continue. If you want to reuse it later, save it as DATAIFY_API_TOKEN. If you do not have one, log in at {} to get one.".format(LOGIN_URL),
            file=sys.stderr,
        )
        return 2

    try:
        groups = build_groups(args)
        file_name = normalize_file_name(args.file_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        task_id, status = submit_builder(args.api_token, groups, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(
        {
            "spider_id": SPIDER_ID,
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
