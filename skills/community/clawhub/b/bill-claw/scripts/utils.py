"""Helpers: Chinese numerals, amount anomaly hints."""

from __future__ import annotations

import re
from typing import Any

# Max amount (yuan) per category for suspicious flag — Agent should confirm with user.
CATEGORY_AMOUNT_HINTS: dict[str, float] = {
    "正餐": 800,
    "零食饮料": 300,
    "出行": 2000,
    "购物": 5000,
    "日常开销": 2000,
    "娱乐": 3000,
    "居住": 20000,
    "医疗健康": 10000,
    "家人": 10000,
    "社交": 3000,
    "其他": 5000,
    "工资": 500000,
    "奖金": 200000,
    "投资": 500000,
    "其他收入": 500000,
}

_CN_DIGITS = "零一二三四五六七八九两幺"
_CN_UNIT_SMALL = "十百千万亿"


def mark_amount_suspicious(category: str, amount: float) -> dict[str, Any]:
    cap = CATEGORY_AMOUNT_HINTS.get(category)
    if cap is None or amount <= cap:
        return {"suspicious": False}
    return {
        "suspicious": True,
        "reason": f"金额 {amount} 超过该类常见上限参考 {cap}（元），请向用户确认是否输错",
        "threshold": cap,
    }


def parse_chinese_number_fragment(text: str) -> float | None:
    """Parse simple Chinese amounts like 十二块五, 三万, 两千三."""
    t = text.strip().replace("块钱", "元").replace("块", "元")
    if not t:
        return None

    # 三万五 -> 35000 (rough)
    m = re.search(
        r"([零一二三四五六七八九两幺百千万亿点两]+)\s*元?",
        t,
    )
    if m:
        num_part = m.group(1).replace("两", "二").replace("幺", "一")
        v = _cn_to_float(num_part)
        if v is not None:
            return v

    # digits mixed
    m2 = re.match(r"^[\d.]+$", t.replace("元", ""))
    if m2:
        try:
            return float(t.replace("元", ""))
        except ValueError:
            pass
    return None


def _cn_to_float(s: str) -> float | None:
    s = s.strip()
    if not s:
        return None
    if "点" in s or "." in s:
        parts = re.split(r"[点.]", s, 1)
        whole = _cn_int(parts[0])
        if whole is None:
            return None
        frac_s = parts[1] if len(parts) > 1 else ""
        frac = 0.0
        for i, ch in enumerate(frac_s):
            if ch in _CN_DIGITS:
                d = _digit_val(ch)
                if d >= 0:
                    frac += d * (0.1 ** (i + 1))
        return whole + frac

    v = _cn_int(s)
    return float(v) if v is not None else None


def _digit_val(ch: str) -> int:
    if ch in "0123456789":
        return int(ch)
    m = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    return m.get(ch, -1)


def _cn_int(s: str) -> int | None:
    """Simplified Chinese integer: supports 十二, 二十三, 一百零五, 三万."""
    s = re.sub(r"\s+", "", s)
    if not s:
        return None
    if re.fullmatch(r"\d+", s):
        return int(s)

    # explicit 万/千
    if "万" in s:
        parts = s.split("万", 1)
        left = parts[0] or "一"
        right = parts[1] if len(parts) > 1 else ""
        lv = _cn_int_simple(left)
        rv = _cn_int_simple(right) if right else 0
        if lv is None:
            return None
        return lv * 10000 + (rv or 0)

    return _cn_int_simple(s)


def _cn_int_simple(s: str) -> int | None:
    if not s:
        return 0
    if re.fullmatch(r"\d+", s):
        return int(s)
    # 千
    total = 0
    if "千" in s:
        i = s.index("千")
        head = s[:i] or "一"
        tail = s[i + 1 :]
        hv = _parse_under_1000(head)
        if hv is None:
            return None
        total += hv * 1000
        s = tail
    v = _parse_under_1000(s)
    if v is None:
        return None
    total += v
    return total


def _parse_under_1000(s: str) -> int | None:
    if not s:
        return 0
    if re.fullmatch(r"\d+", s):
        return int(s)
    n = 0
    if "百" in s:
        i = s.index("百")
        pre = s[:i]
        post = s[i + 1 :]
        if pre == "":
            coef = 1
        elif pre == "十":
            coef = 10
        else:
            d = _digit_val(pre[-1]) if pre else 1
            coef = d if d >= 0 else 1
        n += coef * 100
        s = post
    if s.startswith("十"):
        n += 10
        s = s[1:]
    elif "十" in s:
        i = s.index("十")
        left = s[:i]
        right = s[i + 1 :]
        lv = _digit_val(left) if left else 1
        if lv < 0:
            lv = 1
        rv = _digit_val(right) if right else 0
        if rv < 0:
            rv = 0
        n += lv * 10 + rv
        s = ""
    if s:
        for ch in s:
            if ch in _CN_DIGITS:
                d = _digit_val(ch)
                if d >= 0:
                    n += d
            elif ch == "百":
                pass
    return n
