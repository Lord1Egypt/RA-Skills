#!/usr/bin/env python3
"""
fetch_ai_news.py  —  ai-weekly 的自治主数据源（v4.0）

通过 RSS Feed 抓取 AI 行业新闻，输出与 AI HOT API **兼容的归一化 JSON**，
可直接被 generate_site.py --api-json 消费。无需任何单一第三方商业 API。

输出 schema（与 AI HOT items 兼容）:
  {
    "count": <int>,
    "items": [
      {
        "title": "...",
        "summary": "...",
        "url": "https://...",
        "source": "源名称",
        "publishedAt": "2026-07-20T12:00:00",   # ISO 8601
        "category": "ai-models|ai-products|industry|paper|tip",
        "score": 0
      }, ...
    ]
  }

依赖（必需）:
  pip install feedparser requests beautifulsoup4

用法:
  # 抓取最近 7 天新闻 -> news.json（AI HOT 兼容 schema）
  python scripts/fetch_ai_news.py --output news.json

  # 抓取固定 ISO 周新闻（推荐：生成周报时务必指定，避免内容随运行日期漂移）
  python scripts/fetch_ai_news.py --week 2026-W30 --output news.json

  # 检查 RSS 源健康状态
  python scripts/fetch_ai_news.py --check-feeds

  # 用 News API 增强（需 NEWSAPI_KEY 环境变量）
  NEWSAPI_KEY=xxx python scripts/fetch_ai_news.py --output news.json

  # 跳过 Hugging Face 排行榜（默认会附带）
  python scripts/fetch_ai_news.py --no-hf --output news.json
"""

import argparse
import json
import os
import re
import socket
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from aiweekly.utils import save_json as _save_json

try:
    import feedparser
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ 缺少依赖(feedparser/requests/beautifulsoup4)。")
    print("  请用统一启动器运行：bash run_report.sh scripts/fetch_ai_news.py ...")
    print("  或手动：python -m pip install -r requirements.txt")
    sys.exit(1)


# ── RSS 源（已做健康检查的精选列表）─────────────────────────────
# 字段：(名称, URL, category_hint, region)
#   category_hint：关键词分类失败时的回退分类
#   region：cn=国内源 / global=国外源，用于分区域健康统计与降级判断
# 2026-09-10 实测（国内网络裸连，14 源逐个验证）：国外源 7/7 可达；
#   国内源中 36氪须带 www（不带 www 返回反爬 HTML 页，0 条）；
#   机器之心 RSS 已下线（返回「机器之心·数据服务」落地页），已替换为雷峰网 AI 科技评论。
RSS_FEEDS = [
    # 中文源（国内源：确保国内网络下也有足量覆盖，国外源全挂也有中文地板）
    ("量子位",        "https://www.qbitai.com/rss",                              "industry", "cn"),
    ("36氪 AI",       "https://www.36kr.com/feed",                              "industry", "cn"),
    ("雷峰网 AI 科技评论", "https://www.leiphone.com/feed",                     "ai-models", "cn"),
    ("智东西",        "https://www.zhidx.com/rss",                              "industry", "cn"),
    ("极客公园",      "https://www.geekpark.net/rss",                           "industry", "cn"),
    ("InfoQ 中国",    "https://www.infoq.cn/feed",                              "industry", "cn"),
    ("钛媒体",        "https://www.tmtpost.com/rss",                            "industry", "cn"),
    # 英文源
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", "industry", "global"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/",               "industry", "global"),
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml",               "ai-models", "global"),
    ("TechMeme",      "https://www.techmeme.com/feed.xml",                      "industry", "global"),
    ("MIT News AI",   "https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml", "paper", "global"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/",             "industry", "global"),
    ("Google AI Blog", "https://blog.google/technology/ai/rss/",                "industry", "global"),
]

# 国外源的国内镜像（主源失败时按顺序回退）。
# 注意：镜像必须验证「域名存在 + 返回预期内容」，仅 HTTP 200 不算——
# 曾有 aa-cn.mirror.xyz 返回无关博客页却 200，险些污染数据。
FEED_MIRRORS = {
    "Hugging Face Blog": ["https://hf-mirror.com/blog/feed.xml"],
}

# 抓取用的 User-Agent。
# 实测（2026-09-10）：VentureBeat 等站点会对 `compatible; AIWeeklyReport/x.y`
# 这类**自报爬虫身份**的 UA 直接返回 429，换成常规浏览器 UA 即正常 200。
# 这里只读取各站公开的 RSS/Atom，属于标准 feed 阅读器行为。
FEED_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

