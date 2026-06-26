#!/usr/bin/env python3
"""Helper script to write radar.py"""
import os

SCRIPT = r'''#!/usr/bin/env python3
"""Competitor Radar - 竞品动态监控雷达
Usage: python3 radar.py [--days 7] [--output report.md] [--config config.yaml] [--no-llm] [--verbose]
"""

import argparse, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree as ET

# ── YAML 加载 ──────────────────────────────────────────────────────────────
try:
    import yaml
    def load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    YAML_BACKEND = "pyyaml"
except ImportError:
    YAML_BACKEND = "builtin"
    def load_yaml(path):
        """极简 YAML 解析，仅支持本 skill 配置格式"""
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        result = {"competitors": []}
        current = None
        in_list_field = None
        for raw in lines:
            stripped = raw.rstrip()
            if not stripped or stripped.strip().startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip())
            content = stripped.strip()
            if content == "competitors:":
                continue
            elif indent == 2 and content.startswith("- name:"):
                current = {"name": content.split(":", 1)[1].strip().strip('"')}
                result["competitors"].append(current)
                in_list_field = None
            elif indent == 4 and current is not None:
                if content.startswith("- ") and in_list_field:
                    val = content[2:].strip().strip('"')
                    if isinstance(current.get(in_list_field), list):
                        current[in_list_field].append(val)
                elif ":" in content:
                    key, _, val = content.partition(":")
                    key = key.strip(); val = val.strip().strip('"')
                    if val.startswith("[") and val.endswith("]"):
                        inner = val[1:-1]
                        current[key] = [x.strip().strip('"\'') for x in inner.split(",") if x.strip()]
                        in_list_field = None
                    elif not val:
                        current[key] = []; in_list_field = key
                    else:
                        current[key] = val; in_list_field = None
            elif indent == 6 and current is not None and in_list_field:
                if content.startswith("- "):
                    val = content[2:].strip().strip('"')
                    if isinstance(current.get(in_list_field), list):
                        current[in_list_field].append(val)
        return result

# ── 全局配置 ──────────────────────────────────────────────────────────────
TIMEOUT = 8
LLM_URL = "http://127.0.0.1:18790/anthropic/v1/messages"
LLM_API_KEY = "sk-RPBUoe2SH7KigJ0SZn6IPDirZtJ2fUaWSukEx1FwxjhWFx0G"
LLM_MODEL = "ppio/pa/claude-sonnet-4-6"
VERBOSE = False

def log(m):
    if VERBOSE: print(f"[DEBUG] {m}", file=sys.stderr)
def warn(m): print(f"[WARN]  {m}", file=sys.stderr)
def info(m): print(f"[INFO]  {m}", file=sys.stderr)

# ── HTTP 工具 ─────────────────────────────────────────────────────────────
def http_get(url, extra_headers=None, timeout=TIMEOUT):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, application/xml, text/xml, */*",
        }
        if extra_headers: headers.update(extra_headers)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(), None
    except urllib.error.HTTPError as e: return None, f"HTTP {e.code}"
    except urllib.error.URLError as e: return None, f"连接失败: {e.reason}"
    except Exception as e: return None, f"{type(e).__name__}: {e}"

# ── LLM 调用 ──────────────────────────────────────────────────────────────
def llm_call(prompt, system="你是龙虾公司的信息分析助理", max_tokens=300):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LLM_API_KEY,
        "anthropic-version": "2023-06-01",
    }
    data = json.dumps({
        "model": LLM_MODEL, "max_tokens": max_tokens, "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(LLM_URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["content"][0]["text"]
    except Exception as e:
        warn(f"LLM 失败: {e}"); return None

def score_item(title, summary, source, competitor_name):
    """对单条动态 LLM 评分，返回 (score:int, reason:str)"""
    prompt = (
        f"你是竞品情报分析师。评估以下动态重要性（AI创业公司视角）。\n\n"
        f"竞品：{competitor_name} | 来源：{source}\n"
        f"标题：{title}\n摘要：{(summary or '')[:400]}\n\n"
        f"只返回JSON（无markdown）：{{\"score\": <1-5>, \"reason\": \"<一句话核心摘要>\"}}\n\n"
        f"5=重大战略(新模型/产品/融资) 4=重要功能/合作 3=常规更新 2=次要 1=噪音"
    )
    resp = llm_call(prompt, max_tokens=150)
    if not resp: return 3, ""
    try:
        resp = resp.strip()
        if "```" in resp:
            m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", resp, re.DOTALL)
            if m: resp = m.group(1)
        m = re.search(r"\{[^{}]+\}", resp, re.DOTALL)
        if m: resp = m.group(0)
        parsed = json.loads(resp)
        return max(1, min(5, int(parsed.get("score", 3)))), str(parsed.get("reason","")).strip()
    except Exception as e:
        log(f"评分解析失败: {e} | {resp[:80]}"); return 3, ""

# ── 日期工具 ──────────────────────────────────────────────────────────────
def parse_date(s):
    if not s: return None
    s = s.strip().replace(" GMT", " +0000").replace(" UTC", " +0000")
    fmts = [
        "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError: continue
    return None

def strip_html(t):
    return re.sub(r"<[^>]+>", "", t or "").strip()

def fmt_date(dt):
    return dt.strftime("%Y-%m-%d") if dt else "未知"

# ── 数据源 1: RSS ─────────────────────────────────────────────────────────
def fetch_rss(competitor, cutoff):
    url = competitor.get("blog_rss")
    if not url: return [], None
    log(f"[RSS] {competitor['name']} -> {url}")
    data, err = http_get(url)
    if err: return [], f"RSS 抓取失败 ({err})"
    try: root = ET.fromstring(data)
    except ET.ParseError as e: return [], f"RSS XML 解析失败: {e}"

    items = []
    ATOM = "http://www.w3.org/2005/Atom"

    def add(title, link, summary, date_str):
        dt = parse_date(date_str)
        if dt and dt < cutoff: return
        items.append({
            "title": strip_html(title) or "无标题",
            "url": (link or "").strip(),
            "summary": strip_html(summary)[:500],
            "date": fmt_date(dt),
            "source": "官方博客",
        })

    # RSS 2.0
    for item in root.findall(".//item"):
        add(item.findtext("title",""), item.findtext("link",""),
            item.findtext("description","") or item.findtext("summary",""),
            item.findtext("pubDate","") or item.findtext("{http://purl.org/dc/elements/1.1/}date",""))

    # Atom
    for ns_pfx in [f"{{{ATOM}}}", ""]:
        for entry in root.findall(f"{ns_pfx}entry"):
            t = entry.find(f"{ns_pfx}title")
            l = entry.find(f"{ns_pfx}link")
            s = entry.find(f"{ns_pfx}summary") or entry.find(f"{ns_pfx}content")
            d = entry.find(f"{ns_pfx}updated") or entry.find(f"{ns_pfx}published")
            add(t.text if t is not None else "",
                l.get("href","") if l is not None else "",
                s.text if s is not None else "",
                d.text if d is not None else "")

    log(f"[RSS] {competitor['name']} 得 {len(items)} 条")
    return items[:20], None

# ── 数据源 2: GitHub Releases ─────────────────────────────────────────────
def fetch_github_releases(competitor, cutoff):
    org = competitor.get("github_org","")
    spec_repos = competitor.get("github_repos") or []
    if not org and not spec_repos: return [], None

    token = os.environ.get("GITHUB_TOKEN","")
    auth = {"Authorization": f"token {token}"} if token else {}

    repos = list(spec_repos)
    if not repos and org:
        data, err = http_get(
            f"https://api.github.com/orgs/{org}/repos?sort=updated&per_page=8&type=public",
            extra_headers=auth)
        if err: return [], f"GitHub org repos 失败: {err}"
        try:
            lst = json.loads(data)
            repos = [r["full_name"] for r in lst[:5]] if isinstance(lst, list) else []
        except: return [], "GitHub 响应解析失败"

    items = []
    for repo in repos[:8]:
        log(f"[GitHub] {repo}")
        data, err = http_get(
            f"https://api.github.com/repos/{repo}/releases?per_page=5",
            extra_headers=auth)
        if err:
            log(f"[GitHub] {repo} releases 失败: {err}")
            continue
        try:
            releases = json.loads(data)
            if not isinstance(releases, list): continue
            for rel in releases:
                dt = parse_date(rel.get("published_at",""))
                if dt and dt < cutoff: continue
                body = strip_html(rel.get("body",""))[:400]
                items.append({
                    "title": f"[{repo.split('/')[1]}] {rel.get('name') or rel.get('tag_name','release')}",
                    "url": rel.get("html_url",""),
                    "summary": body,
                    "date": fmt_date(dt),
                    "source": "GitHub Release",
                })
        except Exception as e:
            log(f"[GitHub] {repo} 解析失败: {e}")

    log(f"[GitHub] {competitor['name']} 得 {len(items)} 条")
    return items[:15], None

# ── 数据源 3: HackerNews ──────────────────────────────────────────────────
def fetch_hackernews(competitor, cutoff):
    keywords = competitor.get("keywords") or [competitor["name"]]
    if not keywords: return [], None

    items = []
    seen = set()

    for kw in keywords[:3]:
        encoded = urllib.parse.quote(kw)
        url = (f"https://hn.algolia.com/api/v1/search"
               f"?query={encoded}&tags=story"
               f"&numericFilters=created_at_i>{int(cutoff.timestamp())}"
               f"&hitsPerPage=5")
        log(f"[HN] 搜索 '{kw}'")
        data, err = http_get(url)
        if err:
            log(f"[HN] 搜索失败: {err}")
            continue
        try:
            result = json.loads(data)
            for hit in result.get("hits", []):
                hn_url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}"
                if hn_url in seen: continue
                seen.add(hn_url)
                title = hit.get("title","")
                if not title: continue
                dt = datetime.fromtimestamp(hit.get("created_at_i", 0), tz=timezone.utc)
                points = hit.get("points", 0) or 0
                num_comments = hit.get("num_comments", 0) or 0
                items.append({
                    "title": title, "url": hn_url,
                    "summary": f"HN讨论 | {points}分 | {num_comments}评论",
                    "date": fmt_date(dt), "source": "HackerNews",
                    "_score