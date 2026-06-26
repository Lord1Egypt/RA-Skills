#!/usr/bin/env python3
"""
FootyClaw Chart Generator (zero file-write edition)
从 stdin 读取 Markdown 账本表格，在内存中生成 SVG 图表，
以 Base64 编码的 <img> 标签输出到 stdout，可直接嵌入对话框。

用法：
  echo '| Day1 | 03-15 | ... |' | python3 chart_generator.py
  python3 chart_generator.py < ledger_snippet.md
  python3 chart_generator.py --ascii   # 纯文本 ASCII 图表
"""
import sys, re, base64, argparse


def parse_ledger(text):
    """解析 Markdown 表格文本，返回 [{day, date, pnl, balance}, ...]"""
    days = []
    pattern = re.compile(
        r'\|\s*Day(\d+)\s*\|\s*(\d{2}-\d{2})\s*\|[^|]*\|[^|]*\|\s*([+−\-]?[\d,，]+)\s*\|\s*\*{0,2}([\d,]+)\*{0,2}\s*\|'
    )
    for m in pattern.finditer(text):
        day_num = int(m.group(1))
        date = f"2026-{m.group(2)}"
        pnl_str = m.group(3).replace(",", "").replace("，", "").replace("−", "-")
        balance_str = m.group(4).replace(",", "")
        try:
            days.append({"day": day_num, "date": date,
                         "pnl": int(pnl_str), "balance": int(balance_str)})
        except ValueError:
            pass
    return sorted(days, key=lambda x: x["day"])


