# -*- coding: utf-8 -*-
"""adapters/rendering.py — ct- 系列统一 SVG 内联渲染工具（ct-base §19 标准实现）。

将 coze 返回的 figures[].svg 转为可直接内嵌到对话流的标准 HTML fragment；
并提供 SVG→PNG 落盘路径（figure_mode='png_file'，本地 cairosvg 转换）。

核心问题（实测 2026-08-19，meta-analysis 实战沉淀，现全库统一）：
  svglite 输出固定 viewBox（如 "0 0 504 360"），但内容可能**超出该区域**
  —— meta 包 forest() / 样本量曲线图把部分文字/元素画在图形区外。
  按原 viewBox 渲染会被浏览器裁剪两侧文字。
  解决：content_bbox() 扫描内容元素极值，动态扩展 viewBox + 宽度。

规则（用户偏好，2026-08-19；ct-base §19.4 全库强制）：
  图固定原尺寸不缩放；容器装不下即出横向滚动条（overflow-x:auto）。

用法：
  from rendering import build_figure_widget
  html = build_figure_widget(figures, ["Power curve", "样本量曲线"])

  from rendering import svg_to_png
  svg_to_png(fig_svg, "outputs/ctss_xxx.png", scale=2.0)  # figure_mode='png_file'
"""

from __future__ import annotations

import os
import re
import time

__all__ = ["extract_svg", "content_bbox", "build_figure_widget", "render_html_report"]

_Q = r"['\"]"  # svglite 用单引号属性，兼容双引号


def _num(v: str) -> float:
    """'39.34px' / '504.00' → 39.34 / 504.0"""
    return float(v.replace("px", "").strip())


def extract_svg(svg_str: str) -> tuple[str, str]:
    """从完整 SVG 字符串提取 (inner, viewbox)。兼容单/双引号属性。

    inner = <svg> 内部内容（供嵌入 <svg viewBox=...>），viewbox 为原值。
    """
    m = re.search(
        r"<svg[^>]*viewBox=['\"]([^'\"]+)['\"][^>]*>(.*)</svg>",
        svg_str,
        re.S,
    )
    if m:
        return (m.group(2), m.group(1))
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg_str, re.S)
    if m:
        return (m.group(1), "0 0 504 360")
    return (svg_str, "0 0 504 360")


