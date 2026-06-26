#!/usr/bin/env python3
"""
根据 profile.yaml 自动生成搜索查询列表，分为两类：

1. platform — 纯关键词，给 opencli 平台原生搜索用（微博/小红书/B站/Twitter/Reddit）
2. google   — 带日期过滤的完整查询，给 opencli google search 用

用法：
    python3 scripts/build_queries.py --date 2026-04-04 --window 3
    python3 scripts/build_queries.py --date 2026-04-04 --window 3 --json
    python3 scripts/build_queries.py --date 2026-04-04 --window 3 --type platform
    python3 scripts/build_queries.py --date 2026-04-04 --window 3 --type google

输出每行一条查询，格式：
    [priority] topic_name | 查询文本
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "SKILL.md").exists() and (candidate / "config").is_dir():
            return candidate

    return script_dir.parent


def load_profile(root: Path) -> dict:
    config_path = root / "config" / "profile.yaml"
    if not config_path.exists():
        print(f"ERROR: {config_path} 不存在，请先运行 /daily-init", file=sys.stderr)
        sys.exit(1)

    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass

    # Fallback: simple parser
    result: dict = {"topics": [], "sources": {"direct": [], "search": {"cn": [], "global": []}}, "query_profiles": []}
    text = config_path.read_text(encoding="utf-8")
    current_topic: dict | None = None
    in_keywords = False
    in_seeds = False
    in_direct = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # strip inline comments
        if " #" in stripped:
            stripped = stripped[: stripped.index(" #")].rstrip()

        indent = len(line) - len(line.lstrip())

        if stripped.startswith("- name:"):
            if current_topic:
                result["topics"].append(current_topic)
            current_topic = {
                "name": stripped.split(":", 1)[1].strip().strip("'\""),
                "priority": "medium",
                "keywords": [],
            }
            in_keywords = False
            in_seeds = False
            in_direct = False
        elif stripped.startswith("priority:") and current_topic:
            current_topic["priority"] = stripped.split(":", 1)[1].strip().strip("'\"")
        elif stripped == "keywords:":
            in_keywords = True
            in_seeds = False
            in_direct = False
        elif stripped == "search_seeds:":
            if current_topic:
                result["topics"].append(current_topic)
                current_topic = None
            in_seeds = True
            in_keywords = False
            in_direct = False
        elif stripped == "direct:":
            if current_topic:
                result["topics"].append(current_topic)
                current_topic = None
            in_direct = True
            in_keywords = False
            in_seeds = False
        elif stripped.startswith("- ") and indent >= 4:
            val = stripped[2:].strip().strip("'\"")
            if in_keywords and current_topic:
                current_topic["keywords"].append(val)
            elif in_seeds:
                result["sources"].setdefault("search_seeds", []).append(val)
            elif in_direct:
                result["sources"].setdefault("direct", []).append(val)
        elif indent < 4 and not stripped.startswith("-"):
            if in_keywords:
                in_keywords = False
            if in_seeds:
                in_seeds = False
            if in_direct:
                in_direct = False
            if current_topic and not stripped.startswith("priority:"):
                result["topics"].append(current_topic)
                current_topic = None

    if current_topic:
        result["topics"].append(current_topic)

    return result


def build_date_range(date_str: str, window: int) -> tuple[str, str]:
    """Returns (start_iso, end_iso)."""
    end = datetime.strptime(date_str, "%Y-%m-%d")
    start = end - timedelta(days=window - 1)
    start_iso = start.strftime("%Y-%m-%d")
    end_iso = end.strftime("%Y-%m-%d")
    return start_iso, end_iso


def _is_cn(text: str) -> bool:
    """判断文本是否以中文为主。"""
    return any("\u4e00" <= c <= "\u9fff" for c in text)


def _split_keywords(keywords) -> tuple[list[str], list[str]]:
    """
    将关键词分为中文和英文两组。
    支持两种格式：
    - 新格式 dict: {"cn": [...], "en": [...]}
    - 旧格式 list: ["中文", "English", ...] （按语言自动分）
    """
    if isinstance(keywords, dict):
        cn_kws = keywords.get("cn", []) or []
        en_kws = keywords.get("en", []) or []
        return cn_kws, en_kws

    # 旧格式：扁平列表，按语言自动分
    cn_kws = []
    en_kws = []
    for kw in (keywords or []):
        if _is_cn(kw):
            cn_kws.append(kw)
        else:
            en_kws.append(kw)
    return cn_kws, en_kws


def generate_platform_queries(
    profile: dict, date_str: str, window: int
) -> list[tuple[str, str, str]]:
    """
    生成平台原生搜索用的纯关键词查询（不带日期），按 cn/en 分组。
    返回 (priority, topic_name, keyword) 元组列表。
    priority 带语言前缀：如 "high-cn", "high-en", "medium-cn" 等。
    """
    cn_queries: list[tuple[str, str, str]] = []
    en_queries: list[tuple[str, str, str]] = []

    topics = profile.get("topics", [])
    priority_order = {"high": 0, "medium": 1, "low": 2}
    topics_sorted = sorted(
        topics, key=lambda t: priority_order.get(t.get("priority", "medium"), 1)
    )

    for topic in topics_sorted:
        name = topic.get("name", "")
        priority = topic.get("priority", "medium")
        keywords = topic.get("keywords", [])
        if not name:
            continue

        cn_kws, en_kws = _split_keywords(keywords)

        # topic 名称：按语言判断放哪边
        if _is_cn(name):
            cn_queries.append((priority, name, name))
        else:
            en_queries.append((priority, name, name))

        # 中文关键词（给微博/小红书/B站）
        kw_limit = {"high": len(cn_kws), "medium": 3, "low": 1}.get(priority, 1)
        for kw in cn_kws[:kw_limit]:
            if kw != name:
                cn_queries.append((priority, name, kw))

        # 中文组合（仅 high）
        if priority == "high" and len(cn_kws) >= 2:
            cn_queries.append((priority, name, f"{cn_kws[0]} {cn_kws[1]}"))

        # 英文关键词（给 Twitter/Reddit）
        kw_limit_en = {"high": len(en_kws), "medium": 3, "low": 1}.get(priority, 1)
        for kw in en_kws[:kw_limit_en]:
            if kw != name:
                en_queries.append((priority, name, kw))

        # 英文组合（仅 high）
        if priority == "high" and len(en_kws) >= 2:
            en_queries.append((priority, name, f"{en_kws[0]} {en_kws[1]}"))

    # 去重
    def _dedup(queries):
        seen: set[str] = set()
        result = []
        for p, t, q in queries:
            if q not in seen:
                seen.add(q)
                result.append((p, t, q))
        return result

    # 加语言前缀后合并
    result = []
    for p, t, q in _dedup(cn_queries):
        result.append((f"{p}-cn", t, q))
    for p, t, q in _dedup(en_queries):
        result.append((f"{p}-en", t, q))
    return result


def generate_google_queries(
    profile: dict, date_str: str, window: int
) -> list[tuple[str, str, str]]:
    """
    生成 Google 搜索用的查询（带日期过滤 + site: 定向）。
    返回 (priority, topic_name, query) 元组列表。
    """
    start_iso, end_iso = build_date_range(date_str, window)
    queries: list[tuple[str, str, str]] = []

    topics = profile.get("topics", [])
    priority_order = {"high": 0, "medium": 1, "low": 2}
    topics_sorted = sorted(
        topics, key=lambda t: priority_order.get(t.get("priority", "medium"), 1)
    )

    # Per-topic Google queries
    for topic in topics_sorted:
        name = topic.get("name", "")
        priority = topic.get("priority", "medium")
        keywords = topic.get("keywords", [])
        if not name:
            continue

        cn_kws, en_kws = _split_keywords(keywords)

        # topic 名称 + after:
        queries.append((priority, name, f"{name} after:{start_iso}"))

        # 中文关键词组合 + after:
        if len(cn_kws) >= 2:
            queries.append((priority, name, f"{cn_kws[0]} {cn_kws[1]} after:{start_iso}"))

        # 英文关键词组合 + after:
        if en_kws:
            en_combo = " ".join(en_kws[:3])
            queries.append((priority, name, f"{en_combo} after:{start_iso}"))

        # 单个中文关键词 + after:（high 全部，medium 前 2，low 前 1）
        kw_limit = {"high": len(cn_kws), "medium": 2, "low": 1}.get(priority, 1)
        for kw in cn_kws[:kw_limit]:
            queries.append((priority, name, f"{kw} after:{start_iso}"))

        # 交叉：topic名 + 英文keyword + after:（仅 high）
        if priority == "high":
            for kw in en_kws[:3]:
                if kw != name:
                    queries.append((priority, name, f"{name} {kw} after:{start_iso}"))

    # site: 定向搜索（从 sources 中提取域名）
    sources = profile.get("sources", {})

    # 从 cn/global 结构化来源中提取 URL
    for region_key in ("cn", "global"):
        region_sources = sources.get(region_key, [])
        if not isinstance(region_sources, list):
            continue
        for src in region_sources:
            if not isinstance(src, dict):
                continue
            url = src.get("url", "")
            src_keywords = src.get("keywords", [])
            if not url:
                continue
            # 提取域名
            domain = url.replace("https://", "").replace("http://", "").split("/")[0]
            if domain.startswith("www."):
                domain = domain[4:]
            # 用该来源的关键词做 site: 搜索
            for kw in src_keywords[:3]:
                queries.append(("site", src.get("name", domain), f"site:{domain} {kw} after:{start_iso}"))

    # 从 direct 列表中提取
    direct_cfg = sources.get("direct", {})
    if isinstance(direct_cfg, dict):
        for url in direct_cfg.get("cn", []) or []:
            queries.append(("direct-cn", "国内直抓来源", f"FETCH {url}"))
        for url in direct_cfg.get("global", []) or []:
            queries.append(("direct-global", "海外直抓来源", f"FETCH {url}"))
    elif isinstance(direct_cfg, list):
        for url in direct_cfg:
            queries.append(("direct", "直抓来源", f"FETCH {url}"))

    # Search seeds
    search_cfg = sources.get("search", {}) if isinstance(sources.get("search"), dict) else {}
    for seed in search_cfg.get("cn", []) or []:
        queries.append(("seed-cn", "国内搜索种子", f"{seed} after:{start_iso}"))
    for seed in search_cfg.get("global", []) or []:
        queries.append(("seed-global", "海外搜索种子", f"{seed} after:{start_iso}"))
    for seed in sources.get("search_seeds", []) or []:
        if _is_cn(seed):
            queries.append(("seed-cn", "国内搜索种子", f"{seed} after:{start_iso}"))
        else:
            queries.append(("seed-global", "海外搜索种子", f"{seed} after:{start_iso}"))

    # Per-topic query profiles
    for qp in profile.get("query_profiles", []):
        topic_name = qp.get("topic", "话题")
        for seed in qp.get("cn", []) or []:
            queries.append(("profile-cn", topic_name, f"{seed} after:{start_iso}"))
        for seed in qp.get("global", []) or []:
            queries.append(("profile-global", topic_name, f"{seed} after:{start_iso}"))

    # 综合聚合查询
    role = profile.get("role", "")
    if role:
        queries.append(("extra", "综合", f"{role} 行业动态 after:{start_iso}"))
        queries.append(("extra", "综合", f"{role} 新闻 最新发布 after:{start_iso}"))

    high_names = [t["name"] for t in topics_sorted if t.get("priority") == "high"]
    if len(high_names) >= 2:
        queries.append(("extra", "综合", f"{' '.join(high_names[:3])} 最新动态 after:{start_iso}"))

    # 去重
    seen: set[str] = set()
    deduped: list[tuple[str, str, str]] = []
    for p, t, q in queries:
        if q not in seen:
            seen.add(q)
            deduped.append((p, t, q))
    return deduped


def format_output(
    queries: list[tuple[str, str, str]],
    query_type: str,
    date_str: str,
    window: int,
    as_json: bool,
) -> str:
    if as_json:
        import json
        output = [
            {"priority": p, "topic": t, "query": q, "type": query_type}
            for p, t, q in queries
        ]
        return json.dumps(output, ensure_ascii=False, indent=2)
    else:
        lines = [
            f"# 日报搜索查询（{query_type}）— {date_str}（窗口 {window} 天）",
            f"# 共 {len(queries)} 条查询\n",
        ]
        current_section = None
        for priority, topic, query in queries:
            section = f"[{priority}] {topic}"
            if section != current_section:
                lines.append(f"\n## {section}")
                current_section = section
            lines.append(f"  {query}")
        return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="根据 profile.yaml 生成搜索查询列表（分 platform 和 google 两类）"
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="目标日期，格式 YYYY-MM-DD（默认今天）",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="时间窗口天数（默认 3）",
    )
    parser.add_argument(
        "--type",
        choices=["all", "platform", "google"],
        default="all",
        help="输出类型：all=两种都输出，platform=仅平台关键词，google=仅Google查询（默认 all）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存查询结果到 output/raw/{date}_queries.txt（默认保存）",
    )
    args = parser.parse_args()

    root = resolve_root_dir()
    profile = load_profile(root)

    outputs = []

    if args.type in ("all", "platform"):
        platform_queries = generate_platform_queries(profile, args.date, args.window)
        text = format_output(platform_queries, "platform", args.date, args.window, args.json)
        outputs.append(text)
        print(text)

    if args.type == "all":
        sep = "\n" + "=" * 60 + "\n"
        outputs.append(sep)
        print(sep)

    if args.type in ("all", "google"):
        google_queries = generate_google_queries(profile, args.date, args.window)
        text = format_output(google_queries, "google", args.date, args.window, args.json)
        outputs.append(text)
        print(text)

    if not args.no_save:
        raw_dir = root / "output" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        save_path = raw_dir / f"{args.date}_queries.txt"
        save_path.write_text("\n".join(outputs), encoding="utf-8")
        print(f"\n# 已保存到 {save_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
