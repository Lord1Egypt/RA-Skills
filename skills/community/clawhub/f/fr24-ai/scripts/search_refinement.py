"""搜索条件细化：航司偏好、起飞时段（用于不满意结果后重新搜索）。"""
from __future__ import annotations

import copy
import re
from typing import Any

# 中文航司简称 -> IATA
CARRIER_ALIASES: dict[str, str] = {
    "国航": "CA",
    "中国国航": "CA",
    "东航": "MU",
    "中国东航": "MU",
    "南航": "CZ",
    "中国南航": "CZ",
    "海航": "HU",
    "厦航": "MF",
    "川航": "3U",
    "深航": "ZH",
    "上航": "FM",
    "吉祥": "HO",
    "春秋": "9C",
}

TIME_PERIOD_WINDOWS: dict[str, tuple[str, str]] = {
    "凌晨": ("00:00", "06:00"),
    "早上": ("06:00", "10:00"),
    "上午": ("06:00", "12:00"),
    "中午": ("11:00", "13:00"),
    "午间": ("11:00", "13:00"),
    "下午": ("12:00", "18:00"),
    "傍晚": ("17:00", "20:00"),
    "晚上": ("18:00", "23:59"),
    "夜间": ("20:00", "23:59"),
}

_CARRIER_CODE_RE = re.compile(
    r"(?:要|只要|订|坐|选)?\s*([A-Z]{2})\s*(?:航司|航空|航)?",
    re.I,
)
_CARRIER_ZH_RE = re.compile(
    r"(国航|中国国航|东航|中国东航|南航|中国南航|海航|厦航|川航|深航|上航|吉祥|春秋)"
)
_TIME_PERIOD_RE = re.compile(r"(凌晨|早上|上午|中午|午间|下午|傍晚|晚上|夜间)")
_TIME_POINT_RE = re.compile(
    r"(?:大约|约|大概)?\s*(\d{1,2})\s*[:：点时]\s*(\d{0,2})?\s*(?:分)?\s*(?:左右|前后|附近)?(?:起飞|出发|走)?"
)
_TIME_HALF_RE = re.compile(r"(\d{1,2})\s*点半")


def parse_carriers_from_text(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for m in _CARRIER_CODE_RE.finditer(text):
        code = m.group(1).upper()
        if code not in seen:
            seen.add(code)
            found.append(code)
    for m in _CARRIER_ZH_RE.finditer(text):
        code = CARRIER_ALIASES.get(m.group(1))
        if code and code not in seen:
            seen.add(code)
            found.append(code)
    return found


def _hour_window(center_hour: int, *, span: int = 1) -> tuple[str, str]:
    start_h = max(0, center_hour - span)
    end_h = min(23, center_hour + span)
    return f"{start_h:02d}:00", f"{end_h:02d}:59"


def parse_dep_time_window(text: str) -> tuple[dict[str, str] | None, str | None]:
    """解析起飞时段偏好。返回 (depTimeWindow, 展示用标签)。"""
    for m in _TIME_PERIOD_RE.finditer(text):
        key = m.group(1)
        start, end = TIME_PERIOD_WINDOWS[key]
        return {"from": start, "to": end}, f"{key}起飞"

    m = _TIME_HALF_RE.search(text)
    if m:
        h = int(m.group(1))
        if 0 <= h <= 23:
            start, end = _hour_window(h, span=1)
            return {"from": start, "to": end}, f"约{h}:30起飞"

    m = _TIME_POINT_RE.search(text)
    if m:
        h = int(m.group(1))
        minute = int(m.group(2) or 0)
        if h > 23:
            return None, None
        if minute > 59:
            minute = 0
        center = h + (0.5 if minute >= 30 else 0)
        start, end = _hour_window(int(center), span=1)
        label = f"约{h:02d}:{minute:02d}起飞" if minute else f"约{h}点起飞"
        return {"from": start, "to": end}, label

    return None, None


def extract_search_filters(preferences: dict[str, Any]) -> dict[str, Any]:
    """从 payload.preferences 提取 summarizer 用的过滤条件。"""
    filters: dict[str, Any] = {}
    carriers = preferences.get("preferredCarrier")
    if carriers:
        filters["preferredCarrier"] = [str(c).upper() for c in carriers]
    window = preferences.get("depTimeWindow")
    if isinstance(window, dict) and window.get("from") and window.get("to"):
        filters["depTimeWindow"] = {
            "from": str(window["from"]),
            "to": str(window["to"]),
        }
    return filters


def describe_preferences(prefs: dict[str, Any]) -> str:
    parts: list[str] = []
    carriers = prefs.get("preferredCarrier") or []
    if carriers:
        parts.append("航司 " + "/".join(carriers))
    label = prefs.get("depTimeLabel")
    if label:
        parts.append(str(label))
    elif prefs.get("depTimeWindow"):
        w = prefs["depTimeWindow"]
        parts.append(f"起飞 {w.get('from', '')}-{w.get('to', '')}")
    if prefs.get("stops") == 0:
        parts.append("仅直飞")
    return "，".join(parts) if parts else ""


def apply_refinement(payload: dict[str, Any], text: str) -> tuple[dict[str, Any], str, str | None]:
    """
    在已有 search payload 上合并用户细化条件。
    返回 (新 payload, 条件说明, error)。
    """
    t = (text or "").strip()
    if not t:
        return payload, "", "请说明要调整的条件，例如「要 CA 航司」或「中午 12 点左右起飞」"

    carriers = parse_carriers_from_text(t)
    window, time_label = parse_dep_time_window(t)
    direct_only = "直飞" in t and "不要直飞" not in t and "非直飞" not in t

    if not carriers and not window and not direct_only:
        return (
            payload,
            "",
            "未能识别细化条件，请说明航司（如 CA/国航）或起飞时段（如中午 12 点、下午起飞）",
        )

    out = copy.deepcopy(payload)
    prefs = dict(out.get("preferences") or {})

    if carriers:
        existing = [str(c).upper() for c in (prefs.get("preferredCarrier") or [])]
        merged = list(dict.fromkeys(existing + carriers))
        prefs["preferredCarrier"] = merged

    if window:
        prefs["depTimeWindow"] = window
        if time_label:
            prefs["depTimeLabel"] = time_label

    if direct_only:
        prefs["stops"] = 0

    out["preferences"] = prefs
    note = describe_preferences(prefs)
    return out, note, None
