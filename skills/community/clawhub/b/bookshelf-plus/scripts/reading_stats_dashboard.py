#!/usr/bin/env python3
"""
reading_stats_dashboard.py — 閱讀統計視覺化儀表板
生成精美的 HTML 報告，支援：年度熱力圖、進度環、閱讀趨勢圖、分類分布
"""

import json
import argparse
import datetime
from pathlib import Path

DATE_FMT = "%Y-%m-%d"

RESERVED_COLORS = {
    "python":       "#3776ab",
    "javascript":   "#f7df1e",
    "typescript":   "#3178c6",
    "rust":         "#ce422b",
    "go":           "#00add8",
    "swift":        "#fa7343",
    "kotlin":       "#7f52ff",
    "java":         "#ed8b00",
    "c#":           "#239120",
    "vue":          "#42b883",
    "react":        "#61dafb",
    "django":       "#092e20",
    "flask":        "#000000",
    "sql":          "#e38c00",
    "aws":          "#ff9900",
    "devops":       "#ff6363",
    "商業":         "#4a90d9",
    "小說":         "#e74c3c",
    "技術":         "#27ae60",
    "散文":         "#f39c12",
    "歷史":         "#8e44ad",
    "童書":         "#e91e63",
    "投資":         "#00bcd4",
    "心理":         "#ff5722",
    "self-default": "#95a5a6",
}


# ── 熱力圖 ───────────────────────────────────────────────────────────────────

def _cell_color(pages: int) -> str:
    if pages == 0:   return "#ebedf0"
    if pages < 10:  return "#c6e48b"
    if pages < 30:  return "#7bc96f"
    if pages < 60:  return "#239a3b"
    return "#196127"


def _build_heatmap(year: int, daily_reading: dict) -> str:
    """建立全年熱力圖 HTML，回傳字串"""
    start = datetime.date(year, 1, 1)
    start -= datetime.timedelta(days=start.weekday())   # 對齊週一

    def cell(day: datetime.date) -> str:
        pages = daily_reading.get(day.isoformat(), 0)
        title = day.strftime(DATE_FMT) + ": " + str(pages) + "頁"
        return '<div class="h-cell" style="background:' + _cell_color(pages) + \
               '" title="' + title + '"></div>'

    weeks = []
    cur = start
    for _ in range(53):
        week_cells = "".join(cell(cur + datetime.timedelta(days=d)) for d in range(7))
        weeks.append('<div class="h-week">' + week_cells + '</div>')
        cur += datetime.timedelta(weeks=1)

    cols = []
    for i in range(4):
        chunk = "".join(weeks[i * 13:(i + 1) * 13])
        cols.append('<div class="h-col">' + chunk + '</div>')
    return "".join(cols)


# ── 進度環 ───────────────────────────────────────────────────────────────────

def _build_rings(top_books: list) -> str:
    """SVG 進度環，傳入 [{title, progress, pages_read, total_pages, category}]"""
    out = ""
    r = 2 * 3.141592653589793 * 48
    for book in top_books[:6]:
        pct = book.get("progress", 0)
        color = RESERVED_COLORS.get(book.get("category", "").lower(), "#4a90d9")
        offset = r * (1 - pct / 100)
        title = book.get("title", "未知")
        if len(title) > 18:
            title = title[:17] + "…"
        pr = book.get("pages_read", 0)
        tp = book.get("total_pages", 0)
        out += (
            '<div class="ring-card">'
            '<div class="ring-wrap">'
            '<svg viewBox="0 0 120 120" class="ring-svg">'
            '<circle cx="60" cy="60" r="48" fill="none" stroke="#e0e0e0" stroke-width="10"/>'
            '<circle cx="60" cy="60" r="48" fill="none" stroke="' + color + '" stroke-width="10" '
            'stroke-dasharray="' + str(r) + '" stroke-dashoffset="' + str(offset) + '" '
            'stroke-linecap="round" transform="rotate(-90 60 60)"/>'
            '</svg>'
            '<div class="ring-pct">' + str(round(pct)) + '%</div>'
            '</div>'
            '<div class="ring-title">' + title + '</div>'
            '<div class="ring-pages">' + str(pr) + ' / ' + str(tp) + ' 頁</div>'
            '</div>'
        )
    return out


# ── 分類柱狀圖 ────────────────────────────────────────────────────────────────

