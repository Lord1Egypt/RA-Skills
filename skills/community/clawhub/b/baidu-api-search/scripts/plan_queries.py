#!/usr/bin/env python3
"""Create a deterministic, budget-aware Baidu research query plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


MODE_LIMITS = {
    "fast": 1,
    "normal": 12,
    "deep": 30,
}


MODE_STRATEGY = {
    "fast": {
        "initial_queries": 1,
        "default_top_k": 10,
        "min_unique_yield": 0.35,
        "low_yield_patience": 1,
        "second_pass_terms": 0,
    },
    "normal": {
        "initial_queries": 3,
        "default_top_k": 20,
        "min_unique_yield": 0.25,
        "low_yield_patience": 2,
        "second_pass_terms": 0,
    },
    "deep": {
        "initial_queries": 5,
        "default_top_k": 30,
        "min_unique_yield": 0.18,
        "low_yield_patience": 3,
        "second_pass_terms": 5,
    },
}


# pattern, intent, stage, priority, reason
BASE_TEMPLATES = [
    ("{topic}", "overview", "seed", 10, "baseline query"),
    ("{topic} 评测", "review", "seed", 20, "reviews and evaluations"),
    ("{topic} 缺点", "complaint", "seed", 30, "negative experiences and drawbacks"),
    ("{topic} 官网", "official", "coverage", 35, "official or primary source"),
    ("{topic} 怎么样", "review", "coverage", 55, "general user opinions"),
    ("{topic} 论坛", "forum", "coverage", 65, "forum discussions"),
    ("{topic} 对比", "comparison", "coverage", 75, "comparison content"),
    ("{topic} 售后", "service", "coverage", 85, "service and support reports"),
    ("{topic} 问题", "complaint", "coverage", 95, "known issues"),
    ("{topic} 知乎", "platform", "platform", 115, "Zhihu results"),
    ("{topic} 贴吧", "platform", "platform", 120, "Tieba results"),
    ("{topic} 小红书", "platform", "platform", 125, "Xiaohongshu results"),
    ("{topic} B站", "platform", "platform", 130, "Bilibili results"),
    ("{topic} 微博", "platform", "platform", 135, "Weibo results"),
    ("{topic} 真实体验", "experience", "coverage", 140, "first-hand user experience"),
    ("{topic} 优点", "review", "coverage", 150, "positive experiences"),
    ("{topic} 价格", "price", "coverage", 160, "pricing and purchase context"),
    ("{topic} 故障", "complaint", "coverage", 170, "failure reports"),
]


PRODUCT_TEMPLATES = [
    ("{topic} 车主", "experience", "coverage", 40, "owner reports"),
    ("{topic} 质量", "complaint", "coverage", 45, "quality reports"),
    ("{topic} 价格", "price", "coverage", 50, "pricing and purchase context"),
    ("{topic} 配置", "spec", "coverage", 90, "configuration and specs"),
    ("{topic} 通病", "complaint", "coverage", 100, "common defects"),
    ("{topic} 保养", "service", "coverage", 105, "maintenance cost and service"),
    ("{topic} 油耗", "spec", "coverage", 145, "fuel consumption reports"),
    ("{topic} 续航", "spec", "coverage", 146, "range reports"),
    ("{topic} 二手", "market", "coverage", 155, "used market signals"),
    ("{topic} 保值率", "market", "coverage", 156, "resale value"),
]


EVENT_TEMPLATES = [
    ("{topic} 最新", "freshness", "seed", 15, "recent updates"),
    ("{topic} 官方通报", "official", "coverage", 25, "official notices"),
    ("{topic} 时间线", "timeline", "coverage", 45, "event timeline"),
    ("{topic} 后续", "freshness", "coverage", 60, "follow-up reports"),
    ("{topic} 争议", "controversy", "coverage", 70, "controversies"),
    ("{topic} 原因", "analysis", "coverage", 100, "cause analysis"),
    ("{topic} 影响", "analysis", "coverage", 110, "impact analysis"),
]


PROJECT_TEMPLATES = [
    ("{topic} 文档", "docs", "seed", 25, "documentation"),
    ("{topic} GitHub", "code", "coverage", 40, "GitHub sources"),
    ("{topic} issue", "code", "coverage", 50, "issue trackers"),
    ("{topic} bug", "bug", "coverage", 60, "bug reports"),
    ("{topic} 教程", "tutorial", "coverage", 80, "tutorials"),
    ("{topic} 替代", "comparison", "coverage", 100, "alternatives"),
]


def detect_profile(topic: str) -> str:
    lower = topic.lower()
    if re.search(r"(api|github|mcp|skill|python|golang|js|node|bug|项目|仓库|接口|文档)", lower):
        return "project"
    if re.search(r"(事件|通报|事故|案件|争议|政策|新闻|最新)", topic):
        return "event"
    if re.search(r"(\d|pro|max|plus|车|摩托|手机|电脑|相机|耳机|车型|发动机)", topic):
        return "product"
    return "general"


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.strip())


def unique_queries(items: Iterable[dict]) -> list[dict]:
    seen = set()
    output = []
    for item in items:
        query = normalize_query(item["query"])
        key = query.casefold()
        if not query or key in seen:
            continue
        seen.add(key)
        item = dict(item)
        item["query"] = query
        output.append(item)
    return output


def select_first(items: list[dict], selected: list[dict], predicate) -> None:
    selected_keys = {item["query"].casefold() for item in selected}
    for item in items:
        if item["query"].casefold() not in selected_keys and predicate(item):
            selected.append(item)
            return


def intent_is(name: str):
    return lambda item: item.get("intent") == name


def query_has(text: str):
    return lambda item: text in item.get("query", "")


def render_query(topic: str, pattern: str) -> str:
    prefix = "{topic} "
    if pattern.startswith(prefix):
        suffix = pattern[len(prefix) :].strip()
        if suffix and suffix.casefold() in topic.casefold():
            return topic
    return pattern.format(topic=topic)


def select_diverse_queries(items: list[dict], mode: str, profile: str, limit: int) -> list[dict]:
    """Select queries by coverage slots instead of only priority truncation."""
    ordered = unique_queries(sorted(items, key=lambda item: (item["priority"], item["order"])))
    if mode == "fast":
        return ordered[:limit]

    selected: list[dict] = []
    core_slots_by_profile = {
        "product": [
            intent_is("overview"),
            intent_is("review"),
            intent_is("complaint"),
            intent_is("official"),
        ],
        "event": [
            intent_is("overview"),
            intent_is("freshness"),
            intent_is("official"),
            intent_is("timeline"),
        ],
        "project": [
            intent_is("overview"),
            intent_is("docs"),
            intent_is("code"),
            intent_is("bug"),
            intent_is("official"),
        ],
        "general": [
            intent_is("overview"),
            intent_is("review"),
            intent_is("complaint"),
            intent_is("official"),
        ],
    }
    profile_slots = {
        "product": [
            intent_is("platform"),
            intent_is("platform"),
            intent_is("forum"),
            intent_is("experience"),
            query_has("质量"),
            intent_is("price"),
            intent_is("comparison"),
            intent_is("spec"),
            intent_is("service"),
            intent_is("market"),
        ],
        "event": [
            intent_is("freshness"),
            intent_is("platform"),
            intent_is("platform"),
            intent_is("timeline"),
            intent_is("controversy"),
            intent_is("analysis"),
        ],
        "project": [
            intent_is("docs"),
            intent_is("code"),
            intent_is("bug"),
            intent_is("official"),
            intent_is("platform"),
            intent_is("tutorial"),
            intent_is("comparison"),
        ],
        "general": [
            intent_is("platform"),
            intent_is("platform"),
            intent_is("forum"),
            intent_is("experience"),
            intent_is("comparison"),
            intent_is("price"),
        ],
    }

    core_slots = core_slots_by_profile.get(profile, core_slots_by_profile["general"])
    for slot in core_slots + profile_slots.get(profile, profile_slots["general"]):
        if len(selected) >= limit:
            break
        select_first(ordered, selected, slot)

    for item in ordered:
        if len(selected) >= limit:
            break
        if item["query"].casefold() not in {selected_item["query"].casefold() for selected_item in selected}:
            selected.append(item)
    return selected[:limit]


def make_item(topic: str, template: tuple[str, str, str, int, str], source: str, order: int) -> dict:
    pattern, intent, stage, priority, reason = template
    return {
        "query": render_query(topic, pattern),
        "intent": intent,
        "stage": stage,
        "priority": priority,
        "order": order,
        "source": source,
        "reason": reason,
    }


def load_extra_terms(path: str | None) -> list[str]:
    if not path:
        return []
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, list):
        return [str(item).strip() for item in data if str(item).strip()]
    if isinstance(data, dict):
        terms = data.get("terms", [])
        return [str(item).strip() for item in terms if str(item).strip()]
    raise ValueError("--extra-terms must point to a JSON list or {'terms': [...]}")


def build_candidates(topic: str, profile: str) -> list[dict]:
    templates = list(BASE_TEMPLATES)
    if profile == "product":
        templates.extend(PRODUCT_TEMPLATES)
    elif profile == "event":
        templates.extend(EVENT_TEMPLATES)
    elif profile == "project":
        templates.extend(PROJECT_TEMPLATES)
    return [make_item(topic, template, "template", order) for order, template in enumerate(templates)]


def build_plan(topic: str, mode: str, max_queries: int | None, extra_terms: list[str]) -> dict:
    profile = detect_profile(topic)
    items = build_candidates(topic, profile)
    for offset, term in enumerate(extra_terms, start=1):
        items.append(
            {
                "query": f"{topic} {term}",
                "intent": "expanded",
                "stage": "result_expansion",
                "priority": 70 + offset,
                "order": 10000 + offset,
                "source": "extra_terms",
                "reason": f"result-driven or user-provided expansion term: {term}",
            }
        )

    limit = max_queries or MODE_LIMITS[mode]
    queries = select_diverse_queries(items, mode, profile, limit)
    return {
        "topic": topic,
        "mode": mode,
        "profile": profile,
        "max_queries": limit,
        "strategy": MODE_STRATEGY[mode],
        "queries": queries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--mode", choices=sorted(MODE_LIMITS), default="normal")
    parser.add_argument("--max-queries", type=int)
    parser.add_argument("--extra-terms", help="Optional JSON list or {'terms': [...]} for second-pass expansions.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    plan = build_plan(
        topic=args.topic.strip(),
        mode=args.mode,
        max_queries=args.max_queries,
        extra_terms=load_extra_terms(args.extra_terms),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(plan['queries'])} queries to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
