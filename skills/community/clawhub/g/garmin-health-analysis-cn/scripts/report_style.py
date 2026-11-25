# -*- coding: utf-8 -*-
"""共享报告样式模块

所有生成 HTML 报告的脚本（garmin_chart.py、比赛分析脚本等）统一引用本模块，
保证输出样式一致：
- 纯内联 SVG 图表，无 Chart.js / 无任何外部依赖，可离线直接打开
- 蓝色渐变 hero 横幅 + 编号章节 + 白色圆角卡片 + 统计卡片网格
- 中文界面 + 医疗免责声明页脚
"""

from datetime import datetime

# ================= 调色板 =================
C = dict(blue='#1a73e8', orange='#e8710a', red='#e53935', green='#0f9d58',
         purple='#7e57c2', teal='#00897b', gray='#9aa0a6', dark='#202124',
         lgray='#e8eaed', text='#5f6368', yellow='#fdd663')

# ================= 全局 CSS =================
CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:#f0f3f8;color:#202124;line-height:1.6}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px 60px}
.hero{background:linear-gradient(135deg,#0d47a1 0%,#1a73e8 60%,#2196f3 100%);color:#fff;border-radius:0 0 28px 28px;padding:52px 40px 44px;margin-bottom:28px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-60px;top:-60px;width:340px;height:340px;border-radius:50%;background:rgba(255,255,255,.07)}
.hero::before{content:"";position:absolute;right:60px;bottom:-90px;width:260px;height:260px;border-radius:50%;background:rgba(255,255,255,.06)}
.hero .tag{display:inline-block;background:rgba(255,255,255,.18);padding:4px 14px;border-radius:20px;font-size:13px;letter-spacing:2px;margin-bottom:14px}
.hero h1{font-size:34px;font-weight:700;margin-bottom:10px}
.hero .sub{font-size:15px;opacity:.92}
.hero .pr{display:inline-block;background:#ffd54f;color:#5d4037;font-weight:700;border-radius:8px;padding:3px 12px;font-size:14px;margin-top:14px}
h2{font-size:22px;margin:38px 0 6px;display:flex;align-items:center;gap:10px}
h2 .num{background:#1a73e8;color:#fff;width:30px;height:30px;border-radius:9px;display:inline-flex;align-items:center;justify-content:center;font-size:15px}
.sec-desc{color:#5f6368;font-size:14px;margin-bottom:16px}
.card{background:#fff;border-radius:16px;padding:22px 24px;box-shadow:0 1px 4px rgba(60,64,67,.1);margin-bottom:18px}
.grid{display:grid;gap:14px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
.stat{background:#fff;border-radius:14px;padding:16px 18px;box-shadow:0 1px 4px rgba(60,64,67,.1)}
.stat .k{font-size:12.5px;color:#5f6368;margin-bottom:4px}
.stat .v{font-size:23px;font-weight:700;color:#1a56c4}
.stat .s{font-size:12px;color:#9aa0a6;margin-top:2px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:#f5f7fa;color:#5f6368;font-weight:600;padding:8px 6px;text-align:center;position:sticky;top:0;white-space:nowrap}
td{padding:7px 6px;text-align:center;border-bottom:1px solid #f1f3f4;white-space:nowrap}
tr:hover td{background:#f8fbff}
.tbl-wrap{max-height:520px;overflow:auto;border-radius:10px;border:1px solid #eef0f3}
.chart-cap{text-align:center;color:#5f6368;font-size:12.5px;margin-top:8px}
.note{background:#e8f0fe;border-left:4px solid #1a73e8;border-radius:8px;padding:14px 18px;font-size:13.5px;color:#174ea6;margin:14px 0}
.note.warn{background:#fef7e0;border-color:#f9ab00;color:#8a6100}
.note.good{background:#e6f4ea;border-color:#0f9d58;color:#137333}
.kv{display:flex;justify-content:space-between;padding:7px 4px;border-bottom:1px dashed #eef0f3;font-size:13.5px}
.kv:last-child{border-bottom:none}
.kv b{color:#202124}
.tagline{display:inline-block;font-size:11.5px;padding:2px 10px;border-radius:10px;background:#f1f3f4;color:#5f6368;margin:2px}
.tagline.hot{background:#fce8e6;color:#c5221f}
.tagline.ok{background:#e6f4ea;color:#137333}
.sleepbar{display:flex;height:34px;border-radius:8px;overflow:hidden;margin-top:8px}
.sleepbar div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px}
.sleepblk{margin-bottom:16px}
.sleepblk-h{font-size:13.5px;color:#3c4043}
.footer{text-align:center;color:#9aa0a6;font-size:12px;margin-top:44px;line-height:1.9}
@media(max-width:900px){.g4{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:1fr}.g2{grid-template-columns:1fr}.hero h1{font-size:26px}}
'''

# ================= 基础工具 =================

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def hms(sec):
    """秒 -> 时:分:秒"""
    sec = round(sec)
    return '%d:%02d:%02d' % (sec // 3600, sec % 3600 // 60, sec % 60)


def ms(sec):
    """秒 -> 分:秒"""
    sec = round(sec)
    return '%d:%02d' % (sec // 60, sec % 60)


def short_date(d):
    """'2026-11-08' -> '11.08'"""
    return str(d)[5:].replace('-', '.')


def xlabels(dates, max_labels=7):
    """稀疏 x 轴标签：[(索引, 短日期), ...]"""
    n = len(dates)
    if n == 0:
        return []
    step = max(1, (n + max_labels - 1) // max_labels)
    return [(i, short_date(dates[i])) for i in range(0, n, step)]


# ================= SVG 图表组件 =================

def svg_line_chart(series, w=860, h=300, x_labels=None, y_fmt=None, title='',
                    fill=None, y_min=None, y_max=None, band=None, band_color=None,
                    legend=None):
    """通用折线图。series: [{'data':[(x,y)...], 'color':..., 'width':..., 'dash':..., 'name':...}]
    band: (低值, 高值) 参考区间带；band_color 默认红。"""
    band_color = band_color or C['red']
    pad_l, pad_r, pad_t, pad_b = 56, 16, 18, 34
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    all_x = [p[0] for s in series for p in s['data']]
    all_y = [p[1] for s in series for p in s['data'] if p[1] is not None]
    if band:
        all_y += [band[0], band[1]]
    if not all_x:
        return ''
    x0, x1 = min(all_x), max(all_x)
    y0 = y_min if y_min is not None else min(all_y)
    y1 = y_max if y_max is not None else max(all_y)
    if y1 == y0:
        y1 = y0 + 1

    def X(x):
        return pad_l + (x - x0) / (x1 - x0) * iw if x1 > x0 else pad_l

    def Y(y):
        return pad_t + (1 - (y - y0) / (y1 - y0)) * ih

    p = ['<svg viewBox="0 0 %d %d" style="width:100%%;height:auto" role="img">' % (w, h)]
    gy = 5
    for i in range(gy + 1):
        v = y0 + (y1 - y0) * i / gy
        yy = Y(v)
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee" stroke-width="1"/>' % (pad_l, yy, w - pad_r, yy))
        lbl = y_fmt(v) if y_fmt else ('%g' % round(v, 1))
        p.append('<text x="%d" y="%.1f" text-anchor="end" font-size="11" fill="%s">%s</text>' % (pad_l - 6, yy + 4, C['text'], lbl))
    if band:
        p.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" opacity="0.08"/>' %
                 (pad_l, Y(band[1]), iw, Y(band[0]) - Y(band[1]), band_color))
    for s in series:
        pts = [(X(px), Y(py)) for px, py in s['data'] if py is not None]
        if not pts:
            continue
        dstr = 'M' + ' L'.join('%.1f %.1f' % pt for pt in pts)
        if fill:
            area = dstr + ' L%.1f %.1f L%.1f %.1f Z' % (pts[-1][0], Y(y0), pts[0][0], Y(y0))
            p.append('<path d="%s" fill="%s" opacity="0.12"/>' % (area, fill))
        p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' %
                 (dstr, s.get('color', C['blue']), s.get('width', '2'),
                  ' stroke-dasharray="5 4"' if s.get('dash') else ''))
    if x_labels:
        for xv, txt in x_labels:
            p.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="11" fill="%s">%s</text>' % (X(xv), h - 12, C['text'], txt))
    if legend:
        lx = pad_l + 4
        for name, color in legend:
            p.append('<line x1="%d" y1="10" x2="%d" y2="10" stroke="%s" stroke-width="3"/><text x="%d" y="14" font-size="11" fill="%s">%s</text>' % (lx, lx + 16, color, lx + 21, C['text'], name))
            lx += 21 + len(name) * 11 + 14
    p.append('</svg>')
    return ''.join(p)


def svg_bar_chart(bars, w=860, h=300, y_fmt=None, baseline=None, color_fn=None,
                  x_labels=None, ref_line=None, ref_label='', bar_label_fmt=None,
                  label_every=1):
    """通用柱状图。bars: [(label, value, title, color)]；label_every 控制 x 轴标签稀疏度。"""
    pad_l, pad_r, pad_t, pad_b = 50, 14, 20, 36
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    vals = [b[1] for b in bars if b[1] is not None]
    if not vals:
        return ''
    y0 = baseline if baseline is not None else min(0, min(vals))
    y1 = max(vals)
    if ref_line is not None:
        y1 = max(y1, ref_line)
    span = y1 - y0 or 1
    y0 -= span * 0.05
    y1 += span * 0.08

    def Y(v):
        return pad_t + (1 - (v - y0) / (y1 - y0)) * ih

    bw = iw / len(bars)
    p = ['<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">' % (w, h)]
    for i in range(6):
        v = y0 + (y1 - y0) * i / 5
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee"/>' % (pad_l, Y(v), w - pad_r, Y(v)))
        p.append('<text x="%d" y="%.1f" text-anchor="end" font-size="11" fill="%s">%s</text>' %
                 (pad_l - 6, Y(v) + 4, C['text'], y_fmt(v) if y_fmt else '%g' % round(v)))
    for i, (label, val, title, color) in enumerate(bars):
        if val is None:
            continue
        x = pad_l + i * bw + bw * 0.12
        bwid = bw * 0.76
        ytop = Y(val)
        ybase = Y(max(y0, 0)) if baseline is None and min(vals) >= 0 else (Y(baseline) if baseline is not None else Y(0))
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"><title>%s</title></rect>' %
                 (x, ytop, bwid, max(1, ybase - ytop), color, esc(title)))
        if bar_label_fmt:
            p.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="9.5" fill="%s">%s</text>' %
                     (x + bwid / 2, ytop - 3, C['text'], bar_label_fmt(val)))
        if label_every and i % label_every == 0:
            p.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="10.5" fill="%s">%s</text>' %
                     (x + bwid / 2, h - 14, C['text'], label))
    if ref_line is not None:
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1.6" stroke-dasharray="6 4"/>' %
                 (pad_l, Y(ref_line), w - pad_r, Y(ref_line), C['red']))
        p.append('<text x="%d" y="%.1f" font-size="11" fill="%s">%s</text>' % (pad_l + 4, Y(ref_line) - 4, C['red'], ref_label))
    p.append('</svg>')
    return ''.join(p)


# ================= 睡眠阶段堆叠条 =================

SLEEP_COLORS = [('深睡', '#304ffe'), ('浅睡', '#7ea8ff'), ('REM', '#ff9e40'), ('清醒', '#bdbdbd')]


def sleep_bar(label, deep, light, rem, awake, score=None):
    """睡眠阶段堆叠条 + 标题行。时长单位：秒；score 可为 None。"""
    segs = [(SLEEP_COLORS[0][0], deep or 0, SLEEP_COLORS[0][1]),
            (SLEEP_COLORS[1][0], light or 0, SLEEP_COLORS[1][1]),
            (SLEEP_COLORS[2][0], rem or 0, SLEEP_COLORS[2][1]),
            (SLEEP_COLORS[3][0], awake or 0, SLEEP_COLORS[3][1])]
    total = sum(v for _, v, _ in segs) or 1
    html = ['<div class="sleepbar">']
    for name, v, color in segs:
        pct = v / total * 100
        html.append('<div style="width:%.1f%%;background:%s" title="%s %s (%d%%)"><span>%s</span></div>' %
                    (pct, color, name, hms(v), round(pct), name if pct > 12 else ''))
    html.append('</div>')
    sc_str = ('%s' % score) if score is not None else '—'
    return ('<div class="sleepblk"><div class="sleepblk-h">%s · 总时长 <b>%s</b> · 评分 <b>%s</b></div>%s</div>') % (
        label, hms(total), sc_str, ''.join(html))


def sleep_legend():
    chips = ''.join('<span class="tagline"><span style="color:%s">■</span> %s</span>' % (c, n)
                    for n, c in SLEEP_COLORS)
    return '<div style="margin-bottom:6px">%s</div>' % chips


# ================= 页面组件 =================

def stat(k, v, s=''):
    """统计卡片"""
    return '<div class="stat"><div class="k">%s</div><div class="v">%s</div><div class="s">%s</div></div>' % (k, v, s)


def kv(name, value):
    """键值行"""
    return '<div class="kv"><span>%s</span><b>%s</b></div>' % (name, value)


def note(html, kind='info'):
    """提示条：info（蓝）/ warn（黄）/ good（绿）"""
    cls = 'note' if kind == 'info' else 'note %s' % kind
    return '<div class="%s">%s</div>' % (cls, html)


def card(inner, title=''):
    """白色圆角卡片，title 可选"""
    if title:
        return '<div class="card"><h3 style="font-size:15px;margin-bottom:12px">%s</h3>%s</div>' % (title, inner)
    return '<div class="card">%s</div>' % inner


def grid(items, cols=4):
    """统计卡片/内容网格：cols ∈ 2/3/4"""
    return '<div class="grid g%d">%s</div>' % (cols, ''.join(items))


def chart_cap(text):
    """图表下方的灰色说明文字"""
    return '<div class="chart-cap">%s</div>' % text


def section(num, title, desc=''):
    """编号章节标题 + 说明"""
    h = '<h2><span class="num">%d</span>%s</h2>' % (num, title)
    if desc:
        h += '<div class="sec-desc">%s</div>' % desc
    return h


def hero(title, sub='', tag='HEALTH REPORT · Garmin Connect 数据分析', badge=None):
    """蓝色渐变页首横幅"""
    h = ['<div class="hero"><div class="wrap" style="padding-bottom:0">']
    h.append('<div class="tag">%s</div>' % tag)
    h.append('<h1>%s</h1>' % title)
    if sub:
        h.append('<div class="sub">%s</div>' % sub)
    if badge:
        h.append('<div class="pr">%s</div>' % badge)
    h.append('</div></div>')
    return ''.join(h)


def render_page(title, hero_html, sections, footer_extra=''):
    """组装完整 HTML 页面。sections: [(标题, 说明, 内容 html), ...]，编号自动生成。"""
    p = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">']
    p.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    p.append('<title>%s</title>' % esc(title))
    p.append('<style>%s</style></head><body>' % CSS)
    p.append(hero_html)
    p.append('<div class="wrap">')
    for i, (sec_title, desc, inner) in enumerate(sections, 1):
        p.append(section(i, sec_title, desc))
        p.append(inner)
    gen = datetime.now().strftime('%Y-%m-%d %H:%M')
    p.append('<div class="footer">本报告所有数据来自 Garmin Connect 自动记录，分析结果仅供参考，不构成医疗或专业训练建议。<br>'
             'garmin-health-analysis-cn · 报告生成时间 %s%s</div>' % (gen, footer_extra))
    p.append('</div></body></html>')
    return '\n'.join(p)
