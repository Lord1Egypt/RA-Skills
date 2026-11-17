#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
textmatch.py — OCR 文本容错匹配（形近字 / 标点空格噪声）

纯函数，无 macOS 依赖，供发布器（店名断言、按钮定位）与学习层（回执匹配）共用。
"""
import re

_NOISE = re.compile(r"[\s·•・,，。.!！?？:：;；、\"'“”‘’（）()【】\[\]<>《》\-—…]")


def normalize(s: str) -> str:
    return _NOISE.sub("", s or "")


def default_max_err(n: int) -> int:
    if n <= 2:
        return 0
    return 1 if n <= 6 else 2


def fuzzy_in(needle: str, hay: str, max_err: int = None) -> bool:
    """needle 是否以「≤max_err 个替换字」出现在 hay 中（OCR 形近字：摧→催）。"""
    n, h = normalize(needle), normalize(hay)
    if not n:
        return False
    if n in h:
        return True
    if max_err is None:
        max_err = default_max_err(len(n))
    if max_err <= 0:
        return False
    size = len(n)
    for i in range(len(h) - size + 1):
        diff = 0
        for a, b in zip(n, h[i:i + size]):
            if a != b:
                diff += 1
                if diff > max_err:
                    break
        if diff <= max_err:
            return True
    return False


def split_shop(name: str) -> tuple:
    """「全境骑咖（天府公园店）」/「莫摧咖啡 三圣乡」→ (品牌, 分店核心词)。"""
    name = (name or "").strip()
    m = re.match(r"^(.+?)[（(](.+?)[)）]\s*$", name)
    if m:
        brand, branch = m.group(1), m.group(2)
    elif " " in name:
        brand, branch = name.split(" ", 1)
    else:
        brand, branch = name, ""
    branch = branch.strip()
    if branch.endswith("店") and len(branch) > 2:
        branch = branch[:-1]
    return brand.strip(), branch


def shop_matched(name: str, page_text: str) -> bool:
    """品牌必须命中；给了分店则分店也必须命中，防止同品牌发错店。"""
    brand, branch = split_shop(name)
    if not brand or not fuzzy_in(brand, page_text):
        return False
    return not branch or fuzzy_in(branch, page_text)