RSS_KEYWORDS = ["ai", "llm", "gpt", "claude", "gemini", "model", "funding",
                "acquisition", "芯片", "大模型", "人工智能", "融资", "并购", "agent"]

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
HF_LEADERBOARD_API = "https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard/api/leaderboard"

# 分类关键词（按优先级匹配）
CATEGORY_KEYWORDS = {
    "ai-models": ["gpt", "claude", "gemini", "llama", "deepseek", "qwen", "grok",
                  "mistral", "大模型", "模型", "benchmark", "开源模型", "open weight"],
    "paper":     ["论文", "paper", "research", "arxiv", "预印本", "研究", "study"],
    "ai-products": ["发布", "launch", "release", "product", "app", "工具", "功能更新",
                    "chatgpt", "copilot", "上线", "新功能"],
    "industry":  ["融资", "funding", "acquisition", "并购", "ipo", "投资", "估值",
                  "芯片", "chip", "gpu", "政策", "监管", "regulation", "上市"],
    "tip":       ["教程", "tutorial", "指南", "技巧", "prompt", "how to"],
}
CATEGORY_PRIORITY = ["ai-models", "paper", "ai-products", "industry", "tip"]


# ── 代理 / 环境 ──────────────────────────────────────────────────
def load_env_file() -> None:
    """加载 .env 中的环境变量（NEWSAPI_KEY / 代理）。"""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip("\"'")
        if key and value and key not in os.environ:
            os.environ[key] = value


# ── 工具函数 ─────────────────────────────────────────────────────
def get_week_range(week_str: str | None = None) -> tuple[str, str, str]:
    """计算周范围（ISO 8601 周一为起点）。返回 (week_label, start, end)。"""
    if week_str:
        m = re.match(r"(\d{4})-W(\d+)", week_str)
        if m:
            year, week = int(m.group(1)), int(m.group(2))
            # ISO: 第1周是包含该年第一个周四的周
            jan4 = datetime(year, 1, 4)
            start = jan4 - timedelta(days=jan4.weekday())
            start = start + timedelta(weeks=week - 1)
            end = start + timedelta(days=6)
            return week_str, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    y, w, _ = start.isocalendar()
    return f"{y}-W{w:02d}", start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def parse_date_flexible(date_str: str) -> datetime | None:
    """解析多种日期格式 -> datetime。"""
    if not date_str:
        return None
    formats = [
        "%Y-%m-%d", "%Y/%m/%d", "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
        "%a, %d %b %Y %H:%M:%S GMT", "%d %b %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.replace(tzinfo=None)  # 统一为朴素时间，避免 tz 比较错误
        except ValueError:
            continue
    m = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", date_str)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def is_relevant(title: str, summary: str = "") -> bool:
    text = (title + " " + summary).lower()
    return any(kw in text for kw in RSS_KEYWORDS)


def classify(title: str, summary: str, feed_hint: str) -> str:
    """按关键词 + 源提示分类。"""
    text = (title + " " + summary).lower()
    for cat in CATEGORY_PRIORITY:
        if any(kw in text for kw in CATEGORY_KEYWORDS[cat]):
            return cat
    return feed_hint or "industry"


# ── RSS 抓取（主路径）─────────────────────────────────────────────
def fetch_via_rss(feed_url: str, max_items: int = 30,
                  start: str = "", end: str = "",
                  source_name: str = "", category_hint: str = "industry") -> tuple[list[dict], bool]:
    """RSS 抓取，返回 (归一化 items, 源是否正常)。带 1 次重试与超时保护。"""
    for attempt in range(2):
        try:
            # feedparser 通过 request_headers 设置 UA；代理由环境变量（urllib）生效
            feed = feedparser.parse(feed_url, agent=FEED_UA)
            if feed.bozo and not feed.entries:
                if attempt == 0:
                    time.sleep(1)
                    continue
                print(f"  ⚠️  {source_name}：解析失败（{str(feed.bozo_exception)[:60]}）")
                return [], False
            if not feed.entries:
                if attempt == 0:
                    time.sleep(1)
                    continue
                print(f"  ⚠️  {source_name}：无条目")
                return [], False

            start_dt = datetime.strptime(start, "%Y-%m-%d") if start else None
            end_dt = datetime.strptime(end, "%Y-%m-%d") if end else None
            feed_title = feed.feed.get("title", source_name or urlparse(feed_url).netloc)
            articles = []

            for entry in feed.entries[:max_items]:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                raw = entry.get("summary") or entry.get("description") or ""
                summary = BeautifulSoup(raw, "html.parser").get_text()[:300].strip()
                url = entry.get("link", "")
                date = entry.get("published", entry.get("updated", ""))
                parsed = parse_date_flexible(date)

                # 时间过滤
                if (start_dt or end_dt) and parsed:
                    if start_dt and parsed.date() < start_dt.date():
                        continue
                    if end_dt and parsed.date() > end_dt.date():
                        continue

                if not is_relevant(title, summary):
                    continue

                articles.append({
                    "title": title,
                    "summary": summary,
                    "url": url,
                    "source": feed_title,
                    "publishedAt": parsed.isoformat() if parsed else "",
                    "category": classify(title, summary, category_hint),
                    "score": 0,
                })
            return articles, True
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            print(f"  ⚠️  RSS 抓取失败 {source_name}：{e}")
            return [], False
    return [], False


# ── Hugging Face 模型排行榜（可选）────────────────────────────────
def fetch_hf_leaderboard(max_items: int = 10) -> list[dict]:
    try:
        resp = requests.get(HF_LEADERBOARD_API, timeout=15,
                             headers={"User-Agent": FEED_UA})
        if resp.status_code != 200:
            return []
        data = resp.json()
        items = data.get("data", data) if isinstance(data, dict) else data
        models = []
        for i, item in enumerate(items[:max_items]):
            name = item.get("model") or item.get("name") or item.get("fullname", "")
            score = item.get("average_score") or item.get("score") or item.get("average", 0)
            lic = (item.get("license") or "").lower()
            is_open = any(k in lic for k in ("mit", "apache", "cc", "open", "bsd"))
            models.append({
                "name": name, "developer": item.get("org", ""),
                "open_source": bool(is_open), "score": str(round(float(score), 1)) if score else "0",
                "rank": i + 1,
            })
        if models:
            print(f"  ✅ HF Leaderboard：{len(models)} 个模型")
        return models
    except Exception:
        return []


# ── News API（可选增强）───────────────────────────────────────────
def fetch_via_newsapi(query: str, from_date: str, to_date: str,
                      api_key: str, max_items: int = 20) -> list[dict]:
    if not api_key:
        return []
    try:
        resp = requests.get(NEWS_API_ENDPOINT, params={
            "q": query, "from": from_date, "to": to_date,
            "sortBy": "publishedAt", "language": "en",
            "pageSize": max_items, "apiKey": api_key,
        }, timeout=15)
        if resp.status_code != 200:
            return []
        out = []
        for a in resp.json().get("articles", []):
            title = a.get("title", "")
            if not title:
                continue
            out.append({
                "title": title,
                "summary": (a.get("description") or "")[:300],
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "NewsAPI"),
                "publishedAt": (parse_date_flexible(a.get("publishedAt", "")).isoformat()
                                if a.get("publishedAt") else ""),
                "category": classify(title, a.get("description", ""), "industry"),
                "score": 0,
            })
        return out
    except Exception:
        return []