def content_bbox(
    svg_inner: str, pad: float = 8.0, pad_y: float = 24.0
) -> tuple[float, float, float, float]:
    """扫描 SVG 内容元素，返回 (min_x, min_y, max_x, max_y) 含 padding。

    pad 用于 x 方向（紧凑，避免图过宽）；pad_y 用于 y 方向（留白更多，
    绘图区上下贴近内容时保持呼吸空间，见用户偏好 2026-08-19）。
    覆盖元素：text（含 textLength/text-anchor 计算文本宽度；transform 文本解析
    translate 锚点双向扩展）、rect（跳过 width=100% 白底）、line、circle、
    polyline/polygon points。无内容时回退原画布 (0, 0, 504, 360)。
    """
    xs: list[float] = []
    ys: list[float] = []

    # ---- text ----
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", svg_inner, re.S):
        attrs = m.group(1)
        tl = re.search(rf"textLength={_Q}([^'\"]+)", attrs)
        w = _num(tl.group(1)) if tl else 0.0
        tm = re.search(r"transform=['\"]([^'\"]+)['\"]", attrs)
        if tm:
            # transform 文本（如漏斗图 y 轴旋转标签）：取 translate 锚点，沿 x/y
            # 双向扩展 textLength（旋转方向不定，保守覆盖 → 保证不裁剪）
            t = re.search(
                r"translate\(\s*([-0-9.]+)\s*,\s*([-0-9.]+)\s*\)", tm.group(1)
            )
            if t:
                tx, ty = _num(t.group(1)), _num(t.group(2))
                xs += [tx - w, tx + w]
                ys += [ty - w, ty + w]
                continue
            continue  # 无 translate 的 transform（如纯 rotate）无法定位，跳过
        xm = re.search(rf"\bx={_Q}([^'\"]+)", attrs)
        ym = re.search(rf"\by={_Q}([^'\"]+)", attrs)
        if not xm or not ym:
            continue
        x, y = _num(xm.group(1)), _num(ym.group(1))
        an = re.search(rf"text-anchor={_Q}([^'\"]+)", attrs)
        anchor = an.group(1) if an else "start"
        if anchor == "start":
            x0, x1 = x, x + w
        elif anchor == "middle":
            x0, x1 = x - w / 2, x + w / 2
        else:  # end
            x0, x1 = x - w, x
        xs += [x0, x1]
        ys += [y, y]

    # ---- rect ----
    for m in re.finditer(r"<rect\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("x", "y", "width", "height")) and a["width"] != "100%":
            x, y = _num(a["x"]), _num(a["y"])
            w, h = _num(a["width"]), _num(a["height"])
            xs += [x, x + w]
            ys += [y, y + h]

    # ---- line ----
    for m in re.finditer(r"<line\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("x1", "y1", "x2", "y2")):
            xs += [_num(a["x1"]), _num(a["x2"])]
            ys += [_num(a["y1"]), _num(a["y2"])]

    # ---- circle ----
    for m in re.finditer(r"<circle\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("cx", "cy", "r")):
            r = _num(a["r"])
            cx, cy = _num(a["cx"]), _num(a["cy"])
            xs += [cx - r, cx + r]
            ys += [cy - r, cy + r]

    # ---- polyline / polygon points ----
    for tag in ("polyline", "polygon"):
        for m in re.finditer(rf"<{tag}\b([^>]*)/?>", svg_inner):
            a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
            if "points" in a:
                pts = [_num(v) for v in a["points"].replace(",", " ").split()]
                xs += pts[0::2]
                ys += pts[1::2]

    if not xs or not ys:
        return (0.0, 0.0, 504.0, 360.0)
    return (min(xs) - pad, min(ys) - pad_y, max(xs) + pad, max(ys) + pad_y)


def _strip_clip(svg_inner: str) -> str:
    """移除 svglite 的 clipPath 定义与 clip-path 引用（100% 显示的关键）。

    svglite 用固定 0..504 的 clipPath 裁剪绘图区，但 meta 包森林图的左右文字列
    画在 0 外 / 504 外（实测 x∈[-140,644]），被内部 clip 裁掉——即使外层 viewBox
    已扩展也无效。移除后由外层动态 viewBox（content_bbox）保证完整显示。
    注意：必须在 content_bbox 之前调用（clipPath 里的 rect 0..504 会污染 bbox）。
    """
    s = re.sub(r"<clipPath\b.*?</clipPath>", "", svg_inner, flags=re.S)
    s = re.sub(r"\s*clip-path='url\(#[^)]+\)'", "", s)
    return s


def _fix_xml(s: str) -> str:
    """补齐缺失的闭合标签（svglite 2.2.2 偶发缺一个 </g>）。

    浏览器按 HTML 解析规则宽容渲染没问题，但 cairosvg 用严格 XML 解析会报
    "mismatched tag"。用标签栈扫描，把未闭合的开标签按逆序补齐闭合标签。
    仅 SVG→PNG 路径使用；内联渲染（浏览器）不需要。
    """
    stack: list[str] = []
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        if s[i] != "<":
            out.append(s[i]); i += 1; continue
        if s.startswith("<!--", i):
            j = s.find("-->", i); j = n if j < 0 else j + 3
            out.append(s[i:j]); i = j; continue
        if s.startswith("<![CDATA[", i):
            j = s.find("]]>", i); j = n if j < 0 else j + 3
            out.append(s[i:j]); i = j; continue
        if s[i + 1] in ("!", "?"):
            j = s.find(">", i); j = n if j < 0 else j + 1
            out.append(s[i:j]); i = j; continue
        j = s.find(">", i)
        if j < 0:
            out.append(s[i:]); break
        body = s[i + 1:j].strip()
        out.append(s[i:j + 1]); i = j + 1
        if not body or body.startswith("/") or body.endswith("/"):
            if body.startswith("/") and stack:
                stack.pop()  # 闭合标签弹栈
            continue
        name = body.split()[0]
        stack.append(name)
    for name in reversed(stack):
        out.append(f"</{name}>")
    return "".join(out)


def _wrap_points(line: str, limit: int = 1200) -> str:
    """拆分超长行（svglite polyline points 单行可达 7000+ 字符）"""
    if len(line) <= limit:
        return line

    def repl(m):
        val = m.group(2)
        chunks, cur = [], ""
        for part in val.split():
            if len(cur) + len(part) + 1 > 1000:
                chunks.append(cur)
                cur = part
            else:
                cur = (cur + " " + part) if cur else part
        if cur:
            chunks.append(cur)
        return m.group(1) + chunks[0] + "\n" + "\n".join(chunks[1:]) + m.group(3)

    return re.sub(r"(points=['\"])(.*?)(['\"])", repl, line, flags=re.S)


def build_figure_widget(
    figures: list, titles: list[str], pad: float = 8.0, pad_y: float = 24.0
) -> str:
    """figures: [{svg, type}, ...] → 完整内联 HTML fragment。

    宽度规则：
      1. content_bbox() 扫描内容实际边界 → 动态 viewBox（解决 svglite 内容超界裁剪）
      2. SVG 固定原尺寸（viewBox 宽）不缩放
      3. 外层 overflow-x:auto —— 容器装不下即出横向滚动条
    """
    blocks = []
    for fig, t in zip(figures, titles):
        inner, vb = extract_svg(fig.get("svg") or "")
        inner = _strip_clip(inner)          # ★ 先移除内部 clipPath（否则左右文字列被裁）
        min_x, min_y, max_x, max_y = content_bbox(inner, pad=pad, pad_y=pad_y)
        vb_fit = f"{min_x:g} {min_y:g} {max_x - min_x:g} {max_y - min_y:g}"
        w = max_x - min_x
        blocks.append(
            f'<div><div style="font-size:16px;font-weight:600;margin:0 0 6px;'
            f'color:var(--color-text-primary);">{t}</div>'
            f'<div style="overflow-x:auto;max-width:100%;background:#fff;'
            f'border:0.5px solid var(--color-border-tertiary);'
            f'border-radius:var(--border-radius-md);">'
            # margin:0 auto → 容器比图宽时水平居中；容器窄溢出时 auto 边距归零
            # 自动左对齐出滚动条（flex justify-center 会裁剪左侧不可达，不能用）
            f'<svg viewBox="{vb_fit}" style="width:{w:g}px;height:auto;display:block;'
            f'margin:0 auto;">'
            f"{_wrap_points(inner)}</svg></div></div>"
        )
    return (
        '<div style="display:flex;flex-direction:column;gap:16px;'
        'font-family:var(--font-sans);">' + "".join(blocks) + "</div>"
    )


def svg_to_png(svg_str: str, out_path: str, scale: float = 2.0,
               pad: float = 8.0, pad_y: float = 24.0) -> str:
    """SVG → PNG（本地 cairosvg 转换，coze 端零改动）。

    与内联渲染同一处理链：strip clip → content_bbox 扩展 viewBox（保证完整内容）
    → 重建完整 SVG → cairosvg 按 scale 光栅化 → 写 out_path。

    Returns: out_path（成功）; 转换失败抛 RuntimeError（含原因）。
    """
    try:
        import cairosvg
    except ImportError:
        raise RuntimeError("SVG→PNG 需 cairosvg：pip install cairosvg")

    inner, vb = extract_svg(svg_str)
    inner = _strip_clip(inner)
    inner = _fix_xml(inner)  # svglite 偶发缺 </g>，严格 XML 解析前补齐
    min_x, min_y, max_x, max_y = content_bbox(inner, pad=pad, pad_y=pad_y)
    vb_fit = f"{min_x:g} {min_y:g} {max_x - min_x:g} {max_y - min_y:g}"
    full = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_fit}" '
        f'width="{max_x - min_x}" height="{max_y - min_y}">'
        f"{_wrap_points(inner)}</svg>"
    )
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    cairosvg.svg2png(bytestring=full.encode("utf-8"), write_to=out_path, scale=scale)
    return out_path


# ---------------------------------------------------------------------------
# HTML 聚合报告（ct-samplesize v5.3.2 对齐 meta-analysis 方案 B）
# 把 coze 返回的 stats + SVG 图 + R 复现脚本固化成单文件 HTML，浏览器直接打开。
# 与 meta-analysis 的 render_html_report 同构：内联 SVG（build_figure_widget 已回填
# content）、扁平 stats 表、折叠 R 代码（语法高亮 + copy 按钮）。
# ---------------------------------------------------------------------------

_HTML_ESCAPE = None


def _html_escape(s) -> str:
    """HTML 转义（惰性导入 html.escape）。"""
    global _HTML_ESCAPE
    if _HTML_ESCAPE is None:
        import html as _html_mod

        _HTML_ESCAPE = _html_mod.escape
    return _HTML_ESCAPE(str(s) if s is not None else "")


# ── Hero / 语义分组（2026-08-28 借鉴 meta-analysis 的 HTML 信息架构优化）──
#   样本量计算的核心答案是「要多少例 / 有多少把握」，但原实现把 n/power 平铺进
#   stats 大表，用户要扫完整张表才能找到结论。这里对齐 meta-analysis 的
#   _render_hero + _render_stats_groups：顶部 Hero 一眼看到核心结果，
#   其余 stats 按语义分组（设计参数 / 结果 / 曲线数据）分卡展示。

#: 结果类字段（Hero 优先取用 + 归入「计算结果」组）
_RESULT_KEYS = ("n", "n_per_group", "n_pairs", "total", "total_n", "nobs",
                "events", "event_count", "time_to_target", "n_per_arm",
                "expected_n", "implied_n_clusters", "n_clusters", "total_clusters")
#: 设计参数类字段（归入「设计参数」组）
_PARAM_KEYS = ("alpha", "power", "effect", "d", "f", "p1", "p2", "side", "sd",
               "cv", "k_groups", "design", "theta0", "theta1", "theta2",
               "event_rate", "accrual_time", "hazard_ratio", "hr", "lambda1",
               "lambda2", "margin", "dropout_rate", "followup_time", "n_interim",
               "spending_func", "rho", "wt_delta", "auc0", "auc1", "m", "icc",
               "nsim", "varcorr", "sigma", "prior_a0", "n_doses", "target_dlt")
#: 元信息类字段（归入「计算概要」组）
_META_KEYS = ("solve_for", "type", "method", "test", "axis", "series",
              "alternative", "alt")


def _fmt_num(v) -> str:
    """数值格式化：int 原样；float 保留 4 位有效小数（去掉尾随 0）。"""
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        s = f"{v:.4f}".rstrip("0").rstrip(".")
        return s if s else "0"
    return str(v)


def _render_hero(stats: dict) -> str:
    """顶部结论 Hero：样本量 + 效能（样本量计算的两个核心答案）。

    forward（求 n）→ 主显样本量，副显目标效能；
    reverse（求 power）→ 主显效能，副显给定样本量。
    达标（power ≥ 目标 0.8）显示绿色徽章，否则橙色提醒。
    """
    if not isinstance(stats, dict):
        return ""
    solve_for = str(stats.get("solve_for") or "").lower()
    # 主指标：求 n 时主显 n；求 power 时主显 power
    n_val = next((stats[k] for k in _RESULT_KEYS
                  if k in ("n", "n_per_group", "n_pairs", "total", "total_n")
                  and isinstance(stats.get(k), (int, float))), None)
    p_val = next((stats[k] for k in ("power", "achieved_power")
                  if isinstance(stats.get(k), (int, float))), None)

    if solve_for == "power" or (n_val is None and p_val is not None):
        lead, main_v, main_unit = "达成功效", _fmt_num(p_val), ""
        sub_bits = ([f"给定 n = {_fmt_num(n_val)}"] if n_val is not None else [])
    elif n_val is not None:
        lead, main_v, main_unit = "所需样本量", _fmt_num(n_val), " 例/组"
        sub_bits = ([f"目标功效 {_fmt_num(p_val)}"] if p_val is not None else [])
    else:
        return ""

    # 达标徽章：power 达 0.8 视为达标（常规检验效能阈值）
    badge = ""
    if p_val is not None:
        ok = float(p_val) >= 0.8
        badge = (f'<span class="badge ok"><span class="dot"></span>功效达标</span>'
                 if ok else
                 f'<span class="badge warn"><span class="dot"></span>功效偏低</span>')

    sub = " · ".join(sub_bits + ([badge] if badge else []))
    return (
        f'<div class="hero">'
        f'<div class="lead">{lead}</div>'
        f'<div class="est">{main_v}'
        f'<span class="unit">{main_unit}</span></div>'
        f'<div class="sub">{sub}</div>'
        f'</div>'
    )


def _group_card(title: str, ico: str, rows_html: str) -> str:
    """一张语义分组卡（标题 + 图标 + kv 表）。"""
    if not rows_html:
        return ""
    return (
        f'<details class="grp" open><summary><span>{ico} {title}</span></summary>'
        f'<table class="stats">{rows_html}</table></details>'
    )


def _render_stats_groups(stats: dict) -> str:
    """stats 按语义分组渲染（设计参数 / 计算结果 / 计算概要 / 其它），
    不再压平成单一大表；数组型（曲线/网格数据）单独成折叠卡。"""
    if not isinstance(stats, dict):
        return '<table class="stats">%s</table>' % _kv_rows_compat(stats)
    groups = []
    param_rows, result_rows, meta_rows, other_rows = [], [], [], []
    array_keys = []

    for k, v in stats.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            array_keys.append((k, v))
            continue
        if isinstance(v, dict):
            other_rows.append(_kv_row(k, _json_compact(v)))
            continue
        if k in _PARAM_KEYS:
            param_rows.append(_kv_row(k, v))
        elif k in _RESULT_KEYS:
            result_rows.append(_kv_row(k, v))
        elif k in _META_KEYS:
            meta_rows.append(_kv_row(k, v))
        else:
            other_rows.append(_kv_row(k, v))

    groups.append(_group_card("计算结果", "🎯", "".join(result_rows)))
    groups.append(_group_card("设计参数", "⚙️", "".join(param_rows)))
    groups.append(_group_card("计算概要", "📋", "".join(meta_rows)))
    groups.append(_group_card("其它", "📦", "".join(other_rows)))
    # 数组型（曲线/网格序列）→ 折叠卡，避免超长数组撑爆页面
    if array_keys:
        arr_html = "".join(
            f'<div class="arr"><span class="k">{_html_escape(k)}</span>'
            f'<span class="v">{_html_escape(_arr_summary(v))}</span></div>'
            for k, v in array_keys
        )
        groups.append(
            f'<details class="grp"><summary><span>📈 序列数据'
            f'（{len(array_keys)} 组）</span></summary>'
            f'<div class="arr-wrap">{arr_html}</div></details>'
        )
    return "".join(groups)


# ── 结论结构化解析（2026-08-28：narrative 多行文本 → 层次化结论卡）──
#   narrative 形如：
#     "\n========== t 检验 ==========\nCohen's d: 0.5000\n目标功效: 0.8000\n每组 n: 64"
#   解析为：`==== 标题 ====` → 小节标题；`key: value` → 条目行；其它 → 段落。
def _render_conclusion(narrative: str) -> str:
    """把多行 narrative 渲染成结构化结论（小节标题 + 条目 + 段落），
    替代 raw pre-wrap 平铺，结论更有层次、更易扫读。"""
    if not narrative or not narrative.strip():
        return ""
    blocks = []           # 每个元素: ("h", html) 小节标题 / ("row", html) 条目 / ("p", html)
    cur_title = None
    for raw in narrative.split("\n"):
        line = raw.strip()
        if not line:
            continue
        # 小节标题：`===== xxx =====`
        m = re.match(r"^=+\s*(.+?)\s*=+$", line)
        if m:
            cur_title = _html_escape(m.group(1).strip())
            blocks.append(("h", cur_title))
            continue
        # key: value 条目
        m2 = re.match(r"^(.+?):\s*(.*)$", line)
        if m2 and m2.group(1).strip():
            k = _html_escape(m2.group(1).strip())
            v = _html_escape(m2.group(2).strip())
            blocks.append(("row", (k, v)))
            continue
        # 其它段落
        blocks.append(("p", _html_escape(line)))

    if not blocks:
        return ""
    out = []
    for kind, payload in blocks:
        if kind == "h":
            out.append(f'<div class="concl-sec">📌 {payload}</div>')
        elif kind == "row":
            k, v = payload
            if v:
                out.append(f'<div class="concl-row"><span class="ck">{k}</span>'
                           f'<span class="cv">{v}</span></div>')
            else:
                out.append(f'<div class="concl-row"><span class="ck">{k}</span></div>')
        else:  # paragraph
            out.append(f'<div class="concl-p">{payload}</div>')
    return "".join(out)


def _kv_row(k, v) -> str:
    """单个 kv 行（值已格式化/转义）。"""
    return ('<tr><td class="k">%s</td><td class="v">%s</td></tr>'
            % (_html_escape(str(k)), _html_escape(_fmt_num(v) if isinstance(v, (int, float, bool)) else str(v))))


def _kv_rows_compat(x) -> str:
    """非 dict stats 的兼容渲染。"""
    return _kv_row("value", x)


def _json_compact(d: dict) -> str:
    import json as _json
    return _json.dumps(d, ensure_ascii=False)


def _arr_summary(v) -> str:
    """数组摘要：长度 + 前若干个值（避免超长）。"""
    try:
        n = len(v)
        head = ", ".join(_fmt_num(x) if isinstance(x, (int, float)) else str(x)
                         for x in list(v)[:6])
        return f"[{head}{', …' if n > 6 else ''}] （共 {n} 个）"
    except Exception:
        return str(v)[:200]


def _stats_to_rows(stats: dict) -> str:
    """扁平 stats dict → 两列 kv 行（键/值，值转义）。"""
    rows = []
    for k, v in stats.items():
        if v is None:
            continue
        if isinstance(v, (dict, list)):
            import json

            v = json.dumps(v, ensure_ascii=False)
        rows.append(
            '<tr><td class="k">%s</td><td class="v">%s</td></tr>'
            % (_html_escape(k), _html_escape(v))
        )
    return "".join(rows)


def _pretty_r(code: str) -> str:
    """轻量 R 格式化：仅在「括号深度>0 的逗号后」与「顶层分号后」断行（防破坏语义）。
    字符串/注释内部绝不断行（与 meta-analysis rendering._pretty_r 同思路的简化版）。"""
    out = []
    paren = 0
    in_str = None
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(code[i + 1]); i += 2; continue
            if ch == in_str:
                in_str = None
            i += 1; continue
        if ch == "#":
            j = code.find("\n", i)
            if j == -1:
                out.append(code[i:]); break
            out.append(code[i:j]); i = j; continue
        if ch in ('"', "'", "`"):
            in_str = ch; out.append(ch); i += 1; continue
        if ch in "([{":
            paren += 1; out.append(ch); i += 1; continue
        if ch in ")]}":
            paren = max(0, paren - 1); out.append(ch); i += 1; continue
        if ch == ";" and paren == 0:
            out.append(";\n"); i += 1; continue
        if ch == "," and paren > 0:
            out.append(",")
            k = i + 1
            while k < n and code[k] == " ":
                k += 1
            if re.match(r"[A-Za-z_.][\w.]*\s*=", code[k:]):
                # 只断一次行，缩进 = paren×2 空格；严禁 "\n  "*paren
                # （paren≥2 时会生成 \n  \n  \n… 相邻换行间仅缩进空格，
                #  在 HTML white-space:pre-wrap 下渲染成大片空白行）
                out.append("\n" + "  " * min(paren, 6))
                i = k
            else:
                i += 1
            continue
        out.append(ch); i += 1
    return "".join(out)


def _highlight_r(code: str) -> str:
    """R 代码语法高亮（注释/字符串/函数/数字）。

    单遍扫描：注释（#...）与字符串（"…"/'…'）先隔离成 span，再对普通代码段
    做函数/数字高亮。避免「先整体 escape 再正则加 span」导致后一个 pattern
    匹配前一个生成的 class="c" 等标签属性、产生嵌套损坏 span（2026-08-28 实测
    `<span class=<span class="s">"c"</span>>`）——单遍隔离后 span 标签不再进入
    后续正则的输入。
    """

    def _hl_plain(seg: str) -> str:
        esc = _html_escape(seg)
        esc = re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_.]*)\s*\(", r'<span class="f">\1</span>(', esc)
        esc = re.sub(r"\b(\d+\.?\d*)\b", r'<span class="n">\1</span>', esc)
        return esc

    out = []
    buf = []
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        if ch == "#":  # 注释 → 隔离成 .c span，普通段 flush
            j = code.find("\n", i)
            if j == -1:
                j = n
            out.append(_hl_plain("".join(buf)))
            buf = []
            out.append('<span class="c">%s</span>' % _html_escape(code[i:j]))
            i = j
            continue
        if ch in ('"', "'"):  # 字符串（含转义）→ 隔离成 .s span
            quote = ch
            j = i + 1
            while j < n:
                if code[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if code[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(_hl_plain("".join(buf)))
            buf = []
            out.append('<span class="s">%s</span>' % _html_escape(code[i:j]))
            i = j
            continue
        buf.append(ch)
        i += 1
    out.append(_hl_plain("".join(buf)))
    return "".join(out)


_CTSS_REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ct-samplesize 结果报告 · {test}</title>
<style>
:root{{
  --bg:#f7f8fa;--card:#fff;--border:#e5e7eb;--text:#1f2937;--muted:#6b7280;
  --accent:#2563eb;--accent2:#0ea5e9;--ok:#16a34a;--warn:#d97706;--bad:#dc2626;
  --radius:12px;--shadow:0 1px 3px rgba(15,23,42,.07);
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  /* 与 build_figure_widget 同名变量，确保内联 SVG 区块正确着色 */
  --color-text-primary:#1f2937;--color-border-tertiary:#e5e7eb;--border-radius-md:8px;
}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-sans);font-size:15px;line-height:1.6;}}
header{{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:20px 26px;}}
header h1{{margin:0;font-size:21px;font-weight:700;}}
header .meta{{font-size:13px;opacity:.92;margin-top:5px;}}
main{{max-width:1020px;margin:20px auto;padding:0 16px;display:flex;flex-direction:column;gap:16px;}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);}}
.card h2{{font-size:16px;margin:0 0 12px;color:var(--text);border-left:3px solid var(--accent);padding-left:8px;}}
table.stats{{border-collapse:collapse;width:100%;font-size:15px;}}
table.stats td{{border:1px solid var(--border);padding:6px 10px;vertical-align:top;}}
table.stats td.k{{background:#f9fafb;font-weight:600;width:36%;color:#374151;white-space:nowrap;}}
table.stats td.v{{color:#111827;font-weight:700;font-variant-numeric:tabular-nums;text-align:right;}}
.narrative{{font-size:15px;color:#334155;white-space:pre-wrap;}}
/* ── 结论结构化（2026-08-28：小节标题 + 条目 + 段落）── */
.conclusion{{font-size:15px;}}
.concl-sec{{font-weight:700;color:#1e3a8a;font-size:16px;margin:12px 0 8px;padding-bottom:4px;border-bottom:1px solid var(--border);}}
.conclusion .concl-sec:first-child{{margin-top:0;}}
.concl-row{{display:flex;gap:10px;padding:4px 0;border-bottom:1px dashed #f0f1f3;align-items:baseline;}}
.concl-row .ck{{font-weight:600;color:#374151;min-width:130px;flex-shrink:0;}}
.concl-row .cv{{color:#111827;font-weight:700;font-variant-numeric:tabular-nums;text-align:right;flex:1;}}
.concl-p{{color:#334155;padding:3px 0;}}
.banner{{background:#fef3c7;border:1px solid #f59e0b;color:#92400e;border-radius:var(--radius);padding:11px 15px;font-size:14px;}}
details.repro{{background:#eef1f5;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;}}
details.repro summary{{cursor:pointer;padding:13px 18px;font-size:15px;font-weight:600;color:#1e293b;outline:none;display:flex;justify-content:space-between;align-items:center;list-style:none;}}
details.repro summary::-webkit-details-marker{{display:none;}}
details.repro .meta{{font-size:12px;color:#57606a;margin:0 0 10px;}}
details.repro .body{{padding:0 18px 14px;}}
details.repro pre{{margin:0;max-height:440px;overflow:auto;background:#e3e8ee;padding:10px 12px;border:1px solid #d0d7de;border-radius:8px;}}
details.repro code{{font-family:"SFMono-Regular",Consolas,Menlo,monospace;font-size:12.5px;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;line-height:1.35;color:#24292e;}}
details.repro code .c{{color:#6a737d;font-style:italic;}}
details.repro code .s{{color:#032f62;}}
details.repro code .f{{color:#6f42c1;}}
details.repro code .n{{color:#005cc5;}}
.copy-btn{{font-size:13px;color:#57606a;background:#eaeef2;border:1px solid #d0d7de;border-radius:6px;padding:3px 10px;cursor:pointer;}}
.copy-btn:hover{{color:#1e293b;border-color:#b0b8c0;}}
footer{{text-align:center;color:var(--muted);font-size:12px;padding:18px;}}
/* ── Hero 结论卡（对齐 meta-analysis 参考风格：白色卡片、无底色、数值加粗）── */
.hero{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:20px 22px;box-shadow:var(--shadow);}}
.hero .lead{{font-size:12px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;font-weight:600;}}
.hero .est{{font-size:38px;font-weight:800;line-height:1.1;margin:6px 0 2px;
  color:var(--text);font-variant-numeric:tabular-nums;}}
.hero .est .unit{{font-size:17px;font-weight:700;color:var(--accent);margin-left:6px;}}
.hero .sub{{font-size:15px;color:var(--muted);display:flex;gap:10px;align-items:center;flex-wrap:wrap;}}
.badge{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;
  padding:2px 10px;border-radius:999px;}}
.badge.ok{{background:#dcfce7;color:#166534;}}
.badge.warn{{background:#fef3c7;color:#92400e;}}
.badge.bad{{background:#fee2e2;color:#991b1b;}}
.badge .dot{{width:7px;height:7px;border-radius:50%;background:currentColor;}}
.badge.warn .dot{{background:#fbbf24;}}
/* ── stats 语义分组卡（替代平铺大表）── */
details.grp{{border:1px solid var(--border);border-radius:8px;margin-top:10px;overflow:hidden;background:#fcfcfd;}}
details.grp summary{{cursor:pointer;padding:10px 12px;font-size:15px;font-weight:600;
  color:#1e293b;background:#f3f4f6;list-style:none;outline:none;}}
details.grp summary::-webkit-details-marker{{display:none;}}
details.grp table.stats{{font-size:14px;}}
.arr-wrap{{padding:8px 12px;}}
.arr{{display:flex;gap:10px;font-size:12px;padding:3px 0;border-bottom:1px dashed var(--border);}}
.arr .k{{font-weight:600;color:#374151;min-width:80px;white-space:nowrap;}}
.arr .v{{color:#111827;font-family:"SFMono-Regular",Consolas,Menlo,monospace;
  overflow-wrap:anywhere;}}
/* ── 暗色模式（系统偏好跟随）── */
@media (prefers-color-scheme:dark){{
  :root{{--bg:#0f172a;--card:#1e293b;--border:#334155;--text:#e2e8f0;--muted:#94a3b8;
    --color-text-primary:#e2e8f0;--color-border-tertiary:#334155;}}
  table.stats td.k{{background:#243244;color:#cbd5e1;}}
  table.stats td.v,table.stats td{{color:#e2e8f0;border-color:#334155;}}
  .narrative{{color:#cbd5e1;}}
  .concl-sec{{color:#93c5fd;border-color:#334155;}}
  .concl-row{{border-color:#2a3a50;}}
  .concl-row .ck{{color:#cbd5e1;}} .concl-row .cv{{color:#e2e8f0;}}
  .concl-p{{color:#cbd5e1;}}
  details.grp{{background:#1a2436;}}
  details.grp summary{{background:#243244;color:#e2e8f0;}}
  details.repro{{background:#1a2436;border-color:#334155;}}
  details.repro summary{{color:#e2e8f0;}}
  details.repro pre{{background:#0f172a;border-color:#334155;}}
  details.repro code{{color:#e6edf3;}}
  .arr .k{{color:#cbd5e1;}} .arr .v{{color:#e2e8f0;}}
  .fig-note{{background:#243244;}}
}}
@media (max-width:640px){{
  main{{padding:0 10px;}}
  .hero .est{{font-size:30px;}}
}}
@media print{{
  body{{background:#fff;}} .card{{box-shadow:none;break-inside:avoid;}}
  .copy-btn{{display:none;}}
  details.grp,details.repro{{break-inside:avoid;}}
  details.grp:not([open]),details.repro:not([open]){{display:block;}}
  .hero{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
}}
</style></head>
<body>
<header><h1>ct-samplesize 结果报告 · {test}</h1>
<div class="meta">{generated}</div></header>
<main>
{banner}
{hero_card}
{figures_card}
{stats_card}
{narrative_card}
{repro_card}
</main>
<footer>ct-samplesize · 单文件 HTML 报告（SVG 已内联固化，S3 链接过期不影响查看）</footer>
<script>
function copyR(btn){{
  var pre=btn.closest('details').querySelector('pre');
  navigator.clipboard.writeText(pre.innerText).then(function(){{
    var t=btn.textContent;btn.textContent='已复制 ✓';setTimeout(function(){{btn.textContent=t;}},1500);
  }});
}}
</script>
</body></html>"""


def render_html_report(out: dict, out_dir: str = ".", test: str = "ctss",
                       backend: str = "coze", show_alloc: bool = True) -> str | None:
    """把 coze 结果信封固化成单文件 HTML 报告（浏览器直接打开）。

    out 结构（CozeBackend.compute 已回填后的信封）：
      {status, stats: dict, narrative: str, figures: [{format, content, caption}],
       repro: {r, r_version, packages} | {url,...} | None, warnings, notes}

    策略（对齐 meta-analysis）：SVG 与 R 代码已在本地回填（_fill_external_svgs），
    这里全部**内联固化**进 HTML —— S3 预签名链接 3600s 过期也不影响查看。

    Returns: html 文件绝对路径（成功）或 None（无任何可展示内容 / 写出失败）。
    """
    stats = out.get("stats")
    figs = out.get("figures") or []
    # 本地渲染层：未显式要求不等比例分配时，隐藏 coze 默认返回的「分配比四图」
    # （caption 含 'alloc' 字样，如 'ctss alloc ttest ind 1'）。coze 端仍返回全量图，
    # 仅在此处按用户意图过滤——符合"瘦客户端只消费、不回炉重绘"的架构。
    if not show_alloc:
        figs = [f for f in figs if "alloc" not in (f.get("caption") or "").lower()]
    inline = [f for f in figs if isinstance(f, dict) and f.get("content")]
    repro = out.get("repro")
    narrative = out.get("narrative") or ""
    has_content = bool(inline) or stats is not None or narrative or (
        isinstance(repro, dict) and repro.get("r")
    )
    if not has_content:
        return None

    # ── banner（警告 + 契约漂移，唯一用户可见出口 · ct-base §20.9）──
    warnings = out.get("warnings") or []
    banner = ""
    if warnings:
        banner = '<div class="banner">⚠️ %s</div>' % _html_escape("；".join(str(w) for w in warnings))
    # 契约漂移横幅：仅当 coze 响应结构与本地技能预期不一致（_needs_upgrade 且 _contract_drift 非空）时，
    # 在报告顶部渲染一次升级提示（结构别名已本地自适应，故为"已适配+建议升级"，非中断）。
    drift = out.get("_contract_drift")
    if out.get("_needs_upgrade") and isinstance(drift, list) and drift:
        items = "".join("<li>%s</li>" % _html_escape(d) for d in drift)
        banner += (
            '<div class="banner"><strong>⚠️ coze 返回结构与本地技能预期不一致，已在本地自动适配。'
            '如频繁出现，建议升级 ct-samplesize 技能到最新版：</strong><ul>%s</ul></div>' % items
        )

    # ── 图形卡（复用 build_figure_widget 内联管线）──
    # 2026-08-28 优化：按 figures[].type 分组（曲线类/分布类/热力图/随访），
    # 而非全部平铺；分组标题用中文，组内用 coze 端双语 caption 作子标题。
    figures_card = ""
    if inline:
        type_names = {
            "curve": "样本量 / 效能曲线",
            "effect_curve": "效应量轴曲线",
            "dist": "H0/H1 分布重叠图",
            "heatmap": "效能热力图",
            "surv_time": "效能-随访时间曲线",
            "adaptive": "适应性设计图",
        }
        svg_figs, titles = [], []
        for i, f in enumerate(inline, 1):
            svg_figs.append({"svg": f.get("content", "")})
            ftype = f.get("type") or ""
            grp = type_names.get(ftype)
            titles.append(f"{grp} — {f.get('caption')}" if grp
                          else (f.get("caption") or "图 %d" % i))
        widget = build_figure_widget(svg_figs, titles)
        figures_card = (
            '<section class="card"><h2>📊 图形（%d）</h2>' % len(inline)
            + widget + "</section>"
        )

    # ── Hero + stats 卡（2026-08-28：借鉴 meta-analysis 信息架构）──
    hero_card = _render_hero(stats) if isinstance(stats, dict) else ""
    stats_card = ""
    if stats is not None:
        stats_card = (
            '<section class="card"><h2>🧮 计算结果</h2>'
            "%s</section>" % _render_stats_groups(stats)
        )

    # ── 结论卡（2026-08-28：多行 narrative → 结构化层次结论，替代 raw 平铺）──
    narrative_card = ""
    if narrative.strip():
        concl_html = _render_conclusion(narrative)
        if concl_html:
            narrative_card = (
                '<section class="card"><h2>📝 结论</h2>'
                '<div class="conclusion">%s</div></section>'
                % concl_html
            )
        else:
            narrative_card = (
                '<section class="card"><h2>📝 结论</h2>'
                '<div class="narrative">%s</div></section>'
                % _html_escape(narrative)
            )

    # ── R 复现卡（折叠 + 高亮 + copy；对齐 meta-analysis 架构：R 代码在报告最后）──
    repro_card = ""
    if isinstance(repro, dict) and repro.get("r"):
        rv = repro.get("r_version")
        pkgs = repro.get("packages") or {}
        if isinstance(pkgs, dict):
            pkg_line = " · ".join(f"{_html_escape(k)} {_html_escape(str(v))}"
                                  for k, v in pkgs.items())
        else:
            pkg_line = _html_escape(", ".join(str(p) for p in pkgs))
        rmeta = (f"R {_html_escape(str(rv))} · {pkg_line}" if rv else pkg_line)
        repro_card = (
            '<details class="repro"><summary>R 复现脚本'
            '<span><button class="copy-btn" onclick="copyR(this)">复制</button></span></summary>'
            '<div class="body"><div class="meta">%s</div>'
            '<pre><code>%s</code></pre></div></details>'
            % (rmeta, _highlight_r(_pretty_r(repro["r"])))
        )

    html = _CTSS_REPORT_TEMPLATE.format(
        test=_html_escape(test),
        generated=time.strftime("%Y-%m-%d %H:%M:%S"),
        backend=_html_escape(backend),
        banner=banner,
        hero_card=hero_card,
        figures_card=figures_card,
        stats_card=stats_card,
        narrative_card=narrative_card,
        repro_card=repro_card,
    )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "ctss_report_%s_%d.html" % (test, int(time.time())))
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return os.path.abspath(path)
    except OSError:
        return None


if __name__ == "__main__":
    import sys

    # 自测：python rendering.py <case.json> [titles...]
    import json

    env = json.load(open(sys.argv[1], encoding="utf-8"))
    figs = env.get("figures") or env.get("result", {}).get("figures") or []
    titles = sys.argv[2:] or [f"图 {i+1}" for i in range(len(figs))]
    print(build_figure_widget(figs, titles))
