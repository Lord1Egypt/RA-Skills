"""Terminal formatting helpers."""

from __future__ import annotations

import re


def fmt_float(v: float) -> str:
    """保留最多 2 位小数，去掉尾部多余的零。"""
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def fmt_num(n: int) -> str:
    if abs(n) < 1000:
        return str(n)
    elif abs(n) < 1_000_000:
        return f"{fmt_float(n/1000)}K"
    else:
        return f"{fmt_float(n/1_000_000)}M"


def fmt_pct(pct: float) -> str:
    if pct >= 100:
        return ">100%"
    elif pct >= 90:
        return f"{pct:.1f}% 🚨"
    elif pct >= 60:
        return f"{pct:.1f}% ⚠️"
    else:
        return f"{pct:.1f}% ✅"


def calc_cache_rate(inp: int, cache: int) -> float | None:
    """计算缓存命中率（百分比）。"""
    if cache <= 0 or inp <= 0:
        return None
    if cache > inp:
        return cache / (cache + inp) * 100
    return cache / inp * 100


def fmt_cache_val(cache: int, inp: int) -> str:
    """格式化缓存展示，含缓存命中率。eg: 缓 162.18K (85.5%)"""
    base = f"缓 {fmt_num(cache)}"
    rate = calc_cache_rate(inp, cache)
    if rate is not None:
        return f"{base} ({min(rate, 99.9):.1f}%)"
    return base


def progress_bar(pct: float) -> str:
    """10 段上下文进度条，带 ANSI 颜色。累计模式下 pct 可能超过 100%"""
    n = min(10, max(0, round(min(pct, 100) / 10)))
    bar = "█" * n + "░" * (10 - n)
    if pct >= 90:
        color = "\033[31m"
    elif pct >= 60:
        color = "\033[33m"
    else:
        color = "\033[32m"
    if pct > 100:
        return f"{color}[{bar}]\033[0m >100%"
    return f"{color}[{bar}]\033[0m {pct}%"


def display_width(s: str) -> int:
    """计算终端显示宽度（CJK 字符算 2 列，ASCII 算 1 列）。"""
    w = 0
    for c in s:
        code = ord(c)
        if (0x1100 <= code <= 0x115F or
            0x2E80 <= code <= 0xA4CF or
            0xAC00 <= code <= 0xD7A3 or
            0xF900 <= code <= 0xFAFF or
            0xFE30 <= code <= 0xFE4F or
            0xFF01 <= code <= 0xFF60 or
            0xFFE0 <= code <= 0xFFE6 or
            0x20000 <= code <= 0x2FFFF or
            0x30000 <= code <= 0x3FFFF):
            w += 2
        else:
            w += 1
    return w


def pad_to(s: str, width: int, align: str = "<") -> str:
    """按显示宽度填充到指定列宽。"""
    dw = display_width(s)
    pad = max(0, width - dw)
    if align == ">":
        return " " * pad + s
    return s + " " * pad


def strip_ansi(s: str) -> str:
    """移除 ANSI 转义序列，用于显示宽度计算。"""
    return re.sub(r'\033\[[0-9;]*m', '', s)


def pad_ansi(s: str, width: int, align: str = "<") -> str:
    """按可见宽度填充（忽略 ANSI 码）。"""
    dw = display_width(strip_ansi(s))
    pad = max(0, width - dw)
    if align == ">":
        return " " * pad + s
    return s + " " * pad


def align_rows(rows):
    """rows: list of list of str。每列按最大宽度左对齐。"""
    if not rows:
        return rows
    n_cols = max(len(r) for r in rows)
    widths = [0] * n_cols
    for row in rows:
        for i, col in enumerate(row):
            w = display_width(strip_ansi(col))
            if w > widths[i]:
                widths[i] = w
    result = []
    for row in rows:
        padded = []
        for i, col in enumerate(row):
            padded.append(pad_ansi(col, widths[i], '<'))
        result.append(padded)
    return result


def skip_model(pm: dict) -> bool:
    """过滤掉 unknown 且无数据的模型条目（输出/导出/监控通用）。"""
    model = (pm.get("model", "") or "").strip()
    if not model or model == "unknown":
        inp = pm.get("input", 0) or 0
        out = pm.get("output", 0) or 0
        cache = pm.get("cache", 0) or 0
        calls = pm.get("calls", 0) or 0
        if inp == 0 and out == 0 and cache == 0 and calls == 0:
            return True
    return False


def is_total_mode(pm: dict) -> bool:
    """Whether a per-model row only has a total token count, not I/O split."""
    return (pm.get("token_mode") or pm.get("mode")) == "total"