def _build_bars(category_dist: dict) -> str:
    if not category_dist:
        return ""
    out = ""
    max_val = max(category_dist.values())
    for cat, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True):
        pct = count / max_val * 100
        color = RESERVED_COLORS.get(cat.lower(), "#4a90d9")
        out += (
            '<div class="bar-row">'
            '<span class="bar-label">' + cat + '</span>'
            '<div class="bar-track">'
            '<div class="bar-fill" style="width:' + str(round(pct)) + '%;background:' + color + '"></div>'
            '</div>'
            '<span class="bar-count">' + str(count) + ' 本</span>'
            '</div>'
        )
    return out


# ── 月度趨勢圖 ────────────────────────────────────────────────────────────────

def _build_trend(monthly_data: list) -> str:
    if not monthly_data:
        return '<div style="color:#bbb;text-align:center;padding:40px">累積更多數據後即可顯示趨勢圖 📊</div>'
    last12 = monthly_data[-12:]
    labels = ",".join('"' + m["month"] + '"' for m in last12)
    values = ",".join(str(m["pages"]) for m in last12)
    avg_val = sum(m["pages"] for m in last12) / len(last12)
    return (
        '<canvas id="trendChart" width="700" height="220"></canvas>'
        '<script>'
        'const ctx=document.getElementById("trendChart").getContext("2d");'
        'new Chart(ctx,{type:"line",data:{labels:[' + labels + '],datasets:[{'
        'label:"閱讀頁數",data:[' + values + '],borderColor:"#4a90d9",'
        'backgroundColor:"rgba(74,144,217,0.1)",fill:true,tension:0.4,pointRadius:4,'
        'pointBackgroundColor:"#4a90d9"},{label:"月均",data:Array(12).fill(' + str(round(avg_val, 1)) + '),'
        'borderColor:"#f39c12",borderDash:[5,5],pointRadius:0,fill:false}]},options:{'
        'responsive:false,plugins:{legend:{position:"top"}},scales:{y:{beginAtZero:true}}}});'
        '</script>'
    )


# ── 主 HTML 生成 ─────────────────────────────────────────────────────────────

