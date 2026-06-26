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
MODE_USERNAME = "username"
MODE_PROFILEURL = "profileurl"
SPIDER_IDS = {
    MODE_USERNAME: "ins_profiles_by-username",
    MODE_PROFILEURL: "ins_profiles_by-profileurl",
}
DEFAULT_USERNAME = "zoobarcelona"
DEFAULT_PROFILEURL = "https://www.instagram.com/cats_of_world_/"
DEFAULT_FILE_NAME = "{{TasksID}}"


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_instagram_profiles.py --mode username --username \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_USERNAME,
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use username or profileurl.".format(value))
    return clean


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_profileurl(value):
    clean = normalize_text(value, "profileurl")
    if not clean.startswith("https://www.instagram.com/"):
        raise ValueError("profileurl must start with https://www.instagram.com/")
    return clean


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_username_group(group):
    return {
        "username": normalize_text(group.get("username", DEFAULT_USERNAME), "username"),
    }


def normalize_profileurl_group(group):
    return {
        "profileurl": normalize_profileurl(group.get("profileurl", DEFAULT_PROFILEURL)),
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
        if mode == MODE_USERNAME:
            groups.append(normalize_username_group(item))
        else:
            groups.append(normalize_profileurl_group(item))
    return groups


def build_groups(args, mode):
    if args.params_json:
        return load_groups_from_json(args.params_json, mode)
    if mode == MODE_USERNAME:
        usernames = args.username or [DEFAULT_USERNAME]
        return [normalize_username_group({"username": username}) for username in usernames]
    profileurls = args.profileurl or [DEFAULT_PROFILEURL]
    return [normalize_profileurl_group({"profileurl": profileurl}) for profileurl in profileurls]


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

    parser = argparse.ArgumentParser(description="Submit a guided Dataify Instagram Profiles Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: username, profileurl.")
    parser.add_argument("--username", action="append", help="Username mode only. Instagram username. Repeat for multiple usernames.")
    parser.add_argument("--profileurl", action="append", help="Profile URL mode only. Instagram profile URL. Repeat for multiple URLs.")
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
