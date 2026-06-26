#!/usr/bin/env python3
"""
Extract speech-to-text from a Douyin video using Alibaba Cloud Bailian ASR.
Requires DASHSCOPE_API_KEY environment variable.

Usage:
    DASHSCOPE_API_KEY=sk-xxx python3 douyin_extract_text.py "<douyin_share_link>" [model]

    model defaults to "paraformer-v2"

Output: JSON to stdout
    {"status":"success","video_id":"...","title":"...","text":"..."}
"""
# SECURITY MANIFEST:
#   Environment variables accessed: DASHSCOPE_API_KEY (only)
#   External endpoints called:
#     - https://v.douyin.com/* (share link redirect)
#     - https://www.iesdouyin.com/share/video/* (video page HTML)
#     - https://dashscope.aliyuncs.com/api/* (Alibaba Cloud ASR)
#   Local files read: none
#   Local files written: none

import sys
import os
import re
import json
import requests
from http import HTTPStatus

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
    )
}

DEFAULT_MODEL = "paraformer-v2"


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


def extract_text(video_url: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    try:
        import dashscope
        import dashscope.audio.asr
    except ImportError:
        raise RuntimeError(
            "dashscope package not installed. "
            "Run: pip install dashscope requests"
        )

    dashscope.api_key = api_key

    task_response = dashscope.audio.asr.Transcription.async_call(
        model=model,
        file_urls=[video_url],
        language_hints=['zh', 'en'],
    )

    transcription_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id
    )

    if transcription_response.status_code != HTTPStatus.OK:
        msg = getattr(transcription_response.output, 'message', 'Unknown error')
        raise RuntimeError(f"Transcription failed: {msg}")

    for item in transcription_response.output['results']:
        resp = requests.get(item['transcription_url'], timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if 'transcripts' in result and len(result['transcripts']) > 0:
            return result['transcripts'][0]['text']

    return ""


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "error": "Usage: DASHSCOPE_API_KEY=sk-xxx douyin_extract_text.py <share_link> [model]"
        }))
        sys.exit(1)

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        print(json.dumps({
            "status": "error",
            "error": (
                "DASHSCOPE_API_KEY environment variable is not set. "
                "Get your key at https://help.aliyun.com/zh/model-studio/get-api-key"
            )
        }))
        sys.exit(1)

    share_text = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL

    try:
        info = parse_share_url(share_text)
        text = extract_text(info["download_url"], api_key, model)
        print(json.dumps({
            "status": "success",
            "video_id": info["video_id"],
            "title": info["title"],
            "text": text,
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
