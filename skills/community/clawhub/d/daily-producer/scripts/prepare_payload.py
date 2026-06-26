#!/usr/bin/env python3
"""
从 detail.txt 解析、去重、打分、排序，输出结构化候选 JSON。
AI 只需在此基础上补写 summary/relevance/sidebar。

流程：
  detail.txt → 解析 → 去重 → 过滤噪音 → 打分排序 → 聚合多源 → candidates.json

用法：
    python3 scripts/prepare_payload.py --date 2026-04-05
    python3 scripts/prepare_payload.py --date 2026-04-05 --top 15
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict
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
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if (c / "SKILL.md").exists() and (c / "config").is_dir():
            return c
    return script_dir.parent


def load_profile(root: Path) -> dict:
    config_path = root / "config" / "profile.yaml"
    if not config_path.exists():
        return {}
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        return {}


def get_all_keywords(profile: dict) -> set[str]:
    """从 profile 提取所有关键词（cn + en），转小写用于匹配。"""
    keywords = set()
    for topic in profile.get("topics", []):
        kws = topic.get("keywords", {})
        if isinstance(kws, dict):
            for kw in kws.get("cn", []) or []:
                keywords.add(kw.lower())
            for kw in kws.get("en", []) or []:
                keywords.add(kw.lower())
        elif isinstance(kws, list):
            for kw in kws:
                keywords.add(kw.lower())
    return keywords


def get_exclude_patterns(profile: dict) -> list[str]:
    """从 profile 提取排除话题。"""
    return [t.lower() for t in profile.get("exclude_topics", [])]


# ━━ 解析 detail.txt ━━

def parse_detail(text: str) -> list[dict]:
    """解析 detail.txt 为结构化列表。"""
    items = []
    current: dict | None = None

    for line in text.splitlines():
        if line.startswith("--- ["):
            if current:
                items.append(current)
            m = re.match(r"--- \[(.+?)\] \((.+?)\) ---", line)
            current = {
                "platform": m.group(1) if m else "",
                "region": m.group(2) if m else "",
                "fields": {},
                "content": "",
            }
        elif current is not None:
            if line.startswith("type:"):
                current["fields"]["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("keyword:"):
                current["fields"]["keyword"] = line.split(":", 1)[1].strip()
            elif line.startswith("title:"):
                current["fields"]["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("fetch_status:"):
                current["fields"]["fetch_status"] = line.split(":", 1)[1].strip()
            elif re.match(r"^\w[\w_]*:", line) and ":" in line:
                key, val = line.split(":", 1)
                current["fields"][key.strip()] = val.strip()
            elif line.startswith("      ") and ":" in line[:30]:
                m2 = re.match(r"^\s+(\w[\w_]*):\s*(.*)", line)
                if m2:
                    current["fields"][m2.group(1)] = m2.group(2).strip()
            elif line.startswith("fetched_content:"):
                current["fields"]["has_fetched_content"] = True
            elif current.get("fields", {}).get("has_fetched_content"):
                current["content"] += line + "\n"
            # 正文续行（多行推文等，不匹配任何已知格式的非空行）
            elif line.strip() and not line.startswith("---") and not line.startswith("#") and not line.startswith("="):
                # 追加到 text 字段
                existing_text = current["fields"].get("text", "")
                if existing_text:
                    current["fields"]["text"] = existing_text + "\n" + line.strip()
                else:
                    current["fields"]["text"] = line.strip()

    if current:
        items.append(current)

    return items


# ━━ 去重 ━━

def normalize_title(title: str) -> str:
    """标准化标题用于去重匹配。"""
    t = title.lower().strip()
    # 去掉 emoji、标点、多余空格
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t[:100]  # 取前 100 字符


def deduplicate(items: list[dict]) -> list[dict]:
    """
    去重：同一事件在多平台出现时，合并为一条，记录多源。
    用标题相似度判断（简单版：标准化后前 50 字符相同视为同一事件）。
    """
    groups: dict[str, list[dict]] = defaultdict(list)

    for item in items:
        title = item["fields"].get("title", "")
        key = normalize_title(title)[:50]
        if not key:
            key = item["fields"].get("url", str(id(item)))
        groups[key].append(item)

    deduped = []
    for key, group in groups.items():
        # 取热度最高的作为主条目
        primary = max(group, key=lambda x: parse_hot(x["fields"].get("hot", "0")))

        # 记录多源
        sources = []
        for item in group:
            sources.append({
                "platform": item["platform"],
                "url": item["fields"].get("url", ""),
                "hot": item["fields"].get("hot", ""),
                "author": item["fields"].get("author", ""),
            })

        primary["sources"] = sources
        primary["cross_refs"] = len(group)
        deduped.append(primary)

    return deduped


# ━━ 过滤噪音 ━━

def is_specific_keyword(kw: str) -> bool:
    """
    判断关键词是否为「具体关键词」。
    具体关键词 = 长度 > 3 的英文词组、含中文的词、或含大写字母的品牌名。
    泛义关键词 = 短的常见英文单词如 agent, model, tool, product。
    """
    # 含中文 → 具体（如"智能体"、"大模型"）
    if any("\u4e00" <= c <= "\u9fff" for c in kw):
        return True
    # 含大写字母（品牌名如 OpenAI, Claude, Cursor）
    if any(c.isupper() for c in kw) and len(kw) > 2:
        return True
    # 多个单词的英文短语（如 "AI coding", "large language model"）
    if " " in kw.strip():
        return True
    # 单个英文词且长��� <= 8 → 泛义（agent, model, tool, product, release...）
    if len(kw) <= 8:
        return False
    return True


def count_keyword_matches(text: str, all_keywords: set[str]) -> tuple[int, int]:
    """
    返回 (总命中数, 具体关键词命中数)。
    具体关键词 = 品牌名/中文词/多词短语。
    """
    text_lower = text.lower()
    total = 0
    specific = 0
    for kw in all_keywords:
        if kw.lower() in text_lower:
            total += 1
            if is_specific_keyword(kw):
                specific += 1
    return total, specific


def is_noise(item: dict, exclude_patterns: list[str], all_keywords: set[str]) -> bool:
    """
    基于 profile 关键词匹配度判断是否为噪音。不使用硬编码黑名单，完全通用。

    规则：
    1. 标题为空 -> 噪音
    2. 命中 profile 排除话题 -> 噪音
    3. 网站类条目（region=website）-> 不过滤（Google site: 搜索自带相关性过滤）
    4. 平台搜索结果（有 keyword）-> 宽松：搜索词本身来自 profile，信任搜索相关性
       只过滤：搜索词在内容里都找不到 且 0 个 profile 关键词命中
    5. 热门/趋势类（无 keyword）-> 严格：至少命中 2 个关键词，或 1 个具体关键词
    """
    title = item["fields"].get("title", "")
    text = item["fields"].get("text", "")
    full_text = (title + " " + text)
    keyword = item["fields"].get("keyword", "")
    region = item.get("region", "")

    # 标题为空
    if not title.strip():
        return True

    # profile 排除话题
    full_text_lower = full_text.lower()
    for exc in exclude_patterns:
        if exc in full_text_lower:
            return True

    # 网站类条目（Google site: 搜索来的）直接保留
    if region == "website":
        return False

    total_matches, specific_matches = count_keyword_matches(full_text, all_keywords)

    # 平台搜索结果（有搜索关键词）— 宽松
    if keyword and keyword != "(none)":
        # 搜索词本身来自 profile，有基本相关性
        # 只过滤：搜索词在内容里都找不到 且 0 个关键词命中
        search_word_in_text = keyword.lower() in full_text_lower
        if search_word_in_text or total_matches >= 1:
            return False
        return True

    # 热门/趋势类（无搜索关键词）— 严格
    if specific_matches >= 1 or total_matches >= 2:
        return False
    return True



# ━━ 打分 ━━

def parse_hot(hot_str: str) -> float:
    """将各平台的热度值统一为数字。"""
    if not hot_str:
        return 0
    # 去掉非数字字符（如 "137,010 views" → 137010）
    cleaned = re.sub(r"[^\d.]", "", str(hot_str).replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return 0


def get_tier1_sources(profile: dict) -> set[str]:
    """从 profile 的 sources.websites 动态提取 tier-1 来源名，加上通用权威平台。"""
    tier1: set[str] = {"Twitter/X", "微博"}  # 通用高质量社交信号
    sources = profile.get("sources", {})
    for group in (sources.get("websites", {}).get("cn", []),
                  sources.get("websites", {}).get("global", [])):
        for site in group:
            name = site.get("name", "")
            if name:
                tier1.add(name)
    return tier1


def score_item(item: dict, all_keywords: set[str], tier1: set[str] | None = None) -> float:
    """
    给条目打分。得分 = 热度分 + 关键词匹配分 + 多源分 + 来源可信度分。
    """
    score = 0.0

    # 1. 热度分（归一化到 0-50）
    hot = parse_hot(item["fields"].get("hot", "0"))
    if hot > 0:
        score += min(50, math.log10(hot + 1) * 10)

    # 2. 关键词匹配分（每命中一个 +5，最高 30）
    title = (item["fields"].get("title", "") + " " + item["fields"].get("text", "")).lower()
    matches = sum(1 for kw in all_keywords if kw in title)
    score += min(30, matches * 5)

    # 3. 多源分（跨平台提及 +10/次，最高 20）
    cross_refs = item.get("cross_refs", 1)
    score += min(20, (cross_refs - 1) * 10)

    # 4. 来源可信度加分（从 profile 动态读取，非硬编码）
    if tier1 and item["platform"] in tier1:
        score += 5

    return round(score, 1)


# ━━ 聚合输出 ━━

def _looks_like_web_read_wrapper(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    return text.startswith("web/read") or "1 items ·" in text or "│ Title" in text


def _clean_fetched_content(content: str) -> str:
    """清洗 fetched_content，去掉 opencli 包装噪音，保留正文。"""
    content = (content or "").strip()
    if not content:
        return ""

    lines = []
    for line in content.splitlines():
        s = line.rstrip()
        if not s.strip():
            lines.append("")
            continue
        if s.strip().startswith("web/read"):
            continue
        if " items ·" in s and "web/read" in s:
            continue
        if "│ Title" in s or "┌" in s or "└" in s or "├" in s or "┬" in s or "┴" in s or "┼" in s:
            continue
        lines.append(s)

    return "\n".join(lines).strip()



def format_candidate(item: dict, rank: int) -> dict:
    """格式化单条候选为 JSON 结构。"""
    fields = item["fields"]
    raw_fetched_content = item.get("content", "")
    fetched_content = _clean_fetched_content(raw_fetched_content)
    raw_text = fields.get("text", "")
    text = raw_text
    if _looks_like_web_read_wrapper(raw_text) and fetched_content:
        text = fetched_content
    elif _looks_like_web_read_wrapper(raw_text):
        text = ""
    elif not text and fetched_content:
        text = fetched_content

    has_fetched_content = bool(fetched_content or raw_fetched_content.strip())

    return {
        "id": f"candidate-{rank}",
        "rank": rank,
        "score": item.get("_score", 0),
        "title": fields.get("title", ""),
        "text": text,
        "platform": item["platform"],
        "region": item["region"],
        "author": fields.get("author", ""),
        "time": fields.get("time", ""),
        "time_parsed": fields.get("time_parsed", ""),
        "url": fields.get("url", ""),
        "hot": fields.get("hot", ""),
        "keyword": fields.get("keyword", ""),
        "subreddit": fields.get("subreddit", ""),
        "snippet": fields.get("snippet", ""),
        "summary": fields.get("summary", ""),
        "has_fetched_content": has_fetched_content,
        "fetched_content": fetched_content,
        # 以下字段留给 AI 填写
        "ai_summary": {"what_happened": "", "why_it_matters": ""},
        "ai_relevance": "",
        "ai_priority": "",
        "ai_tags": [],
    }


# ━━ 主流程 ━━

def _normalize_tag(tag: str) -> str:
    """去掉 # 前缀并转小写，用于统一 feedback tag 匹配格式。"""
    return tag.lstrip("#").lower()