def fetch_feed_with_mirror(name: str, url: str, hint: str, region: str = "cn",
                           **kw) -> tuple[list[dict], bool]:
    """抓取单个源；主源完全失败时按顺序回退 `FEED_MIRRORS` 里的国内镜像。"""
    items, ok = fetch_via_rss(url, source_name=name, category_hint=hint, **kw)
    if ok and items:
        return items, True
    for mirror in FEED_MIRRORS.get(name, []):
        m_items, m_ok = fetch_via_rss(mirror, source_name=name, category_hint=hint, **kw)
        if m_ok and m_items:
            print(f"  🔁 {name}：主源不可用，已回退国内镜像")
            return m_items, True
    return items, ok


# ── RSS 健康检查 ─────────────────────────────────────────────────
def check_feeds() -> dict:
    print("🏥 RSS 源健康检查")
    print("=" * 60)
    results = []
    for name, url, hint, region in RSS_FEEDS:
        t0 = time.time()
        print(f"  🔄 [{region:6s}] {name:<20} ...", end=" ", flush=True)
        try:
            feed = feedparser.parse(url, agent=FEED_UA)
            latency = int((time.time() - t0) * 1000)
            if feed.bozo and not feed.entries:
                print("❌ 失败")
                status, count = "error", 0
            elif not feed.entries:
                print("⚠️  0 条（可能失效）")
                status, count = "empty", 0
            else:
                print(f"✅ {len(feed.entries)} 条 ({latency}ms)")
                status, count = "ok", len(feed.entries)
            results.append({"name": name, "url": url, "region": region, "status": status,
                            "count": count, "latency_ms": latency})
        except Exception as e:
            print(f"❌ {str(e)[:50]}")
            results.append({"name": name, "url": url, "region": region, "status": "error",
                            "count": 0, "latency_ms": int((time.time() - t0) * 1000)})
    ok = sum(1 for r in results if r["status"] == "ok")
    cn = [r for r in results if r["region"] == "cn"]
    gl = [r for r in results if r["region"] == "global"]
    cn_ok = sum(1 for r in cn if r["status"] == "ok")
    gl_ok = sum(1 for r in gl if r["status"] == "ok")
    print("\n" + "=" * 60)
    print(f"📊 汇总：{ok}/{len(results)} 个源正常 "
          f"（国内 {cn_ok}/{len(cn)} · 国外 {gl_ok}/{len(gl)}）")
    if cn_ok == 0:
        print("  ⚠️ 国内源全部不可用：报告会只剩英文条目，中文地板失效，建议检查本机网络连通性")
    elif gl_ok == 0:
        print("  ⚠️ 国外源全部不可用：**这是预期内的降级路径，不影响出报告**（国内源兜底），"
              "仅会缺英文一手信源")
    for r in results:
        if r["status"] != "ok":
            tip = ("国内源，检查网络是否能访问该站；多为临时故障，稍后重试即可"
                   if r["region"] == "cn" else
                   "国外源不可达属预期内的降级：其余源会兜底，不会出空报告。"
                   "若本机网络架构要求全部出站流量经统一代理（如企业内网），"
                   "可通过标准环境变量 HTTPS_PROXY 提供")
            print(f"  💡 {r['name']}（{r['region']}）不可用 → {tip}")
    return {"feeds": results, "summary": {"total": len(results), "ok": ok,
            "cn_ok": cn_ok, "cn_total": len(cn), "global_ok": gl_ok, "global_total": len(gl),
            "failed": len(results) - ok, "checked_at": datetime.now().isoformat()}}


