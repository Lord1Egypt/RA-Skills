#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透系统 — 健康度趋势追踪报告生成器 (dlt_health_trend.py)

读取 dlt_healthcheck_all.py 每次运行追加的:
  - health_history.csv   (每次一行: 时间戳/总项/通过/阻断/运维告警/耗时/状态)
  - health_latest.json   (最近一次逐检查明细)
生成**零依赖、自包含**的 HTML 趋势报告(内联 SVG, 不引用任何外部 JS/CDN),
落到桌面(保底可双击打开)与项目根目录, 并打印绝对路径。

价值: 把"每次只看当下全绿"升级为"长期退化可预警" ——
  通过率持续下滑、某项耗时持续攀升、某运维告警开始反复出现, 都能在图表上提前看见。

用法:
  python dlt_health_trend.py
"""
import os
import sys
import csv
import json

def _detect_project_root():
    """动态解析项目根(健康趋势落盘位置), 不写死用户名。
    优先级: ① 环境变量 DLT_PROJECT_ROOT; ② 本文件位置推导(Root/lib 或 SKILL/scripts/lib 皆为其部署根)。"""
    env = os.environ.get("DLT_PROJECT_ROOT")
    if env and os.path.isdir(env):
        return env
    here = os.path.dirname(os.path.abspath(__file__))  # lib/
    for cand in (os.path.dirname(here), os.path.dirname(os.path.dirname(here))):
        if (os.path.exists(os.path.join(cand, "lib", "dlt_smart.py")) or
                os.path.exists(os.path.join(cand, "dlt_smart.py"))):
            return cand
    return os.path.dirname(here)  # 兜底: lib 的父级


PROJECT_ROOT = _detect_project_root()
HISTORY_CSV = os.path.join(PROJECT_ROOT, "health_history.csv")
LATEST_JSON = os.path.join(PROJECT_ROOT, "health_latest.json")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def desktop_path():
    """桌面目录兜底: Desktop -> 桌面 -> Documents -> ~ (兼容中英文系统)。"""
    candidates = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "桌面"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.expanduser("~"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return os.path.expanduser("~")


def load_history():
    rows = []
    if not os.path.exists(HISTORY_CSV):
        return rows
    with open(HISTORY_CSV, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            try:
                r["total"] = int(r["total"])
                r["passed"] = int(r["passed"])
                r["blockers"] = int(r["blockers"])
                r["warns"] = int(r["warns"])
                r["duration_sec"] = float(r["duration_sec"])
            except (ValueError, KeyError):
                continue
            rows.append(r)
    return rows


def load_latest():
    if not os.path.exists(LATEST_JSON):
        return None
    try:
        return json.load(open(LATEST_JSON, encoding="utf-8"))
    except Exception:
        return None


def svg_line_chart(rows, w=720, h=240):
    """内联 SVG 通过率折线图(0-100%), 无外部依赖。"""
    if not rows:
        return "<p style='color:#888'>暂无历史数据</p>"
    pad_l, pad_r, pad_t, pad_b = 44, 16, 16, 28
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    n = len(rows)
    x = lambda i: pad_l + (plot_w * i / max(1, n - 1)) if n > 1 else pad_l + plot_w / 2
    y = lambda v: pad_t + plot_h * (1 - v / 100.0)

    # 网格 + Y 轴标签(0/50/100)
    grid = ""
    for gv in (0, 50, 100):
        gy = y(gv)
        grid += f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{w-pad_r}" y2="{gy:.1f}" stroke="#e3e3e3"/>'
        grid += f'<text x="{pad_l-6}" y="{gy+4:.1f}" text-anchor="end" font-size="10" fill="#888">{gv}%</text>'

    pts = []
    for i, r in enumerate(rows):
        rate = (r["passed"] / r["total"] * 100.0) if r["total"] else 0.0
        pts.append((x(i), y(rate), rate))
    poly = " ".join(f"{px:.1f},{py:.1f}" for px, py, _ in pts)
    dots = "".join(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{("#2e8b57" if r["status"]=="OK" else ("#e50012" if r["status"]=="FAIL" else "#e8a317"))}"/>'
        for (px, py, _), r in zip(pts, rows)
    )
    # X 轴首尾时间标签
    first_ts = rows[0]["timestamp"][5:16]
    last_ts = rows[-1]["timestamp"][5:16]
    xlabels = (
        f'<text x="{pad_l}" y="{h-8}" font-size="10" fill="#888">{first_ts}</text>'
        f'<text x="{w-pad_r}" y="{h-8}" text-anchor="end" font-size="10" fill="#888">{last_ts}</text>'
    )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">'
        f'{grid}'
        f'<polyline points="{poly}" fill="none" stroke="#1f6feb" stroke-width="2"/>'
        f'{dots}{xlabels}</svg>'
    )


def svg_check_grid(checks, cols=4):
    """逐检查状态彩色网格(最新一次)。"""
    if not checks:
        return "<p style='color:#888'>暂无明细</p>"
    cell_w, cell_h = 168, 30
    rows = (len(checks) + cols - 1) // cols
    w = cols * cell_w
    h = rows * cell_h
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    for i, c in enumerate(checks):
        r, col = divmod(i, cols)
        cx, cy = col * cell_w, r * cell_h
        color = "#2e8b57" if c["ok"] else ("#e50012" if c["blocking"] else "#e8a317")
        label = c["name"][:14]
        out.append(f'<rect x="{cx+2}" y="{cy+2}" width="{cell_w-4}" height="{cell_h-4}" rx="4" fill="{color}" opacity="0.85"/>')
        out.append(f'<text x="{cx+cell_w/2:.0f}" y="{cy+cell_h/2+4:.0f}" text-anchor="middle" font-size="11" fill="#fff">{i+1}.{label}</text>')
    out.append("</svg>")
    return "".join(out)


def build_html(rows, latest):
    n = len(rows)
    last = rows[-1] if rows else None
    last_status = last["status"] if last else "N/A"
    status_color = {"OK": "#2e8b57", "WARN": "#e8a317", "FAIL": "#e50012"}.get(last_status, "#888")
    avg_dur = (sum(r["duration_sec"] for r in rows) / n) if n else 0.0
    min_rate = min((r["passed"] / r["total"] * 100.0) for r in rows) if rows else 0.0

    # 历史表格(最近 15 条, 倒序)
    table_rows = ""
    for r in reversed(rows[-15:]):
        sc = {"OK": "#2e8b57", "WARN": "#e8a317", "FAIL": "#e50012"}.get(r["status"], "#888")
        table_rows += (
            f"<tr><td>{r['timestamp']}</td><td>{r['passed']}/{r['total']}</td>"
            f"<td>{r['blockers']}</td><td>{r['warns']}</td>"
            f"<td>{r['duration_sec']:.1f}s</td>"
            f"<td style='color:{sc};font-weight:bold'>{r['status']}</td></tr>"
        )

    checks_html = svg_check_grid(latest["checks"]) if latest else "<p style='color:#888'>暂无</p>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>大乐透系统 · 健康度趋势报告</title>
<style>
  body{{font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;background:#f5f6f8;color:#222;margin:0;padding:24px}}
  .wrap{{max-width:860px;margin:0 auto;background:#fff;border-radius:10px;padding:24px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
  h1{{font-size:20px;margin:0 0 4px}}
  .sub{{color:#888;font-size:13px;margin-bottom:18px}}
  .cards{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}}
  .card{{flex:1;min-width:140px;background:#fafbfc;border:1px solid #eee;border-radius:8px;padding:14px}}
  .card .v{{font-size:22px;font-weight:700}}
  .card .k{{font-size:12px;color:#888;margin-top:2px}}
  .sec{{margin:22px 0 8px;font-size:15px;font-weight:600;border-left:4px solid #1f6feb;padding-left:8px}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th,td{{padding:6px 8px;text-align:center;border-bottom:1px solid #eee}}
  th{{background:#f0f3f7;color:#555}}
  .grid-note{{font-size:12px;color:#888;margin-top:6px}}
</style></head>
<body><div class="wrap">
  <h1>大乐透系统 · 健康度趋势报告</h1>
  <div class="sub">数据源: health_history.csv + health_latest.json · 生成于 {__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}</div>
  <div class="cards">
    <div class="card"><div class="v" style="color:{status_color}">{last_status}</div><div class="k">最近一次状态</div></div>
    <div class="card"><div class="v">{n}</div><div class="k">累计运行次数</div></div>
    <div class="card"><div class="v">{min_rate:.1f}%</div><div class="k">历史最低通过率</div></div>
    <div class="card"><div class="v">{avg_dur:.1f}s</div><div class="k">平均自检耗时</div></div>
  </div>

  <div class="sec">通过率趋势 (每次运行)</div>
  {svg_line_chart(rows)}

  <div class="sec">最近一次 · 逐检查状态</div>
  {checks_html}
  <div class="grid-note">绿=通过 · 红=正确性类失败(阻断交付) · 橙=运维告警(不阻断)</div>

  <div class="sec">历史记录 (最近 {min(15, n)} 次)</div>
  <table><thead><tr><th>时间</th><th>通过</th><th>阻断</th><th>告警</th><th>耗时</th><th>状态</th></tr></thead>
  <tbody>{table_rows}</tbody></table>

  <div class="grid-note" style="margin-top:18px">
    说明: 本报告由 dlt_health_trend.py 生成, 源于 dlt_healthcheck_all.py 每次运行的回归护栏结果。
    任一检查从绿转红/橙, 或通过率/耗时出现劣化趋势, 即应复核对应模块。
  </div>
</div></body></html>"""
    return html


def main():
    rows = load_history()
    latest = load_latest()
    html = build_html(rows, latest)

    out_name = "health_trend_report.html"
    targets = [
        os.path.join(desktop_path(), out_name),
        os.path.join(PROJECT_ROOT, out_name),
    ]
    written = []
    for t in targets:
        try:
            with open(t, "w", encoding="utf-8") as f:
                f.write(html)
            written.append(t)
        except Exception as e:
            print(f"  [warn] 写入失败 {t}: {e}")
    if not written:
        print("  ❌ 趋势报告未能写入任何位置")
        return 1
    print(f"  ✅ 健康度趋势报告已生成 ({len(rows)} 条历史):")
    for w in written:
        print(f"     -> {w}")
    print(f"  REPORT_DESKTOP_PATH:{written[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
