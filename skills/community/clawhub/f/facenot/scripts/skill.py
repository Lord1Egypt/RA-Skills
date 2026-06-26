#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""facebook_post_reader - script đơn file để lấy nội dung "bài viết đầu tiên" của 1 trang.

Cách chạy:
python3 scripts/skill.py --url "https://example.com"

Output:
JSON printed ra stdout:
{
  "status": "success",
  "content": "..."
}
"""

import argparse
import json
import sys
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except Exception as e:
    print(json.dumps({"status":"error", "content": f"Missing dependency: {e}"}))
    sys.exit(1)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
}

def extract_text_from_soup(soup):
    # Tiền xử lý: tìm thẻ article -> div[role='article'] -> first <article> or first <p> or meta og:description
    selectors = [
        ("article", lambda el: el.get_text(separator="\n", strip=True)),
        ("div[role='article']", lambda el: el.get_text(separator="\n", strip=True)),
        ("div._5pcr", lambda el: el.get_text(separator="\n", strip=True)),  # facebook old class fallback
        ("p", lambda el: el.get_text(separator="\n", strip=True))
    ]
    for sel, fn in selectors:
        el = soup.select_one(sel)
        if el:
            text = fn(el).strip()
            if text:
                return text

    # fallback meta og:description
    meta = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name":"description"})
    if meta and meta.get("content"):
        return meta.get("content").strip()

    return None

def run(url):
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url

        r = requests.get(url, headers=DEFAULT_HEADERS, timeout=12)
        if r.status_code >= 400:
            return {"status":"error", "content": f"HTTP {r.status_code} returned for {url}"}

        soup = BeautifulSoup(r.text, "html.parser")
        text = extract_text_from_soup(soup)
        if text:
            return {"status":"success", "content": text}
        else:
            return {"status":"error", "content": "Không tìm thấy nội dung rõ ràng. Trang có thể dùng JavaScript hoặc yêu cầu đăng nhập."}

    except Exception as e:
        return {"status":"error", "content": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Facebook Post Reader - simple web reader")
    parser.add_argument("--url", required=True, help="URL trang cần đọc")
    args = parser.parse_args()

    result = run(args.url)
    # print JSON to stdout
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
