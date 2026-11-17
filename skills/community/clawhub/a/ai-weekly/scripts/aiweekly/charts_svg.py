# -*- coding: utf-8 -*-
"""服务端渲染的市场图表（内联 SVG）—— 零 JS / 零 Canvas 依赖。

背景（2026-09-22 实测）：
  6 张市场图原先完全依赖浏览器端 Chart.js。一旦查看环境拦掉 JS 或 Canvas 2D
  （预览面板 / 内置 WebView / 隐私插件屏蔽 canvas），`initCharts()` 就只剩
  「发现 Chart 不存在 → return」，页面上留下 6 个空白 canvas 框——数据等于丢失。
  而新闻列表、排行榜都不依赖 Chart.js，所以症状恰好是「别的都正常、只有市场图空白」。

设计：
  * 本模块把同样的数据在**服务端**画成内联 SVG，直接写进静态 HTML。
    不执行任何 JS 也能看见，符合本项目「服务端预渲染，不依赖前端 JS」的既定原则。
  * 与 Chart.js 双轨共存：canvas 默认隐藏、SVG 默认显示；Chart.js 逐张建图成功后
    由 JS 给容器加 `.charts-live`，CSS 再翻转为「canvas 显示 / SVG 隐藏」。
    这样两边能力都保住——现代浏览器可交互，受限环境照样有图。
  * 颜色/口径刻意与 `market.py::build_charts` 的 Chart.js 配置保持一致，
    避免两条轨视觉不一致。

无障碍：每张图带 role=img + aria-label；每根柱/每个点内含 <title>，
        悬停即出原生提示（无需 JS 也能看数值）。
"""
from __future__ import annotations

import html
import math

# ---- 画布几何（viewBox 坐标系；显示尺寸由 CSS 决定，等比缩放不变形）----
_W, _H = 520, 320
_ML, _MR, _MT, _MB = 58, 34, 18, 44          # 左 右 上 下 留白
_X0, _X1 = _ML, _W - _MR                     # 绘图区左右边界
_Y0, _Y1 = _MT, _H - _MB                     # 绘图区上下边界
_PW, _PH = _X1 - _X0, _Y1 - _Y0
_AR = "xMidYMid meet"                        # 等比缩放，避免文字被横向拉伸

# ---- 与 Chart.js 轨一致的配色 ----
C_BLUE = "37,99,235"        # marketSize（实测）
C_PURPLE = "124,58,237"     # fundingChart
C_RED = "220,38,38"         # cn*（中国口径）
C_GREEN = "22,163,74"       # YoY 折线
C_ORANGE = "234,88,12"
C_AMBER = "217,119,6"
C_SLATE = "100,116,139"


def _esc(s) -> str:
    return html.escape(str(s), quote=True)


def _rgba(rgb: str, alpha: float) -> str:
    return f"rgba({rgb},{alpha})"


def _nice_max(v: float) -> float:
    """把最大值抬到「好看」的刻度上限（1/1.5/2/2.5/3/4/5/6/8/10 × 10^n）。"""
    if v is None or v <= 0:
        return 1.0
    exp = math.floor(math.log10(v))
    base = 10.0 ** exp
    for m in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if v <= m * base + 1e-9:
            return m * base
    return 10.0 * base


def _fmt_num(v, unit: str = "") -> str:
    """数值标签：千分位 + 按量级控制小数（72.4 → 72.4；9188 → 9,188）。"""
    if v is None:
        return "—"
    a = abs(v)
    if a >= 1000:
        s = f"{v:,.0f}"
    elif a >= 100:
        s = f"{v:.0f}"
    elif a >= 10:
        s = f"{v:.1f}"
    else:
        s = f"{v:.2f}"
    return f"{s}{unit}"


def _fmt_signed(v, unit: str = "") -> str:
    if v is None:
        return "—"
    return f"{'+' if v >= 0 else ''}{v:.1f}{unit}"


def _y_ticks(y_max: float, n: int = 4):
    return [y_max * i / n for i in range(n + 1)]


def _open_svg(title: str) -> list:
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" '
            f'role="img" aria-label="{_esc(title)}" '
            f'preserveAspectRatio="{_AR}" class="chart-svg">']


