#!/usr/bin/env python3
"""contrast_check.py — WCAG 2.1 颜色对比度检查（确定性、可重复执行）。

计算前景/背景两色的相对亮度与对比度，并判定正文与大字在 AA / AAA 下是否达标。
纯标准库实现，无外部依赖。

用法:
    python3 contrast_check.py "#777777" "#ffffff"
    python3 contrast_check.py 119,119,119 255,255,255 --json
    python3 contrast_check.py "#ff0" "#000" --strict      # 任一阈值不达标 → 退出码 1
"""
import argparse
import json
import re
import sys


def parse_color(s):
    """支持 #fff / #ffffff / r,g,b 三种写法，返回 [r,g,b] (0-255)。"""
    s = s.strip().lstrip("#")
    if re.fullmatch(r"\d{1,3},\d{1,3},\d{1,3}", s):
        parts = [int(x) for x in s.split(",")]
    elif re.fullmatch(r"[0-9a-fA-F]{3}", s):
        parts = [int(c * 2, 16) for c in s]
    elif re.fullmatch(r"[0-9a-fA-F]{6}", s):
        parts = [int(s[i:i + 2], 16) for i in (0, 2, 4)]
    else:
        raise ValueError(f"无法解析颜色: {s!r}（支持 #fff / #ffffff / r,g,b）")
    if any(p > 255 for p in parts):
        raise ValueError(f"颜色通道超出 0-255: {parts}")
    return parts


def _linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(rgb):
    r, g, b = (_linear(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1, rgb2):
    l1 = rel_luminance(rgb1)
    l2 = rel_luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate(ratio):
    return {
        "normal_text": {"aa": ratio >= 4.5, "aaa": ratio >= 7.0},
        "large_text": {"aa": ratio >= 3.0, "aaa": ratio >= 4.5},
    }


def main():
    ap = argparse.ArgumentParser(
        description="WCAG 对比度检查：计算两色对比度并判定 AA/AAA 达标情况"
    )
    ap.add_argument("fg", help="前景色：#fff / #ffffff / 255,255,255")
    ap.add_argument("bg", help="背景色：#fff / #ffffff / 255,255,255")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument(
        "--strict", action="store_true",
        help="任一 AA 阈值不达标则退出码 1（可作 CI 门禁）",
    )
    args = ap.parse_args()

    try:
        fg = parse_color(args.fg)
        bg = parse_color(args.bg)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    ratio = contrast_ratio(fg, bg)
    thresholds = evaluate(ratio)
    passed_aa = thresholds["normal_text"]["aa"] and thresholds["large_text"]["aa"]

    if args.json:
        print(json.dumps(
            {"fg": fg, "bg": bg, "ratio": round(ratio, 2), "thresholds": thresholds},
            ensure_ascii=False, indent=2,
        ))
    else:
        print(f"前景 {fg}  背景 {bg}")
        print(f"对比度: {ratio:.2f}:1")
        print(f"  正文  AA(4.5): {'PASS' if thresholds['normal_text']['aa'] else 'FAIL'}  "
              f"AAA(7.0): {'PASS' if thresholds['normal_text']['aaa'] else 'FAIL'}")
        print(f"  大字  AA(3.0): {'PASS' if thresholds['large_text']['aa'] else 'FAIL'}  "
              f"AAA(4.5): {'PASS' if thresholds['large_text']['aaa'] else 'FAIL'}")

    if args.strict and not passed_aa:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
