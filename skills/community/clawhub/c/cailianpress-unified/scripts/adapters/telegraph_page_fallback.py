from __future__ import annotations

import json
import re

import requests

CLS_TELEGRAPH_PAGE_URL = "https://www.cls.cn/telegraph"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cls.cn/telegraph",
}


def fetch_telegraph_page_data(timeout: int = 20) -> list[dict]:
    response = requests.get(CLS_TELEGRAPH_PAGE_URL, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    html = response.text

    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if not match:
        return []

    payload = json.loads(match.group(1))
    telegraph_list = _find_telegraph_list(payload)
    return telegraph_list if isinstance(telegraph_list, list) else []


def _find_telegraph_list(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"roll_data", "telegraphList", "telegraph_list"} and isinstance(value, list):
                return value
            found = _find_telegraph_list(value)
            if found:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find_telegraph_list(item)
            if found:
                return found
    return None
