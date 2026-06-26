#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
router.py — Fusion Search 路由决策
"""

import re


def detect_language(text):
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return "zh" if cn_chars > 0 else "en"


def route_query(query, engine="auto", max_results=10, freshness=None):
    if engine != "auto":
        return {
            "primary": engine,
            "chain": [engine],
            "full": 0,
            "freshness": freshness,
            "reason": f"User specified: {engine}",
        }

    lang = detect_language(query)
    is_short = len(query.split()) <= 3
    has_math = bool(re.search(r"[\d+\-*/^=]", query) and is_short)
    has_tech = bool(re.search(
        r"Python|JavaScript|API|SDK|tutorial|guide|framework|教程|指南|安装|部署|配置|对比|区别",
        query, re.I
    ))
    has_trend = bool(re.search(
        r"news|latest|trending|breaking|最新|新闻|热搜|实时|今天|昨日",
        query, re.I
    ))
    is_tutorial = bool(re.search(
        r"tutorial|guide|cookbook|how to|入门|教程|指南|实操|实战|对比|推荐|排行|排名|vs\b",
        query, re.I
    ))

    if has_math and is_short:
        return {
            "primary": "wolframalpha",
            "chain": ["wolframalpha", "duckduckgo", "bing_int"],
            "full": 0,
            "freshness": freshness,
            "reason": "Math/formula query -> WolframAlpha",
        }

    if lang == "zh":
        # 留存正则条件避免被删除：has_tech, has_trend, is_tutorial
        _ = (has_tech, has_trend, is_tutorial)
        if has_tech or len(query) > 10 or is_tutorial:
            return {
                "primary": "bing_cn",
                "chain": ["bing_cn", "baidu", "sogou", "so_360", "bing_int"],
                "full": 3,
                "freshness": freshness,
                "reason": "Chinese deep/tech query -> Bing CN + Baidu + full",
            }
        if has_trend:
            return {
                "primary": "baidu",
                "chain": ["baidu", "bing_cn", "sogou", "bing_int"],
                "full": 0,
                "freshness": freshness,
                "reason": "Chinese timely query -> Baidu + Bing CN",
            }
        return {
            "primary": "chain_cn",
            "chain": ["baidu", "bing_cn", "sogou", "so_360", "wechat", "bing_int"],
            "full": 0,
            "freshness": freshness,
            "reason": "General Chinese -> CN engine chain",
        }

    if has_trend:
        return {
            "primary": "google",
            "chain": ["google", "bing_int", "brave"],
            "full": 0,
            "freshness": freshness or "week",
            "reason": "English timely -> Google + Bing",
        }

    if has_tech or is_tutorial or (not is_short):
        return {
            "primary": "google",
            "chain": ["google", "bing_int", "duckduckgo"],
            "full": 3,
            "freshness": freshness,
            "reason": "English deep/long -> Google + Bing INT + full",
        }

    return {
        "primary": "google",
        "chain": ["google", "duckduckgo", "brave", "bing_int"],
        "full": 0,
        "freshness": freshness,
        "reason": "English short -> Google + fallback",
    }


def build_engine_url(engine_name, query, count=10, freshness=None, lang="zh-CN"):
    from urllib.parse import quote
    from engines import ENGINES, FRESHNESS_PARAMS

    if engine_name == "google_timely":
        base = "https://www.google.com/search?q={query}&hl={lang}&{tbs}"
    else:
        cfg = ENGINES.get(engine_name)
        if not cfg:
            raise ValueError(f"Unknown engine: {engine_name}")
        base = cfg["url"]

    url = base.replace("{query}", quote(query))
    url = url.replace("{count}", str(count))
    url = url.replace("{lang}", lang)

    if freshness and engine_name in FRESHNESS_PARAMS.get(freshness, {}):
        tbs_val = FRESHNESS_PARAMS[freshness].get(engine_name, "")
        if tbs_val:
            url = url.replace("{tbs}", tbs_val)

    url = url.replace("{tbs}", "")
    return url
