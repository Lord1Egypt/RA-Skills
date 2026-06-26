#!/usr/bin/env python3
"""
Expense Charts — Visual Chart Generator (PNG output)
Generates PNG charts (pie, bar, line) + full HTML report, sends as image.
Run: python3 charts.py <pie|bar|line|report|png> [json_args]
"""

import json, sys, math, subprocess, os, io, base64
from typing import Optional
from datetime import datetime
from pathlib import Path

LEDGER_DIR = Path.home() / ".qclaw" / "workspace" / "expense-ledger"
CHART_DIR  = LEDGER_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = LEDGER_DIR / "config.json"

# ─── Palette ────────────────────────────────────────────────────────────────

CURRENCY_SYMBOL = {
    "CNY": "¥",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

CATEGORY_COLORS = {
    "food":"#FF6B6B","shopping":"#4ECDC4","housing":"#45B7D1",
    "transport":"#96CEB4","comm":"#FFEAA7","medical":"#DDA0DD",
    "social":"#98D8C8","entertain":"#F7DC6F","education":"#BB8FCE",
    "childcare":"#85C1E9","travel":"#F0A500","investment":"#2ECC71",
    "other":"#BDC3C7",
}
CATEGORY_EMOJI = {
    "food":"🍽️","shopping":"🛒","housing":"🏠","transport":"🚗",
    "comm":"📡","medical":"🏥","social":"❤️","entertain":"🎮",
    "education":"📚","childcare":"👶","travel":"✈️","investment":"📈","other":"📦",
}
CAT_ZH = {
    "food":"餐饮","shopping":"购物","housing":"住房","transport":"交通",
    "comm":"通讯","medical":"医疗","social":"人情","entertain":"娱乐",
    "education":"学习","childcare":"育儿","travel":"旅行",
    "investment":"投资","other":"其他",
}
CAT_EN = {
    "food":"Food & Drink","shopping":"Shopping","housing":"Housing",
    "transport":"Transport","comm":"Communication","medical":"Medical",
    "social":"Social","entertain":"Entertainment","education":"Education",
    "childcare":"Baby & Child","travel":"Travel",
    "investment":"Investment","other":"Others",
}

# ─── SVG generators ─────────────────────────────────────────────────────────

def polar_xy(cx, cy, r, deg):
    rad = math.radians(deg - 90)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)

def arc_path(cx, cy, r, start, end):
    if end - start >= 359.5:
        return f"M {cx} {cy-r} A {r} {r} 0 1 1 {cx-0.001} {cy-r} Z"
    x1,y1 = polar_xy(cx,cy,r,start)
    x2,y2 = polar_xy(cx,cy,r,end)
    large = 1 if (end-start) > 180 else 0
    return f"M {cx} {cy} L {x1} {1} A {r} {r} 0 {large} 1 {x2} {y2} Z"

