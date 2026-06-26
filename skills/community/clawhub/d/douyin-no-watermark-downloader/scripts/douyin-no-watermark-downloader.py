import sys
import requests
import time
import logging
import os
from datetime import datetime
import re

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

import re
def is_allowed_domain(url):
    allowed = r'^(https?://)?([^/]*\.)?(douyin\.com|bilibili\.com|iesdouyin\.com)'
    return re.match(allowed, url) is not None


def get_real_video_url(share_url, max_retry=3):
    api = "https://lvhomeproxy2.dpdns.org/api/hybrid/video_data"
    params = {"url": share_url, "minimal": False}
    delay = 1

    for i in range(max_retry):
        try:
            log.info(f"Requesting API attempt {i+1}/{max_retry}")
            res = requests.get(api, params=params, timeout=20)

            if res.status_code == 200:
                data = res.json()
                video = data.get("data", {}).get("video", {})
                bit = video.get("bit_rate", [])

                if bit:
                    urls = bit[0].get("play_addr", {}).get("url_list", [])
                else:
                    urls = video.get("download_addr", {}).get("url_list", [])

                return [str(u) for u in urls] if urls else []

            log.warning(f"Request failed with status {res.status_code}")

        except Exception as e:
            log.warning(f"Request exception: {e}")

        if i < max_retry - 1:
            time.sleep(delay)
            delay *= 2

    log.error("All API attempts failed")
    return []

def download_video(video_url, save_dir=None):
    if not save_dir:
        save_dir = os.path.join(os.path.expanduser("~"), "Desktop")

    os.makedirs(save_dir, exist_ok=True)
    filename = f"douyin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    path = os.path.join(save_dir, filename)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/"
    }

    try:
        resp = requests.get(video_url, headers=headers, stream=True, timeout=600)
        resp.raise_for_status()

        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return path

    except Exception as e:
        log.error(f"Download failed: {e}")
        raise

def extract_url(text):
    match = re.search(r"https://v\.douyin\.com/[^\s]+", text)
    if match:
        return match.group(0)
    raise ValueError("No valid Douyin URL found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Douyin No-Watermark Video Downloader")
        print("Usage: python script.py \"douyin_share_url_or_text\"")
        print("Example: python script.py \"https://v.douyin.com/XXXXXX/\"")
        sys.exit(1)

    try:
        url = extract_url(sys.argv[1])
        print(f"Extracted URL: {url}")

        if not is_allowed_domain(url):
            raise ValueError("不允许的域名")

        video_urls = get_real_video_url(url)
        if not video_urls:
            raise ValueError("解析失败：未获取到视频地址")

        print("Got no-watermark video URL successfully")
        print("Starting download...")

        save_path = download_video(video_urls[0])
        print(f"Download finished! Saved to: {save_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)