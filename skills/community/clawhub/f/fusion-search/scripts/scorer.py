#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scorer.py — Fusion Search 质量评分 + Query改写 + 去重
"""

import re
from urllib.parse import urlparse

LOW_QUALITY_DOMAINS = [
    "jingyan.baidu.com", "zhidao.baidu.com", "tieba.baidu.com",
    "baike.baidu.com", "wenku.baidu.com", "bbs.16fan.com",
    "zhihu.com", "zhuanlan.zhihu.com", "51cto.com",
    "blog.csdn.net", "cnblogs.com", "jianshu.com",
]

AUTHORITY_HINTS = [
    ".gov.", "gov.cn", ".org.", ".edu.",
    "github.com", "stackoverflow.com", "wikipedia.org",
    "docs.python.org", "developer.mozilla.org",
]

CITIES = "|".join([
    "深圳", "广州", "北京", "上海", "杭州", "成都", "武汉", "南京",
    "重庆", "西安", "长沙", "苏州", "厦门", "青岛", "大连", "天津",
    "昆明", "珠海", "东莞", "佛山", "惠州", "中山",
])

INTENT_RULES = [
    (re.compile(rf'({CITIES})\s*(有什么好玩的|哪里好玩|好玩的地方|去哪玩|周末.*去哪|好去处|逛|玩什么)'),
     lambda m, q: f'{m.group(1)} 景点', 'city travel -> attractions'),
    (re.compile(rf'({CITIES})\s*(活动|展览|演出|市集|音乐会|演唱会)'),
     lambda m, q: f'{m.group(1)} {m.group(2)}', 'city events -> simplify'),
    (re.compile(r'今日(金价|银价|油价|铜价|铂金价)'),
     lambda m, q: f'{m.group(1)}', 'today price -> price'),
    (re.compile(r'(.+?)是什么(?:意思)?$', re.IGNORECASE),
     lambda m, q: f'{m.group(1)} 介绍', 'what is X -> X intro'),
    (re.compile(r'(.+?)怎么样$', re.IGNORECASE),
     lambda m, q: f'{m.group(1)} 评价', 'how is X -> X review'),
    (re.compile(r'^怎么(.+)', re.IGNORECASE),
     lambda m, q: f'{m.group(1)} 方法', 'how to -> method'),
    (re.compile(r'(.+?)和(.+?)(哪个好|哪个更好|选哪个)'),
     lambda m, q: f'{m.group(1)} {m.group(2)} 对比', 'A vs B -> comparison'),
]


def score_result(result):
    s = 0.5
    url = result.get("url", "")
    snippet = result.get("snippet", "")
    title = result.get("title", "")
    if any(d in url for d in LOW_QUALITY_DOMAINS):
        s -= 0.3
    if re.search(r'\d{2,}', snippet):
        s += 0.15
    if len(snippet) < 20:
        s -= 0.1
    if len(title) < 10:
        s -= 0.05
    for h in AUTHORITY_HINTS:
        if h in url:
            s += 0.2
            break
    return max(0.0, min(1.0, s))


def score_results(results):
    if not results:
        return 0.0
    return sum(score_result(r) for r in results) / len(results)


def get_dominant_domain(results):
    if not results:
        return (None, 0, 0)
    domains = {}
    for r in results:
        d = urlparse(r["url"]).netloc.replace("www.", "")
        domains[d] = domains.get(d, 0) + 1
    top = max(domains, key=domains.get)
    if domains[top] > len(results) * 0.5:
        return (top, domains[top], len(results))
    return (None, 0, len(results))


def rewrite_query(query):
    for pattern, rewrite_fn, desc in INTENT_RULES:
        m = pattern.search(query)
        if m:
            rewritten = rewrite_fn(m, query)
            rewritten = re.sub(r'\s+', ' ', rewritten).strip()
            return rewritten, desc
    return query, None


def merge_and_deduplicate(results_list, max_results=10):
    seen = set()
    merged = []
    for results in results_list:
        for r in results:
            url = r.get("url", "")
            if url and url not in seen:
                seen.add(url)
                if "score" not in r:
                    r["score"] = score_result(r)
                merged.append(r)
    merged.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    return merged[:max_results]


def is_low_quality_domain(url):
    return any(d in url for d in LOW_QUALITY_DOMAINS)


def filter_low_quality(results, do_filter=True):
    if not do_filter or not results:
        return results
    filtered = [r for r in results if not is_low_quality_domain(r.get("url", ""))]
    return filtered if filtered else results
