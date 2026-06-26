# 本文件负责请求律动 BlockBeats Pro API，并把响应整理成统一内容结构。

import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import BASE_URL, ENDPOINTS


def _extract_items(data):
    """兼容列表、分页对象和嵌套列表等常见 API 响应形态。"""
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []
    for key in ("list", "items", "data", "result", "records"):
        value = data.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            nested = _extract_items(value)
            if nested:
                return nested
    return []


def _parse_published_at(raw_item, fallback_dt):
    """尽量使用 API 返回的绝对时间；缺失时使用采集时间兜底。"""
    candidates = [
        raw_item.get("published_at"),
        raw_item.get("publish_time"),
        raw_item.get("create_time"),
        raw_item.get("created_at"),
        raw_item.get("time"),
        raw_item.get("date"),
    ]
    for value in candidates:
        if not value:
            continue
        if isinstance(value, (int, float)):
            timestamp = value / 1000 if value > 100000000000 else value
            return datetime.fromtimestamp(timestamp, tz=fallback_dt.tzinfo).isoformat()
        if isinstance(value, str):
            text = value.strip()
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
                try:
                    parsed = datetime.strptime(text, fmt)
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=fallback_dt.tzinfo)
                    return parsed.isoformat()
                except ValueError:
                    pass
            try:
                return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(fallback_dt.tzinfo).isoformat()
            except ValueError:
                pass
    return fallback_dt.isoformat()


def _pick_url(raw_item):
    return raw_item.get("url") or raw_item.get("link") or raw_item.get("source_url") or ""


def normalize_item(raw_item, source_type, fetched_at):
    """只保留已确认内容字段，不引入未确认的互动类指标。"""
    return {
        "source": "blockbeats",
        "source_type": source_type,
        "title": raw_item.get("title") or raw_item.get("name") or "",
        "abstract": raw_item.get("abstract") or raw_item.get("summary") or raw_item.get("description") or "",
        "content": raw_item.get("content") or raw_item.get("body") or "",
        "url": _pick_url(raw_item),
        "published_at": _parse_published_at(raw_item, fetched_at),
        "raw_json": json.dumps(raw_item, ensure_ascii=False, sort_keys=True),
    }


class BlockBeatsClient:
    def __init__(self, api_key, lang="zh", timeout=20):
        self.api_key = api_key
        self.lang = lang
        self.timeout = timeout

    def request_json(self, endpoint, params=None):
        """统一封装 API 请求和错误处理。"""
        params = params or {}
        query = urlencode(params)
        url = BASE_URL + endpoint + (("?" + query) if query else "")
        request = Request(url, headers={"api-key": self.api_key})
        with urlopen(request, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("status") not in (0, "0", None):
            raise RuntimeError("BlockBeats API 请求失败：%s" % payload)
        return payload.get("data", payload)

    def fetch_category(self, category, now):
        endpoint = ENDPOINTS[category]
        params = {"lang": self.lang}
        if category.endswith("important"):
            params.update({"size": 50})
        data = self.request_json(endpoint, params=params)
        return [
            normalize_item(raw_item, category, now)
            for raw_item in _extract_items(data)
            if isinstance(raw_item, dict)
        ]

    def fetch_all(self, now):
        """采集普通 24h 内容和 important 内容。"""
        items = []
        for category in ("newsflash_24h", "article_24h", "newsflash_important", "article_important"):
            items.extend(self.fetch_category(category, now))
        return items