def _grid_and_yaxis(y_max, unit) -> list:
    """横网格线 + 左侧刻度标签。"""
    out = []
    for t in _y_ticks(y_max):
        y = _Y1 - (t / y_max) * _PH
        dash = ' stroke-dasharray="3 3"' if 0 < t < y_max else ""
        out.append(f'<line x1="{_X0:.1f}" y1="{y:.1f}" x2="{_X1:.1f}" y2="{y:.1f}" '
                   f'stroke="currentColor" stroke-opacity="0.14" stroke-width="1"{dash}/>')
        out.append(f'<text x="{_X0 - 8:.1f}" y="{y + 3.5:.1f}" text-anchor="end" '
                   f'fill="currentColor" fill-opacity="0.62" font-size="10.5">'
                   f'{_esc(_fmt_num(t))}{_esc(unit)}</text>')
    return out


def _x_labels(labels) -> list:
    """x 轴分类标签；数量多时自动隔项显示，避免糊成一片。"""
    n = max(1, len(labels))
    step = _PW / n
    every = max(1, math.ceil(n / 9))
    out = []
    for i, lab in enumerate(labels):
        if i % every:
            continue
        x = _X0 + step * (i + 0.5)
        out.append(f'<text x="{x:.1f}" y="{_Y1 + 16:.1f}" text-anchor="middle" '
                   f'fill="currentColor" fill-opacity="0.62" font-size="10.5">'
                   f'{_esc(lab)}</text>')
    return out


def _legend(items) -> list:
    """顶部紧凑图例；items = [(文字, rgb)]。按估算文字宽度递增 x。"""
    if not items:
        return []
    out, x = [], _X0
    for text, rgb in items:
        out.append(f'<rect x="{x:.1f}" y="{_Y0:.1f}" width="9" height="9" rx="2" '
                   f'fill="{_rgba(rgb, 0.8)}"/>')
        out.append(f'<text x="{x + 13:.1f}" y="{_Y0 + 8.5:.1f}" fill="currentColor" '
                   f'fill-opacity="0.75" font-size="10.5">{_esc(text)}</text>')
        cjk = sum(1 for c in str(text) if ord(c) > 0x2E80)
        x += 22 + cjk * 10.6 + (len(str(text)) - cjk) * 5.8
    return out