def generate_html(stats: dict, log_path: str = "") -> str:
    streak         = stats.get("streak", {})
    total_pages    = stats.get("total_pages_read", 0)
    total_books    = stats.get("books_read", 0)
    total_minutes  = stats.get("total_minutes", 0)
    avg_pages      = stats.get("avg_pages_per_day", 0)
    category_dist  = stats.get("category_distribution", {})
    daily_reading  = stats.get("daily_reading", {})
    monthly_data   = stats.get("monthly_data", [])
    top_books      = stats.get("top_books", [])

    today = datetime.date.today()
    year  = today.year

    heatmap_html = _build_heatmap(year, daily_reading)
    rings_html   = _build_rings(top_books)
    bars_html    = _build_bars(category_dist)
    trend_html   = _build_trend(monthly_data)

    cur_streak = streak.get("current", 0)
    long_streak = streak.get("longest", 0)
    hours = total_minutes // 60
    mins  = total_minutes % 60

    rings_section = (
        '<div class="card">'
        '<h2><span class="emoji">📖</span> 閱讀中書籍進度</h2>'
        '<div class="rings-grid">' + rings_html + '</div>'
        '</div>'
    ) if rings_html else ""

    bars_section = (
        '<div class="card">'
        '<h2><span class="emoji">📊</span> 分類閱讀分布</h2>'
        '<div style="display:flex;flex-direction:column;gap:8px">' + bars_html + '</div>'
        '</div>'
    ) if bars_html else ""

    hm_row = (
        '  <div class="card">\n'
        '    <h2><span class="emoji">🔥</span> 年度閱讀熱力圖 '
        '<span style="font-size:12px;color:#aaa;font-weight:400">（' + str(year) + ' 年）</span></h2>\n'
        '    <div class="heatmap-wrap"><div class="heatmap">' + heatmap_html + '</div></div>\n'
        '    <div style="font-size:11px;color:#bbb;margin-top:8px;text-align:right">'
        'Less ▪▪▪▪▪ More &nbsp;&nbsp; 0 → 60+ 頁/天</div>\n'
        '  </div>'
    )

    css = (
        "*{box-sizing:border-box;margin:0;padding:0}"
        "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
        "background:#f0f2f5;color:#1a1a2e;padding:24px}"
        ".container{max-width:1000px;margin:0 auto}"
        ".card{background:#fff;border-radius:16px;padding:24px;margin-bottom:20px;"
        "box-shadow:0 2px 8px rgba(0,0,0,0.06)}"
        "h2{font-size:18px;color:#333;margin-bottom:16px;"
        "display:flex;align-items:center;gap:8px}"
        "h2 .emoji{font-size:22px}"
        ".kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}"
        ".kpi-card{background:#fff;border-radius:16px;padding:20px;text-align:center;"
        "box-shadow:0 2px 8px rgba(0,0,0,0.06)}"
        ".kpi-num{font-size:36px;font-weight:700;color:#4a90d9}"
        ".kpi-unit{font-size:14px;color:#888;margin-top:4px}"
        ".kpi-title{font-size:13px;color:#aaa;margin-top:8px}"
        ".heatmap-wrap{overflow-x:auto;padding:8px 0}"
        ".heatmap{display:flex;flex-direction:column;gap:3px}"
        ".h-col{display:flex;gap:3px}"
        ".h-week{display:flex;flex-direction:column;gap:3px}"
        ".h-cell{width:12px;height:12px;border-radius:2px;cursor:pointer;transition:transform .1s}"
        ".h-cell:hover{transform:scale(1.5);z-index:1;position:relative}"
        ".rings-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:16px}"
        ".ring-card{text-align:center;padding:12px}"
        ".ring-wrap{position:relative;width:100px;height:100px;margin:0 auto 8px}"
        ".ring-svg{width:100%;height:100%}"
        ".ring-pct{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        "font-size:18px;font-weight:700;color:#333}"
        ".ring-title{font-size:12px;color:#555;font-weight:600}"
        ".ring-pages{font-size:11px;color:#aaa;margin-top:2px}"
        ".bar-row{display:flex;align-items:center;gap:12px;margin:8px 0}"
        ".bar-label{font-size:13px;width:50px;color:#555;text-align:right;flex-shrink:0}"
        ".bar-track{flex:1;height:16px;background:#f0f0f0;border-radius:8px;overflow:hidden}"
        ".bar-fill{height:100%;border-radius:8px;transition:width 1s ease}"
        ".bar-count{font-size:12px;color:#aaa;width:55px;flex-shrink:0}"
        ".quote-card{background:linear-gradient(135deg,#667eea,#764ba2);"
        "color:#fff;padding:24px 28px;border-radius:16px;margin-bottom:20px}"
        ".quote-text{font-size:18px;line-height:1.7;font-style:italic}"
        ".quote-from{margin-top:10px;font-size:13px;opacity:0.8;text-align:right}"
        ".footer{text-align:center;color:#bbb;font-size:12px;margin-top:24px}"
        ".fab{position:fixed;bottom:32px;right:32px;background:#4a90d9;color:#fff;"
        "width:56px;height:56px;border-radius:50%;border:none;font-size:24px;"
        "cursor:pointer;box-shadow:0 4px 12px rgba(74,144,217,0.4);"
        "display:flex;align-items:center;justify-content:center}"
        ".fab:hover{background:#3a7fc1}"
    )

    body = (
        '<div class="container">\n\n'
        '  <div class="kpi-grid">\n'
        '    <div class="kpi-card"><div class="kpi-num">' + f'{total_pages:,}' + '</div>'
        '      <div class="kpi-unit">頁</div><div class="kpi-title">年度總閱讀頁數</div></div>\n'
        '    <div class="kpi-card"><div class="kpi-num">' + str(total_books) + '</div>'
        '      <div class="kpi-unit">本</div><div class="kpi-title">已讀完書籍</div></div>\n'
        '    <div class="kpi-card"><div class="kpi-num">' + str(hours) + 'h</div>'
        '      <div class="kpi-unit">' + f'{mins:02d}min' + '</div><div class="kpi-title">總閱讀時長</div></div>\n'
        '    <div class="kpi-card"><div class="kpi-num">' + f'{avg_pages:.0f}' + '</div>'
        '      <div class="kpi-unit">頁/天</div><div class="kpi-title">日均閱讀量</div></div>\n'
        '    <div class="kpi-card"><div class="kpi-num">' + str(cur_streak) + '</div>'
        '      <div class="kpi-unit">天 🔥</div><div class="kpi-title">當前連續打卡</div></div>\n'
        '    <div class="kpi-card"><div class="kpi-num">' + str(long_streak) + '</div>'
        '      <div class="kpi-unit">天 🏆</div><div class="kpi-title">歷史最高連續</div></div>\n'
        '  </div>\n\n' +
        hm_row + '\n' +
        ('\n' + rings_section + '\n' if rings_section else '') +
        ('\n' + bars_section + '\n' if bars_section else '') +
        '  <div class="card">\n'
        '    <h2><span class="emoji">📈</span> 月度閱讀趨勢</h2>\n'
        '    ' + trend_html + '\n'
        '  </div>\n\n'
        '  <div class="quote-card">\n'
        '    <div class="quote-text">「一本書的意義，不在於你讀了多少頁，而在於你改變了多少。」</div>\n'
        '    <div class="quote-from">— 致持續閱讀的你 📚</div>\n'
        '  </div>\n\n'
        '  <div class="footer">\n'
        '    圖書館管家 Plus bookshelf-plus · 自動生成 · ' + today.strftime(DATE_FMT) + '<br>\n' +
        ('    數據來源：' + log_path if log_path else '') + '\n'
        '  </div>\n'
        '</div>\n'
    )

    return (
        '<!DOCTYPE html>\n'
        '<html lang="zh-TW">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        '<title>📚 閱讀統計報告 — ' + today.strftime(DATE_FMT) + '</title>\n'
        '<style>' + css + '</style>\n'
        '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n'
        '</head>\n'
        '<body>\n' +
        body +
        '</body>\n'
        '</html>\n'
    )


