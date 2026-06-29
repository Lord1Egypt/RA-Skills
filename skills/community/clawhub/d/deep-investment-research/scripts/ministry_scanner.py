#!/usr/bin/env python3
"""
China Ministry Scanner v2 — 宽度部委政策扫描（policy_gov 的互补）

定位（与 policy_gov_fetcher 错位互补，避免重复）:
- policy_gov_fetcher = 深度信号源：央行/证监会/发改委/工信部/统计局/海关/国常会
  （带 signal_level，进 data_daily 主管道，hk-research 消费）
- ministry_scanner   = 宽度扫描器：只覆盖 policy_gov 没有的部委
  （财政/商务/税务/农业/国资/科技/能源/住建/交通/教育/卫健/环境/市监/金监/外汇/外交）
  目的：当天这些部委有没有重大动静，作为宽覆盖盲区补充。

核心改进（v1 的问题→v2 的修复）:
- v1 用死字符串日期匹配，6/7 部委返回 0  → v2 抓列表 top-N + 鲁棒日期解析，
  正则覆盖全部格式（2026-06-04 / 2026.06.04 / 2026年6月4日 / [06-04] / 06-04），
  解析真实发布日期，只保留 ≤RECENT_DAYS 天的条目。
- v1 search 兜底 date 全是 unknown、返回官网首页/栏目页 → v2 解析 Serper 相对日期
  （X days/hours ago）转绝对日期并按 ≤RECENT_DAYS 过滤；剔除首页/栏目/导航页。

输出：~/research-data/data/daily/{date}/ministry_scan.json
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
TIMEOUT = 12
RECENT_DAYS = 7  # 只保留发布日期距今 <= 此天数的条目
LIST_TOPN = 15   # 每个列表页最多解析前 N 个 <li>，避免遍历整页
DATA_DIR = Path(os.path.expanduser(os.environ.get("RESEARCH_DATA_ROOT", "~/research-data"))) / "data" / "daily"
SEARCH_SCRIPT = os.path.expanduser(
    os.environ.get(
        "SEARCH_SKILL_PATH",
        "~/.openclaw/skills/web-search-plus/scripts/search.py",
    )
)


# ============================================================
# 鲁棒日期解析引擎（v2 核心修复）
# ============================================================

# 各种绝对日期格式：返回 (year, month, day) 或 None
_DATE_PATTERNS = [
    # 2026-06-04 / 2026/06/04 / 2026.06.04
    (re.compile(r'(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})'), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    # 2026年6月4日 / 2026年06月04日
    (re.compile(r'(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    # 20260604
    (re.compile(r'(20\d{2})(\d{2})(\d{2})'), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
]
# 只有月-日（无年份），如 [06-04] / 06-04 / 6月4日 → 需结合 today 推断年份
_MONTHDAY_PATTERNS = [
    re.compile(r'(?<!\d)(\d{1,2})[-/.](\d{1,2})(?!\d)'),
    re.compile(r'(\d{1,2})\s*月\s*(\d{1,2})\s*日'),
]
# Serper 相对日期：X hours/days/weeks ago（及中文）
_REL_PATTERNS = [
    (re.compile(r'(\d+)\s*hour', re.I), 'hours'),
    (re.compile(r'(\d+)\s*day', re.I), 'days'),
    (re.compile(r'(\d+)\s*week', re.I), 'weeks'),
    (re.compile(r'(\d+)\s*小时'), 'hours'),
    (re.compile(r'(\d+)\s*天'), 'days'),
    (re.compile(r'(\d+)\s*周'), 'weeks'),
]


def parse_date(text, today):
    """从任意文本里提取最可信的发布日期，返回 datetime.date 或 None。
    today: datetime.date 基准（用于月-日补年份、相对日期换算）。"""
    if not text:
        return None
    text = str(text)

    # 1) 相对日期（Serper news）
    low = text.lower()
    if 'just now' in low or '刚刚' in text or 'minutes ago' in low or '分钟' in text:
        return today
    if 'yesterday' in low or '昨天' in text:
        return today - timedelta(days=1)
    for pat, unit in _REL_PATTERNS:
        m = pat.search(text)
        if m:
            n = int(m.group(1))
            return today - timedelta(**{unit: n})

    # 2) 绝对完整日期（带年份）
    for pat, conv in _DATE_PATTERNS:
        for m in pat.finditer(text):
            try:
                y, mo, d = conv(m)
                if 1 <= mo <= 12 and 1 <= d <= 31 and 2020 <= y <= today.year + 1:
                    return datetime(y, mo, d).date()
            except (ValueError, TypeError):
                continue

    # 3) 仅月-日 → 用 today 的年份；若推断日期在未来超 3 天，视为去年
    for pat in _MONTHDAY_PATTERNS:
        m = pat.search(text)
        if m:
            try:
                mo, d = int(m.group(1)), int(m.group(2))
                if 1 <= mo <= 12 and 1 <= d <= 31:
                    cand = datetime(today.year, mo, d).date()
                    if (cand - today).days > 3:
                        cand = datetime(today.year - 1, mo, d).date()
                    return cand
            except (ValueError, TypeError):
                continue
    return None


def days_old(d, today):
    """返回日期距今天数；None 视为很旧。"""
    if d is None:
        return 9999
    return (today - d).days


# ============================================================
# Ministry definitions —— 只覆盖 policy_gov 没有的部委（错位互补）
# policy_gov 已有：pboc/csrc/ndrc/miit/nbs/customs/state_council
# 故此处剔除上述，专注宽度盲区。
# ============================================================

MINISTRIES_SCRAPE = {
    "财政部": {
        "url": "https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/",
        "base": "https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/",
    },
    "农业农村部": {
        "url": "https://www.moa.gov.cn/xw/zwdt/",
        "base": "https://www.moa.gov.cn/xw/zwdt/",
    },
    "国资委": {
        "url": "http://www.sasac.gov.cn/n2588025/n2588119/index.html",
        "base": "http://www.sasac.gov.cn",
    },
    "科技部": {
        "url": "https://www.most.gov.cn/kjbgz/",
        "base": "https://www.most.gov.cn/kjbgz/",
    },
    "税务总局": {
        "url": "https://www.chinatax.gov.cn/chinatax/n810219/n810724/index.html",
        "base": "https://www.chinatax.gov.cn",
    },
    "能源局": {
        "url": "https://www.nea.gov.cn/xwzx/nyyw.htm",
        "base": "https://www.nea.gov.cn",
    },
}

# JS 渲染/反爬/无稳定列表页的部委 → search 兜底（精准 query + 动作词）
MINISTRIES_SEARCH = [
    ("商务部", "商务部 公告 OR 通知 OR 印发"),
    ("住建部", "住房城乡建设部 公告 OR 通知 OR 印发"),
    ("交通运输部", "交通运输部 公告 OR 通知 OR 印发"),
    ("人社部", "人力资源社会保障部 公告 OR 通知"),
    ("教育部", "教育部 公告 OR 通知 OR 印发"),
    ("卫健委", "国家卫生健康委 公告 OR 通知"),
    ("生态环境部", "生态环境部 公告 OR 通知 OR 印发"),
    ("自然资源部", "自然资源部 公告 OR 通知 OR 印发"),
    ("市场监管总局", "市场监管总局 公告 OR 通知 OR 印发"),
    ("金融监管总局", "国家金融监督管理总局 通知 OR 办法 OR 监管"),
    ("外汇管理局", "外汇管理局 公告 OR 通知 OR 政策"),
]

# 跳过的噪音 URL：首页/栏目/导航/搜索页（不是具体政策文章）
# 注意不加 $ 锚（URL 常带查询串/锚点），用包含匹配
_JUNK_URL_RE = re.compile(
    r'(/index(_\d+)?\.html?|/index\.htm|/list/|/column/|'
    r'/search|/zhuanti/|/special/|sitemap)', re.I
)
# 纯域名根（首页）
_ROOT_URL_RE = re.compile(r'^https?://[^/]+/?(\?|#|$)')
# 跳过的噪音标题（栏目名/首页名/媒体机构名）
_JUNK_TITLE_RE = re.compile(
    r'^(中华人民共和国[\u4e00-\u9fa5]{0,6}(部|局|委|总局|集团))$|^(政策发布|新闻发布|政务公开|'
    r'通知通告|首页|政策法规|工作动态|公告公示|要闻动态)$|'
    r'(全媒体集团|传媒集团|新闻网|日报社|财经网)$'
)


def is_junk(title, url):
    t = (title or "").strip()
    u = (url or "").strip()
    if not t or len(t) < 10:
        return True
    if _JUNK_TITLE_RE.search(t):
        return True
    if _ROOT_URL_RE.match(u):
        return True
    if _JUNK_URL_RE.search(u):
        return True
    return False


def title_core(title):
    """归一化标题用于近似去重：去标点/空白/常见后缀，取核心。"""
    t = re.sub(r'[\s\|｜·—\-—_，,。、；;：:！!？?"\u201c\u201d\u2018\u2019（）()《》【】\[\]]', '', title or '')
    t = re.sub(r'(丨|V观话题|视频|图解|图说|专访|独家|快讯|滚动).*$', '', t)
    return t[:24]  # 取前 24 字符做指纹（同一事件不同媒体标题前缀通常一致）


# ============================================================
# 抓取
# ============================================================

def safe_fetch(url, encoding='utf-8'):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code != 200:
            return None
        # 自动探测编码（部分部委用 gb2312/gbk）
        ctype = resp.headers.get('Content-Type', '').lower()
        if 'gb' in ctype or 'gbk' in ctype or 'gb2312' in ctype:
            return resp.content.decode('gbk', errors='ignore')
        try:
            return resp.content.decode(encoding)
        except UnicodeDecodeError:
            return resp.content.decode('gbk', errors='ignore')
    except Exception:
        return None


def scrape_ministry(name, config, today):
    """通用列表抓取：取 top-N <li>，鲁棒解析日期，只留 <=RECENT_DAYS 天。"""
    html = safe_fetch(config["url"])
    if not html:
        return {"status": "fetch_failed", "items": []}

    soup = BeautifulSoup(html, 'html.parser')
    base = config["base"]
    items = []
    seen = set()

    # 优先在常见列表容器内找 <li>，否则全页 <li>
    lis = soup.find_all('li')
    count = 0
    for li in lis:
        if count >= LIST_TOPN * 3:  # 扫描上限，避免遍历超长页
            break
        a = li.find('a')
        if not a:
            continue
        title = a.get_text(strip=True)
        href = a.get('href', '')
        if not title or len(title) < 6:
            continue
        count += 1

        # 日期：优先 <span>/紧邻文本，回退到 li 全文 与 href
        span = li.find('span')
        date_src = " ".join(filter(None, [
            span.get_text(strip=True) if span else "",
            li.get_text(" ", strip=True),
            href,
        ]))
        pub = parse_date(date_src, today)
        old = days_old(pub, today)
        if old > RECENT_DAYS:
            continue

        url = href if href.startswith('http') else urljoin(base, href)
        if is_junk(title, url):
            continue
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "title": title,
            "url": url,
            "date": pub.strftime("%Y-%m-%d") if pub else "unknown",
            "days_old": old,
        })
        if len(items) >= LIST_TOPN:
            break

    return {"status": "ok", "items": items}


def search_ministry(name, query, today):
    """Serper news 兜底：解析相对/绝对日期，按 RECENT_DAYS 过滤，剔除噪音页。"""
    try:
        result = subprocess.run(
            ["python3", SEARCH_SCRIPT,
             "--query", query,
             "--provider", "serper",
             "--type", "news",
             "--time-range", "week",
             "--max-results", "8"],
            capture_output=True, text=True, timeout=25
        )
        data = json.loads(result.stdout)
    except Exception as e:
        return {"status": "error", "items": [], "error": str(e)}

    provider = data.get("provider", "?")
    items = []
    seen = set()
    for r in data.get("results", []):
        title = r.get("title", "")
        url = r.get("url", "")
        if is_junk(title, url):
            continue
        # 日期来源：date 字段 + snippet（snippet 常含 2026-06-04 这类绝对日期）
        date_src = " ".join(filter(None, [
            str(r.get("date") or ""),
            r.get("snippet", "")[:200],
            title,
        ]))
        pub = parse_date(date_src, today)
        old = days_old(pub, today)
        if old > RECENT_DAYS:
            continue
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "title": title,
            "url": url,
            "date": pub.strftime("%Y-%m-%d") if pub else "unknown",
            "days_old": old,
            "snippet": r.get("snippet", "")[:200],
            "source": r.get("source", ""),
        })
    return {"status": "ok", "items": items, "provider": provider}


def fetch_article_content(url, max_chars=3000):
    try:
        html = safe_fetch(url)
        if not html:
            return None
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<[^>]+>', ' ', html)
        html = re.sub(r'\s+', ' ', html).strip()
        return html[:max_chars] if html else None
    except Exception:
        return None


# ============================================================
# Main
# ============================================================

def run(target_date=None, fetch_content=False):
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    today = datetime.strptime(target_date, "%Y-%m-%d").date()
    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = {}
    total_items = 0

    # Phase 1: 直接抓取
    for name, config in MINISTRIES_SCRAPE.items():
        r = scrape_ministry(name, config, today)
        results[name] = r
        total_items += len(r["items"])

    # Phase 2: search 兜底
    for name, query in MINISTRIES_SEARCH:
        r = search_ministry(name, query, today)
        results[name] = r
        total_items += len(r["items"])

    # Phase 3: 可选全文
    if fetch_content:
        for ministry, data in results.items():
            for item in data.get("items", []):
                if item.get("url"):
                    c = fetch_article_content(item["url"])
                    if c:
                        item["content"] = c

    output = {
        "date": target_date,
        "fetch_time": fetch_time,
        "version": "v2",
        "recent_days_window": RECENT_DAYS,
        "scope_note": "宽度补充扫描；深度信号源见 policy_gov.json（央行/证监会/发改委/工信部/统计局/海关/国常会）",
        "total_items": total_items,
        "ministries_scanned": len(results),
        "sources": {
            name: {
                "status": data["status"],
                "items_count": len(data.get("items", [])),
                "method": "scrape" if name in MINISTRIES_SCRAPE else "search",
                "provider": data.get("provider", ""),
            }
            for name, data in results.items()
        },
        "items": [],
    }
    for ministry, data in results.items():
        for item in data.get("items", []):
            item["ministry"] = ministry
            output["items"].append(item)

    # 按新鲜度排序（最新在前）
    output["items"].sort(key=lambda x: x.get("days_old", 9999))

    # 跨部委近似去重：同一事件多家媒体只留最新一条
    deduped = []
    seen_core = set()
    for it in output["items"]:
        core = title_core(it["title"])
        if core and core in seen_core:
            continue
        seen_core.add(core)
        deduped.append(it)
    dropped_dup = len(output["items"]) - len(deduped)
    output["items"] = deduped
    output["total_items"] = len(deduped)
    output["near_dup_dropped"] = dropped_dup
    total_items = len(deduped)

    out_dir = DATA_DIR / target_date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "ministry_scan.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Ministry Scan v2 Complete: {target_date}  (window<={RECENT_DAYS}d)")
    print(f"Total recent items: {total_items}")
    print(f"Output: {out_file}\n")
    print("Per ministry:")
    for name, data in results.items():
        cnt = len(data.get("items", []))
        status = data["status"]
        marker = "✅" if status == "ok" and cnt > 0 else ("⚪" if status == "ok" else "❌")
        prov = f" [{data.get('provider')}]" if data.get("provider") else ""
        print(f"  {marker} {name:10s}: {cnt} items ({status}){prov}")
    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="China Ministry Scanner v2 (width complement)")
    parser.add_argument("--date", default=None, help="Target date (YYYY-MM-DD)")
    parser.add_argument("--fetch-content", action="store_true", help="Also fetch article full text")
    parser.add_argument("--days", type=int, default=None, help="Override recency window (days)")
    args = parser.parse_args()
    if args.days:
        RECENT_DAYS = args.days
    run(target_date=args.date, fetch_content=args.fetch_content)
