#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engines.py — Fusion Search 16引擎配置
"""

ENGINE_COOLDOWN = 2.0

ENGINES = {
    "baidu": {
        "url": "https://www.baidu.com/s?wd={query}&ie=utf-8",
        "selector": "div.result, div.c-container, div[class*='result-op']",
        "title_sel": "h3 a",
        "snippet_sel": "span.content-right_8Zs40, div.c-abstract, span.c-gap-bottom-small",
        "language": "zh",
        "parser": "dom",
    },
    "bing_cn": {
        "url": "https://cn.bing.com/search?q={query}&mkt=zh-CN&setlang=zh-CN&cc=CN&count={count}",
        "selector": "li.b_algo",
        "title_sel": "h2 a",
        "snippet_sel": "div.b_caption p, div.b_lineclamp2, div.b_caption",
        "language": "zh",
        "parser": "dom",
    },
    "sogou": {
        "url": "https://sogou.com/web?query={query}",
        "selector": "div.vrwrap, div.results, div.vr-title",
        "title_sel": "h3 a, div.vr-title a",
        "snippet_sel": "div.str-text, div.str-info, div.str-ab",
        "language": "zh",
        "parser": "dom",
    },
    "so_360": {
        "url": "https://www.so.com/s?q={query}",
        "selector": "li.res-list, ul.result li",
        "title_sel": "h3 a",
        "snippet_sel": "p.str-text, span.mh-abstract",
        "language": "zh",
        "parser": "dom",
    },
    "wechat": {
        "url": "https://wx.sogou.com/weixin?type=2&query={query}",
        "selector": "div.news-box li, ul.news-list li",
        "title_sel": "h3 a",
        "snippet_sel": "p.txt-info",
        "language": "zh",
        "parser": "dom",
    },
    "shenma": {
        "url": "https://m.sm.cn/s?q={query}",
        "selector": "div.result, div.result-brief",
        "title_sel": "h3 a",
        "snippet_sel": "p.desc",
        "language": "zh",
        "parser": "dom",
    },
    "bing_int": {
        "url": "https://www.bing.com/search?q={query}&count={count}",
        "selector": "li.b_algo",
        "title_sel": "h2 a",
        "snippet_sel": "div.b_caption p, div.b_caption",
        "language": "en",
        "parser": "dom",
    },
    "google": {
        "url": "https://www.google.com/search?q={query}&hl={lang}",
        "selector": "div.g, div[data-hveid], div[data-hvef]",
        "title_sel": "h3 a, a[href^='/url']",
        "snippet_sel": "div.VwiC3b, span.aCOpRe, div[data-snf]",
        "language": "en",
        "parser": "dom",
    },
    "duckduckgo": {
        "url": "https://duckduckgo.com/html/?q={query}",
        "selector": "article[data-testid='result'], div.result, li[data-layout='organic']",
        "title_sel": "h2 a[data-testid='result-title-a'], h2 a, a[data-testid='result-title-a']",
        "snippet_sel": "a[data-testid='result-snippet'], div.result__snippet, span.snippet",
        "language": "en",
        "parser": "dom",
    },
    "brave": {
        "url": "https://search.brave.com/search?q={query}",
        "selector": "div.snippet, div.search-result, div.search-item",
        "title_sel": "a.heading-link, h3 a",
        "snippet_sel": "div.snippet-description, p.snippet-description",
        "language": "en",
        "parser": "dom",
    },
    "yahoo": {
        "url": "https://search.yahoo.com/search?p={query}",
        "selector": "div.dd.algo, div.searchCenterMiddle li",
        "title_sel": "h3.title a, h4 a",
        "snippet_sel": "div.compText.a, div.ov-a",
        "language": "en",
        "parser": "dom",
    },
    "startpage": {
        "url": "https://www.startpage.com/sp/search?query={query}",
        "selector": "div.result, div.w-gl__result, div.search-result",
        "title_sel": "h3 a, a.result-title, a[data-testid='result-title']",
        "snippet_sel": "p.description, div.result-description",
        "language": "en",
        "parser": "dom",
    },
    "ecosia": {
        "url": "https://www.ecosia.org/search?q={query}",
        "selector": "div.result, article, div.search-result",
        "title_sel": "a.result-title, h2 a, a[data-testid='result-title']",
        "snippet_sel": "p.result-snippet, div.result-snippet",
        "language": "en",
        "parser": "dom",
    },
    "qwant": {
        "url": "https://www.qwant.com/?q={query}",
        "selector": "div.result, article.web-result, section.web-results div",
        "title_sel": "h3 a, a.title",
        "snippet_sel": "p.desc, div.description",
        "language": "en",
        "parser": "dom",
    },
    "wolframalpha": {
        "url": "https://www.wolframalpha.com/input?i={query}",
        "selector": "div.output, div.result, div.warning",
        "title_sel": "h2, h3",
        "snippet_sel": "div.output, pre.output",
        "language": "en",
        "parser": "dom",
        "special": "计算/知识类",
    },
}

CN_CHAIN = ["baidu", "bing_cn", "sogou", "so_360", "wechat", "shenma"]
INT_CHAIN_SHORT = ["google", "duckduckgo", "brave", "yahoo", "startpage"]
INT_CHAIN_FULL = ["google", "bing_int", "duckduckgo"]
TIMELY_CHAIN = ["google_timely", "bing_cn", "baidu"]
DEEP_CHAIN = ["bing_int", "google"]

FRESHNESS_PARAMS = {
    "hour": {"google": "tbs=qdr:h", "bing_int": ""},
    "day": {"google": "tbs=qdr:d", "bing_int": ""},
    "week": {"google": "tbs=qdr:w", "bing_int": ""},
    "month": {"google": "tbs=qdr:m", "bing_int": ""},
    "year": {"google": "tbs=qdr:y", "bing_int": ""},
}


def get_engine_config(name):
    return ENGINES.get(name)


def get_engine_url(name, query, count=10, lang="zh-CN"):
    from urllib.parse import quote
    cfg = get_engine_config(name)
    if not cfg:
        raise ValueError(f"Unknown engine: {name}")
    url = cfg["url"]
    url = url.replace("{query}", quote(query))
    url = url.replace("{count}", str(count))
    url = url.replace("{lang}", lang)
    return url


def is_cn_engine(name):
    return name in CN_CHAIN


def is_int_engine(name):
    return name in ENGINES and name not in CN_CHAIN and name != "wolframalpha"


def get_engine_language(name):
    cfg = get_engine_config(name)
    return cfg.get("language", "en") if cfg else "en"