# ── 主流程 ────────────────────────────────────────────────────────
def fetch_all(week_str: str | None = None, use_news_api: bool = False,
              use_hf: bool = True) -> dict:
    load_env_file()
    socket.setdefaulttimeout(20)  # 防止单个 feed 卡死整轮抓取
    week_label, wk_start, wk_end = get_week_range(week_str)
    if week_str:
        # 真正按该 ISO 周的范围抓取（周一~周日），而非永远 trailing 7 天。
        # 这样 `bash run_report.sh scripts/fetch_ai_news.py --week 2026-W30`
        # 才会去取 07-20~07-26 这一周的新闻，而不是「今天往前 7 天」。
        start_date = wk_start
        end_date = wk_end
    else:
        # 未指定周：保持原行为（最近 7 天）
        today = datetime.today()
        start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    print(f"📅 新闻窗口：{start_date} ~ {end_date}（{week_label}）")
    print(f"📡 RSS 源：{len(RSS_FEEDS)} 个")

    all_items = []
    feeds_ok = 0
    cn_ok = gl_ok = 0
    for name, url, hint, region in RSS_FEEDS:
        print(f"  🔄 [{region:6s}] {name} ...", end=" ", flush=True)
        items, ok = fetch_feed_with_mirror(name, url, hint, region, max_items=50,
                                           start=start_date, end=end_date)
        feeds_ok += 1 if ok else 0
        if ok:
            if region == "cn":
                cn_ok += 1
            else:
                gl_ok += 1
        print(f"✅ {len(items)} 条" + ("" if ok else " ⚠️ 源异常"))
        all_items.extend(items)
    print(f"📡 源健康：{feeds_ok}/{len(RSS_FEEDS)} 个正常（国内 {cn_ok}/7 · 国外 {gl_ok}/7）")
    if cn_ok == 0:
        print("  ⚠️ 国内源全部不可用：本报告将只有英文条目，建议检查网络后重跑")

    # News API 增强
    if use_news_api:
        key = os.environ.get("NEWSAPI_KEY", "")
        if key:
            print("  🔑 News API 增强...")
            for q in ["AI artificial intelligence", "LLM large language model", "AI funding"]:
                all_items.extend(fetch_via_newsapi(q, start_date, end_date, key, 10))
        else:
            print("  ⚠️  NEWSAPI_KEY 未设置，跳过")

    # 去重（标题前 30 字符）
    seen, unique = set(), []
    for a in all_items:
        k = re.sub(r"\s+", "", a["title"][:30].lower())
        if k and k not in seen:
            seen.add(k)
            unique.append(a)

    # 按时间倒序
    unique.sort(key=lambda a: parse_date_flexible(a.get("publishedAt", "")) or datetime(1970, 1, 1),
                reverse=True)

    hf_models = fetch_hf_leaderboard(10) if use_hf else []

    return {
        "count": len(unique),
        "items": unique,
        "hf_models": hf_models,
        "week": week_label,
        "date_start": start_date,
        "date_end": end_date,
        "feeds_ok": feeds_ok,
    }


