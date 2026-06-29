"""
lib/fetch.py - 书籍源数据抓取（轻量版：requests + 简单 HTML 解析）

不走 playwright（避免 169MB 浏览器下载）。
数据源：百度百科 + 维基百科（中文）+ 知乎（搜书评）

输入：书名 (+ 可选 作者)
输出：结构化 JSON 到 stdout 或文件
"""

import sys
import json
import re
import argparse
import os
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
from html import unescape

import requests

# 代理配置（用户偏好 7897 端口）
PROXY_HTTP = os.environ.get("PROXY_HTTP", "http://127.0.0.1:7897")
PROXY_HTTPS = os.environ.get("PROXY_HTTPS", "http://127.0.0.1:7897")
PROXIES = {"http": PROXY_HTTP, "https": PROXY_HTTPS}

# 是否走代理（默认开，用户可关）
USE_PROXY = os.environ.get("USE_PROXY", "1") == "1"

CACHE_DIR = Path(__file__).parent.parent / "sources" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TIMEOUT = 12


def get(url: str, cache_name: str, force: bool = False) -> str:
    """GET with cache + proxy support"""
    cache_path = CACHE_DIR / cache_name
    if not force and cache_path.exists() and (datetime.now().timestamp() - cache_path.stat().st_mtime) < 86400 * 7:
        return cache_path.read_text(encoding="utf-8", errors="ignore")
    try:
        headers = {
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        # 百度/知乎对 Referer 敏感，加上
        if "baidu.com" in url:
            headers["Referer"] = "https://www.baidu.com/"
        elif "zhihu.com" in url:
            headers["Referer"] = "https://www.zhihu.com/"

        r = requests.get(url, headers=headers, timeout=TIMEOUT,
                         proxies=PROXIES if USE_PROXY else None)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        html = r.text
        cache_path.write_text(html, encoding="utf-8")
        return html
    except Exception as e:
        print(f"[WARN] GET {url} 失败：{type(e).__name__}: {e}", file=sys.stderr)
        return ""


def strip_html(html: str) -> str:
    """简单 HTML 去标签"""
    text = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ----------------- 百度百科 -----------------

def fetch_baidu_baike(title: str) -> dict:
    # 优先用移动版（反爬较松），失败回退桌面版
    candidates = [
        f"https://m.baike.baidu.com/item/{quote(title)}",
        f"https://baike.baidu.com/item/{quote(title)}",
    ]
    safe = re.sub(r"[^\w\-]", "_", title)[:40]
    cache_name = f"baidu__{safe}.html"
    url = ""
    html = ""
    for u in candidates:
        url = u
        html = get(url, cache_name)
        if html and "百度百科" in html:
            break
    if not html:
        return {"source": "baidu", "url": url, "ok": False}

    out = {"source": "baidu", "url": url, "ok": True, "title": title}

    # meta description
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
    if m:
        out["summary"] = m.group(1).strip()

    # 备选：lemmaSummary / para
    if "summary" not in out:
        m = re.search(r'class="lemmaSummary[^"]*"[^>]*>([\s\S]{50,2000}?)</div>', html)
        if m:
            out["summary"] = strip_html(m.group(1))[:800]
    if "summary" not in out:
        m = re.search(r'class="para[^"]*"[^>]*>([\s\S]{50,2000}?)</div>', html)
        if m:
            out["summary"] = strip_html(m.group(1))[:800]

    # info box
    info = {}
    for k, v in re.findall(r'<dt[^>]*>([^<]+)</dt>\s*<dd[^>]*>([\s\S]{1,800}?)</dd>', html):
        key = re.sub(r"\s+", "", k)
        val = strip_html(v)
        if val and len(val) < 300:
            info[key] = val
    if info:
        out["info_box"] = info

    # 正文段落
    body_parts = []
    for m in re.finditer(r'class="para[^"]*"[^>]*>([\s\S]{20,2000}?)</div>', html):
        t = strip_html(m.group(1))
        if 10 < len(t) < 1000:
            body_parts.append(t)
        if sum(len(x) for x in body_parts) > 4000:
            break
    if body_parts:
        out["body_excerpt"] = "\n".join(body_parts)[:5000]

    return out


# ----------------- 维基百科 -----------------

def fetch_wikipedia(title: str, lang: str = "zh") -> dict:
    """维基百科 - 抓主条目
    lang: 'zh' | 'en' | 'ja' | 'fr' | 'de' | 'es' | 'ru' | 'ko'
    """
    wiki_domains = {
        "zh": "zh.wikipedia.org",
        "en": "en.wikipedia.org",
        "ja": "ja.wikipedia.org",
        "fr": "fr.wikipedia.org",
        "de": "de.wikipedia.org",
        "es": "es.wikipedia.org",
        "ru": "ru.wikipedia.org",
        "ko": "ko.wikipedia.org",
    }
    domain = wiki_domains.get(lang, "zh.wikipedia.org")
    if lang == "zh":
        url = f"https://{domain}/wiki/{quote(title)}"
    else:
        url = f"https://{domain}/wiki/{quote(title.replace(' ', '_'))}"
    safe = re.sub(r"[^\w\-]", "_", title)[:40]
    html = get(url, f"wiki_{lang}__{safe}.html")
    if not html:
        return {"source": f"wiki_{lang}", "url": url, "ok": False}

    out = {"source": f"wiki_{lang}", "url": url, "ok": True, "title": title}

    # 主体段落
    m = re.search(r'<div id="mw-content-text"[^>]*>([\s\S]{200,80000}?)</div>\s*<div', html)
    if m:
        out["body_excerpt"] = strip_html(m.group(1))[:5000]

    # infobox
    info = {}
    for row in re.findall(r'<tr[^>]*>([\s\S]{1,1500}?)</tr>', html[:30000]):
        th = re.search(r'<th[^>]*>([^<]+)</th>', row)
        td = re.search(r'<td[^>]*>([\s\S]{1,1000}?)</td>', row)
        if th and td:
            k = re.sub(r"\s+", "", th.group(1))
            v = strip_html(td.group(1))
            if v and len(v) < 300:
                info[k] = v
    if info:
        out["info_box"] = info

    return out


# ----------------- 知乎 -----------------

def fetch_zhihu(title: str) -> dict:
    """知乎 - 搜书评 / 评价（用知乎 API，反爬较松）"""
    # 知乎搜索 API 路径
    api_url = f"https://www.zhihu.com/api/v4/search_v3?t=general&q={quote(title + ' 书评')}&correction=1&offset=0&limit=10"
    safe = re.sub(r"[^\w\-]", "_", title)[:40]
    html = get(api_url, f"zhihu_api__{safe}.html", force=False)
    if not html or len(html) < 100:
        # 退回搜索页（可能 403）
        fallback_url = f"https://www.zhihu.com/search?type=content&q={quote(title + ' 评价')}"
        html = get(fallback_url, f"zhihu__{safe}.html")
    if not html:
        return {"source": "zhihu", "url": api_url, "ok": False}

    out = {"source": "zhihu", "url": api_url, "ok": True}

    # 尝试解析 API JSON
    snippets = []
    try:
        data = json.loads(html)
        # API v3 返回结构：data[].highlight, data[].excerpt, data[].content
        for item in (data.get("data") or [])[:10]:
            for k in ("excerpt", "highlight", "content", "excerpt_new"):
                v = item.get(k, "")
                if v:
                    text = strip_html(v)
                    if 15 < len(text) < 400:
                        snippets.append(text)
                        break
    except json.JSONDecodeError:
        # HTML 退回路径
        for m in re.finditer(r'class="RichText[^"]*"[^>]*>([\s\S]{30,500}?)</span>', html):
            text = strip_html(m.group(1))
            if 15 < len(text) < 300:
                snippets.append(text)
    out["snippets"] = snippets[:10]
    return out


def fetch_goodreads(title: str) -> dict:
    """Goodreads - 英文书的读者评分 + 书评摘要
    注意：Goodreads 反爬很严，2024 后基本挡未登录请求
    """
    safe = re.sub(r"[^\w\-]", "_", title)[:40]
    # 用搜索 URL（不是书页 URL，搜索页反爬稍松）
    url = f"https://www.goodreads.com/search?q={quote(title)}"
    html = get(url, f"goodreads__{safe}.html")
    if not html:
        return {"source": "goodreads", "url": url, "ok": False}

    out = {"source": "goodreads", "url": url, "ok": True}
    # 抓书搜索结果的标题 + 评分
    snippets = []
    for m in re.finditer(r'<span[^>]+class="[^"]*Text__title[^"]*"[^>]*>([\s\S]{1,200}?)</span>', html):
        text = strip_html(m.group(1))
        if 3 < len(text) < 200:
            snippets.append(text)
    # 评分（ratingsCount + averageRating）
    rating_match = re.search(r'"ratingCount":\s*(\d+)', html)
    avg_match = re.search(r'"averageRating":\s*([\d.]+)', html)
    if rating_match:
        out["rating_count"] = int(rating_match.group(1))
    if avg_match:
        try:
            out["avg_rating"] = float(avg_match.group(1))
        except ValueError:
            pass
    out["snippets"] = snippets[:5]
    return out


def fetch_douban_en(title: str) -> dict:
    """豆瓣 - 英文区的中文书评 / 译本讨论
    用于：英文书的中文读者评价
    """
    safe = re.sub(r"[^\w\-]", "_", title)[:40]
    url = f"https://book.douban.com/subject_search?search_text={quote(title)}&cat=1001"
    html = get(url, f"douban_en__{safe}.html")
    if not html:
        return {"source": "douban_en", "url": url, "ok": False}
    out = {"source": "douban_en", "url": url, "ok": True}
    # 抓搜索结果的标题/作者/评分
    snippets = []
    for m in re.finditer(r'<a[^>]+title="([^"]{3,200}?)"[^>]*>\s*([^<]{1,100})', html):
        if 3 < len(m.group(1)) < 200:
            snippets.append(m.group(1))
    out["snippets"] = snippets[:5]
    return out


# ----------------- 主入口 -----------------

def fetch_all(title: str, author: str = "", lang: str = "zh") -> dict:
    """主入口：抓全部源，组装成结构化数据
    lang=zh: 百度百科 + 维基(zh) + 知乎
    lang=en: 维基(en) + Goodreads + 豆瓣英文区
    """
    print(f"[fetch] 抓取《{title}》... lang={lang} 代理={'开' if USE_PROXY else '关'}", file=sys.stderr)

    if lang == "zh":
        baidu = fetch_baidu_baike(title)
        print(f"[fetch] 百度百科: {'OK' if baidu['ok'] else 'FAIL'} {('summary='+str(len(baidu.get('summary','')))) if baidu['ok'] else ''}", file=sys.stderr)
    else:
        baidu = {"source": "baidu", "ok": False, "skipped": "lang=en (中文源) 跳过"}

    wiki = fetch_wikipedia(title, lang)
    print(f"[fetch] 维基百科({lang}): {'OK' if wiki['ok'] else 'FAIL'} {('body='+str(len(wiki.get('body_excerpt','')))) if wiki['ok'] else ''}", file=sys.stderr)

    if lang == "zh":
        zhihu = fetch_zhihu(title)
        print(f"[fetch] 知乎: {'OK' if zhihu['ok'] else 'FAIL'} ({len(zhihu.get('snippets', []))} 条片段)", file=sys.stderr)
    else:
        zhihu = {"source": "zhihu", "ok": False, "skipped": "lang=en (中文源) 跳过"}

    extras = {}
    if lang == "en":
        goodreads = fetch_goodreads(title)
        print(f"[fetch] Goodreads: {'OK' if goodreads['ok'] else 'FAIL'} rating={goodreads.get('avg_rating','-')}", file=sys.stderr)
        douban = fetch_douban_en(title)
        print(f"[fetch] 豆瓣(英文区): {'OK' if douban['ok'] else 'FAIL'} ({len(douban.get('snippets', []))} 条片段)", file=sys.stderr)
        extras["goodreads"] = goodreads
        extras["douban_en"] = douban

    return {
        "title": title,
        "author": author,
        "lang": lang,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "proxy": "on" if USE_PROXY else "off",
        "sources": {
            "baidu": baidu,
            "wiki": wiki,  # 不再写死 wiki_zh，lang 可变
            "zhihu": zhihu,
            **extras,
        }
    }


def main():
    p = argparse.ArgumentParser(description="书籍源数据抓取")
    p.add_argument("--title", required=True, help="书名")
    p.add_argument("--author", default="", help="作者（可选）")
    p.add_argument("--lang", choices=["zh", "en"], default="zh", help="语言（zh=中文经典, en=英文经典）")
    p.add_argument("--out", help="输出 JSON 路径（默认 stdout）")
    p.add_argument("--no-proxy", action="store_true", help="不走代理")
    args = p.parse_args()

    global USE_PROXY
    if args.no_proxy:
        USE_PROXY = False

    data = fetch_all(args.title, args.author, args.lang)
    text = json.dumps(data, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"[fetch] 已写 {args.out}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
