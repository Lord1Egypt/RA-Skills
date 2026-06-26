"""Parse time, amount, income/expense type, and category hints from text."""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from typing import Any

import dateparser

from db import DEFAULT_EXPENSE_CATEGORIES, DEFAULT_INCOME_CATEGORIES
from utils import mark_amount_suspicious, parse_chinese_number_fragment

# Keyword -> (type, category) for expense
_EXPENSE_KEYWORDS: list[tuple[str, str]] = [
    ("吃饭", "正餐"),
    ("午餐", "正餐"),
    ("晚餐", "正餐"),
    ("早餐", "正餐"),
    ("外卖", "正餐"),
    ("奶茶", "零食饮料"),
    ("咖啡", "零食饮料"),
    ("零食", "零食饮料"),
    ("饮料", "零食饮料"),
    ("打车", "出行"),
    ("滴滴", "出行"),
    ("地铁", "出行"),
    ("公交", "出行"),
    ("高铁", "出行"),
    ("机票", "出行"),
    ("加油", "出行"),
    ("停车", "出行"),
    ("房租", "居住"),
    ("水电", "居住"),
    ("物业", "居住"),
    ("电影", "娱乐"),
    ("游戏", "娱乐"),
    ("医院", "医疗健康"),
    ("药", "医疗健康"),
    ("礼物", "购物"),
    ("淘宝", "购物"),
    ("京东", "购物"),
]

_INCOME_KEYWORDS: list[tuple[str, str]] = [
    ("工资", "工资"),
    ("薪水", "工资"),
    ("奖金", "奖金"),
    ("分红", "投资"),
    ("股票", "投资"),
    ("理财", "投资"),
]


def parse_natural_bundle(
    text: str, now: datetime | None = None
) -> dict[str, Any]:
    """Best-effort extraction from a single NL string."""
    now = now or datetime.now()
    out: dict[str, Any] = {"raw": text}
    tinfo = parse_time_expression(text, now)
    out["time"] = tinfo
    ainfo = parse_amount_expression(text)
    out["amount"] = ainfo
    tincome = detect_type(text)
    out["type_hint"] = tincome
    cat = infer_category(text, tincome.get("type") if tincome.get("type") else None)
    out["category_hint"] = cat
    return out


def detect_type(text: str) -> dict[str, Any]:
    if re.search(r"收入|到账|发工资|奖金|进账|赚了", text):
        return {"type": "收入", "confidence": "medium"}
    if re.search(r"支出|花了|消费|付款|买|打车|吃饭", text):
        return {"type": "支出", "confidence": "low"}
    return {"type": None, "confidence": "none"}


def infer_category(text: str, type_: str | None) -> dict[str, Any]:
    if type_ == "收入":
        for kw, cat in _INCOME_KEYWORDS:
            if kw in text:
                return {"category": cat, "via": kw}
        return {"category": "其他收入", "via": None}
    for kw, cat in _EXPENSE_KEYWORDS:
        if kw in text:
            return {"category": cat, "via": kw}
    return {"category": "其他", "via": None}


def parse_time_expression(text: str, now: datetime) -> dict[str, Any]:
    text_l = text.strip()

    if m := re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", text_l):
        y, mo, d_ = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dt = datetime(y, mo, d_, now.hour, now.minute, now.second)
            return {
                "resolved": True,
                "datetime": dt.isoformat(timespec="seconds"),
                "date": dt.date().isoformat(),
                "ambiguous": False,
            }
        except ValueError:
            pass

    if "刚刚" in text_l or "刚才" in text_l:
        return {
            "resolved": True,
            "datetime": now.isoformat(timespec="seconds"),
            "date": now.date().isoformat(),
            "ambiguous": False,
        }

    if "中午" in text_l:
        dt = now.replace(hour=12, minute=0, second=0, microsecond=0)
        return {
            "resolved": True,
            "datetime": dt.isoformat(timespec="seconds"),
            "date": dt.date().isoformat(),
            "ambiguous": False,
        }
    if "晚上" in text_l and not re.search(r"\d{4}[-/]", text_l):
        dt = now.replace(hour=20, minute=0, second=0, microsecond=0)
        return {
            "resolved": True,
            "datetime": dt.isoformat(timespec="seconds"),
            "date": dt.date().isoformat(),
            "ambiguous": True,
            "note": "“晚上”已默认当天 20:00，若用户指别的日期请确认",
        }

    rel = _relative_date_phrase(text_l, now)
    if rel is not None:
        d0, amb_note = rel
        dt = datetime.combine(d0, now.time().replace(microsecond=0))
        return {
            "resolved": True,
            "datetime": dt.isoformat(timespec="seconds"),
            "date": d0.isoformat(),
            "ambiguous": amb_note is not None,
            "note": amb_note,
        }

    settings = {
        "RELATIVE_BASE": now,
        "PREFER_DATES_FROM": "past",
        "DATE_ORDER": "YMD",
    }
    parsed = dateparser.parse(text_l, languages=["zh", "en"], settings=settings)
    if parsed:
        return {
            "resolved": True,
            "datetime": parsed.isoformat(timespec="seconds"),
            "date": parsed.date().isoformat(),
            "ambiguous": False,
        }

    return {
        "resolved": False,
        "ambiguous": True,
        "candidates": [],
        "note": "无法从文本解析时间，请向用户确认具体日期",
    }


