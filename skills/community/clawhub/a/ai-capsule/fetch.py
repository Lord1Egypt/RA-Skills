#!/usr/bin/env python3
"""
AI 胶囊抓取脚本
抓取所有数据源 → 去重 → 输出 data/pending.json
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from concurrent.futures import ThreadPoolExecutor, as_completed

import feedparser
import requests
import trafilatura
import yaml
from bs4 import BeautifulSoup
from scrapling.fetchers import Fetcher as ScraplingFetcher

SKILL_DIR = Path(__file__).parent
SOURCES_DIR = SKILL_DIR / "sources"

def _resolve_data_dir() -> Path:
    config_path = Path(os.environ.get("AI_CAPSULE_CONFIG", str(Path.home() / ".ai-capsule" / "config.yaml")))
    if config_path.exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        raw = cfg.get("data_dir", "")
        if raw:
            p = Path(raw.replace("~", str(Path.home()))).expanduser()
            p.mkdir(parents=True, exist_ok=True)
            return p
    fallback = Path.home() / ".ai-capsule" / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback

DATA_DIR = _resolve_data_dir()
DEDUP_FILE = DATA_DIR / "dedup-titles.txt"
PENDING_FILE = DATA_DIR / "pending.json"

CUTOFF_DAYS = 3  # 只收录过去 N 天内发布的内容

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def load_dedup() -> set:
    if not DEDUP_FILE.exists():
        return set()
    return set(line.strip() for line in DEDUP_FILE.read_text().splitlines() if line.strip())


def is_duplicate(title: str, dedup: set) -> bool:
    return title.strip() in dedup


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  [WARN] fetch failed: {url} — {e}", file=sys.stderr)
        return None


def parse_rss(url: str) -> list[dict]:
    """解析 RSS，返回 [{title, url, summary, published_at}]，已按时效过滤"""
    cutoff = datetime.utcnow() - timedelta(days=CUTOFF_DAYS)
    try:
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries[:20]:
            # 尝试解析发布时间
            pub = None
            if hasattr(e, "published_parsed") and e.published_parsed:
                try:
                    pub = datetime(*e.published_parsed[:6])
                except Exception:
                    pass
            if hasattr(e, "updated_parsed") and e.updated_parsed and pub is None:
                try:
                    pub = datetime(*e.updated_parsed[:6])
                except Exception:
                    pass

            # 有时间则过滤，无时间则放行（宁可多收不漏）
            if pub is not None and pub < cutoff:
                continue

            items.append({
                "title": e.get("title", "").strip(),
                "url": e.get("link", ""),
                "summary": e.get("summary", e.get("description", ""))[:300],
                "content": "",
                "published_at": pub.isoformat() if pub else None,
            })
        return items
    except Exception as e:
        print(f"  [WARN] RSS parse failed: {url} — {e}", file=sys.stderr)
        return []


def soup_text(html: str, selector: str = None) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if selector:
        el = soup.select_one(selector)
        return el.get_text(" ", strip=True)[:400] if el else ""
    return soup.get_text(" ", strip=True)[:400]


# ── 各数据源抓取函数 ──────────────────────────────────────────────────────────

def fetch_huggingface() -> list[dict]:
    print("  HuggingFace Papers API...")
    cutoff = datetime.utcnow() - timedelta(days=CUTOFF_DAYS)
    data = fetch_url("https://huggingface.co/api/papers?limit=50")
    if not data:
        # 降级 WebFetch（无时间信息，放行）
        html = fetch_url("https://huggingface.co/papers")
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        items = []
        for a in soup.select("h3 a, h2 a")[:20]:
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if title and href:
                items.append({
                    "title": title,
                    "url": f"https://huggingface.co{href}" if href.startswith("/") else href,
                    "summary": "",
                    "source": "HuggingFace 论文",
                })
        return items

    papers = json.loads(data)
    items = []
    skipped = 0
    for p in papers:
        title = p.get("title", "").strip()
        if not title:
            continue
        # 过滤发布时间
        pub_str = p.get("publishedAt") or p.get("published_at") or ""
        if pub_str:
            try:
                pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00")).replace(tzinfo=None)
                if pub < cutoff:
                    skipped += 1
                    continue
            except Exception:
                pass
        pid = p.get("id", "")
        abstract = (p.get("summary") or p.get("abstract") or p.get("ai_summary") or "")[:1000]
        url = f"https://arxiv.org/abs/{pid}" if pid else ""
        items.append({
            "title": title,
            "url": url,
            "summary": abstract[:300],
            "content": abstract,
            "source": "HuggingFace 论文",
            "published_at": pub_str,
        })
    if skipped:
        print(f"    → 过滤掉 {skipped} 篇 {CUTOFF_DAYS} 天前的旧论文")
    return items


def fetch_rss_source(url: str, source_name: str, limit: int = 5) -> list[dict]:
    print(f"  {source_name} RSS...")
    items = parse_rss(url)
    for item in items:
        item["source"] = source_name
    return items[:limit]


def fetch_webpage_articles(url: str, source_name: str, limit: int = 5) -> list[dict]:
    """抓取博客首页，提取文章列表"""
    print(f"  {source_name} WebFetch...")
    html = fetch_url(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")

    items = []
    seen = set()
    # 通用策略：找 <a> 标签里包含文章标题的链接
    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        href = a["href"]
        # 过滤：标题长度合理、不是导航链接
        if len(title) < 15 or len(title) > 200:
            continue
        if any(skip in href for skip in ["#", "mailto:", "twitter", "github.com/", "javascript"]):
            continue
        if title in seen:
            continue
        seen.add(title)

        if href.startswith("/"):
            base = "/".join(url.rstrip("/").split("/")[:3])
            href = base + href
        elif not href.startswith("http"):
            continue

        items.append({
            "title": title,
            "url": href,
            "summary": "",
            "source": source_name,
        })
        if len(items) >= limit:
            break

    return items


def enrich_items_with_content(items: list[dict], max_workers: int = 6) -> list[dict]:
    """
    对 content 字段为空的条目并发抓取文章正文。
    已有 content（如 HuggingFace abstract）的条目直接跳过。
    失败时保留原条目（content 保持空字符串，由 Claude WebFetch 兜底）。
    """
    to_enrich = [i for i in items if not i.get("content", "").strip() and i.get("url")]
    if not to_enrich:
        return items

    print(f"  正文抓取: {len(to_enrich)} 篇...")

    def fetch_article(item: dict) -> dict:
        try:
            resp = _scrapling_fetcher.get(item["url"], timeout=12)
            html = resp.html_content or ""
            if html and len(html) > 500:
                text = trafilatura.extract(html) or ""
                if text:
                    item["content"] = text[:1000]
        except Exception:
            pass
        return item

    enriched_map = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(fetch_article, i): i["url"] for i in to_enrich}
        for fut in as_completed(futures):
            result = fut.result()
            enriched_map[result["url"]] = result

    return [enriched_map.get(i["url"], i) if not i.get("content", "").strip() else i for i in items]


def fetch_hacker_news() -> list[dict]:
    print("  Hacker News RSS (100分+)...")
    items = parse_rss("https://hnrss.org/newest?q=AI&points=100")
    for item in items:
        item["source"] = "Hacker News"
    return items[:5]


# ── webfetch 来源抓取 ─────────────────────────────────────────────────────────

_scrapling_fetcher = ScraplingFetcher()


def _fetch_one_webfetch(source: dict) -> Optional[list[dict]]:
    """
    用 Scrapling HTTP-only + BeautifulSoup + trafilatura 抓取单个 webfetch 源。
    返回 item 列表（含 content 字段），失败返回 None（由调用方跳过）。
    sources/ai.yaml 里可设 link_pattern（正则）来过滤只保留文章链接。
    """
    name = source["name"]
    url = source["url"]
    limit = source.get("limit", 5)
    link_pattern = source.get("link_pattern")
    compiled_pattern = re.compile(link_pattern) if link_pattern else None

    print(f"  {name} (Python fetch)...")
    try:
        resp = _scrapling_fetcher.get(url, timeout=12)
        html = resp.html_content or ""
    except Exception as e:
        print(f"  [WARN] {name}: Scrapling 失败 — {e}", file=sys.stderr)
        return None

    if not html or len(html) < 500:
        print(f"  [WARN] {name}: HTML 太短 ({len(html)} 字符)，跳过", file=sys.stderr)
        return None

    # 用 trafilatura 提取正文作为 content
    content_raw = trafilatura.extract(html) or ""
    content = content_raw[:1000]

    # 用 BeautifulSoup 提取文章链接列表（title + url）
    soup = BeautifulSoup(html, "html.parser")
    base = "/".join(url.rstrip("/").split("/")[:3])
    items = []
    seen = set()
    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        href = a["href"]
        if len(title) < 15 or len(title) > 200:
            continue
        if any(skip in href for skip in ["#", "mailto:", "twitter", "javascript"]):
            continue
        # 过滤纯时间/日期格式的标题（如 "5:30 PM – 6:23 PM" 或 "21st Jun 2026, 11:30 pm"）
        if re.search(r'^\d{1,2}:\d{2}\s*(AM|PM)', title, re.IGNORECASE):
            continue
        if re.search(r'^\d{1,2}(?:st|nd|rd|th)\s+[A-Z][a-z]+\s+\d{4}', title):
            continue
        if title in seen:
            continue
        if href.startswith("/"):
            href = base + href
        elif not href.startswith("http"):
            continue
        # 有 link_pattern 时只保留匹配的链接
        if compiled_pattern and not compiled_pattern.search(href):
            continue
        # title 太短时从 URL 路径末段提取备用标题
        if len(title) < 15:
            slug = href.rstrip("/").split("/")[-1]
            title = slug.replace("-", " ").replace("_", " ").strip()
            if len(title) < 5:
                continue
        seen.add(title)
        items.append({
            "title": title,
            "url": href,
            "summary": "",
            "content": content,
            "source": name,
        })
        if len(items) >= limit:
            break

    if not items:
        print(f"  [WARN] {name}: 未提取到任何文章链接", file=sys.stderr)
        return None

    print(f"  → {name}: {len(items)} 条，content {len(content)} 字符")
    return items


def load_webfetch_sources(industry: str = "ai") -> list[dict]:
    """从 sources/{industry}.yaml 加载 type=webfetch 且 python_fetch != false 的来源"""
    path = SOURCES_DIR / f"{industry}.yaml"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [
        s for s in (data.get("sources") or [])
        if s.get("type") == "webfetch" and s.get("python_fetch", True)
    ]


def fetch_webfetch_sources(sources: list[dict]) -> list[dict]:
    """并发抓取所有 webfetch 来源，返回合并的 item 列表。sources 为空返回 []。"""
    if not sources:
        return []
    all_items: list[dict] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(_fetch_one_webfetch, s): s["name"] for s in sources}
        for fut in as_completed(futures):
            result = fut.result()
            if result:
                all_items.extend(result)
    return all_items


# ── Twitter/X 来源抓取 ───────────────────────────────────────────────────────

def fetch_twitter_sources(twitter_sources: list[dict]) -> list[dict]:
    """
    用 browser_cookie3 提取本机 Chrome 中 x.com 的 Cookie，
    然后调 twitter-cli 获取指定账号的最新推文。

    Args:
        twitter_sources: load_twitter_sources() 返回的 type: twitter 配置列表。
                         每个配置需包含 accounts（账号列表）和 limit。

    Privacy: 仅读取 x.com 域名的 Cookie，仅在进程内存中传给 twitter-cli，
    不写入磁盘、不上传。如果 Cookie 缺失/过期，跳过并返回 []。
    """
    import subprocess
    import os

    if not twitter_sources:
        return []

    # 1. 提取 x.com Cookie
    try:
        import browser_cookie3
        cj = browser_cookie3.chrome(domain_name="x.com")
        cookies = {c.name: c.value for c in cj}
        auth_token = cookies.get("auth_token", "")
        ct0 = cookies.get("ct0", "")
        if not auth_token or not ct0:
            print("  [WARN] X/Twitter: x.com Cookie 缺失（未登录？），跳过", file=sys.stderr)
            return []
    except Exception as e:
        print(f"  [WARN] X/Twitter: browser_cookie3 读取失败 — {e}", file=sys.stderr)
        return []

    # 2. 找到 twitter-cli 的路径
    _twitter_bin = None
    for _p in [os.path.dirname(sys.executable), os.path.dirname(__file__) + "/.venv/bin"]:
        _candidate = os.path.join(_p, "twitter")
        if os.path.isfile(_candidate):
            _twitter_bin = _candidate
            break
    if not _twitter_bin:
        print("  [WARN] X/Twitter: twitter-cli 未找到。请运行: pip3 install twitter-cli", file=sys.stderr)
        return []

    # 3. 逐账号抓取
    env = os.environ.copy()
    env["TWITTER_AUTH_TOKEN"] = auth_token
    env["TWITTER_CT0"] = ct0

    # twitter-cli 底层 curl-cffi 不读系统代理设置，需显式传递
    # 优先用用户手动设的 https_proxy，没设则自动探测常见代理端口
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY") or ""
    if not proxy:
        # 自动探测常见本地代理端口（ClashX 7890, Surge 6152, ShadowsocksX 1080/1087）
        import socket
        for port in ["7890", "6152", "1080", "1087"]:
            try:
                s = socket.create_connection(("127.0.0.1", int(port)), timeout=0.3)
                s.close()
                proxy = f"http://127.0.0.1:{port}"
                print(f"  [INFO] 检测到本地代理: {proxy}", file=sys.stderr)
                break
            except (OSError, ValueError):
                continue
    if proxy:
        env["https_proxy"] = proxy
        env["HTTPS_PROXY"] = proxy

    all_items = []
    for src in twitter_sources:
        accounts = src.get("accounts", [])
        limit = src.get("limit", 5)
        for handle in accounts:
            print(f"  X/Twitter @{handle}...")
            try:
                # 多拉一些确保时间过滤后还能拿到目标条数
                result = subprocess.run(
                    [_twitter_bin, "user-posts", f"@{handle}", "--max", "20"],
                    capture_output=True, text=True, timeout=20, env=env
                )
                if result.returncode != 0:
                    stderr = result.stderr.strip()[:120]
                    print(f"    [WARN] @{handle}: twitter-cli 返回 {result.returncode} — {stderr}", file=sys.stderr)
                    continue
                yaml_text = result.stdout.strip()
                if not yaml_text:
                    print(f"    [WARN] @{handle}: 无输出", file=sys.stderr)
                    continue

                # twitter-cli 输出为 yaml 格式，data 字段是真正的推文列表
                try:
                    parsed = yaml.safe_load(yaml_text)
                    tweets = parsed.get("data", []) if isinstance(parsed, dict) else []
                except Exception as e:
                    print(f"    [WARN] @{handle}: yaml 解析失败 — {e}", file=sys.stderr)
                    continue
                cutoff = datetime.utcnow() - timedelta(days=CUTOFF_DAYS)
                for t in tweets:
                    text = (t.get("text") or "").strip()
                    if len(text) < 5:
                        continue
                    # 时间过滤：createdAt 格式如 "Fri Jun 12 17:45:54 +0000 2026"
                    created = t.get("createdAt", "")
                    if created:
                        try:
                            pub = datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=None)
                            if pub < cutoff:
                                continue
                        except (ValueError, TypeError):
                            pass  # 解析失败则放行
                    tweet_id = t.get("id", "")
                    # media 字段：图片/视频链接
                    media_urls = []
                    for m in t.get("media") or []:
                        if m.get("url"):
                            media_urls.append({
                                "type": m.get("type", "photo"),
                                "url": m["url"],
                            })
                    all_items.append({
                        "title": text[:120],
                        "url": f"https://x.com/{handle}/status/{tweet_id}" if tweet_id else f"https://x.com/{handle}/status/",
                        "author": f"@{handle}",
                        "summary": text[:300],
                        "content": text,
                        "source": "X/Twitter",
                        "media": media_urls if media_urls else None,
                    })
            except subprocess.TimeoutExpired:
                print(f"    [WARN] @{handle}: 超时", file=sys.stderr)
            except Exception as e:
                print(f"    [WARN] @{handle}: 未知错误 — {e}", file=sys.stderr)
    print(f"  → X/Twitter: 合计 {len(all_items)} 条")
    return all_items


def load_twitter_sources(industry: str = "ai") -> list[dict]:
    """从 sources/{industry}.yaml 加载 type=twitter 的来源"""
    path = SOURCES_DIR / f"{industry}.yaml"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [
        s for s in (data.get("sources") or [])
        if s.get("type") == "twitter"
    ]


# ── 主流程 ────────────────────────────────────────────────────────────────────

def load_rss_sources(industry: str = "ai") -> list[tuple[str, callable]]:
    """从 sources/{industry}.yaml 加载 type=rss 的来源，返回 (name, fn) 列表"""
    path = SOURCES_DIR / f"{industry}.yaml"
    if not path.exists():
        print(f"  [WARN] 找不到 {path}，使用内置默认来源", file=sys.stderr)
        return _default_sources()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    sources = []
    for s in (data.get("sources") or []):
        if s.get("type") != "rss":
            continue
        name = s["name"]
        handler = s.get("handler")
        url = s.get("url", "")
        limit = s.get("limit", 5)
        if handler == "huggingface":
            sources.append((name, fetch_huggingface))
        elif handler == "hacker_news":
            sources.append((name, fetch_hacker_news))
        else:
            sources.append((name, lambda u=url, n=name, lim=limit: fetch_rss_source(u, n, limit=lim)))
    return sources


def _default_sources() -> list[tuple[str, callable]]:
    """内置兜底来源，当 yaml 文件不存在时使用"""
    return [
        ("HuggingFace 论文",   fetch_huggingface),
        ("OpenAI 官方",        lambda: fetch_rss_source("https://openai.com/news/rss.xml", "OpenAI 官方")),
        ("Microsoft Research", lambda: fetch_rss_source("https://www.microsoft.com/en-us/research/feed/", "Microsoft Research")),
        ("Ben's Bites",        lambda: fetch_rss_source("https://www.bensbites.com/feed", "Ben's Bites", limit=2)),
        ("Hacker News",        fetch_hacker_news),
    ]


def main(industry: str = "ai"):
    DATA_DIR.mkdir(exist_ok=True)
    dedup = load_dedup()
    print(f"已处理标题: {len(dedup)} 条")
    print(f"数据源行业: {industry}")

    all_items = []
    failed = []

    # ── RSS 来源（串行）
    for name, fn in load_rss_sources(industry):
        try:
            items = fn()
            new_items = [i for i in items if i.get("title") and not is_duplicate(i["title"], dedup)]
            print(f"  → {name}: 抓到 {len(items)} 条，新增 {len(new_items)} 条")
            all_items.extend(new_items)
        except Exception as e:
            failed.append(name)
            print(f"  [ERROR] {name}: {e}", file=sys.stderr)
        time.sleep(0.3)

    # ── RSS 条目正文补充（对 content 为空的条目抓取文章正文）
    all_items = enrich_items_with_content(all_items)

    # ── webfetch 来源（并发，python_fetch: false 的源跳过）
    webfetch_sources = load_webfetch_sources(industry)
    if webfetch_sources:
        print(f"\n抓取 {len(webfetch_sources)} 个 webfetch 来源（并发）...")
        wf_items = fetch_webfetch_sources(webfetch_sources)
        new_wf = [i for i in wf_items if i.get("title") and not is_duplicate(i["title"], dedup)]
        print(f"  → webfetch 合计: {len(wf_items)} 条，新增 {len(new_wf)} 条")
        all_items.extend(new_wf)

    # ── Twitter/X 来源（需要本机 Chrome 登录 x.com）
    twitter_sources = load_twitter_sources(industry)
    if twitter_sources:
        print(f"\n抓取 {len(twitter_sources)} 个 X/Twitter 来源...")
        tw_items = fetch_twitter_sources(twitter_sources)
        new_tw = [i for i in tw_items if i.get("title") and not is_duplicate(i["title"], dedup)]
        print(f"  → X/Twitter 合计: {len(tw_items)} 条，新增 {len(new_tw)} 条")
        all_items.extend(new_tw)

    # 去掉标题重复（跨来源）
    seen_titles = set()
    unique_items = []
    for item in all_items:
        t = item["title"].strip()
        if t not in seen_titles:
            seen_titles.add(t)
            unique_items.append(item)

    print(f"\n待评分: {len(unique_items)} 条")
    if failed:
        print(f"失败来源: {', '.join(failed)}")

    PENDING_FILE.write_text(
        json.dumps(unique_items, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"已写入: {PENDING_FILE}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry", default="ai", help="行业名称（对应 sources/{industry}.yaml）")
    args = ap.parse_args()
    main(industry=args.industry)
