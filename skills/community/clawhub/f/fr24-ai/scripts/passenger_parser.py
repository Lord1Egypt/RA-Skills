"""乘客人数解析。"""
from __future__ import annotations

import re

DEFAULT = {"adultNum": 1, "childNum": 0, "infantNum": 0}


def parse_passengers(text: str | None) -> dict[str, int]:
    if not text:
        return dict(DEFAULT)
    s = text.replace(" ", "")
    adult = (
        _first_int(r"(\d+)\s*个?\s*成人|(\d+)\s*大|(\d+)\s*adt", s)
        or _from_cn_num(s, "大", "成人", "大人", "adult")
    )
    child = (
        _first_int(r"(\d+)\s*小|(\d+)\s*儿童|(\d+)\s*chd", s)
        or _from_cn_num(s, "小", "儿童", "小孩", "child")
    )
    infant = _first_int(r"(\d+)\s*婴|(\d+)\s*婴儿|(\d+)\s*inf", s) or _from_cn_num(s, "婴儿", "infant")
    if adult is None and child is None and infant is None:
        return dict(DEFAULT)
    return {
        "adultNum": max(1, adult or 1),
        "childNum": max(0, child or 0),
        "infantNum": max(0, infant or 0),
    }


def validate_passengers(p: dict[str, int]) -> str | None:
    a, c, i = p["adultNum"], p["childNum"], p["infantNum"]
    if a + c > 9:
        return "成人+儿童不能超过9人"
    if c > a * 2:
        return "1位成人最多带2位儿童"
    if a + i > 18:
        return "成人+婴儿不能超过18人"
    if i > a:
        return "婴儿数量不能超过成人数量"
    return None


def _first_int(pattern: str, s: str) -> int | None:
    m = re.search(pattern, s, re.I)
    if not m:
        return None
    for g in m.groups():
        if g:
            return int(g)
    return None


def _from_cn_num(s: str, *keywords: str) -> int | None:
    for kw in keywords:
        m = re.search(rf"([一二两三四五六七八九十\d]+)\s*{kw}", s, re.I)
        if m:
            return _cn_to_int(m.group(1))
    return None


def _cn_to_int(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    mapping = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    if token in mapping:
        return mapping[token]
    return None
