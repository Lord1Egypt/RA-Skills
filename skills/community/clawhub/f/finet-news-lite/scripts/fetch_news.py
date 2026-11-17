"""
finet_news_lite — 财华社财经新闻获取（最小版）

仅提供 fetch_news(limit, days)：实时拉取财华社最新财经新闻，
统一输出扁平的标准文章字段。内置超时与重试，不做本地缓存，不依赖第三方库。

接口: https://cps.finet.com.cn/cps_api/news/recent-list
"""
from __future__ import annotations

__version__ = "1.0.1"

import argparse
import json
import os
import re
import sys
sys.dont_write_bytecode = True
import time
import urllib.parse
import urllib.request

API_HOST = os.environ.get("FINET_API_HOST", "https://cps.finet.com.cn").rstrip("/")
API_URL = f"{API_HOST}/cps_api/news/recent-list"

DEFAULT_TIMEOUT = 8
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 1.5
DEFAULT_COVER_IMAGE = (
    "https://ffpro-fs.finet.com.cn/app_data/upload/finet_news_cover.jpg"
)

_BAD_HOST_RE = re.compile(r"(https?:)?//images\.finet\.hk/", flags=re.IGNORECASE)
_BARE_HOST_RE = re.compile(r"(?<![/:\\w.-])images\.finet\.hk/", flags=re.IGNORECASE)
_GOOD_PREFIX = "https://fs.finet.com.cn/"
_IMG_SRC_RE = re.compile(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", flags=re.I | re.S)

NEWS_URL_TPL = "https://www.finet.com.cn/news/{id}.html"


def rewrite_hosts(s):
    """把不可达图片 host images.finet.hk 替换为可直连的 fs.finet.com.cn。"""
    if not s:
        return s or ""
    out = _BAD_HOST_RE.sub(_GOOD_PREFIX, s)
    return _BARE_HOST_RE.sub(_GOOD_PREFIX, out)


def normalize_publish_time(s):
    """publish_time 形如 'YYYY-MM-DDTHH:MM:SS'（北京时区），补 +08:00。"""
    if not s:
        return ""
    if s.endswith("Z") or re.search(r"[+-]\d{2}:?\d{2}$", s):
        return s
    return f"{s}+08:00"


def split_keywords(s):
    if not s:
        return []
    return [p.strip() for p in re.split(r"[,，]", s) if p.strip()]


def extract_img_urls(content):
    """从已替换域名的正文提取 <img src>，保序去重。"""
    urls, seen = [], set()
    for m in _IMG_SRC_RE.finditer(content):
        url = m.group(1).strip()
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def to_article(raw):
    """把接口一条原始记录映射为统一的标准文章字段。"""
    nid = raw.get("_id") or ""
    content = rewrite_hosts(raw.get("content_sc") or "")
    return {
        "source_id":         nid,
        "title":             raw.get("title_sc") or "",
        "content":           content,
        "summary":           (raw.get("summary_sc") or "").strip(),
        "cover_image":       rewrite_hosts(raw.get("title_img") or "").strip()
                             or DEFAULT_COVER_IMAGE,
        "content_img_urls":  extract_img_urls(content),
        "keywords":          split_keywords(raw.get("keyword_sc")),
        "creator":           raw.get("author_sc") or "",
        "publish_time":      normalize_publish_time(raw.get("publish_time")),
        "category":          list(raw.get("category_sc") or []),
        "news_url":          NEWS_URL_TPL.format(id=nid) if nid else "",
    }


def _http_get_json(url, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def _http_get_with_retries(url, timeout, retries, backoff):
    attempts = max(1, int(retries))
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            return _http_get_json(url, timeout=timeout)
        except Exception as exc:
            last_exc = exc
            if attempt >= attempts:
                break
            time.sleep(max(0.0, float(backoff)) ** (attempt - 1))
    raise last_exc


def fetch_news(
    limit=None,
    days=None,
    timeout=DEFAULT_TIMEOUT,
    retries=DEFAULT_RETRIES,
    retry_backoff=DEFAULT_RETRY_BACKOFF,
):
    """实时获取财华社财经新闻，统一输出标准文章字段。

    - limit: 返回条数，None=接口返回的全部
    - days: 查询最近 N 天，None=不带该参数（接口默认）
    - timeout: 单次请求超时秒数
    - retries: 失败重试次数
    - retry_backoff: 重试退避底数（指数退避）
    """
    params = {}
    if days is not None:
        params["days"] = int(days)
    url = API_URL + (("?" + urllib.parse.urlencode(params)) if params else "")

    payload = _http_get_with_retries(url, timeout, retries, retry_backoff)
    if payload.get("code") != 200:
        raise RuntimeError(
            f"finet API 非 200: code={payload.get('code')} msg={payload.get('message')}"
        )
    items = [to_article(r) for r in (payload.get("data") or [])]
    if limit and limit > 0:
        items = items[:limit]
    return items


def main(argv=None):
    parser = argparse.ArgumentParser(description="获取财华社最新财经新闻")
    parser.add_argument("--limit", type=int, default=None, help="返回条数")
    parser.add_argument("--days", type=int, default=None, help="查询最近 N 天")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args(argv)
    print(json.dumps(fetch_news(limit=args.limit, days=args.days, timeout=args.timeout),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
