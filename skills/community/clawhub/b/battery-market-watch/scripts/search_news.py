#!/usr/bin/env python3
"""
搜索五国电池行业相关新闻。
优化点：
1. 优先抓官方/行业 RSS，避免百度/Bing 结果漂移
2. 用 Google News RSS 做补充，稳定拿标题、链接、日期
3. 统一过滤、去重、按国家限额输出
"""

import asyncio
import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote, urlparse

import httpx
from curl_cffi import requests as curl_requests


BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"


def load_config() -> Dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()
BATTERY_KEYWORDS = [
    "电池", "battery", "储能", "energy storage", "动力电池", "锂电", "lithium",
    "ev battery", "bess", "accumulator", "배터리", "аккумулятор"
]


def clean_text(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_date(raw: str) -> str:
    if not raw:
        return ""
    raw = raw.strip()
    try:
        dt = parsedate_to_datetime(raw)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    for pattern in [r"(\d{4}-\d{2}-\d{2})", r"(\d{4}/\d{2}/\d{2})", r"(\d{4}年\d{1,2}月\d{1,2}日)"]:
        m = re.search(pattern, raw)
        if m:
            return m.group(1).replace('/', '-')
    return raw[:20]


def parse_date_obj(raw: str) -> Optional[datetime]:
    if not raw:
        return None
    raw = raw.strip()
    try:
        return parsedate_to_datetime(raw).replace(tzinfo=None)
    except Exception:
        pass
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日"]:
        try:
            return datetime.strptime(raw[:10] if fmt != "%Y年%m月%d日" else raw, fmt)
        except Exception:
            pass
    m = re.search(r"(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})", raw)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except Exception:
            return None
    return None


def is_valid_title(title: str, content: str = "") -> bool:
    title_lower = title.lower()
    text_lower = f"{title} {content}".lower()

    for pattern in CONFIG["filters"]["invalid_patterns"]:
        if pattern.lower() in title_lower:
            return False

    has_battery = any(kw.lower() in text_lower for kw in BATTERY_KEYWORDS)
    if not has_battery:
        return False

    valid_keywords = CONFIG["filters"]["valid_keywords"]
    has_valid_keyword = any(kw.lower() in text_lower for kw in valid_keywords)
    return has_valid_keyword or has_battery


def normalize_url(url: str) -> str:
    if url.startswith("//"):
        return "https:" + url
    return url.strip()


def host_matches(url: str, allowed_hosts: List[str]) -> bool:
    if not allowed_hosts:
        return True
    try:
        host = (urlparse(url).netloc or "").lower()
    except Exception:
        return False
    return any(host == h or host.endswith('.' + h) for h in allowed_hosts)


def country_terms_match(title: str, snippet: str, country_terms: List[str]) -> bool:
    if not country_terms:
        return True
    text = f"{title} {snippet}".lower()
    return any(term.lower() in text for term in country_terms)


def is_recent_enough(raw_date: str, max_age_days: int) -> bool:
    if not raw_date:
        return True
    dt = parse_date_obj(raw_date)
    if not dt:
        return True
    return (datetime.now() - dt).days <= max_age_days


def dedupe_results(items: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []
    for item in items:
        url = normalize_url(item.get("url", ""))
        title = item.get("title", "").strip()
        key = url or title.lower()
        if not key or key in seen:
            continue
        seen.add(key)
        item["url"] = url
        unique.append(item)
    return unique


def fetch_rss(feed_url: str) -> List[Dict]:
    try:
        resp = httpx.get(feed_url, timeout=20, follow_redirects=True)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        items = []
        for node in root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = clean_text(node.findtext("title") or node.findtext("{http://www.w3.org/2005/Atom}title") or "")
            link = node.findtext("link") or ""
            if not link:
                link_node = node.find("{http://www.w3.org/2005/Atom}link")
                if link_node is not None:
                    link = link_node.attrib.get("href", "")
            desc = clean_text(
                node.findtext("description")
                or node.findtext("summary")
                or node.findtext("{http://www.w3.org/2005/Atom}summary")
                or ""
            )
            pub = parse_date(
                node.findtext("pubDate")
                or node.findtext("published")
                or node.findtext("updated")
                or node.findtext("{http://www.w3.org/2005/Atom}published")
                or node.findtext("{http://www.w3.org/2005/Atom}updated")
                or ""
            )
            if title and link:
                items.append({"title": title, "url": normalize_url(link), "snippet": desc, "published_at": pub})
        return items
    except Exception as e:
        print(f"    RSS failed: {feed_url} | {e}")
        return []


def search_google_news_rss(query: str, country: str, lang: str, region: str, allowed_hosts: List[str], country_terms: List[str], max_age_days: int) -> List[Dict]:
    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}&hl={lang}&gl={region}&ceid={region}:{lang.split('-')[0]}"
    )
    results = fetch_rss(url)
    out = []
    for item in results:
        title = item["title"].replace(" - Google News", "").strip()
        snippet = item.get("snippet", "")
        if not is_valid_title(title, snippet):
            continue
        if not is_recent_enough(item.get("published_at", ""), max_age_days):
            continue
        if not host_matches(item["url"], allowed_hosts) and not country_terms_match(title, snippet, country_terms):
            continue
        out.append({
                "country": country,
                "title": title,
                "url": item["url"],
                "query": query,
                "source": "google-news-rss",
                "published_at": item.get("published_at", ""),
                "search_time": datetime.now().isoformat()
            })
    return out


