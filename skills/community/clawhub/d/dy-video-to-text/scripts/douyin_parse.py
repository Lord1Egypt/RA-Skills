#!/usr/bin/env python3
"""
Parse a Douyin share link and return video metadata (ID, title, watermark-free URL).
No API key required.

Usage:
    python3 douyin_parse.py "<douyin_share_link_or_text>"

Output: JSON to stdout
    {"status":"success","video_id":"...","title":"...","download_url":"..."}
"""
# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called:
#     - https://v.douyin.com/* (share link redirect)
#     - https://www.iesdouyin.com/share/video/* (video page HTML)
#   Local files read: none
#   Local files written: none

import sys
import re
import json
import requests

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
    )
}


def parse_share_url(share_text: str) -> dict:
    urls = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        share_text,
    )
    if not urls:
        raise ValueError("No valid share link found in input")

    share_url = urls[0]
    share_response = requests.get(share_url, headers=HEADERS, timeout=15)
    video_id = share_response.url.split("?")[0].strip("/").split("/")[-1]
    page_url = f'https://www.iesdouyin.com/share/video/{video_id}'

    response = requests.get(page_url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    pattern = re.compile(
        r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
        flags=re.DOTALL,
    )
    match = pattern.search(response.text)
    if not match or not match.group(1):
        raise ValueError("Failed to parse video info from HTML")

    json_data = json.loads(match.group(1).strip())
    VIDEO_KEY = "video_(id)/page"
    NOTE_KEY = "note_(id)/page"

    if VIDEO_KEY in json_data["loaderData"]:
        video_info_res = json_data["loaderData"][VIDEO_KEY]["videoInfoRes"]
    elif NOTE_KEY in json_data["loaderData"]:
        video_info_res = json_data["loaderData"][NOTE_KEY]["videoInfoRes"]
    else:
        raise ValueError("Cannot find video or note data in page JSON")

    data = video_info_res["item_list"][0]
    video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
    desc = data.get("desc", "").strip() or f"douyin_{video_id}"
    desc = re.sub(r'[\\/:*?"<>|]', '_', desc)

    return {
        "video_id": video_id,
        "title": desc,
        "download_url": video_url,
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "Usage: douyin_parse.py <share_link>"}))
        sys.exit(1)

    share_text = sys.argv[1]
    try:
        info = parse_share_url(share_text)
        print(json.dumps({"status": "success", **info}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
