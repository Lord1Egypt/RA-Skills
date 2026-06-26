#!/usr/bin/env python3
"""
Bangumi Explorer — V1 信息查询版
通过 Bangumi（bgm.tv）公开 API 实现番剧搜索、详情查询、番表、排行、人物查询。
无需认证，零第三方依赖。
"""

import argparse
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.stdout and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# === 常量 ===

BASE_URL = "https://api.bgm.tv/v0"
HEADERS = {"User-Agent": "MountLynx/bangumi_skill (https://github.com/MountLynx/bangumi_skill)"}
TYPE_MAP = {
    "anime": 2, "book": 1, "game": 4,
    "music": 3, "real": 6,
}
TYPE_MAP_REVERSE = {v: k for k, v in TYPE_MAP.items()}
PLATFORM_LABELS = {
    "TV": "📺 TV", "Web": "🌐 Web", "OVA": "📦 OVA",
    "剧场版": "🎬 剧场版", "TVSP": "📺 SP", "DVD": "💿 DVD",
}
CACHE_DIR = Path.home() / ".bangumi" / "cache"
CACHE_TTL = {
    "search": 3600,      # 1h
    "subject": 86400,    # 24h
    "season": 21600,     # 6h
    "rank": 21600,       # 6h
    "person": 86400,     # 24h
    "calendar": 21600,  # 6h
    "character": 86400, # 24h
}
RATE_LIMIT = 0.5  # 秒


# === 缓存层 ===

def _ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(category: str, key: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)[:120]
    return CACHE_DIR / f"{category}_{safe}.json"


def get_cache(category: str, key: str):
    path = _cache_path(category, key)
    if not path.exists():
        return None
    try:
        mtime = path.stat().st_mtime
        ttl = CACHE_TTL.get(category, 3600)
        if time.time() - mtime > ttl:
            path.unlink()
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def set_cache(category: str, key: str, data):
    _ensure_cache_dir()
    path = _cache_path(category, key)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except OSError:
        pass