def _relative_date_phrase(text: str, now: datetime) -> tuple[date, str | None] | None:
    today = now.date()
    if "前天" in text:
        return today - timedelta(days=2), None
    if "昨天" in text:
        return today - timedelta(days=1), None
    if "今天" in text:
        return today, None

    if "上个月" in text:
        first = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        return first, "已取上个月第一天，若需精确日期请用户确认"

    m = re.search(r"上(?:周|星期)([一二三四五六日天1-7])", text)
    if m:
        ch = m.group(1)
        target = _weekday_cn_to_iso(ch)
        if target is not None:
            d0 = _date_in_previous_week(today, target)
            return d0, None

    m2 = re.search(r"上周", text)
    if m2:
        return today - timedelta(days=7), "“上周”已按约 7 天前估算，建议用户确认"

    return None


def _weekday_cn_to_iso(ch: str) -> int | None:
    m = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}
    if ch in m:
        return m[ch]
    if ch.isdigit():
        n = int(ch)
        if 1 <= n <= 7:
            return (n - 1) % 7
    return None


def _last_weekday(today: date, weekday: int) -> date:
    # Monday=0 .. Sunday=6
    d = today - timedelta(days=1)
    while d.weekday() != weekday:
        d -= timedelta(days=1)
    return d


def parse_amount_expression(text: str) -> dict[str, Any]:
    raw = text.strip()

    # 23w, 1k, 3千, 2.3万
    m = re.search(
        r"(\d+(?:\.\d+)?)\s*([wW万kK千])",
        raw,
    )
    if m:
        val = float(m.group(1))
        u = m.group(2).lower()
        if u in ("w", "万"):
            val *= 10000
        elif u in ("k", "千"):
            val *= 1000
        return _amount_result(val)

    m2 = re.search(r"(\d+(?:\.\d+)?)\s*元?", raw)
    if m2:
        return _amount_result(float(m2.group(1)))

    cn = parse_chinese_number_fragment(raw)
    if cn is not None:
        return _amount_result(cn)

    return {
        "value": None,
        "resolved": False,
        "note": "未能解析金额",
    }


def _amount_result(val: float) -> dict[str, Any]:
    return {"value": val, "resolved": True}


def validate_record_fields(
    *,
    date_str: str,
    type_: str,
    category: str,
    amount: float,
    note: str | None,
    expense_defaults: tuple[str, ...] = DEFAULT_EXPENSE_CATEGORIES,
    income_defaults: tuple[str, ...] = DEFAULT_INCOME_CATEGORIES,
) -> dict[str, Any]:
    issues: list[str] = []
    if type_ not in ("收入", "支出"):
        issues.append("type 必须是 收入 或 支出")
    if type_ == "支出" and category not in expense_defaults:
        pass  # custom categories allowed
    if type_ == "收入" and category not in income_defaults:
        pass
    suspicious = mark_amount_suspicious(category, amount)
    return {"valid": len(issues) == 0, "issues": issues, **suspicious}


def list_default_categories() -> dict[str, list[str]]:
    return {
        "支出": list(DEFAULT_EXPENSE_CATEGORIES),
        "收入": list(DEFAULT_INCOME_CATEGORIES),
    }