def load_feedback_boost(root: Path, date: str) -> dict[str, float]:
    """
    读取最近 3 天内最新的 feedback JSON，提取 voted 文章的 tags 和 top_interests，
    返回 {keyword_lower: boost_score} 字典，用于在打分时加权。
    """
    try:
        base = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {}
    fb_path = None
    for days_back in range(1, 4):
        candidate = root / "data" / "feedback" / f"{(base - timedelta(days=days_back)).strftime('%Y-%m-%d')}.json"
        if candidate.exists():
            fb_path = candidate
            break
    if fb_path is None:
        return {}
    try:
        data = json.loads(fb_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    boost: dict[str, float] = {}
    for session in data.get("sessions", []):
        explicit = session.get("explicit_feedback", {})
        # voted 文章的 tags: +15
        for article in explicit.get("voted", []):
            for tag in article.get("tags", []):
                key = _normalize_tag(tag)
                boost[key] = boost.get(key, 0) + 15
        # top_interests: +8
        for tag in session.get("interest_profile", {}).get("top_interests", []):
            key = _normalize_tag(tag)
            boost[key] = boost.get(key, 0) + 8
        # tags_followed: +10
        for tag in explicit.get("tags_followed", []):
            key = _normalize_tag(tag)
            boost[key] = boost.get(key, 0) + 10

    return boost


def main() -> None:
    parser = argparse.ArgumentParser(description="从 detail.txt 生成结构化候选 JSON")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="目标日期")
    parser.add_argument("--top", type=int, default=0, help="保留前 N 条候选，0=全部保留（默认全部）")
    parser.add_argument("--no-save", action="store_true", help="不保存结果")
    parser.add_argument("--no-feedback", action="store_true", help="不读取历史 feedback 加权")
    args = parser.parse_args()

    root = resolve_root_dir()

    # 读取 detail.txt
    detail_path = root / "output" / "raw" / f"{args.date}_detail.txt"
    if not detail_path.exists():
        print(f"ERROR: {detail_path} 不存在", file=sys.stderr)
        sys.exit(1)

    text = detail_path.read_text(encoding="utf-8")
    profile = load_profile(root)
    all_keywords = get_all_keywords(profile)
    exclude_patterns = get_exclude_patterns(profile)
    tier1 = get_tier1_sources(profile)

    # 读取历史 feedback boost
    feedback_boost: dict[str, float] = {}
    if not args.no_feedback:
        feedback_boost = load_feedback_boost(root, args.date)
        if feedback_boost:
            print(f"Feedback boost: {len(feedback_boost)} 个标签加权（来自前一天反馈）", file=sys.stderr)
        else:
            print("Feedback boost: 无历史反馈数据", file=sys.stderr)

    # 1. 解析
    items = parse_detail(text)
    print(f"解析: {len(items)} 条", file=sys.stderr)

    # 2. 过滤噪音
    before_noise = len(items)
    items = [item for item in items if not is_noise(item, exclude_patterns, all_keywords)]
    print(f"过滤噪音: {before_noise} → {len(items)} 条（移除 {before_noise - len(items)} 条）", file=sys.stderr)

    # 3. 打分排序（不去重，多源出现 = 更可靠）
    for item in items:
        base_score = score_item(item, all_keywords, tier1)
        # feedback boost：title/text 命中 boost 标签则加分
        if feedback_boost:
            title = (item["fields"].get("title", "") + " " + item["fields"].get("text", "")).lower()
            fb_bonus = sum(v for k, v in feedback_boost.items() if k in title)
            item["_score"] = round(base_score + min(fb_bonus, 30), 1)  # boost 上限 30
        else:
            item["_score"] = base_score
    items.sort(key=lambda x: x["_score"], reverse=True)

    # 4. 取 top N（0=全部保留）
    top_items = items[:args.top] if args.top > 0 else items
    print(f"保留: {len(top_items)} 条", file=sys.stderr)

    # 6. 格式化输出
    candidates = []
    for i, item in enumerate(top_items, 1):
        candidates.append(format_candidate(item, i))

    output = {
        "meta": {
            "date": args.date,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_parsed": before_noise,
            "after_noise_filter": len(items),
            "top_n": len(top_items),
            "role": profile.get("role", ""),
        },
        "candidates": candidates,
        "ai_todo": {
            "instruction": "请为每条候选填写 ai_summary、ai_relevance、ai_priority、ai_tags。然后从中选出 target_items 条生成最终日报 JSON。",
            "target_items": profile.get("daily", {}).get("target_items", 15),
            "profile_role": profile.get("role", ""),
            "profile_context": profile.get("role_context", ""),
        },
    }

    output_json = json.dumps(output, ensure_ascii=False, indent=2)

    if not args.no_save:
        save_path = root / "output" / "raw" / f"{args.date}_candidates.json"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(output_json, encoding="utf-8")
        print(f"\n已保存到 {save_path}", file=sys.stderr)

    # 打印摘要
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"候选 Top {len(top_items)} 条:", file=sys.stderr)
    for c in candidates[:20]:
        score = c["score"]
        title = c["title"][:60]
        platform = c["platform"]
        hot = c["hot"]
        print(f"  [{c['rank']:2d}] {score:5.1f}分 | {platform:8s} | hot:{str(hot):>8s} | {title}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)


if __name__ == "__main__":
    main()
