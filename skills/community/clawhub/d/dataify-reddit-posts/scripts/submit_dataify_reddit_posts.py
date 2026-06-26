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
MODE_KEYWORDS = "keywords"
MODE_SUBREDDITURL = "subredditurl"
SPIDER_IDS = {
    MODE_URL: "reddit_posts_by-url",
    MODE_KEYWORDS: "reddit_posts_by-keywords",
    MODE_SUBREDDITURL: "reddit_posts_by-subredditurl",
}
DEFAULT_URL = "https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"
DEFAULT_KEYWORD = "datascience"
DEFAULT_SUBREDDIT_URL = "https://www.reddit.com/r/battlefield2042"
DEFAULT_NUM_OF_POSTS = "10"
DEFAULT_SORT_BY = "Hot"
DEFAULT_SORT_BY_TIME = "Now"
DEFAULT_FILE_NAME = "{{TasksID}}"
SORT_BY_VALUES = ("Hot", "Top", "New", "Rising")
SORT_BY_TIME_VALUES = ("Now", "Today", "This Week", "This Month", "This Year", "All Time")


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_reddit_posts.py --mode keywords --keyword \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_KEYWORD,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url, keywords, or subredditurl.".format(value))
    return clean


def normalize_url(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("url cannot be empty")
    if not clean.startswith("https://www.reddit.com/"):
        raise ValueError("url must start with https://www.reddit.com/")
    return clean


def normalize_keyword(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("keyword cannot be empty")
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean or not clean.isdigit():
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return clean


def normalize_choice(value, field_name, allowed):
    clean = str(value).strip()
    for item in allowed:
        if clean.lower() == item.lower():
            return item
    raise ValueError("{} must be one of {}".format(field_name, ", ".join(allowed)))


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_url_group(group):
    return {
        "url": normalize_url(group.get("url", DEFAULT_URL)),
    }


def normalize_keywords_group(group):
    return {
        "keyword": normalize_keyword(group.get("keyword", DEFAULT_KEYWORD)),
        "num_of_posts": normalize_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
    }


def normalize_subredditurl_group(group):
    return {
        "url": normalize_url(group.get("url", DEFAULT_SUBREDDIT_URL)),
        "sort_by": normalize_choice(group.get("sort_by", DEFAULT_SORT_BY), "sort_by", SORT_BY_VALUES),
        "num_of_posts": normalize_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
        "sort_by_time": normalize_choice(group.get("sort_by_time", DEFAULT_SORT_BY_TIME), "sort_by_time", SORT_BY_TIME_VALUES),
    }


def normalize_group(group, mode):
    if mode == MODE_URL:
        return normalize_url_group(group)
    if mode == MODE_KEYWORDS:
        return normalize_keywords_group(group)
    return normalize_subredditurl_group(group)


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
    if mode == MODE_KEYWORDS:
        keywords = args.keyword or [DEFAULT_KEYWORD]
        return [
            normalize_group(
                {
                    "keyword": keyword,
                    "num_of_posts": args.num_of_posts,
                },
                mode,
            )
            for keyword in keywords
        ]
    urls = args.url or [DEFAULT_SUBREDDIT_URL]
    return [
        normalize_group(
            {
                "url": url,
                "sort_by": args.sort_by,
                "num_of_posts": args.num_of_posts,
                "sort_by_time": args.sort_by_time,
            },
            mode,
        )
        for url in urls
    ]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "reddit.com",
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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify Reddit Posts Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: url, keywords, subredditurl.")
    parser.add_argument("--url", action="append", help="URL mode or subredditurl mode. Repeat for multiple URLs.")
    parser.add_argument("--keyword", action="append", help="Keywords mode only. Repeat for multiple keywords.")
    parser.add_argument("--num-of-posts", default=DEFAULT_NUM_OF_POSTS, help="Integer greater than or equal to 0.")
    parser.add_argument("--sort-by", default=DEFAULT_SORT_BY, help="Subreddit URL mode only. One of: Hot, Top, New, Rising.")
    parser.add_argument("--sort-by-time", default=DEFAULT_SORT_BY_TIME, help="Subreddit URL mode only. One of: Now, Today, This Week, This Month, This Year, All Time.")
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