def generate_svg(days, width=900, height=520):
    """在内存中生成 SVG 字符串"""
    if not days:
        return None
    pad_left, pad_right, pad_top, pad_bot = 80, 30, 50, 60
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bot
    n = len(days)
    bar_w = chart_w / n * 0.7
    pnls = [d["pnl"] for d in days]
    balances = [d["balance"] for d in days]
    max_pnl = max(abs(p) for p in pnls) * 1.2 or 1000
    max_bal = max(balances) * 1.1
    min_bal = min(balances) * 0.95

    def x_pos(i): return pad_left + (i + 0.5) * chart_w / n
    def bar_h(pnl): return chart_h * abs(pnl) / max_pnl * 0.45
    def line_y(bal):
        r = (bal - min_bal) / (max_bal - min_bal) if max_bal != min_bal else 0.5
        return pad_top + chart_h * 0.5 + (1 - r) * chart_h * 0.45

    bg = "#1a1a2e"; grid = "#2a2a4a"; pos = "#00d4aa"; neg = "#ff4757"
    gold = "#ffd700"; text = "#e0e0e0"; axis = "#4a4a6a"

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="{bg}"/>',
        f'<text x="{width // 2}" y="30" text-anchor="middle" fill="{text}" '
        f'font-size="16" font-family="Arial" font-weight="bold">FootyClaw — 投注账本走势</text>',
    ]
    # Grid lines
    mid_y = pad_top + chart_h * 0.5
    zero_y = pad_top + chart_h * 0.48
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        y = pad_top + chart_h * 0.5 + (1 - frac) * chart_h * 0.45
        bal_val = min_bal + frac * (max_bal - min_bal)
        lines += [
            f'<line x1="{pad_left}" y1="{y:.1f}" x2="{width - pad_right}" y2="{y:.1f}" '
            f'stroke="{grid}" stroke-width="1" stroke-dasharray="4,4"/>',
            f'<text x="{pad_left - 5}" y="{y + 4:.1f}" text-anchor="end" fill="{axis}" '
            f'font-size="10" font-family="Arial">¥{int(bal_val):,}</text>',
        ]
    lines += [
        f'<line x1="{pad_left}" y1="{mid_y}" x2="{width - pad_right}" y2="{mid_y}" '
        f'stroke="{axis}" stroke-width="1"/>',
        f'<line x1="{pad_left}" y1="{zero_y}" x2="{width - pad_right}" y2="{zero_y}" '
        f'stroke="{axis}" stroke-width="0.5" stroke-dasharray="2,2"/>',
    ]
    # Bars
    for i, d in enumerate(days):
        x = x_pos(i) - bar_w / 2
        h = bar_h(d["pnl"])
        color = pos if d["pnl"] >= 0 else neg
        bar_top = zero_y - h if d["pnl"] >= 0 else zero_y
        label = (f'+¥{d["pnl"]:,}' if d["pnl"] >= 0 else f'¥{d["pnl"]:,}')
        label_y = bar_top - 4 if d["pnl"] >= 0 else bar_top + h + 12
        lines += [
            f'<rect x="{x:.1f}" y="{bar_top:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
            f'fill="{color}" rx="2"/>',
            f'<text x="{x_pos(i):.1f}" y="{label_y:.1f}" text-anchor="middle" '
            f'fill="{color}" font-size="9" font-family="Arial">{label}</text>',
        ]
    # Line chart
    pts = [(x_pos(i), line_y(d["balance"])) for i, d in enumerate(days)]
    lines.append(
        f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" '
        f'fill="none" stroke="{gold}" stroke-width="2.5" stroke-linejoin="round"/>'
    )
    for i, (d, (px, py)) in enumerate(zip(days, pts)):
        lines.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{gold}" '
            f'stroke="{bg}" stroke-width="1.5"/>'
        )
        if i == 0 or i == len(days) - 1 or i % max(1, len(days) // 5) == 0:
            lines.append(
                f'<text x="{px:.1f}" y="{py - 8:.1f}" text-anchor="middle" '
                f'fill="{gold}" font-size="9" font-family="Arial">¥{d["balance"]:,}</text>'
            )
    # X labels
    for i, d in enumerate(days):
        lines += [
            f'<text x="{x_pos(i):.1f}" y="{height - pad_bot + 15:.1f}" text-anchor="middle" '
            f'fill="{text}" font-size="9" font-family="Arial">D{d["day"]}</text>',
            f'<text x="{x_pos(i):.1f}" y="{height - pad_bot + 27:.1f}" text-anchor="middle" '
            f'fill="{axis}" font-size="8" font-family="Arial">{d["date"][5:]}</text>',
        ]
    # Legend
    lx, ly = pad_left, height - 15
    lines += [
        f'<rect x="{lx}" y="{ly - 8}" width="12" height="8" fill="{pos}" rx="1"/>',
        f'<text x="{lx + 15}" y="{ly}" fill="{text}" font-size="10" font-family="Arial">盈利</text>',
        f'<rect x="{lx + 60}" y="{ly - 8}" width="12" height="8" fill="{neg}" rx="1"/>',
        f'<text x="{lx + 75}" y="{ly}" fill="{text}" font-size="10" font-family="Arial">亏损</text>',
        f'<line x1="{lx + 130}" y1="{ly - 4}" x2="{lx + 145}" y2="{ly - 4}" '
        f'stroke="{gold}" stroke-width="2"/>',
        f'<text x="{lx + 148}" y="{ly}" fill="{text}" font-size="10" font-family="Arial">资金曲线</text>',
        '</svg>',
    ]
    return "\n".join(lines)


def generate_ascii(days, width=60):
    """生成纯文本 ASCII 柱状图（备用方案，纯 ASCII 字符，无编码问题）"""
    if not days:
        return "(no data)"
    max_pnl = max(abs(d["pnl"]) for d in days) or 1
    bar_max = width - 20  # 留出标签空间
    lines = ["FootyClaw Betting Trend (ASCII)", "=" * width]
    for d in days:
        bar_len = int(abs(d["pnl"]) / max_pnl * bar_max)
        if d["pnl"] >= 0:
            bar = "#" * bar_len
            lines.append(f'D{d["day"]:>2} {d["date"][5:]} |{bar} +{d["pnl"]:,}')
        else:
            bar = "-" * bar_len
            lines.append(f'D{d["day"]:>2} {d["date"][5:]} |{bar} {d["pnl"]:,}')
    lines.append("=" * width)
    lines.append("Balance:")
    for d in days:
        lines.append(f'  D{d["day"]:>2}: {d["balance"]:,}')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="FootyClaw 账本图表生成器（零文件写入）")
    parser.add_argument("--ascii", action="store_true",
                        help="输出纯文本 ASCII 图表而非 Base64 图片")
    args = parser.parse_args()

    # 从 stdin 读取 Markdown 账本
    text = sys.stdin.read()
    if not text.strip():
        print("[ERROR] stdin 为空，请传入 Markdown 账本内容", file=sys.stderr)
        sys.exit(1)

    days = parse_ledger(text)
    if not days:
        print("[ERROR] 未能解析到 Day 记录，请检查 Markdown 表格格式", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] 解析到 {len(days)} 条记录（Day{days[0]['day']} ~ Day{days[-1]['day']}）",
          file=sys.stderr)

    if args.ascii:
        # 纯文本 ASCII 图表
        print(generate_ascii(days))
    else:
        # SVG → Base64 → <img> 标签
        svg = generate_svg(days)
        b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        print(f'<img src="data:image/svg+xml;base64,{b64}" '
              f'alt="FootyClaw 投注走势" width="900" height="520" />')


if __name__ == "__main__":
    main()