# --------------------------------------------------------------------------- #
# 图型 1：竖向柱状图（可选「预测柱」浅色区分）
# --------------------------------------------------------------------------- #
def vbar_svg(labels, values, *, rgb=C_BLUE, forecast_flags=None, unit="",
             title="", show_values=True) -> str:
    y_max = _nice_max(max(values) if values else 1)
    n = max(1, len(values))
    slot = _PW / n
    bar_w = min(48.0, slot * 0.62)

    parts = _open_svg(title)
    parts += _grid_and_yaxis(y_max, unit)
    parts += _x_labels(labels)

    for i, (lab, v) in enumerate(zip(labels, values)):
        is_fc = bool(forecast_flags[i]) if forecast_flags and i < len(forecast_flags) else False
        h = 0 if not v else max(2.0, (v / y_max) * _PH)
        x = _X0 + slot * (i + 0.5) - bar_w / 2
        y = _Y1 - h
        parts.append(
            f'<g><title>{_esc(lab)}：{_esc(_fmt_num(v, unit))}'
            f'{"（CAGR 外推，非实测）" if is_fc else "（实测/机构估算）"}</title>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="4" '
            f'fill="{_rgba(rgb, 0.32 if is_fc else 0.72)}" '
            f'stroke="{_rgba(rgb, 0.5 if is_fc else 0.95)}" stroke-width="1"/></g>')
        if show_values and n <= 9:
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" '
                         f'fill="{_rgba(rgb, 0.95)}" font-size="10.5" font-weight="600">'
                         f'{_esc(_fmt_num(v))}</text>')
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------- #
# 图型 2：横向柱状图（赛道结构 / 头部集中度）
# --------------------------------------------------------------------------- #
def hbar_svg(labels, values, *, rgbs, unit="", title="") -> str:
    v_max = _nice_max(max(values) if values else 1)
    n = max(1, len(values))
    slot = _PH / n
    bar_h = min(34.0, slot * 0.56)
    avail = _PW - 78                      # 右侧留给数值标签

    parts = _open_svg(title)
    for t in _y_ticks(v_max):
        x = _X0 + (t / v_max) * avail
        dash = ' stroke-dasharray="3 3"' if 0 < t < v_max else ""
        parts.append(f'<line x1="{x:.1f}" y1="{_Y0:.1f}" x2="{x:.1f}" y2="{_Y1:.1f}" '
                     f'stroke="currentColor" stroke-opacity="0.14" stroke-width="1"{dash}/>')
        parts.append(f'<text x="{x:.1f}" y="{_Y1 + 16:.1f}" text-anchor="middle" '
                     f'fill="currentColor" fill-opacity="0.62" font-size="10.5">'
                     f'{_esc(_fmt_num(t))}</text>')

    for i, (lab, v) in enumerate(zip(labels, values)):
        rgb = rgbs[i] if i < len(rgbs) else C_SLATE
        w = 0 if not v else max(2.0, (v / v_max) * avail)
        y = _Y0 + slot * (i + 0.5) - bar_h / 2
        parts.append(f'<text x="{_X0 - 10:.1f}" y="{y + bar_h / 2 + 3.5:.1f}" text-anchor="end" '
                     f'fill="currentColor" fill-opacity="0.78" font-size="11.5">{_esc(lab)}</text>')
        parts.append(f'<g><title>{_esc(lab)}：{_esc(_fmt_num(v, unit))}</title>'
                     f'<rect x="{_X0:.1f}" y="{y:.1f}" width="{w:.1f}" height="{bar_h:.1f}" '
                     f'rx="4" fill="{_rgba(rgb, 0.78)}"/></g>')
        parts.append(f'<text x="{_X0 + w + 8:.1f}" y="{y + bar_h / 2 + 3.5:.1f}" '
                     f'fill="currentColor" fill-opacity="0.8" font-size="10.5" font-weight="600">'
                     f'{_esc(_fmt_num(v, unit))}</text>')
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------- #
# 图型 3：折线 + 面积填充（融资趋势）
# --------------------------------------------------------------------------- #
def line_svg(labels, values, *, rgb=C_PURPLE, unit="", title="", show_points=True) -> str:
    y_max = _nice_max(max(values) if values else 1)
    n = max(1, len(values))
    step = _PW / n
    pts = [(_X0 + step * (i + 0.5), _Y1 - ((v or 0) / y_max) * _PH)
           for i, v in enumerate(values)]

    parts = _open_svg(title)
    parts += _grid_and_yaxis(y_max, unit)
    parts += _x_labels(labels)
    area = ("M " + f"{pts[0][0]:.1f},{_Y1:.1f} L "
            + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            + f" L {pts[-1][0]:.1f},{_Y1:.1f} Z")
    parts.append(f'<path d="{area}" fill="{_rgba(rgb, 0.12)}"/>')
    parts.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                 + f'" fill="none" stroke="{_rgba(rgb, 1)}" stroke-width="2.2" '
                   'stroke-linejoin="round" stroke-linecap="round"/>')
    if show_points:
        for (lab, v), (x, y) in zip(zip(labels, values), pts):
            parts.append(f'<g><title>{_esc(lab)}：{_esc(_fmt_num(v, unit))}</title>'
                         f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{_rgba(rgb, 1)}" '
                         f'stroke="#fff" stroke-width="1.2"/></g>')
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------- #
# 图型 4：柱 + 折线双轴（中国核心产业规模 + YoY%）
# --------------------------------------------------------------------------- #
def dual_axis_svg(labels, values, line_values, *, rgb=C_RED, line_rgb=C_GREEN,
                  unit="亿", line_unit="%", title="", legend=None) -> str:
    y_max = _nice_max(max(values) if values else 1)
    ln_vals = [v for v in line_values if v is not None]
    ly_max = _nice_max(max(ln_vals) if ln_vals else 1)

    n = max(1, len(values))
    slot = _PW / n
    bar_w = min(56.0, slot * 0.42)

    parts = _open_svg(title)
    parts += _grid_and_yaxis(y_max, unit)
    for t in _y_ticks(ly_max):
        y = _Y1 - (t / ly_max) * _PH
        parts.append(f'<text x="{_X1 + 6:.1f}" y="{y + 3.5:.1f}" text-anchor="start" '
                     f'fill="{_rgba(line_rgb, 1)}" font-size="10.5">'
                     f'{_esc(_fmt_num(t))}{_esc(line_unit)}</text>')
    parts += _x_labels(labels)

    # 柱（核心产业规模）
    for i, (lab, v) in enumerate(zip(labels, values)):
        h = 0 if not v else max(2.0, (v / y_max) * _PH)
        x = _X0 + slot * (i + 0.5) - bar_w / 2
        y = _Y1 - h
        yoy = line_values[i] if i < len(line_values) else None
        tip = f"{lab}：{_fmt_num(v, unit)}" + (
            f"，同比 {_fmt_signed(yoy, line_unit)}" if yoy is not None else "")
        parts.append(f'<g><title>{_esc(tip)}</title>'
                     f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="4" '
                     f'fill="{_rgba(rgb, 0.72)}" stroke="{_rgba(rgb, 1)}" stroke-width="1"/></g>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" '
                     f'fill="{_rgba(rgb, 0.95)}" font-size="10.5" font-weight="600">'
                     f'{_esc(_fmt_num(v))}</text>')

    # 折线（YoY%）—— 点自带数值，避免二次查找
    pts = [(labels[i] if i < len(labels) else "", _X0 + slot * (i + 0.5),
            _Y1 - (v / ly_max) * _PH, v) for i, v in enumerate(line_values) if v is not None]
    if len(pts) >= 2:
        parts.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for _, x, y, _ in pts)
                     + f'" fill="none" stroke="{_rgba(line_rgb, 1)}" stroke-width="2.2" '
                       'stroke-dasharray="5 3" stroke-linejoin="round"/>')
    for lab, x, y, v in pts:
        parts.append(f'<g><title>{_esc(lab)} 同比：{_esc(_fmt_signed(v, line_unit))}</title>'
                     f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{_rgba(line_rgb, 1)}" '
                     f'stroke="#fff" stroke-width="1.2"/></g>')
    parts += _legend(legend)
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------- #
# 对外入口：一次产出 6 张 SVG
# --------------------------------------------------------------------------- #
def build_svg_charts(data: dict) -> dict:
    """把 `market.resolve_chart_data()` 的结果渲染成 6 张内联 SVG。

    输入每个键含 {"labels": [...], "values": [...]}；
    输出 {canvas_id: svg_markup}，键与模板里的 canvas id 一一对应，便于占位替换。
    """
    mk, fd, cm = data["market"], data["funding"], data["cn_market"]
    cf, cs, cc = data["cn_funding"], data["cn_structure"], data["cn_concentration"]

    # 中国核心产业规模的同比由数据自行推算（与 Chart.js 轨同口径）
    cn_vals = cm["values"]
    yoy = [None] + [round((cn_vals[i] / cn_vals[i - 1] - 1) * 100, 1)
                    for i in range(1, len(cn_vals)) if cn_vals[i - 1]]

    forecasts = [str(l).strip().endswith("F") for l in mk["labels"]]

    return {
        "marketSizeChart": vbar_svg(
            mk["labels"], mk["values"], rgb=C_BLUE, forecast_flags=forecasts,
            unit="B", title="AI 市场规模（十亿美元）"),
        "fundingChart": line_svg(
            fd["labels"], fd["values"], rgb=C_PURPLE, unit="B",
            title="AI 融资趋势（十亿美元）"),
        "cnMarketChart": dual_axis_svg(
            cm["labels"], cn_vals, yoy, rgb=C_RED, line_rgb=C_GREEN, unit="亿",
            title="中国 AI 核心产业规模（亿元）与同比增速",
            legend=[("核心产业规模（亿元）", C_RED), ("同比增速 YoY（%）", C_GREEN)]),
        "cnFundingChart": line_svg(
            cf["labels"], cf["values"], rgb=C_RED, unit="亿",
            title="中国 AI 融资趋势（亿元）"),
        "cnStructureChart": hbar_svg(
            cs["labels"], cs["values"], rgbs=[C_RED, C_ORANGE, C_AMBER, C_SLATE],
            unit="亿", title="2026H1 AI 融资赛道结构（亿元）"),
        "cnConcentrationChart": hbar_svg(
            cc["labels"], cc["values"], rgbs=[C_RED, C_ORANGE, C_SLATE],
            unit="亿", title="AI 融资头部集中度（亿元）"),
    }


__all__ = [
    "build_svg_charts", "vbar_svg", "hbar_svg", "line_svg", "dual_axis_svg",
]
