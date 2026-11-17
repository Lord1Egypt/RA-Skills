#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""免费工具平替雷达 - 16 渠道统一搜索脚本。

用法:
  python alt_search.py "关键词1,关键词2" [--channels alternativeto,github,...] [--limit 8] [--json out.json]
  python alt_search.py --check          # 仅渠道自检

输出: markdown 摘要(渠道覆盖表 + 工具向/技能向分流结果表) 打到 stdout;
      --json 指定路径时同时落盘完整结果。
渠道内关键词串行, 渠道间线程并发; 单渠道失败不中断整体。
渠道: 技能向 10(SkillHub/虾评/ClawHub/Vercel/SkillsMP/GitHub/awesome-agent-skills/Anthropic/小红书/Coze)
      + 工具向 6(AlternativeTo/awesome-selfhosted/HackerNews/Reddit/ProductHunt/WebSearch)
"""

import argparse
import base64
import html as html_mod
import json
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT_API = 15
TIMEOUT_PROXY = 20
TIMEOUT_CLI = 90
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

TIER_W = {"oss": 100, "freemium": 60, "unknown": 30, "paid": 0}
TIER_TAG = {"oss": "[免费开源]", "freemium": "[免费额度]", "unknown": "[未验证]", "paid": "[付费]"}

# 渠道分类: skill=技能向(Agent 技能), tool=工具向(软件平替); 报告按此分流展示
# 注: GitHub 为双栖渠道, 工具平替场景其结果按软件仓库归入 tool
CHANNEL_CATEGORY = {
    "skillhub": "skill", "xiaping": "skill", "clawhub": "skill", "vercel": "skill",
    "skillsmp": "skill", "awesome": "skill", "anthropic": "skill",
    "xhs": "skill", "coze": "skill",
    "github": "tool", "alternativeto": "tool", "selfhosted": "tool",
    "hackernews": "tool", "reddit": "tool", "producthunt": "tool", "websearch": "tool",
}
# 当前搜索任务的全部关键词核心词并集(main() 注入), GitHub 相关性过滤用
_QUERY_CORE = []

# 本机真实代理(7897); 沙箱注入的随机端口代理常是死的, 不使用环境变量代理
REAL_PROXY = os.environ.get("ALT_RADAR_PROXY", "http://127.0.0.1:7897")
PROXY_KEYS = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")
_proxy_state = {}


def _proxy_up():
    """TCP 探测真实代理是否在监听(带缓存)。"""
    if "up" in _proxy_state:
        return _proxy_state["up"]
    try:
        host, port = urllib.parse.urlsplit(REAL_PROXY).netloc.split(":")
        with socket.create_connection((host, int(port)), timeout=2):
            _proxy_state["up"] = True
    except OSError:
        _proxy_state["up"] = False
    return _proxy_state["up"]


def _opener(no_proxy=False):
    if no_proxy:
        return urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener()


def _open(req, timeout=TIMEOUT_API):
    """先直连; 直连失败且真实代理(7897)存活时走代理。不使用环境变量注入的代理。"""
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=timeout) as r:
            return r.read()
    except Exception as first_err:
        if not _proxy_up():
            raise
        try:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({"http": REAL_PROXY, "https": REAL_PROXY}))
            with opener.open(req, timeout=TIMEOUT_PROXY) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if "rate limit" in (e.reason or "").lower():
                raise RuntimeError("HTTP 403: GitHub 匿名 API 限流(60次/时), 装 gh CLI 可解") from first_err
            raise
        except Exception:
            raise first_err


def _rate_limit_note(first_err):
    if isinstance(first_err, urllib.error.HTTPError) and "rate limit" in (first_err.reason or "").lower():
        return RuntimeError("HTTP 403: GitHub 匿名 API 限流(60次/时), 装 gh CLI 可解")
    return first_err


def _get_json(url, no_proxy=False, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    if no_proxy:
        try:
            with _opener(True).open(req, timeout=TIMEOUT_API) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            raise _rate_limit_note(e) from e
    return json.loads(_open(req).decode("utf-8", "replace"))


def _get_text(url, no_proxy=False, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    if no_proxy:
        try:
            with _opener(True).open(req, timeout=TIMEOUT_API) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            raise _rate_limit_note(e) from e
    return _open(req).decode("utf-8", "replace")


def _clean(s, n=100):
    return re.sub(r"\s+", " ", s or "").strip()[:n]


def _run(cmd, env_extra=None, timeout=TIMEOUT_CLI, no_proxy=False):
    """no_proxy=True 时剥离所有代理环境变量(gh/npx 直连 registry/github 更稳)。"""
    env = {**os.environ, **(env_extra or {})}
    if no_proxy:
        for k in PROXY_KEYS:
            env.pop(k, None)
        env["no_proxy"] = "*"
    p = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout, env=env, shell=(os.name == "nt") and cmd[0].endswith((".cmd", ".bat")),
    )
    return (p.stdout or "") + (p.stderr or "")


def _item(name, desc="", stars=0, url="", channel="", tier="unknown"):
    return {"name": _clean(name, 60), "desc": _clean(desc, 120), "stars": stars or 0,
            "url": url, "channel": channel, "tier": tier if tier in TIER_W else "unknown",
            "category": CHANNEL_CATEGORY.get(channel, "tool")}


def _license_tier(lic):
    lic = (lic or "").lower()
    if not lic:
        return "unknown"
    if any(k in lic for k in ("open", "free", "gpl", "mit", "apache", "bsd", "mpl", "unlicense", "zlib", "isc")):
        return "oss"
    if "freemium" in lic:
        return "freemium"
    if any(k in lic for k in ("commercial", "proprietary", "paid", "trial")):
        return "paid"
    return "unknown"


def _xiaping_key():
    for k in ("XIAPING_KEY", "XIAPING_API_KEY"):
        if os.environ.get(k):
            return os.environ[k]
    p = os.path.expanduser("~/.workbuddy/secrets/xiaping_api_key.txt")
    try:
        with open(p, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return None


def _npx_tool():
    return shutil.which("npx") or shutil.which("npx.cmd")


def _gh_cmd():
    return shutil.which("gh")


def _readme_raw(repo):
    """优先 gh api(base64), 降级匿名 REST(raw)。"""
    gh = _gh_cmd()
    if gh:
        out = _run([gh, "api", f"repos/{repo}/readme", "--jq", ".content"], timeout=90, no_proxy=True)
        if out.strip():
            return base64.b64decode(out.strip()).decode("utf-8", "replace")
    return _get_text(f"https://api.github.com/repos/{repo}/readme",
                     no_proxy=True, headers={"Accept": "application/vnd.github.raw+json"})


# ---------------- GitHub 相关性过滤 ----------------

# 意图词: 表达"找平替"的动作/属性词, 不算核心词, 不要求命中仓库
GH_INTENT_STOP = {
    "alternative", "alternatives", "alt", "free", "open", "opensource", "source",
    "selfhosted", "self", "hosted", "host", "vs", "versus", "best", "top",
    "tool", "tools", "app", "apps", "software", "list", "awesome", "replace",
    "replacement", "clone", "similar", "like", "download", "online",
    "平替", "免费", "免费版", "替代", "替代品", "开源", "自托管", "有没有", "推荐", "的", "了",
}
# 领域黑名单: 即使含核心词也排除(政治宣传/书单影视聚合等无关领域, 宁缺毋滥)
GH_BLOCK_PAT = re.compile(
    r"dictatorship|独裁|政变|书单|藏书|many[- ]books|影视|剧集|追剧|动漫", re.I)


def _gh_core_tokens(q):
    """从单个关键词提取核心词(剔除意图词)。中文>=2字, 英文>=3字母。"""
    core = []
    for t in re.split(r"[\s,+/_\-]+", q.lower()):
        t = t.strip()
        if not t or t.isdigit() or t in GH_INTENT_STOP:
            continue
        if re.search(r"[\u4e00-\u9fff]", t):
            if len(t) >= 2:
                core.append(t)
        elif len(t) >= 3:
            core.append(t)
    return core


def _gh_all_core(keywords):
    """全部关键词的核心词并集: L1-L5 关键词表共同定义主题空间, 提升召回。
    例: 目标 AppFlowy 描述为"Bring projects, wikis, and teams together with AI",
    不含"notion"但含 L2 品类词"wiki", 并集过滤可保住; 无关库(政治/书单)仍被拦截。"""
    seen, out = set(), []
    for q in keywords:
        for t in _gh_core_tokens(q):
            if t not in seen:
                seen.add(t)
                out.append(t)
    return out


def _gh_relevant(name, desc, core):
    """核心词命中 name/description 才保留; 命中黑名单领域直接排除; 无核心词时不过滤。"""
    if not core:
        return True
    text = f"{name} {desc}".lower()
    if GH_BLOCK_PAT.search(text):
        return False
    return any(t in text for t in core)


# ---------------- 技能向渠道(复用技能查找实现) ----------------

def ch_skillhub(q, limit):
    try:
        data = _get_json("https://lightmake.site/api/v1/search?"
                         + urllib.parse.urlencode({"q": q, "limit": 15}))
        items = [_item(r.get("name") or r.get("slug"), r.get("description_zh") or r.get("description"),
                       r.get("stars") or r.get("installs"),
                       r.get("homepage") or f"https://lightmake.site/skills/{r.get('slug', '')}",
                       "skillhub", "oss") for r in data.get("results", [])]
        return ("ok", items, "" if items else "无结果")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: 可能需代理(Bitz Net)")


def ch_skillsmp(q, limit):
    try:
        data = _get_json("https://skillsmp.com/api/v1/skills/search?"
                         + urllib.parse.urlencode({"q": q, "limit": 15}), no_proxy=True)
        items = [_item(r.get("name"), r.get("description"), r.get("stars"),
                       r.get("url") or r.get("homepage") or "", "skillsmp", "oss")
                 for r in data.get("results", [])]
        return ("ok", items, "" if items else "无结果")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: 需直连(勿走代理)")


def ch_xiaping(q, limit):
    key = _xiaping_key()
    if not key:
        return ("skip", [], "缺 XIAPING_KEY(环境变量或 secrets/xiaping_api_key.txt)")
    cli = os.path.expanduser("~/.workbuddy/skills/虾评技能管理/scripts/xiaping-cli.py")
    if not os.path.exists(cli):
        return ("skip", [], "未找到 xiaping-cli.py")
    env = {"XIAPING_KEY": key, "XIAPING_API_KEY": key}
    try:
        out = _run([sys.executable, cli, "search", q], env_extra=env, timeout=60, no_proxy=True)
        items = []
        for ln in out.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(("{", "[", "#", "===")):
                continue
            m = re.search(r"https?://\S+", ln)
            items.append(_item(ln[:80], "", 0, m.group(0) if m else "", "xiaping", "oss"))
        return ("ok", items[:15], "" if items else "无结果/解析为空")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_clawhub(q, limit):
    npx = _npx_tool()
    if not npx:
        return ("skip", [], "npx 不可用")
    try:
        out = _run([npx, "--yes", "clawhub", "search", q], no_proxy=True)
        items = []
        for ln in out.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(("Searching", "npm", ">", "WARN")):
                continue
            m = re.search(r"(\d[\d.]*)$", ln)
            items.append(_item(ln[:90], "", int(float(m.group(1))) if m else 0, "", "clawhub", "oss"))
        return ("ok", items[:15], "" if items else "无结果/解析为空")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_vercel(q, limit):
    npx = _npx_tool()
    if not npx:
        return ("skip", [], "npx 不可用")
    try:
        out = _run([npx, "--yes", "skills", "find", q], no_proxy=True)
        items = []
        for ln in out.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(("Searching", "npm", ">", "WARN", "Need")):
                continue
            if "@" in ln:
                items.append(_item(ln[:90], "", 0, "", "vercel", "oss"))
        return ("ok", items[:15], "" if items else "无结果/解析为空")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_github(q, limit):
    try:
        gh = _gh_cmd()
        if gh:
            out = _run([gh, "search", "repos", q, "--limit", "25", "--sort", "stars",
                        "--json", "fullName,stargazersCount,description"], timeout=60, no_proxy=True)
            data = json.loads(out)
            items = [_item(d["fullName"], d.get("description"), d.get("stargazersCount"),
                           f"https://github.com/{d['fullName']}", "github", "oss") for d in data]
        else:
            url = ("https://api.github.com/search/repositories?"
                   + urllib.parse.urlencode({"q": q, "sort": "stars", "per_page": 25}))
            data = _get_json(url, no_proxy=True)
            items = [_item(d["full_name"], d.get("description"), d.get("stargazers_count"),
                           d.get("html_url"), "github", "oss") for d in data.get("items", [])]
        # 相关性过滤: 核心词(全部关键词的并集)须命中 name/description
        # (gh 默认连 README 一起搜, 会混入无关仓库; 并集过滤依托 L1-L5 关键词表, 兼顾精度与召回)
        core = _QUERY_CORE or _gh_core_tokens(q)
        kept = [it for it in items if _gh_relevant(it["name"], it["desc"], core)]
        dropped = len(items) - len(kept)
        note = f"相关性过滤 {dropped} 条" if dropped else ""
        return ("ok", kept[:15], note or ("" if kept else "无结果"))
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_awesome(q, limit):
    try:
        raw = _readme_raw("VoltAgent/awesome-agent-skills")
        if not raw:
            return ("fail", [], "readme 获取失败")
        kws = [w for w in re.split(r"[,\s]+", q) if w]
        items = []
        for ln in raw.splitlines():
            if "|" not in ln or not re.search(r"\[[^\]]+\]\(http", ln):
                continue
            low = ln.lower()
            if any(k.lower() in low for k in kws):
                m = re.search(r"\[([^\]]+)\]\((http[^)]+)\)", ln)
                if m:
                    items.append(_item(m.group(1), ln.replace("|", " ")[:120], 0, m.group(2), "awesome", "oss"))
        return ("ok", items[:15], "" if items else "无匹配行")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_anthropic(q, limit):
    try:
        gh = _gh_cmd()
        if gh:
            out = _run([gh, "api", "repos/anthropics/skills/contents/skills", "--jq", ".[].name"],
                       timeout=60, no_proxy=True)
            names = [n.strip() for n in out.splitlines() if n.strip()]
        else:
            data = _get_json("https://api.github.com/repos/anthropics/skills/contents/skills", no_proxy=True)
            names = [d["name"] for d in data]
        kws = [w.lower() for w in re.split(r"[,\s]+", q) if w]
        items = [_item(n, "Anthropic 官方技能", 0, f"https://github.com/anthropics/skills/tree/main/skills/{n}",
                       "anthropic", "oss") for n in names if any(k[:4] in n.lower() for k in kws)]
        return ("ok", items, "" if items else f"官方库共{len(names)}个技能, 无关键词匹配")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_xhs(q, limit):
    return ("skip", [], "需 tabbit CDP 浏览器, AI 手动辅助渠道")


def ch_coze(q, limit):
    return ("skip", [], "coze.cn/skills 需登录, AI 手动辅助渠道")


# ---------------- 工具向渠道(本技能新增 6 渠道) ----------------

def ch_alternativeto(q, limit):
    # 三级降级: API → HTML 搜索页(www/非www) → DDG site: 兜底
    try:
        data = _get_json("https://www.alternativeto.net/api/search/?"
                         + urllib.parse.urlencode({"q": q}))
        items = []
        for r in (data.get("results") or [])[:15]:
            lic = r.get("license") or r.get("licence") or ""
            stars = r.get("likes") or r.get("followers") or r.get("votes") or 0
            items.append(_item(r.get("name") or r.get("title"),
                               r.get("description") or r.get("tagline") or "",
                               stars, r.get("url") or r.get("homepage") or "",
                               "alternativeto", _license_tier(lic)))
        if items:
            return ("ok", items, "")
    except Exception:
        pass
    for host in ("https://www.alternativeto.net", "https://alternativeto.net"):
        try:
            page = _get_text(f"{host}/browse/search/?" + urllib.parse.urlencode({"q": q}))
            items, seen = [], set()
            for m in re.finditer(r'/software/([a-z0-9\-]+)/?"[^>]*>([^<]{2,80})<', page):
                slug, title = m.group(1), html_mod.unescape(m.group(2)).strip()
                if slug in seen or not title:
                    continue
                seen.add(slug)
                items.append(_item(title, "", 0, f"https://www.alternativeto.net/software/{slug}/",
                                   "alternativeto", "unknown"))
                if len(items) >= 15:
                    break
            if items:
                return ("ok", items, "HTML降级")
        except Exception:
            continue
    # 注: 域名限定搜索(site:)在 DDG(触发验证页)/Bing(忽略运算符)均不可用,
    # 且本机到 Cloudflare 全链路 403; 标注 AI 侧 WebFetch 兜底(已验证服务端可达)
    return ("fail", [], "API/HTML 均 403(Cloudflare), AI 用 WebFetch 补 alternativeto.net/software/<目标工具slug>/")


def ch_selfhosted(q, limit):
    try:
        raw = _readme_raw("awesome-selfhosted/awesome-selfhosted")
        if not raw:
            return ("fail", [], "readme 获取失败")
        kws = [w.lower() for w in re.split(r"[,\s]+", q) if len(w) > 2]
        items = []
        for ln in raw.splitlines():
            ln = ln.strip()
            if not ln.startswith("- [") or "](" not in ln:
                continue
            low = ln.lower()
            if not any(k in low for k in kws):
                continue
            m = re.search(r"\[([^\]]+)\]\((http[^)]+)\)", ln)
            if not m:
                continue
            name, url = m.group(1), m.group(2)
            tier = "unknown"
            for tok in re.findall(r"`([^`]+)`", ln):
                tier = _license_tier(tok)
                if tier != "unknown":
                    break
            sm = re.search(r"(\d[\d.]*)\s*k", ln)
            stars = int(float(sm.group(1)) * 1000) if sm and "k" in sm.group(0) else 0
            desc = re.sub(r"\[[^\]]+\]\([^)]+\)|`[^`]+`", "", ln)
            items.append(_item(name, desc, stars, url, "selfhosted", tier))
            if len(items) >= 15:
                break
        return ("ok", items, "" if items else "无匹配行")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_hackernews(q, limit):
    try:
        data = _get_json("https://hn.algolia.com/api/v1/search?"
                         + urllib.parse.urlencode({"query": q, "tags": "story", "hitsPerPage": 10}))
        items = []
        for h in data.get("hits", []):
            hid = h.get("objectID")
            url = h.get("url") or f"https://news.ycombinator.com/item?id={hid}"
            desc = (f"HN {h.get('points') or 0} 分 / {h.get('num_comments') or 0} 评论"
                    f" ({str(h.get('created_at') or '')[:10]})")
            items.append(_item(h.get("title") or "", desc, h.get("points") or 0, url, "hackernews", "unknown"))
        return ("ok", items, "" if items else "无结果")
    except Exception as e:
        return ("fail", [], f"{type(e).__name__}: {e}")


def ch_reddit(q, limit):
    # 三级降级: www search.json → old.reddit search.json → DDG site: 兜底
    last_err = None
    for host in ("https://www.reddit.com", "https://old.reddit.com"):
        try:
            data = _get_json(f"{host}/search.json?"
                             + urllib.parse.urlencode({"q": q, "limit": 10, "sort": "relevance", "type": "link"}))
            items = []
            for c in (data.get("data", {}).get("children") or [])[:10]:
                d = c.get("data", {})
                desc = (d.get("selftext") or "")[:100] or f"r/{d.get('subreddit')} 讨论"
                items.append(_item(d.get("title") or "", desc, d.get("score") or 0,
                                   "https://www.reddit.com" + (d.get("permalink") or ""),
                                   "reddit", "unknown"))
            if items:
                return ("ok", items, "")
            last_err = RuntimeError("无结果")
        except Exception as e:
            last_err = e
    # 第三级: PullPush Reddit 数据镜像(不受本机封锁影响; 数据截至 2023 年中, 仅作补充)
    try:
        data = _get_json("https://api.pullpush.io/reddit/search/submission/?"
                         + urllib.parse.urlencode({"q": q, "size": 10}))
        items = []
        for d in (data.get("data") or [])[:10]:
            desc = (d.get("selftext") or "")[:100] or f"r/{d.get('subreddit')} 讨论(PullPush 镜像, 覆盖或不完整)"
            items.append(_item(d.get("title") or "", desc, d.get("score") or 0,
                               "https://www.reddit.com" + (d.get("permalink") or ""),
                               "reddit", "unknown"))
        if items:
            return ("ok", items, "PullPush 镜像")
    except Exception:
        pass
    return ("fail", [], "Reddit 全链路不可达, AI 用 WebSearch site:reddit.com 补")


def ch_producthunt(q, limit):
    # 两级降级: HTML 搜索页 → DDG site: 兜底
    try:
        page = _get_text("https://www.producthunt.com/search?" + urllib.parse.urlencode({"q": q}))
        items, seen = [], set()
        for slug in re.findall(r'/posts/([a-z0-9\-]{3,60})', page):
            if slug in seen:
                continue
            seen.add(slug)
            items.append(_item(slug.replace("-", " ").title(), "", 0,
                               f"https://www.producthunt.com/posts/{slug}", "producthunt", "unknown"))
            if len(items) >= 10:
                break
        if items:
            return ("ok", items, "")
    except Exception:
        pass
    # 注: 域名限定搜索不可用; 标注 AI 侧 WebFetch 兜底(已验证服务端可达)
    return ("fail", [], "HTML 403(Cloudflare), AI 用 WebFetch 补 producthunt.com/search?q=<关键词>")


def _unwrap_ddg(href):
    if "uddg=" in href:
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(href).query)
        if "uddg" in qs:
            return qs["uddg"][0]
    return href


def _ddg_search(q, limit=10):
    """DDG html/lite 抓取, 返回 [(title, url)]; 两个端点都失败返回 []。"""
    for base in ("https://html.duckduckgo.com/html/?", "https://lite.duckduckgo.com/lite/?"):
        try:
            page = _get_text(base + urllib.parse.urlencode({"q": q}))
            out = []
            pats = [r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
                    r'<a[^>]+class="result-link"[^>]+href="([^"]+)"[^>]*>(.*?)</a>']
            for pat in pats:
                for m in re.finditer(pat, page, re.S):
                    href = _unwrap_ddg(html_mod.unescape(m.group(1)))
                    title = html_mod.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
                    if title and href.startswith("http"):
                        out.append((title, href))
                if out:
                    break
            if out:
                return out[:limit]
        except Exception:
            continue
    return []


def _bing_rss(q, limit=10):
    """Bing RSS 输出(结果干净且不易触发验证页); DDG 被限流时的兜底搜索引擎。"""
    try:
        url = ("https://www.bing.com/search?"
               + urllib.parse.urlencode({"q": q, "format": "rss", "count": limit}))
        xml = _get_text(url)
        items = []
        for t, l in re.findall(r"<item>.*?<title>(.*?)</title>.*?<link>(.*?)</link>", xml, re.S):
            title = html_mod.unescape(re.sub(r"<[^>]+>", "", t)).strip()
            if title and l.startswith("http"):
                items.append((title, l))
        return items[:limit]
    except Exception:
        return []


def ch_websearch(q, limit):
    pairs = _ddg_search(q, 15)
    if not pairs:
        pairs = _bing_rss(q, 15)  # DDG 限流/验证页时用 Bing RSS 兜底
    if not pairs:
        return ("fail", [], "DDG/Bing 均失败, AI 用 WebSearch 手动补")
    return ("ok", [_item(t, "", 0, u, "websearch", "unknown") for t, u in pairs], "")


CHANNELS = {
    # 技能向
    "skillhub": ch_skillhub, "xiaping": ch_xiaping, "clawhub": ch_clawhub, "vercel": ch_vercel,
    "skillsmp": ch_skillsmp, "github": ch_github, "awesome": ch_awesome, "anthropic": ch_anthropic,
    "xhs": ch_xhs, "coze": ch_coze,
    # 工具向
    "alternativeto": ch_alternativeto, "selfhosted": ch_selfhosted, "hackernews": ch_hackernews,
    "reddit": ch_reddit, "producthunt": ch_producthunt, "websearch": ch_websearch,
}
CHANNEL_LABEL = {
    "skillhub": "SkillHub", "xiaping": "虾评", "clawhub": "ClawHub", "vercel": "Vercel Skills",
    "skillsmp": "SkillsMP", "github": "GitHub", "awesome": "awesome-agent-skills",
    "anthropic": "Anthropic 官方", "xhs": "小红书", "coze": "Coze 技能商店",
    "alternativeto": "AlternativeTo", "selfhosted": "awesome-selfhosted", "hackernews": "HackerNews",
    "reddit": "Reddit", "producthunt": "Product Hunt", "websearch": "WebSearch(DDG)",
}


def search_channel(name, keywords, limit):
    fn = CHANNELS[name]
    all_items, notes, statuses = [], [], []
    with ThreadPoolExecutor(max_workers=max(len(keywords), 2)) as ex:
        futs = {ex.submit(fn, q, limit): q for q in keywords}
        for f in as_completed(futs):
            q = futs[f]
            try:
                status, items, note = f.result()
            except Exception as e:
                status, items, note = "fail", [], f"{type(e).__name__}: {e}"
            all_items.extend(items)
            statuses.append(status)
            if note:
                notes.append(f"{q}: {note}")
    if all(s == "ok" for s in statuses):
        overall = "ok"
    elif all(s in ("fail", "skip") for s in statuses):
        overall = "skip" if "skip" in statuses else "fail"
    else:
        overall = "partial"  # 部分关键词成功、部分失败/跳过
    return overall, all_items, "; ".join(notes)


def dedup_sort(items):
    seen, out = {}, []
    for it in items:
        key = re.sub(r"^[^/]+/", "", it["name"].lower())
        key = re.sub(r"[\s_\-]+", "", key)
        if key in seen:
            prev = seen[key]
            chans = prev["channel"].split("/")
            if it["channel"] not in chans:
                prev["channel"] += "/" + it["channel"]
            prev["stars"] = max(prev["stars"], it["stars"])
            if TIER_W[it["tier"]] > TIER_W[prev["tier"]]:
                prev["tier"] = it["tier"]
            continue
        seen[key] = it
        out.append(it)
    for it in out:
        # star 贡献取 log10 刻度(封顶100): 同档内保序(铁律4), 又不让高星库压倒分层
        it["score"] = TIER_W[it["tier"]] + min(20 * math.log10(max(it["stars"], 1)), 100)
    out.sort(key=lambda x: -x["score"])
    return out


def _print_leadgen():
    # 引流信息（固定输出）
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="?", help="逗号分隔关键词(中英文可并列)")
    ap.add_argument("--channels", default="", help="逗号分隔渠道子集, 空=全部")
    ap.add_argument("--limit", type=int, default=8, help="最终展示条数(默认8)")
    ap.add_argument("--json", dest="json_path", default="", help="完整结果 JSON 落盘路径")
    ap.add_argument("--check", action="store_true", help="仅渠道自检")
    args = ap.parse_args()

    names = [c.strip() for c in args.channels.split(",") if c.strip()] or list(CHANNELS)
    bad = [c for c in names if c not in CHANNELS]
    if bad:
        print(f"未知渠道: {bad}\n可用: {list(CHANNELS)}")
        sys.exit(2)
    keywords = [w.strip() for w in (args.keywords or "").split(",") if w.strip()]

    global _QUERY_CORE
    _QUERY_CORE = _gh_all_core(keywords or ["test"])

    if args.check or not keywords:
        rows = []
        with ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(CHANNELS[n], "test", 1): n for n in names}
            for f in as_completed(futs):
                n = futs[f]
                try:
                    s, _, note = f.result()
                except Exception as e:
                    s, note = "fail", f"{type(e).__name__}: {e}"
                rows.append((CHANNEL_LABEL[n], s, note))
        print("| 渠道 | 状态 | 备注 |")
        print("|------|------|------|")
        for label, s, note in sorted(rows):
            print(f"| {label} | {s} | {_clean(note, 80) or '-'} |")
        return

    results, coverage = {}, []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(search_channel, n, keywords, args.limit): n for n in names}
        for f in as_completed(futs):
            n = futs[f]
            try:
                status, items, note = f.result()
            except Exception as e:
                status, items, note = "fail", [], f"{type(e).__name__}: {e}"
            results[n] = items
            coverage.append((CHANNEL_LABEL[n], status, len(items), note))

    merged = [it for items in results.values() for it in items]
    ranked = dedup_sort(merged)

    print(f"# 免费平替搜索结果: {' / '.join(keywords)}\n")
    print("## 1. 渠道覆盖\n")
    print("| 渠道 | 状态 | 命中数 | 备注 |")
    print("|------|:----:|:------:|------|")
    for label, status, cnt, note in sorted(coverage, key=lambda x: x[0]):
        print(f"| {label} | {status} | {cnt} | {_clean(note, 80) or '-'} |")

    tool_items = [it for it in ranked if it.get("category") == "tool"]
    skill_items = [it for it in ranked if it.get("category") == "skill"]

    def _rows(items, n):
        lines = ["| # | 标签 | 名称 | ★ | 渠道 | 描述 | 链接 |",
                 "|--:|------|------|--:|------|------|------|"]
        for i, it in enumerate(items[:n], 1):
            stars = f"{it['stars']}" if it["stars"] else "未验证"
            url = f"[链接]({it['url']})" if it["url"] else "-"
            lines.append(f"| {i} | {TIER_TAG[it['tier']]} | {it['name']} | {stars} | {it['channel']} | {it['desc']} | {url} |")
        return lines

    print(f"\n## 2. 工具向结果(免费开源>免费额度>未验证>付费; 共 {len(tool_items)} 条, 展示 Top {args.limit})\n")
    print("\n".join(_rows(tool_items, args.limit)) if tool_items else "（无工具向结果）")
    print(f"\n## 3. 技能向结果(附录; 共 {len(skill_items)} 条, 展示 Top {args.limit})\n")
    print("\n".join(_rows(skill_items, args.limit)) if skill_items else "（无技能向结果）")

    if args.json_path:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_path)), exist_ok=True)
        payload = {"keywords": keywords, "coverage": [
            {"channel": c, "status": s, "count": n, "note": t} for c, s, n, t in coverage],
            "results": ranked,
            "summary": {"total": len(ranked),
                        "tool": sum(1 for it in ranked if it.get("category") == "tool"),
                        "skill": sum(1 for it in ranked if it.get("category") == "skill")}}
        with open(args.json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print(f"\nJSON 已落盘: {args.json_path}")

    _print_leadgen()


if __name__ == "__main__":
    main()