# ── 統計計算 ─────────────────────────────────────────────────────────────────

def load_stats_from_log(log_path: str) -> dict:
    """從 reading_log.json 讀取並計算年度統計"""
    path = Path(log_path).expanduser()
    if not path.exists():
        return {}

    with open(path) as f:
        data = json.load(f)

    sessions = data.get("sessions", [])
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)

    year_sessions = [
        s for s in sessions
        if s.get("date", "") >= year_start.isoformat()
    ]

    total_pages   = sum(s.get("pages_read", 0) for s in year_sessions)
    total_minutes = sum(s.get("duration_minutes", 0) for s in year_sessions)
    days_passed   = (today - year_start).days + 1
    avg_pages     = total_pages / days_passed if days_passed > 0 else 0

    daily_reading = {}
    for s in year_sessions:
        d = s["date"]
        daily_reading[d] = daily_reading.get(d, 0) + s.get("pages_read", 0)

    monthly_data = {}
    for s in year_sessions:
        month_key = s["date"][:7]
        monthly_data[month_key] = monthly_data.get(month_key, 0) + s.get("pages_read", 0)
    monthly_list = [{"month": k, "pages": v} for k, v in sorted(monthly_data.items())]

    return {
        "sessions": year_sessions,
        "streak": data.get("streak", {}),
        "total_pages_read": total_pages,
        "total_minutes": total_minutes,
        "avg_pages_per_day": avg_pages,
        "books_read": len([s for s in sessions if s.get("finished", False)]),
        "daily_reading": daily_reading,
        "monthly_data": monthly_list,
        "category_distribution": {},   # 預留，未來從 Notion 拉取時填充
        "top_books": [],               # 預留
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="閱讀統計視覺化儀表板")
    parser.add_argument("--log", default="~/.bookshelf-plus/reading_log.json")
    parser.add_argument("--output", "-o", default="~/Downloads/reading_dashboard.html")
    args = parser.parse_args()

    log_path = Path(args.log).expanduser()

    if log_path.exists():
        stats = load_stats_from_log(str(log_path))
        print("📊 讀取 " + str(len(stats.get("sessions", []))) + " 筆記錄中...")
    else:
        print("⚠️  reading_log.json 不存在，將生成空白模板報告")
        stats = {
            "total_pages_read": 0, "total_minutes": 0,
            "avg_pages_per_day": 0, "books_read": 0,
            "sessions": [], "streak": {"current": 0, "longest": 0},
            "daily_reading": {}, "monthly_data": [],
            "category_distribution": {}, "top_books": [],
        }

    html = generate_html(stats, str(log_path))

    out_path = Path(args.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 儀表板已生成：" + str(out_path))
    print("   📌 用瀏覽器打開：file://" + str(out_path))


if __name__ == "__main__":
    main()
