from __future__ import annotations

import requests

CLS_TELEGRAPH_URL = "https://www.cls.cn/nodeapi/telegraphList"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cls.cn/telegraph",
}


def fetch_telegraph_list(timeout: int = 20) -> list[dict]:
    response = requests.get(CLS_TELEGRAPH_URL, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", {}).get("roll_data", [])