def search_official_feeds(country: str, config: Dict) -> List[Dict]:
    results = []
    for feed in config.get("rss_feeds", []):
        print(f"    RSS: {feed['name']}")
        items = fetch_rss(feed["url"])
        for item in items[:20]:
            title = item["title"]
            snippet = item.get("snippet", "")
            if is_valid_title(title, snippet) and is_recent_enough(item.get("published_at", ""), config.get("max_age_days", 60)):
                results.append({
                    "country": country,
                    "title": title,
                    "url": item["url"],
                    "query": feed["name"],
                    "source": feed["name"],
                    "published_at": item.get("published_at", ""),
                    "search_time": datetime.now().isoformat()
                })
        time.sleep(0.4)
    return results


def fallback_web_search(query: str, country: str, engine: str) -> List[Dict]:
    results = []
    try:
        if engine == "baidu":
            resp = curl_requests.get(
                "https://www.baidu.com/s",
                params={"wd": query, "rn": 10},
                timeout=20,
                impersonate="chrome"
            )
            titles = re.findall(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', resp.text, re.DOTALL)
            links = re.findall(r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"', resp.text, re.DOTALL)
        else:
            resp = curl_requests.get(
                "https://www.bing.com/search",
                params={"q": query, "count": 10},
                timeout=20,
                impersonate="chrome"
            )
            matches = re.findall(r'<li class="b_algo.*?<h2><a href="([^"]+)"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
            links = [m[0] for m in matches]
            titles = [m[1] for m in matches]

        for title, url in zip(titles, links):
            title = clean_text(title)
            if title and url.startswith("http") and is_valid_title(title):
                results.append({
                    "country": country,
                    "title": title,
                    "url": normalize_url(url),
                    "query": query,
                    "source": engine,
                    "search_time": datetime.now().isoformat()
                })
    except Exception as e:
        print(f"    {engine} failed: {e}")
    return results


async def search_country_news(country: str, config: Dict) -> List[Dict]:
    all_results = []

    # 1. 先抓官方/行业 RSS
    rss_results = search_official_feeds(country, config)
    all_results.extend(rss_results)
    print(f"    RSS got {len(rss_results)}")

    # 2. 再用 Google News RSS 补足
    gn_lang = config.get("google_news", {}).get("lang", "en-US")
    gn_region = config.get("google_news", {}).get("region", "US")
    allowed_hosts = config.get("allowed_hosts", [])
    country_terms = config.get("country_terms", [])
    max_age_days = config.get("max_age_days", 60)
    for keyword in config.get("keywords", []):
        gnews_results = search_google_news_rss(keyword, country, gn_lang, gn_region, allowed_hosts, country_terms, max_age_days)
        all_results.extend(gnews_results)
        await asyncio.sleep(0.3)

    # 3. 如果还太少，再回退网页搜索
    if len(dedupe_results(all_results)) < config.get("min_results", 6):
        engine = config.get("search_engine", "bing")
        for keyword in config.get("keywords", [])[:3]:
            fallback_results = [
                r for r in fallback_web_search(keyword, country, engine)
                if host_matches(r.get("url", ""), allowed_hosts) or country_terms_match(r.get("title", ""), "", country_terms)
            ]
            all_results.extend(fallback_results)
            await asyncio.sleep(0.5)

    unique_results = dedupe_results(all_results)
    max_news = CONFIG["output"]["max_news_per_country"]
    return unique_results[:max_news]


async def main():
    print("[START] Searching battery market news from 5 countries...")
    all_news = []

    for country, country_config in CONFIG["countries"].items():
        print(f"  Searching {country}...")
        news = await search_country_news(country, country_config)
        all_news.extend(news)
        print(f"    Got {len(news)} valid results")

    all_news = dedupe_results(all_news)[:CONFIG["output"]["max_news_total"]]

    today = datetime.now().strftime("%Y%m%d")
    output_file = DATA_DIR / f"news_raw_{today}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Total: {len(all_news)} valid news")
    print(f"Output: {output_file}")
    return all_news


if __name__ == "__main__":
    asyncio.run(main())