def clean_old_cache(max_age_days=7):
    """清理过期缓存文件"""
    if not CACHE_DIR.exists():
        return
    cutoff = time.time() - max_age_days * 86400
    for f in CACHE_DIR.glob("*.json"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
        except OSError:
            pass


# === 网络层 ===

_last_request_time = 0


def _rate_limit():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < RATE_LIMIT:
        time.sleep(RATE_LIMIT - elapsed)
    _last_request_time = time.time()


def api_get(path: str, params: dict = None, cache_category: str = None, cache_key: str = None):
    """GET 请求，支持缓存"""
    if cache_category and cache_key:
        cached = get_cache(cache_category, cache_key)
        if cached is not None:
            return cached

    _rate_limit()
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if cache_category and cache_key:
                set_cache(cache_category, cache_key, data)
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"❌ API 错误 {e.code}: {body[:200]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def api_post(path: str, data: dict = None, params: dict = None):
    """POST 请求，支持 URL 查询参数"""
    _rate_limit()
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else b"{}"
    req = urllib.request.Request(url, data=body, headers={
        **HEADERS,
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"❌ API 错误 {e.code}: {body[:200]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


# === 工具函数 ===

def _rating_str(rating: dict) -> str:
    if not rating or not rating.get("score"):
        return "暂无评分"
    score = rating["score"]
    rank = rating.get("rank")
    total = rating.get("total", 0)
    result = f"⭐ {score}"
    if rank and rank > 0:
        result += f" | Rank #{rank}"
    result += f"（{total}人评分）"
    return result


def _date_range_str(infobox: list) -> str:
    """从 infobox 提取放送日期"""
    start = end = None
    for item in (infobox or []):
        if item.get("key") in ("放送开始", "发售日", "开始"):
            start = item.get("value")
        if item.get("key") in ("放送结束", "结束"):
            end = item.get("value")
    if start and end:
        return f"{start} ~ {end}"
    return start or "未知"


def _platform_str(subject: dict) -> str:
    platform = subject.get("platform", "")
    return PLATFORM_LABELS.get(platform, platform or "未知")


def _eps_str(subject: dict) -> str:
    total = subject.get("total_episodes") or subject.get("eps", 0)
    if total and total > 0:
        return f"{total}集"
    return ""


def _tags_str(tags: list, max_count=5) -> str:
    if not tags:
        return ""
    top = sorted(tags, key=lambda t: t.get("count", 0), reverse=True)[:max_count]
    return "、".join(f"{t['name']}({t['count']})" for t in top)


def _collection_str(col: dict) -> str:
    if not col:
        return ""
    parts = []
    labels = {"wish": "想看", "collect": "看过", "doing": "在看", "on_hold": "搁置", "dropped": "抛弃"}
    for key, label in labels.items():
        v = col.get(key)
        if v and v > 0:
            parts.append(f"{label} {v}")
    return " | ".join(parts)


# === 格式化层 ===

def format_search(results: list, keyword: str) -> str:
    if not results:
        return f'【搜索结果】「{keyword}」 — 未找到相关结果'
    lines = [f'【搜索结果】「{keyword}」 — 找到 {len(results)} 条', ""]
    for i, item in enumerate(results, 1):
        title = item.get("name_cn") or item.get("name", "未知")
        orig = item.get("name", "")
        if orig and orig != title:
            title += f" / {orig}"
        score = item.get("rating", {}) or {}
        score_val = score.get("score")
        rank_val = score.get("rank")
        meta = f"⭐ {score_val}" if score_val else "⭐ 新番"
        if rank_val and rank_val > 0:
            meta += f" | Rank #{rank_val}"
        typ = TYPE_MAP_REVERSE.get(item.get("type"), "未知")
        eps = _eps_str(item)
        date = item.get("date", "") or ""
        tags = _tags_str(item.get("tags", []), 3)
        lines.append(f"{i}. {meta}")
        lines.append(f"   {title}（ID: {item['id']}）")
        detail_parts = []
        if typ != "未知":
            detail_parts.append(typ)
        if platform := _platform_str(item):
            detail_parts.append(platform)
        if eps:
            detail_parts.append(eps)
        if date:
            detail_parts.append(date)
        lines.append(f"   {' · '.join(detail_parts)}")
        if tags:
            lines.append(f"   标签：{tags}")
        lines.append("")
    return "\n".join(lines).rstrip()


def format_info(subject: dict) -> str:
    title = subject.get("name_cn") or subject.get("name", "未知")
    orig = subject.get("name", "")
    if orig and orig != title:
        title = f"{title} / {orig}"
    lines = [f"【{title}】"]
    lines.append(_rating_str(subject.get("rating", {})))

    # 类型信息
    typ = TYPE_MAP_REVERSE.get(subject.get("type"), "未知")
    platform = _platform_str(subject)
    eps = _eps_str(subject)
    date = _date_range_str(subject.get("infobox", []))
    parts = [typ]
    if platform and platform != "未知":
        parts.append(platform)
    if eps:
        parts.append(eps)
    if date:
        parts.append(date)
    lines.append(" · ".join(parts))

    # 制作信息
    for item in (subject.get("infobox", []) or []):
        key = item.get("key", "")
        val = item.get("value", "")
        if key in ("动画制作", "制作公司", "开发商", "出版社", "导演", "音乐", "人物设定",
                    "系列构成", "脚本", "原作", "总导演", "演出", "美术监督", "色彩设计",
                    "摄影监督", "音响监督", "剪辑"):
            lines.append(f"{key}：{val}")

    # 标签
    tags = _tags_str(subject.get("tags", []))
    if tags:
        lines.append(f"标签：{tags}")

    # 收藏统计
    col = _collection_str(subject.get("collection", {}))
    if col:
        lines.append(f"收藏：{col}")

    # 简介
    summary = (subject.get("summary") or "").strip()
    if summary:
        # 截断过长简介
        if len(summary) > 300:
            summary = summary[:300] + "……"
        lines.append("")
        lines.append(f"简介：{summary}")

    return "\n".join(lines)


def format_episodes(episodes: list, subject_title: str = "") -> str:
    if not episodes:
        return "暂无集数信息"
    # 按类型分组
    ep_types = {0: "本篇", 1: "SP", 2: "OP", 3: "ED", 4: "预告", 5: "MAD", 6: "其他"}
    groups = {}
    for ep in episodes:
        t = ep_types.get(ep.get("type", 0), "其他")
        groups.setdefault(t, []).append(ep)

    header = f"【{subject_title}】集数列表" if subject_title else "【集数列表】"
    lines = [header, ""]

    # 优先显示本篇
    for type_name in ["本篇", "SP", "OP", "ED", "其他"]:
        eps_list = groups.get(type_name, [])
        if not eps_list:
            continue
        eps_list.sort(key=lambda e: e.get("sort", e.get("ep", 0) or 0))
        lines.append(f"— {type_name}（{len(eps_list)}集）—")
        for ep in eps_list:
            num = ep.get("ep", ep.get("sort", "?"))
            name = ep.get("name_cn") or ep.get("name", "")
            airdate = ep.get("airdate", "")
            duration = ep.get("duration", "")
            desc = ep.get("desc", "")
            parts = [f"  第{num}集"]
            if name:
                parts.append(f"「{name}」")
            if airdate:
                parts.append(airdate)
            if duration:
                parts.append(f"({duration})")
            line = " ".join(parts)
            if desc:
                line += f"\n    {desc}"
            lines.append(line)
        lines.append("")

    return "\n".join(lines).rstrip()


def format_season(subjects: list, year: int, month: int) -> str:
    if not subjects:
        return f"【{year}年{month}月】暂无番剧信息"
    # 按平台分组
    groups = {}
    for s in subjects:
        p = s.get("platform", "其他")
        groups.setdefault(p, []).append(s)

    lines = [f"【{year}年{month}月新番】共 {len(subjects)} 部", ""]
    for platform in ["TV", "Web", "剧场版", "OVA", "TVSP", "DVD", "其他"]:
        eps_list = groups.get(platform, [])
        if not eps_list:
            continue
        label = PLATFORM_LABELS.get(platform, platform)
        lines.append(f"{label} 动画（{len(eps_list)}部）")
        for s in sorted(eps_list, key=lambda x: x.get("date", "")):
            title = s.get("name_cn") or s.get("name", "未知")
            score = (s.get("rating") or {}).get("score")
            score_str = f"⭐ {score}" if score else "🆕 新番"
            studio = ""
            for item in (s.get("infobox", []) or []):
                if item.get("key") in ("动画制作", "制作公司"):
                    studio = item.get("value", "")
                    break
            date = s.get("date", "") or ""
            eps = _eps_str(s)
            line = f"  {date} ┃ {title} | {score_str}"
            if studio:
                line += f" | {studio}"
            if eps:
                line += f" | {eps}"
            lines.append(line)
        lines.append("")

    return "\n".join(lines).rstrip()


def format_rank(subjects: list, subject_type: str = "anime") -> str:
    type_label = {"anime": "动画", "book": "书籍", "game": "游戏", "music": "音乐", "real": "三次元"}.get(subject_type, "")
    if not subjects:
        return f"【{type_label}排行】暂无数据"
    lines = [f"【{type_label}评分排行】Top {len(subjects)}", ""]
    for i, s in enumerate(subjects, 1):
        title = s.get("name_cn") or s.get("name", "未知")
        score = (s.get("rating") or {}).get("score")
        rank = (s.get("rating") or {}).get("rank", 0)
        total = (s.get("rating") or {}).get("total", 0)
        score_str = f"⭐ {score}" if score else "—"
        rank_str = f"#{rank}" if rank else "—"
        date = s.get("date", "") or ""
        eps = _eps_str(s)
        parts = [f"{i}. {score_str} | Rank {rank_str} | {title}（ID: {s['id']}）"]
        detail_parts = []
        if date:
            detail_parts.append(date)
        if eps:
            detail_parts.append(eps)
        if detail_parts:
            parts.append(" · ".join(detail_parts))
        lines.append("  ".join(parts))
    return "\n".join(lines)


def format_person(person: dict) -> str:
    if not person:
        return "未找到该人物"
    name = person.get("name", "未知")
    gender = {"male": "男", "female": "女"}.get(person.get("gender", ""), "")
    blood = person.get("blood_type", "")
    birth_parts = []
    if person.get("birth_year"):
        birth_parts.append(str(person["birth_year"]))
    if person.get("birth_mon"):
        birth_parts.append(f"{person['birth_mon']:02d}")
    if person.get("birth_day"):
        birth_parts.append(f"{person['birth_day']:02d}")
    birth = ".".join(birth_parts) if birth_parts else ""

    lines = [f"【{name}】"]
    info_parts = []
    if gender:
        info_parts.append(gender)
    if birth:
        info_parts.append(birth)
    if blood:
        info_parts.append(f"血型: {blood}")
    if info_parts:
        lines.append(" / ".join(info_parts))

    # infobox 信息
    for item in (person.get("infobox", []) or []):
        key = item.get("key", "")
        val = item.get("value", "")
        if key and val:
            lines.append(f"{key}：{val}")

    # 简介
    summary = (person.get("summary") or "").strip()
    if summary and len(summary) > 10:
        if len(summary) > 300:
            summary = summary[:300] + "……"
        lines.append("")
        lines.append(summary)

    return "\n".join(lines)


def format_persons(persons: list, keyword: str) -> str:
    if not persons:
        return f'【人物搜索】「{keyword}」 — 未找到结果'
    lines = [f'【人物搜索】「{keyword}」 — 找到 {len(persons)} 条', ""]
    for i, p in enumerate(persons, 1):
        name = p.get("name", "未知")
        gender = p.get("gender", "")
        birth = ""
        if p.get("birth_year") and p.get("birth_mon") and p.get("birth_day"):
            birth = f"{p['birth_year']}.{p['birth_mon']:02d}.{p['birth_day']:02d}"
        line = f"{i}. {name}（ID: {p['id']}）"
        parts = []
        if gender:
            parts.append(gender)
        if birth:
            parts.append(birth)
        if p.get("summary"):
            brief = p["summary"].strip().split("\n")[0].strip()
            if len(brief) > 60:
                brief = brief[:60] + "…"
            if brief:
                parts.append(brief)
        if parts:
            line += f" — {' / '.join(parts)}"
        lines.append(line)
    return "\n".join(lines)


def format_calendar(calendar: list) -> str:
    """格式化每日放送"""
    if not calendar:
        return "【每日放送】暂无数据"

    weekday_map = {
        1: "周一", 2: "周二", 3: "周三", 4: "周四",
        5: "周五", 6: "周六", 7: "周日"
    }

    lines = ["【每日放送】", ""]
    for day in calendar:
        weekday = day.get("weekday", {})
        wday_cn = weekday.get("cn", "")
        wday_id = weekday.get("id", 0)
        items = day.get("items", [])

        if items:
            lines.append(f"— {wday_cn} —")
            for item in items:
                title = item.get("name_cn") or item.get("name", "未知")
                eps = item.get("eps", item.get("ep", ""))
                if eps:
                    title += f" (第{eps}集)"
                lines.append(f"  {title}")
            lines.append("")

    return "\n".join(lines).rstrip()


def format_character(character: dict) -> str:
    """格式化角色详情"""
    if not character:
        return "未找到该角色"

    name = character.get("name", "未知")
    name_cn = character.get("name_cn", "")

    lines = [f"【{name}】"]
    if name_cn and name_cn != name:
        lines.append(name_cn)

    # 性别和血型
    info_parts = []
    gender = character.get("gender", "")
    if gender:
        info_parts.append(gender)
    blood_type = character.get("blood_type")
    if blood_type:
        bt = {1: "A", 2: "B", 3: "AB", 4: "O"}.get(blood_type, "")
        if bt:
            info_parts.append(f"血型: {bt}")
    if info_parts:
        lines.append(" / ".join(info_parts))

    # 生日
    birth = ""
    if character.get("birth_year"):
        birth = str(character.get("birth_year", ""))
        if character.get("birth_mon"):
            birth += f".{character['birth_mon']:02d}"
            if character.get("birth_day"):
                birth += f".{character['birth_day']:02d}"
    if birth:
        lines.append(f"生日: {birth}")

    # infobox 信息
    for item in (character.get("infobox", []) or []):
        key = item.get("key", "")
        val = item.get("value", "")
        if key and val:
            lines.append(f"{key}：{val}")

    # 简介
    summary = (character.get("summary") or "").strip()
    if summary and len(summary) > 10:
        if len(summary) > 300:
            summary = summary[:300] + "……"
        lines.append("")
        lines.append(summary)

    return "\n".join(lines)


def format_characters(characters: list, keyword: str) -> str:
    """格式化角色搜索列表"""
    if not characters:
        return f'【角色搜索】「{keyword}」 — 未找到结果'

    lines = [f'【角色搜索】「{keyword}」 — 找到 {len(characters)} 条', ""]
    for i, c in enumerate(characters, 1):
        name = c.get("name", "未知")
        name_cn = c.get("name_cn", "")
        gender = c.get("gender", "")
        summary = c.get("summary", "")

        line = f"{i}. {name}"
        if name_cn and name_cn != name:
            line += f" / {name_cn}"
        line += f"（ID: {c['id']}）"

        parts = []
        if gender:
            parts.append(gender)
        if summary:
            brief = summary.strip().split("\n")[0].strip()
            if len(brief) > 50:
                brief = brief[:50] + "…"
            if brief:
                parts.append(brief)

        if parts:
            line += f" — {' / '.join(parts)}"

        lines.append(line)

    return "\n".join(lines)


# === 命令入口 ===

def cmd_search(args):
    keyword = args.keyword
    type_val = args.type
    limit = args.limit

    # 构建搜索请求
    filter_data = {}
    if type_val and type_val in TYPE_MAP:
        filter_data["type"] = [TYPE_MAP[type_val]]

    body = {"keyword": keyword}
    if filter_data:
        body["filter"] = filter_data

    # 使用 offset 分页获取足够结果
    all_results = []
    offset = 0
    page_size = min(limit, 25)

    while len(all_results) < limit:
        # limit/offset 需要作为 query 参数传递
        resp = api_post("/search/subjects", body, params={"limit": page_size, "offset": offset})
        # POST 搜索不走缓存参数，手动缓存

        # 根据 v0.yaml，响应是 Paged_Subject 格式
        if isinstance(resp, dict):
            data = resp.get("data", [])
            total = resp.get("total", 0)
        else:
            data = []
        if not data:
            break
        all_results.extend(data)
        if len(data) < page_size or (total > 0 and offset >= total):
            break
        offset += page_size

    all_results = all_results[:limit]
    print(format_search(all_results, keyword))


def cmd_info(args):
    subject_id = args.subject_id
    cache_key = str(subject_id)
    data = api_get(f"/subjects/{subject_id}", cache_category="subject", cache_key=cache_key)
    print(format_info(data))


def cmd_episodes(args):
    subject_id = args.subject_id
    # 先获取条目标题
    subject_data = api_get(f"/subjects/{subject_id}", cache_category="subject", cache_key=f"{subject_id}_ep")
    title = subject_data.get("name_cn") or subject_data.get("name", "")

    # 获取全部集数（分页）
    all_eps = []
    offset = 0
    while True:
        data = api_get("/episodes", params={
            "subject_id": subject_id, "limit": 100, "offset": offset
        })
        if not data or not isinstance(data, dict):
            break
        ep_list = data.get("data", [])
        if not ep_list:
            break
        all_eps.extend(ep_list)
        if len(ep_list) < 100:
            break
        offset += 100

    print(format_episodes(all_eps, title))


def cmd_season(args):
    now = datetime.now()
    year = args.year or now.year
    month = args.month or ((now.month - 1) // 3 * 3 + 1)

    cache_key = f"{year}_{month}"
    data = api_get("/subjects", params={
        "type": 2, "year": year, "month": month,
        "sort": "date", "limit": 100,
    }, cache_category="season", cache_key=cache_key)

    if not isinstance(data, list):
        data = data.get("data", [])
    print(format_season(data, year, month))


def cmd_rank(args):
    subject_type = args.type or "anime"
    top = args.top
    type_id = TYPE_MAP.get(subject_type)
    if not type_id:
        print(f"❌ 未知类型: {subject_type}，可选: {', '.join(TYPE_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    cache_key = f"{subject_type}_{top}"
    data = api_get("/subjects", params={
        "type": type_id, "sort": "rank", "limit": top,
    }, cache_category="rank", cache_key=cache_key)

    if not isinstance(data, list):
        data = data.get("data", [])
    print(format_rank(data, subject_type))


def cmd_person(args):
    keyword = args.keyword
    # 先尝试搜索人物
    body = {"keyword": keyword}
    resp = api_post("/search/persons", body)
    persons = resp
    if not isinstance(persons, list):
        persons = persons.get("data", persons.get("list", []))

    if persons and len(persons) > 0:
        if len(persons) == 1:
            # 只有一个结果，直接取详情
            pid = persons[0]["id"]
            data = api_get(f"/persons/{pid}", cache_category="person", cache_key=str(pid))
            print(format_person(data))
        else:
            # 多个结果，列出
            print(format_persons(persons, keyword))
    else:
        # 搜索无结果
        print(f'【人物搜索】「{keyword}」 — 未找到结果')


def cmd_calendar(args):
    """每日放送"""
    # /calendar 是旧版 API，不在 /v0 下
    cache_key = "today"
    cached = get_cache("calendar", cache_key)
    if cached is not None:
        data = cached
    else:
        _rate_limit()
        url = "https://api.bgm.tv/calendar"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                set_cache("calendar", cache_key, data)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            print(f"❌ API 错误 {e.code}: {body[:200]}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
            sys.exit(1)

    print(format_calendar(data))


def cmd_character(args):
    keyword = args.keyword
    # 搜索角色
    body = {"keyword": keyword}
    resp = api_post("/search/characters", body)
    characters = resp
    if not isinstance(characters, list):
        characters = characters.get("data", characters.get("list", []))

    if characters and len(characters) > 0:
        if len(characters) == 1:
            # 只有一个结果，直接取详情
            cid = characters[0]["id"]
            data = api_get(f"/characters/{cid}", cache_category="character", cache_key=str(cid))
            print(format_character(data))
        else:
            # 多个结果，列出
            print(format_characters(characters, keyword))
    else:
        print(f'【角色搜索】「{keyword}」 — 未找到结果')


# === CLI ===

def main():
    parser = argparse.ArgumentParser(
        prog="bangumi",
        description="Bangumi Explorer — V1 信息查询版",
    )
    sub = parser.add_subparsers(dest="command", help="命令")

    # search
    p_search = sub.add_parser("search", help="搜索番剧/条目")
    p_search.add_argument("keyword", help="搜索关键词")
    p_search.add_argument("--type", choices=list(TYPE_MAP.keys()), default="anime", help="条目类型（默认 anime）")
    p_search.add_argument("--limit", type=int, default=10, help="返回数量（默认 10）")

    # info
    p_info = sub.add_parser("info", help="条目详情")
    p_info.add_argument("subject_id", type=int, help="条目 ID")

    # episodes
    p_eps = sub.add_parser("episodes", help="集数列表")
    p_eps.add_argument("subject_id", type=int, help="条目 ID")

    # season
    p_season = sub.add_parser("season", help="当季番表")
    p_season.add_argument("--year", type=int, default=None, help="年份（默认当年）")
    p_season.add_argument("--month", type=int, default=None, help="月份（默认当季）")

    # rank
    p_rank = sub.add_parser("rank", help="评分排行")
    p_rank.add_argument("--type", choices=list(TYPE_MAP.keys()), default="anime", help="条目类型（默认 anime）")
    p_rank.add_argument("--top", type=int, default=20, help="排行数量（默认 20）")

    # person
    p_person = sub.add_parser("person", help="查询声优/制作人员")
    p_person.add_argument("keyword", help="人物关键词")

    # calendar
    p_calendar = sub.add_parser("calendar", help="每日放送")

    # character
    p_character = sub.add_parser("character", help="查询动画角色")
    p_character.add_argument("keyword", help="角色关键词")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 启动时清理旧缓存
    clean_old_cache()

    commands = {
        "search": cmd_search,
        "info": cmd_info,
        "episodes": cmd_episodes,
        "season": cmd_season,
        "rank": cmd_rank,
        "person": cmd_person,
        "calendar": cmd_calendar,
        "character": cmd_character,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
