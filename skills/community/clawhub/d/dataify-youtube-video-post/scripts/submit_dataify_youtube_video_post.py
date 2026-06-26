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
MODE_SEARCH_FILTERS = "search_filters"
MODE_HASHTAG = "hashtag"
MODE_PODCAST_URL = "podcast_url"
MODE_KEYWORD = "keyword"
MODE_EXPLORE = "explore"
SPIDER_IDS = {
    MODE_URL: "youtube_video-post_by-url",
    MODE_SEARCH_FILTERS: "youtube_video-post_by-search-filters",
    MODE_HASHTAG: "youtube_video-post_by-hashtag",
    MODE_PODCAST_URL: "youtube_video-post_by-podcast-url",
    MODE_KEYWORD: "youtube_video-post_by-keyword",
    MODE_EXPLORE: "youtube_video-post_by-explore",
}
DEFAULT_FILE_NAME = "{{TasksID}}"
DEFAULT_URL = "https://www.youtube.com/@stephcurry/videos"
DEFAULT_PODCAST_URL = "https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0"
DEFAULT_EXPLORE_URL = "https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D"
DEFAULT_ORDER_BY = "最新"
DEFAULT_START_INDEX = "1"
DEFAULT_NUM_OF_POSTS_URL = "5"
DEFAULT_KEYWORD_SEARCH = "popular music"
DEFAULT_FEATURES = "All"
DEFAULT_TYPE = "Videos"
DEFAULT_DURATION = "Under 3 minutes"
DEFAULT_UPLOAD_DATE = "Last hour"
DEFAULT_NUM_OF_POSTS_SEARCH = "200"
DEFAULT_HASHTAG = "shopping"
DEFAULT_KEYWORD = "top videos"
DEFAULT_NUM_OF_POSTS = "10"
DEFAULT_ALL_TABS = "true"
ORDER_BY_VALUES = {"最新", "热门", "最早"}
FEATURES_VALUES = {"All", "Live", "4K", "HD", "Subtitles/CC", "Creative Commons", "360°", "VR180", "3D", "HDR"}
TYPE_VALUES = {"Videos", "Movies"}
UPLOAD_DATE_VALUES = {"Last hour", "Today", "This week", "This month", "This year", "All"}
ALL_TABS_VALUES = {"true", "false"}
DURATION_MAP = {
    "Under 3 minutes": "4 分钟以内",
    "4 分钟以内": "4 分钟以内",
    "4-20 minutes": "4-20 分钟",
    "4-20 分钟": "4-20 分钟",
    "Over 20 minutes": "20 分钟以上",
    "20 分钟以上": "20 分钟以上",
    "All": "None",
    "全部": "None",
    "None": "None",
}


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_youtube_video_post.py --mode keyword --keyword \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_KEYWORD,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower().replace("-", "_")
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url, search_filters, hashtag, podcast_url, keyword, or explore.".format(value))
    return clean


def validate_youtube_url(value):
    clean = str(value).strip()
    parsed = urllib.parse.urlparse(clean)
    if parsed.scheme != "https" or parsed.netloc != "www.youtube.com":
        raise ValueError("URL must use https://www.youtube.com: {}".format(clean))
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


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_choice(value, allowed, field_name):
    clean = str(value).strip()
    if clean not in allowed:
        raise ValueError("Unsupported {}: {}. Use an allowed dropdown value from the skill parameter table.".format(field_name, clean))
    return clean


def normalize_duration(value):
    clean = str(value).strip()
    if clean not in DURATION_MAP:
        raise ValueError("Unsupported duration: {}. Use an allowed dropdown value from the skill parameter table.".format(clean))
    return DURATION_MAP[clean]


def normalize_all_tabs(value):
    clean = str(value).strip().lower()
    if clean not in ALL_TABS_VALUES:
        raise ValueError("Unsupported all_tabs: {}. Use true or false.".format(value))
    return clean


def normalize_hashtag(value):
    clean = str(value).strip()
    if clean.startswith("#"):
        clean = clean[1:].strip()
    if not clean:
        raise ValueError("hashtag cannot be empty")
    return clean


