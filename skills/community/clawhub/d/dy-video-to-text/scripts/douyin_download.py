#!/usr/bin/env python3
"""
Download a watermark-free Douyin video to a local file.
No API key required.

Usage:
    python3 douyin_download.py "<douyin_share_link>" [output_dir]

Output: JSON to stdout
    {"status":"success","video_id":"...","title":"...","file_path":"...","size_bytes":...}
"""
# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called:
#     - https://v.douyin.com/* (share link redirect)
#     - https://www.iesdouyin.com/share/video/* (video page HTML)
#     - Douyin CDN (video download)
#   Local files read: none
#   Local files written: downloaded .mp4 video file in output_dir

import sys
import os
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


def download_video(video_url: str, filename: str, output_dir: str) -> tuple:
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    resp = requests.get(video_url, headers=HEADERS, stream=True, timeout=60)
    resp.raise_for_status()

    total = int(resp.headers.get('content-length', 0))
    downloaded = 0
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)

    return filepath, downloaded


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "Usage: douyin_download.py <share_link> [output_dir]"}))
        sys.exit(1)

    share_text = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    try:
        info = parse_share_url(share_text)
        safe_title = re.sub(r'[^\w\-.]', '_', info["title"])[:80]
        filename = f"{safe_title}_{info['video_id']}.mp4"
        filepath, size = download_video(info["download_url"], filename, output_dir)

        print(json.dumps({
            "status": "success",
            "video_id": info["video_id"],
            "title": info["title"],
            "file_path": os.path.abspath(filepath),
            "size_bytes": size,
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
