#!/usr/bin/env python3
"""
parse_date 回归测试。

网站时间格式会变——新格式出现时：
1. 把真实样本加到下面的 CASES 里（标注来源）
2. 跑 pytest，红了说明解析器没覆盖
3. 在 normalize_agent_reach.py 的 parse_date 里补规则
4. 绿了就提交

用法：
  cd ai_news_fetcher && python3 -m pytest tests/test_parse_date.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from normalize_agent_reach import parse_date


# (raw_input, expected_date_prefix, source_label)
# expected_date_prefix: 解析结果转 CST 后以此开头即视为正确
#   - 绝对时间：精确匹配到分钟
#   - 相对时间：只验证"能解析"（expected = "RELATIVE"）
CASES = [
    # === 财联社 cls.cn ===
    ("2026-03-18 23:50", "2026-03-18 23:50", "cls.cn"),
    ("2026-03-19 08:30:00", "2026-03-19 08:30", "cls.cn"),
    ("2026-03-18", "2026-03-18 00:00", "cls.cn"),

    # === 36kr ===
    ("1小时前", "RELATIVE", "36kr"),
    ("30分钟前", "RELATIVE", "36kr"),
    ("2天前", "RELATIVE", "36kr"),

    # === Readhub ===
    ("1 分钟前", "RELATIVE", "Readhub"),
    ("11 分钟前", "RELATIVE", "Readhub"),
    ("30 分钟前", "RELATIVE", "Readhub"),

    # === Anthropic ===
    ("Mar 18, 2026", "2026-03-18 00:00", "Anthropic"),
    ("Feb 17, 2026", "2026-02-17 00:00", "Anthropic"),
    ("Jan 30, 2026", "2026-01-30 00:00", "Anthropic"),

    # === Forrester ===
    ("January 15, 2026", "2026-01-15 00:00", "Forrester"),
    ("March 18, 2026", "2026-03-18 00:00", "Forrester"),

    # === 欧式日期（英文源可能出现）===
    ("18 Mar 2026", "2026-03-18 00:00", "European"),
    ("18 March 2026", "2026-03-18 00:00", "European"),

    # === 英文月日无年 ===
    ("Mar 18", "YEARLESS", "English month-day"),
    ("March 18", "YEARLESS", "English month-day"),

    # === ISO 8601 ===
    ("2026-03-18T14:30:00Z", "2026-03-18 22:30", "ISO8601 UTC"),
    ("2026-03-18T14:30:00+08:00", "2026-03-18 14:30", "ISO8601 +08"),

    # === 中文日期 ===
    ("2026年3月18日", "2026-03-18 00:00", "Chinese full"),
    ("2026年3月18日 14:30", "2026-03-18 14:30", "Chinese full+time"),
    ("3月18日", "YEARLESS", "Chinese no year"),
    ("3月18日 14:30", "YEARLESS", "Chinese no year+time"),

    # === 其他分隔符 ===
    ("2026/03/18", "2026-03-18 00:00", "slash"),
    ("2026.03.18", "2026-03-18 00:00", "dot"),

    # === 英文相对 ===
    ("2 hours ago", "RELATIVE", "English relative"),
    ("5 minutes ago", "RELATIVE", "English relative"),
    ("yesterday", "RELATIVE", "English relative"),
    ("today", "RELATIVE", "English relative"),
]


def _to_cst_str(dt):
    from zoneinfo import ZoneInfo
    return dt.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M")


def test_all_formats():
    failures = []
    for raw, expected, label in CASES:
        result = parse_date(raw)
        if result is None:
            failures.append(f"  ❌ [{label}] '{raw}' -> None (expected parse)")
            continue

        if expected == "RELATIVE":
            continue  # just needs to not be None
        if expected == "YEARLESS":
            # verify month-day matches, year can vary
            cst_str = _to_cst_str(result)
            # extract month-day from expected by parsing raw
            if "月" in raw:
                import re
                m = re.search(r"(\d{1,2})月(\d{1,2})日", raw)
                if m:
                    exp_md = f"-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
                    if exp_md not in cst_str:
                        failures.append(f"  ❌ [{label}] '{raw}' -> {cst_str} (month-day mismatch)")
            continue

        cst_str = _to_cst_str(result)
        if not cst_str.startswith(expected):
            failures.append(f"  ❌ [{label}] '{raw}' -> {cst_str} (expected {expected})")

    if failures:
        raise AssertionError("parse_date failures:\n" + "\n".join(failures))


def test_unparseable_returns_none():
    """Garbage input should return None, not crash."""
    for garbage in ("", "not a date", "???", "foo bar baz"):
        assert parse_date(garbage) is None, f"Expected None for '{garbage}'"