def save_json(data: dict, output_path: str) -> None:
    _save_json(output_path, data)  # 委托到 aiweekly.utils.save_json（原子写 + 共享助手）
    print(f"\n✅ 已保存 {output_path}（{data['count']} 条新闻）")
    cats = {}
    for it in data["items"]:
        cats[it["category"]] = cats.get(it["category"], 0) + 1
    print("   分类：", "  ".join(f"{k}:{v}" for k, v in sorted(cats.items())))


def main():
    p = argparse.ArgumentParser(description="RSS 抓取 AI 新闻 -> AI HOT 兼容 JSON")
    p.add_argument("--week", default=None,
                   help="周数，如 2026-W30（未指定则抓取最近 7 天，不是固定 ISO 周；"
                        "想生成固定周报请显式传 --week）")
    p.add_argument("--output", "-o", default="news.json", help="输出 JSON 路径")
    p.add_argument("--news-api", action="store_true", help="启用 News API 增强")
    p.add_argument("--no-hf", action="store_true", help="跳过 Hugging Face 排行榜")
    p.add_argument("--check-feeds", action="store_true", help="仅检查 RSS 源健康状态")
    # 可选：抓取阶段即用本地 Ollama 预译英文报道（写回 news.json，generate 阶段零推理）
    p.add_argument("--translate-en", action="store_true",
                   help="抓取阶段即用本地 Ollama 为英文报道生成中文总结（需本机运行 Ollama）")
    p.add_argument("--translate-model", default="qwen2.5:7b",
                   help="翻译所用本地 Ollama 模型（默认 qwen2.5:7b）")
    p.add_argument("--translate-workers", type=int, default=3,
                   help="翻译并发线程数（默认 3；CPU 本地推理下过高会互相抢资源导致超时丢条）")
    p.add_argument("--translate-timeout", type=int, default=45,
                   help="单条翻译超时秒数（默认 45；CPU 本地推理较慢，过短会大量超时丢条）")
    p.add_argument("--translate-retries", type=int, default=2,
                   help="单条翻译失败后的重试次数（默认 2，总尝试 = retries+1）")
    args = p.parse_args()

    if args.check_feeds:
        result = check_feeds()
        d = Path(__file__).parent.parent / "data"
        d.mkdir(exist_ok=True)
        (d / "feed_health.json").write_text(json.dumps(result, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
        print(f"\n📝 健康检查已保存：{d / 'feed_health.json'}")
        return

    data = fetch_all(week_str=args.week, use_news_api=args.news_api, use_hf=not args.no_hf)

    # 可选：抓取阶段预译英文报道（结果写回 news.json），generate 阶段直接命中缓存、零推理。
    # 用 try/except 包裹：翻译异常（Ollama 未运行/import 失败）绝不影响抓取主体，
    # generate 阶段会再次尝试（或静默保留英文原文）。
    if args.translate_en:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from aiweekly.translate import Translator
            cache_path = os.path.join(
                os.path.dirname(os.path.abspath(args.output)), ".translate_cache.json")
            tr = Translator(enabled=True, model=args.translate_model,
                            timeout=args.translate_timeout, max_workers=args.translate_workers,
                            retries=args.translate_retries, translate_title=True,
                            cache_path=cache_path)
            n = tr.translate_items(data["items"])
            print(f"🌐 抓取阶段预译：本地 Ollama 翻译 {n} 条英文报道")
        except Exception as e:  # noqa: BLE001
            print(f"  ⚠️ 抓取阶段预译跳过（{type(e).__name__}: {e}）；generate 阶段将重试")

    save_json(data, args.output)

    # 退出码分级：0=全成功 / 2=部分降级(源偏少或新闻偏少) / 1=全失败
    total = data.get("count", 0)
    feeds_ok = data.get("feeds_ok", 0)
    if total == 0 or feeds_ok == 0:
        print("⚠️ 抓取结果可能为空,退出码 1(全失败)")
        sys.exit(1)
    if feeds_ok < 3 or total < 20:
        print(f"⚠️ 降级完成(源 {feeds_ok}/{len(RSS_FEEDS)} 正常,新闻 {total} 条),退出码 2")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