def normalize_file_name(value):
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_group(group, mode):
    if mode == MODE_URL:
        return {
            "url": validate_youtube_url(group.get("url", DEFAULT_URL)),
            "order_by": normalize_choice(group.get("order_by", DEFAULT_ORDER_BY), ORDER_BY_VALUES, "order_by"),
            "start_index": validate_non_negative_integer(group.get("start_index", DEFAULT_START_INDEX), "start_index"),
            "num_of_posts": validate_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS_URL), "num_of_posts"),
        }
    if mode == MODE_SEARCH_FILTERS:
        return {
            "keyword_search": normalize_text(group.get("keyword_search", DEFAULT_KEYWORD_SEARCH), "keyword_search"),
            "features": normalize_choice(group.get("features", DEFAULT_FEATURES), FEATURES_VALUES, "features"),
            "type": normalize_choice(group.get("type", DEFAULT_TYPE), TYPE_VALUES, "type"),
            "duration": normalize_duration(group.get("duration", DEFAULT_DURATION)),
            "upload_date": normalize_choice(group.get("upload_date", DEFAULT_UPLOAD_DATE), UPLOAD_DATE_VALUES, "upload_date"),
            "num_of_posts": validate_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS_SEARCH), "num_of_posts"),
        }
    if mode == MODE_HASHTAG:
        return {
            "hashtag": normalize_hashtag(group.get("hashtag", DEFAULT_HASHTAG)),
            "num_of_posts": validate_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
        }
    if mode == MODE_PODCAST_URL:
        return {
            "url": validate_youtube_url(group.get("url", DEFAULT_PODCAST_URL)),
            "num_of_posts": validate_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
        }
    if mode == MODE_KEYWORD:
        return {
            "keyword": normalize_text(group.get("keyword", DEFAULT_KEYWORD), "keyword"),
            "num_of_posts": validate_non_negative_integer(group.get("num_of_posts", DEFAULT_NUM_OF_POSTS), "num_of_posts"),
        }
    return {
        "url": validate_youtube_url(group.get("url", DEFAULT_EXPLORE_URL)),
        "all_tabs": normalize_all_tabs(group.get("all_tabs", DEFAULT_ALL_TABS)),
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


def build_default_group(args, mode):
    if mode == MODE_URL:
        return {
            "url": args.url or DEFAULT_URL,
            "order_by": args.order_by,
            "start_index": args.start_index,
            "num_of_posts": args.num_of_posts if args.num_of_posts is not None else DEFAULT_NUM_OF_POSTS_URL,
        }
    if mode == MODE_SEARCH_FILTERS:
        return {
            "keyword_search": args.keyword_search,
            "features": args.features,
            "type": args.type,
            "duration": args.duration,
            "upload_date": args.upload_date,
            "num_of_posts": args.num_of_posts if args.num_of_posts is not None else DEFAULT_NUM_OF_POSTS_SEARCH,
        }
    if mode == MODE_HASHTAG:
        return {
            "hashtag": args.hashtag,
            "num_of_posts": args.num_of_posts if args.num_of_posts is not None else DEFAULT_NUM_OF_POSTS,
        }
    if mode == MODE_PODCAST_URL:
        return {
            "url": args.url or DEFAULT_PODCAST_URL,
            "num_of_posts": args.num_of_posts if args.num_of_posts is not None else DEFAULT_NUM_OF_POSTS,
        }
    if mode == MODE_KEYWORD:
        return {
            "keyword": args.keyword,
            "num_of_posts": args.num_of_posts if args.num_of_posts is not None else DEFAULT_NUM_OF_POSTS,
        }
    return {
        "url": args.url or DEFAULT_EXPLORE_URL,
        "all_tabs": args.all_tabs,
    }


def build_groups(args, mode):
    if args.params_json:
        return load_groups_from_json(args.params_json, mode)
    return [normalize_group(build_default_group(args, mode), mode)]


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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify YouTube Video Post Builder task.")
    parser.add_argument("--mode", required=True, help="Allowed values: url, search_filters, hashtag, podcast_url, keyword, explore.")
    parser.add_argument("--url", help="URL-based modes only.")
    parser.add_argument("--order-by", default=DEFAULT_ORDER_BY, help="URL mode only. Allowed values: 最新, 热门, 最早.")
    parser.add_argument("--start-index", default=DEFAULT_START_INDEX, help="URL mode only. Integer >= 0.")
    parser.add_argument("--keyword-search", default=DEFAULT_KEYWORD_SEARCH, help="Search filters mode only.")
    parser.add_argument("--features", default=DEFAULT_FEATURES, help="Search filters mode only.")
    parser.add_argument("--type", default=DEFAULT_TYPE, help="Search filters mode only.")
    parser.add_argument("--duration", default=DEFAULT_DURATION, help="Search filters mode only.")
    parser.add_argument("--upload-date", default=DEFAULT_UPLOAD_DATE, help="Search filters mode only.")
    parser.add_argument("--hashtag", default=DEFAULT_HASHTAG, help="Hashtag mode only.")
    parser.add_argument("--keyword", default=DEFAULT_KEYWORD, help="Keyword mode only.")
    parser.add_argument("--all-tabs", default=DEFAULT_ALL_TABS, help="Explore mode only. Allowed values: true, false.")
    parser.add_argument("--num-of-posts", help="Mode-specific post count. Integer >= 0.")
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