def svg_pie(data, title, currency_symbol="¥", size=480):
    total = sum(data.values())
    if total == 0: return None
    W = H = size
    cx = cy = size//2
    outer_r, inner_r = size*0.36, size*0.22
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    svg.append('<defs><style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}</style></defs>')
    svg.append(f'<rect width="{W}" height="{H}" fill="white" rx="16"/>')
    svg.append(f'<text x="{cx}" y="36" text-anchor="middle" font-size="15" font-weight="700" fill="#2C3E50">{title}</text>')
    svg.append(f'<text x="{cx}" y="58" text-anchor="middle" font-size="20" font-weight="800" fill="#2C3E50">{currency_symbol}{total:,.2f}</text>')
    sorted_data = sorted(data.items(), key=lambda x:-x[1])
    angle = 0
    for cat, amt in sorted_data:
        pct = amt/total*100
        sweep = pct*3.6
        color = CATEGORY_COLORS.get(cat,"#BDC3C7")
        emoji = CATEGORY_EMOJI.get(cat,"📦")
        label = CAT_ZH.get(cat,cat)
        path = arc_path(cx, cy+24, outer_r, angle, angle+sweep-0.5)
        if sweep > 1.5:
            svg.append(f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2"><title>{emoji}{label}: {currency_symbol}{amt:,.2f} ({pct:.1f}%)</title></path>')
        angle += sweep
    svg.append(f'<circle cx="{cx}" cy="{cy+24}" r="{inner_r}" fill="white"/>')
    svg.append(f'<text x="{cx}" y="{cy+18}" text-anchor="middle" font-size="12" font-weight="600" fill="#888">{len(data)} 类</text>')
    svg.append(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="11" fill="#aaa">categories</text>')
    svg.append('</svg>')
    return '\n'.join(svg)

def svg_bar(data, title, currency_symbol="¥", width=560, bar_h=36, pad=50):
    total = sum(data.values())
    if total == 0: return None
    sorted_data = sorted(data.items(), key=lambda x:-x[1])
    max_v = sorted_data[0][1]
    H = len(sorted_data)*(bar_h+8) + pad + 28
    bw_max = width - 160
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}">']
    svg.append('<defs><style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}</style></defs>')
    svg.append(f'<rect width="{width}" height="{H}" fill="white" rx="12"/>')
    svg.append(f'<text x="12" y="28" font-size="14" font-weight="700" fill="#2C3E50">{title}</text>')
    for g in range(5):
        x = pad + (bw_max/4)*g
        y_top = pad+4
        svg.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{H-24}" stroke="#f0f0f0" stroke-width="1"/>')
        svg.append(f'<text x="{x-4}" y="{H-8}" text-anchor="middle" font-size="10" fill="#bbb">{currency_symbol}{max_v/4*g:,.0f}</text>')
    y = pad
    for cat, amt in sorted_data:
        color = CATEGORY_COLORS.get(cat,"#BDC3C7")
        emoji = CATEGORY_EMOJI.get(cat,"📦")
        label = CAT_ZH.get(cat,cat)
        pct = amt/total*100
        bw = max(4, (amt/max_v)*bw_max)
        svg.append(f'<text x="6" y="{y+bar_h*0.62}" font-size="13" fill="#333">{emoji} {label}</text>')
        svg.append(f'<rect x="{pad}" y="{y+4}" width="{bw_max}" height="{bar_h-6}" rx="4" fill="#f5f5f5"/>')
        svg.append(f'<rect x="{pad}" y="{y+4}" width="{bw}" height="{bar_h-6}" rx="4" fill="{color}"><title>{label}: {currency_symbol}{amt:,.2f}</title></rect>')
        svg.append(f'<text x="{pad+bw+6}" y="{y+bar_h*0.62}" font-size="12" fill="#555">{currency_symbol}{amt:,.0f} ({pct:.0f}%)</text>')
        y += bar_h+8
    svg.append('</svg>')
    return '\n'.join(svg)

def svg_line(daily, title, currency_symbol="¥", width=560, height=200):
    if not daily: return None
    sorted_days = sorted(daily.items())
    vals = [v for _,v in sorted_days]
    max_v = max(vals) if vals else 1
    pad_l,pad_r,pad_t,pad_b = 50,16,32,36
    cw = width-pad_l-pad_r
    ch = height-pad_t-pad_b
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}">']
    svg.append('<defs><style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}</style></defs>')
    svg.append(f'<rect width="{width}" height="{height}" fill="white" rx="12"/>')
    svg.append(f'<text x="{pad_l}" y="22" font-size="13" font-weight="700" fill="#2C3E50">{title}</text>')
    n = len(sorted_days)
    sx = cw/max(n-1,1) if n>1 else 0
    for g in range(5):
        y = pad_t + (ch/4)*g
        v = max_v - max_v/4*g
        svg.append(f'<line x1="{pad_l}" y1="{y}" x2="{width-pad_r}" y2="{y}" stroke="#eee" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l-5}" y="{y+4}" text-anchor="end" font-size="10" fill="#bbb">{currency_symbol}{v:,.0f}</text>')
    if n > 1:
        pts = [f"{pad_l+i*sx:.1f},{pad_t+ch-v/max_v*ch:.1f}" for i,(_,v) in enumerate(sorted_days)]
        area = f"{pad_l},{pad_t+ch} "+" ".join(pts)+f" {pad_l+(n-1)*sx:.1f},{pad_t+ch}"
        svg.append(f'<polygon points="{area}" fill="#4ECDC4" opacity="0.12"/>')
        svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#4ECDC4" stroke-width="2.5" stroke-linejoin="round"/>')
        for i,(day,v) in enumerate(sorted_days):
            x = pad_l+i*sx
            y = pad_t+ch-v/max_v*ch
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#4ECDC4"/>')
            if n<=8 or i%(max(1,n//6))==0:
                svg.append(f'<text x="{x:.1f}" y="{height-8}" text-anchor="middle" font-size="9" fill="#bbb">{day[5:]}</text>')
    svg.append('</svg>')
    return '\n'.join(svg)

# ─── HTML report ─────────────────────────────────────────────────────────────

def build_html(report, period_label, lang="zh"):
    by_cat = report.get("by_category", {})
    daily = report.get("daily", {})
    total = report.get("total", 0)
    top = report.get("top_category","")
    top_pct = report.get("top_pct", 0)
    currency_code = (report.get("currency") or "CNY").upper()
    currency_symbol = CURRENCY_SYMBOL.get(currency_code, "¥" if currency_code == "CNY" else "")
    emoji_top = CATEGORY_EMOJI.get(top,"📊")
    top_zh = CAT_ZH.get(top, top)
    top_en = CAT_EN.get(top, top)
    pie  = svg_pie(by_cat,  "📊 支出占比 | Category %", currency_symbol=currency_symbol)
    bar  = svg_bar(by_cat,  "📊 分类明细 | Breakdown", currency_symbol=currency_symbol)
    line = svg_line(daily,  "📊 日趋势 | Daily Trend", currency_symbol=currency_symbol)
    rows = []
    for cat, amt in sorted(by_cat.items(), key=lambda x:-x[1]):
        pct = amt/total*100
        rows.append(f'<tr><td>{CATEGORY_EMOJI.get(cat,"📦")} {CAT_ZH.get(cat,cat)}</td><td style="text-align:right">{currency_symbol}{amt:,.2f}</td><td style="text-align:right">{pct:.1f}%</td></tr>')
    rows_html = '\n'.join(rows)
    return f"""<!DOCTYPE html><html lang="{lang}"><head>
<meta charset="UTF-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f8f9fa;padding:12px}}
.card{{background:white;border-radius:16px;padding:18px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.row{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}}
.box{{background:white;border-radius:16px;padding:14px;box-shadow:0 2px 12px rgba(0,0,0,.08);text-align:center;flex:1 1 280px}}
.hl{{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:18px;color:white;text-align:center}}
table{{width:100%;border-collapse:collapse;margin-top:8px}}
th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid #f0f0f0;font-size:13px}}
th{{color:#888;font-weight:500}}
.ft{{text-align:center;font-size:11px;color:#ccc;margin-top:10px}}
</style></head><body>
<div class="card" style="text-align:center">
  <div style="font-size:16px;font-weight:700;color:#2C3E50">{period_label}</div>
  <div style="font-size:30px;font-weight:800;color:#2C3E50;margin:6px 0">{currency_symbol}{total:,.2f}</div>
  <div style="font-size:12px;color:#888">{report.get('count',0)} 笔 · {len(by_cat)} 个分类</div>
</div>
<div class="hl">
  <div style="font-size:12px;opacity:.85">🏆 最高消费 | Top Category</div>
  <div style="font-size:22px;font-weight:800;margin:4px 0">{emoji_top} {top_zh}</div>
  <div style="font-size:13px;opacity:.8">{top_en} · {top_pct:.1f}%</div>
</div>
<div class="row">
  <div class="box">{pie or ''}</div>
  <div class="box">{bar or ''}</div>
</div>
<div class="box">{line or ''}</div>
<div class="card">
  <table>{rows_html}</table>
</div>
<div class="ft">Accounting Assistant / 记账助手 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</body></html>"""

# ─── PNG conversion via macOS tools ─────────────────────────────────────────

def html_to_png(html_path: Path) -> Optional[Path]:
    """Convert HTML to PNG using macOS built-in tools."""
    tmp_png = html_path.with_suffix('.png')
    # Try qlmanage first (most reliable on macOS)
    try:
        r = subprocess.run(
            ['qlmanage', '-t', '-s', '900', '-o', str(tmp_png.parent), str(html_path)],
            capture_output=True, timeout=15
        )
        potential = tmp_png.parent / f'{html_path.name}.png'
        if potential.exists():
            return potential
        if tmp_png.exists():
            return tmp_png
    except Exception as e:
        pass
    # Fallback: use Safari/webkit
    try:
        r = subprocess.run(
            ['screencapture', '-x', '-t', 'png', str(tmp_png)],
            capture_output=True, timeout=5
        )
        if tmp_png.exists():
            return tmp_png
    except:
        pass
    return None

def png_b64_to_data_uri(png_b64: str) -> str:
    return f"data:image/png;base64,{png_b64}"

def png_b64_to_markdown(png_b64: str, alt: str = "chart") -> str:
    # Many chat UIs render data-URI images; if not, the caller can still use png_b64/png_path.
    return f"![{alt}]({png_b64_to_data_uri(png_b64)})"

def svg_to_png(svg_text: str, size: int = 600) -> Optional[bytes]:
    """Convert SVG string to PNG bytes using macOS tools."""
    tmp_svg = CHART_DIR / f'_tmp_{datetime.now().strftime("%H%M%S")}.svg'
    tmp_png = tmp_svg.with_suffix('.png')
    tmp_svg.write_text(svg_text, encoding='utf-8')
    try:
        r = subprocess.run(
            ['qlmanage', '-t', '-s', str(size), '-o', str(tmp_png.parent), str(tmp_svg)],
            capture_output=True, timeout=15
        )
        potential = tmp_png.parent / f'{tmp_svg.name}.png'
        if potential.exists():
            return potential.read_bytes()
        if tmp_png.exists():
            return tmp_png.read_bytes()
    except: pass
    finally:
        tmp_svg.unlink(exist_ok=True)
        # qlmanage may output to either tmp_png or f"{tmp_svg.name}.png"
        try:
            if tmp_png.exists():
                tmp_png.unlink()
        except Exception:
            pass
        try:
            potential = tmp_png.parent / f'{tmp_svg.name}.png'
            if potential.exists():
                potential.unlink()
        except Exception:
            pass
    return None

def svg_to_b64(svg_text: str, size=600) -> str:
    """Convert SVG to base64 PNG for embedding."""
    png = svg_to_png(svg_text, size)
    if png:
        return base64.b64encode(png).decode()
    return ""

def get_default_currency_code() -> str:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                config = json.load(f)
            return str(config.get("default_currency", "CNY")).upper()
        except Exception:
            pass
    return "CNY"

# ─── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: charts.py <pie|bar|line|report|png> [json_args]"}))
        sys.exit(1)

    cmd  = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    lang = args.get("lang", "zh")
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")

    if cmd == "report":
        report = args.get("report", {})
        period = args.get("period_label", "支出报表")
        html   = build_html(report, period, lang)
        path   = CHART_DIR / f"report_{ts}.html"
        path.write_text(html, encoding='utf-8')
        # Try to also make PNG
        png_path = html_to_png(path)
        result = {
            "ok": True,
            "type": "report",
            "html_path": str(path),
            "count": report.get('count', 0),
            "total": report.get('total', 0),
            "currency": report.get("currency", "CNY"),
        }
        if png_path:
            result["png_path"] = str(png_path)
            png_b64 = base64.b64encode(png_path.read_bytes()).decode()
            result["png_b64"] = png_b64
            result["png_data_uri"] = png_b64_to_data_uri(png_b64)
            result["png_markdown"] = png_b64_to_markdown(png_b64, alt="expense report")
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "png":
        report = args.get("report", {})
        period = args.get("period_label", "支出报表")
        html   = build_html(report, period, lang)
        path   = CHART_DIR / f"chart_{ts}.html"
        path.write_text(html, encoding='utf-8')
        png_path = html_to_png(path)
        result = {"ok": True, "html_path": str(path), "currency": report.get("currency", "CNY")}
        if png_path:
            result["png_path"] = str(png_path)
            png_b64 = base64.b64encode(png_path.read_bytes()).decode()
            result["png_b64"] = png_b64
            result["png_data_uri"] = png_b64_to_data_uri(png_b64)
            result["png_markdown"] = png_b64_to_markdown(png_b64, alt="expense chart")
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "pie":
        data  = args.get("data", {})
        title = args.get("title", "支出占比")
        currency_code = (args.get("currency") or get_default_currency_code()).upper()
        currency_symbol = CURRENCY_SYMBOL.get(currency_code, "¥" if currency_code == "CNY" else "")
        svg   = svg_pie(data, title, currency_symbol=currency_symbol)
        if svg:
            png_bytes = svg_to_png(svg, 480)
            if png_bytes:
                png_path = CHART_DIR / f"pie_{ts}.png"
                try:
                    png_path.write_bytes(png_bytes)
                except Exception:
                    png_path = None
                png_b64 = base64.b64encode(png_bytes).decode()
                b64 = png_b64  # backward-compatible
            else:
                b64 = svg_to_b64(svg, 480)
                png_b64 = b64
            result = {
                "ok": True,
                "type": "pie",
                "svg": svg,
                "b64": b64,  # backward-compatible
                "png_b64": png_b64,
                "png_data_uri": png_b64_to_data_uri(png_b64),
                "png_markdown": png_b64_to_markdown(png_b64, alt=title),
                "currency": currency_code,
            }
            if png_bytes and 'png_path' in locals() and png_path:
                result["png_path"] = str(png_path)
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(json.dumps({"ok": False, "error": "No data"}))

    elif cmd == "bar":
        data  = args.get("data", {})
        title = args.get("title", "分类明细")
        currency_code = (args.get("currency") or get_default_currency_code()).upper()
        currency_symbol = CURRENCY_SYMBOL.get(currency_code, "¥" if currency_code == "CNY" else "")
        svg   = svg_bar(data, title, currency_symbol=currency_symbol)
        if svg:
            png_bytes = svg_to_png(svg, 560)
            if png_bytes:
                png_path = CHART_DIR / f"bar_{ts}.png"
                try:
                    png_path.write_bytes(png_bytes)
                except Exception:
                    png_path = None
                png_b64 = base64.b64encode(png_bytes).decode()
                b64 = png_b64  # backward-compatible
            else:
                b64 = svg_to_b64(svg, 560)
                png_b64 = b64
            result = {
                "ok": True,
                "type": "bar",
                "svg": svg,
                "b64": b64,  # backward-compatible
                "png_b64": png_b64,
                "png_data_uri": png_b64_to_data_uri(png_b64),
                "png_markdown": png_b64_to_markdown(png_b64, alt=title),
                "currency": currency_code,
            }
            if png_bytes and 'png_path' in locals() and png_path:
                result["png_path"] = str(png_path)
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(json.dumps({"ok": False, "error": "No data"}))

    elif cmd == "line":
        data  = args.get("data", {})
        title = args.get("title", "日趋势")
        currency_code = (args.get("currency") or get_default_currency_code()).upper()
        currency_symbol = CURRENCY_SYMBOL.get(currency_code, "¥" if currency_code == "CNY" else "")
        svg   = svg_line(data, title, currency_symbol=currency_symbol)
        if svg:
            png_bytes = svg_to_png(svg, 560)
            if png_bytes:
                png_path = CHART_DIR / f"line_{ts}.png"
                try:
                    png_path.write_bytes(png_bytes)
                except Exception:
                    png_path = None
                png_b64 = base64.b64encode(png_bytes).decode()
                b64 = png_b64  # backward-compatible
            else:
                b64 = svg_to_b64(svg, 560)
                png_b64 = b64
            result = {
                "ok": True,
                "type": "line",
                "svg": svg,
                "b64": b64,  # backward-compatible
                "png_b64": png_b64,
                "png_data_uri": png_b64_to_data_uri(png_b64),
                "png_markdown": png_b64_to_markdown(png_b64, alt=title),
                "currency": currency_code,
            }
            if png_bytes and 'png_path' in locals() and png_path:
                result["png_path"] = str(png_path)
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(json.dumps({"ok": False, "error": "No data"}))

    else:
        print(json.dumps({"error": f"Unknown: {cmd}"}))
        sys.exit(1)
