#!/usr/bin/env python3
"""report_charts.py - 报告内的图表构造与低置信度 / 通用格式化辅助。
从 generate_report.py 拆出的自洽闭包：纯展示层，不依赖报告编排逻辑。
通用辅助（_esc / _fmt_inline / format_number / _disp_width / _pad_label）被 generate_report
re-export 以保向后兼容；图表构造（donut / bar / cost-chart）与低置信度标记（_lc_*）一并归属此模块。
"""
import html
import json
import math
import unicodedata

def _esc(value):
    """HTML 转义：防止会话标题 / 模型名 / 自动化名等用户派生文本注入 HTML（XSS）。"""
    return html.escape(str(value), quote=True)
# ── 共享渲染层（D7 去重：MD / HTML 共用同一套数据计算，仅渲染层不同）─────────────
# 中性内联标记：**粗体** / `代码`；md 原样保留，html 转为 <b>/<code> 并对纯文本段转义。
def _fmt_inline(text, fmt):
    """把中性内联标记（**粗体** / `代码`）渲染为 md 或 html；html 下对纯文本段做 HTML 转义。
    md 下原样保留标记（与历史输出一致）。"""
    if fmt == "md":
        return text
    out, buf = [], []
    i, n = 0, len(text)
    while i < n:
        if text[i:i + 2] == "**":
            if buf:
                out.append(_esc("".join(buf))); buf = []
            j = text.find("**", i + 2)
            if j == -1:
                out.append(_esc(text[i:])); break
            out.append("<b>" + _esc(text[i + 2:j]) + "</b>")
            i = j + 2
        elif text[i] == "`":
            if buf:
                out.append(_esc("".join(buf))); buf = []
            j = text.find("`", i + 1)
            if j == -1:
                out.append(_esc(text[i:])); break
            out.append("<code>" + _esc(text[i + 1:j]) + "</code>")
            i = j + 1
        else:
            buf.append(text[i]); i += 1
    if buf:
        out.append(_esc("".join(buf)))
    return "".join(out)
def format_number(n):
    """数字格式化：K/M/G 后缀"""
    if n is None:
        return "0"
    n = float(n)
    if n >= 1_000_000_000:
        return f"{n / 1e9:.2f}G"
    elif n >= 1_000_000:
        return f"{n / 1e6:.2f}M"
    elif n >= 1_000:
        return f"{n / 1e3:.1f}K"
    return str(int(n)) if n == int(n) else f"{n:.1f}"
def _disp_width(s):
    """等宽字体下的显示宽度：CJK / 全角字符计 2，其余（含 ASCII）计 1。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in str(s))
def _pad_label(s, width):
    """按显示宽度右侧补空格，使等宽字体下中文 / 英文混排的标签列对齐。"""
    return str(s) + " " * max(0, width - _disp_width(s))
# 环形图调色板（与表格配色协调）
_DONUT_PALETTE = [
    "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b",
    "#8e44ad", "#27ae60",
]
def build_donut_chart(stats, title="实际消耗 Token 占比（按任务类型，计费等效）",
                      center_label="实际消耗", value_key="effective_tokens", unit=""):
    """生成自包含内联 SVG 环形图（双主题兼容，currentColor + CSS 变量）。

    stats: 含 task_type 与各数值字段的列表。value_key 指定扇形取值字段，
    unit / center_label 控制图例单位与中心文字，使同一函数既能画「任务类型
    Token 占比」（默认），也能画「每会话成本分布」（value_key="count"、
    unit=" 会话"、center_label="会话数"）。无数据时返回空串；不依赖外部 CDN。
    """
    items = [s for s in stats if s.get(value_key, 0) > 0]
    total = sum(s.get(value_key, 0) for s in items)
    if total <= 0:
        return ""
    # 按占比降序，保证配色稳定
    items = sorted(items, key=lambda x: x.get(value_key, 0), reverse=True)

    cx, cy, r, sw = 110, 110, 80, 34
    circ = 2 * math.pi * r
    cum = 0.0
    arcs = []
    legend = []
    for i, s in enumerate(items):
        frac = s.get(value_key, 0) / total
        seg_len = frac * circ
        color = _DONUT_PALETTE[i % len(_DONUT_PALETTE)]
        pct = frac * 100
        # 用 stroke-dasharray 画出圆环段；dashoffset 让各段首尾相接
        arcs.append(
            f'        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" '
            f'stroke-dasharray="{seg_len:.2f} {circ - seg_len:.2f}" '
            f'stroke-dashoffset="{-cum:.2f}" />'
        )
        legend.append(
            f'            <div class="legend-item">'
            f'<span class="swatch" style="background:{color}"></span>'
            f'{_esc(s["task_type"])}：{pct:.1f}%'
            f'<span class="pct">（{format_number(s.get(value_key, 0))}{unit}）</span></div>'
        )
        cum += seg_len

    svg = f"""    <div class="chart-pie">
        <svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="{title}">
            <g transform="rotate(-90 {cx} {cy})">
                <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" style="stroke:var(--table-border)" stroke-width="{sw}" />
{chr(10).join(arcs)}
            </g>
            <text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="15" font-weight="bold" style="fill:var(--accent-fg)">{format_number(total)}</text>
            <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="11" style="fill:var(--muted)">{center_label}</text>
        </svg>
        <div class="legend">
{chr(10).join(legend)}
        </div>
    </div>"""
    return svg
def build_session_cost_bar_md(buckets, title="每会话成本分布（按会话数）"):
    """Markdown 横向条形图（fenced ``` 代码块）：每会话成本分布，按会话数。

    与 HTML 版环形图数据同源：成本区间 → 会话数。纯文本代码块随查看器浅/深主题
    自适应，各区间独立一行绝不重叠，窄区间只是短条不会糊；行尾标注会话数。
    """
    items = [b for b in buckets if b.get("count", 0) > 0]
    if not items:
        return ""
    maxc = max(b["count"] for b in items) or 1
    bar_w = 20
    label_w = max((_disp_width(b["label"]) for b in items), default=10)
    rows = [f"**{title}**", "", f"{_pad_label('成本区间', label_w)} | {'会话数'}"]
    for b in items:
        n = max(int(bar_w * b["count"] / maxc), 1)
        bar = "█" * n
        rows.append(f"{_pad_label(b['label'], label_w)} | {bar} {b['count']}")
    return "```\n" + "\n".join(rows) + "\n```"
def build_task_type_chart_md(stats, title="各任务类型 实际消耗 Token 占比"):
    """Markdown 横向条形图：各任务类型 实际消耗 Token 占比。

    替换原先的 mermaid 饼图——因为 mermaid 饼图在 .md 预览里无法稳定满足：
    (1) 浅/深外观下文字可能消失（强制 theme 不可靠）；
    (2) 窄扇区标签会糊在一起（mermaid 无「仅图例」模式，标签直接画在扇区上）。

    横向条形图用 fenced ``` 纯文本代码块，与 3.1/3.2 模型条形图同风格：
    - 主题安全：文字取查看器代码块前景色，切换浅/深外观绝不消失；
    - 永不重叠：每个任务类型独立一行；
    - 窄项只是短条，不会糊；标签用 _pad_label 按显示宽度对齐（兼容中英文混排）。
    """
    items = [s for s in stats
             if s.get("effective_tokens", 0) > 0]
    total = sum(s.get("effective_tokens", 0) for s in items)
    if total <= 0:
        return ""
    # 合并窄项，保持行数清爽
    MERGE_THRESHOLD = 2.5  # 百分比
    rows_data = []
    other_pct = 0.0
    other_tok = 0
    for s in items:
        pct = s.get("effective_tokens", 0) / total * 100
        if pct < MERGE_THRESHOLD and s["task_type"] != "其他":
            other_pct += pct
            other_tok += s.get("effective_tokens", 0)
        else:
            rows_data.append([s["task_type"], pct, s.get("effective_tokens", 0)])
    if other_pct > 0:
        rows_data.append(["其他", other_pct, other_tok])
    rows_data.sort(key=lambda x: x[1], reverse=True)
    rows_data = rows_data[:10]
    max_pct = max(r[1] for r in rows_data) or 1
    bar_w = 32
    label_w = 16
    out = []
    for label, pct, toks in rows_data:
        n = max(int(bar_w * pct / max_pct), 1)
        bar = "█" * n
        lab = _pad_label(label, label_w)
        out.append(f"{lab} | {bar} {pct:.1f}% ({format_number(toks)})")
    return "```\n" + "\n".join(out) + "\n```"
# ── 模型使用与成本对比（新章节）────────────────────────────
def _lc_reason(name, low_conf_map):
    """查模型是否属低置信度（估算与实际计费存在已知系统性偏差），返回原因或空串。"""
    if not low_conf_map or not name:
        return ""
    return low_conf_map.get(name) or low_conf_map.get(str(name).lower()) or ""
def build_model_cost_chart_md(model_stats, title="各模型估算实际花费对比", low_conf_map=None, low_conf_bias_map=None):
    """Markdown 横向条形图：各模型估算实际花费对比（与 HTML 条形图对齐）。

    用 fenced ``` 代码块承载 ASCII 横向条：查看器按代码块主题自适应明暗，
    且对超长模型名（如 custom-local:GLM-4.5-air）无渲染问题。条形长度按
    最大花费线性映射，行尾标注金额，与 HTML `build_model_cost_chart` 同源。

    低置信度模型（受服务端时段减免 / 配额影响）在行首标 ⚠，
    并在图下追加免责脚注，避免用户拿它做预算。
    """
    items = [m for m in model_stats if (m.get("effective_cost", 0) or 0) > 0]
    if not items:
        return ""
    items = sorted(items, key=lambda x: x.get("effective_cost", 0), reverse=True)
    maxc = max(m.get("effective_cost", 0) for m in items) or 1
    bar_w = 32          # ASCII 条最大长度
    label_w = 28        # 模型名列宽（含 2 字符置信度标记位）
    rows = [f"**{title}**", ""]
    n_lc = 0
    for m in items:
        c = m.get("effective_cost", 0)
        n = max(int(bar_w * c / maxc), 1)
        bar = "█" * n
        hit = bool(_lc_reason(m.get("model"), low_conf_map))
        if hit:
            n_lc += 1
        arrow = _lc_arrow(_lc_bias(m.get("model"), low_conf_bias_map)) if hit else ""
        label = (arrow + " " if hit else "  ") + str(m["model"])
        if len(label) > label_w:
            label = label[:label_w - 1] + "…"
        else:
            label = label.ljust(label_w)
        rows.append(f"{label} | {bar} ¥{c:.2f}")
    if n_lc:
        rows.append("")
        # 图例只在真的画出了方向箭头时出现（无 bias 映射时行内是纯 ⚠，讲箭头方向是噪音）
        _has_arrow = any(_lc_bias(m.get("model"), low_conf_bias_map) in ("over", "under")
                         for m in items if _lc_reason(m.get("model"), low_conf_map))
        _legend = "箭头表示偏差方向：⚠↑ 高估 / ⚠↓ 低估。" if _has_arrow else ""
        rows.append(f"⚠ = 低置信度估算（{n_lc} 个模型存在服务端时段减免 / 配额，"
                    "估算与实际计费偏差已知较大），不参与成本结论，请勿据此做预算。" + _legend)
    return "```\n" + "\n".join(rows) + "\n```"
def build_model_cost_chart(model_stats, title="各模型估算实际花费对比", low_conf_map=None, low_conf_bias_map=None):
    """HTML 内联条形图：各模型估算实际花费对比（仅含已配置单价模型）。

    低置信度模型标 ⚠ 并附 title 提示，图下追加免责脚注。
    """
    items = [m for m in model_stats if (m.get("effective_cost", 0) or 0) > 0]
    if not items:
        return ""
    items = sorted(items, key=lambda x: x.get("effective_cost", 0), reverse=True)
    maxc = max(m.get("effective_cost", 0) for m in items) or 1
    rows = []
    n_lc = 0
    for m in items:
        c = m.get("effective_cost", 0)
        w = max(int(220 * c / maxc), 1)
        reason = _lc_reason(m.get("model"), low_conf_map)
        if reason:
            n_lc += 1
        mark = _lc_arrow(_lc_bias(m.get("model"), low_conf_bias_map)) if reason else ""
        rows.append(
            f'        <div class="bar-row"><span class="bar-label" title="{_esc(m["model"])}">{mark}{_esc(m["model"])}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{w}px"></span></span>'
            f'<span class="bar-val">¥{c:.2f}</span></div>'
        )
    foot = ""
    if n_lc:
        # 图例只在真的画出了方向箭头时出现（与 MD 版口径一致）
        _has_arrow_h = any(_lc_bias(m.get("model"), low_conf_bias_map) in ("over", "under")
                           for m in items if _lc_reason(m.get("model"), low_conf_map))
        _legend_h = '箭头表示偏差方向：⚠↑ 高估 / ⚠↓ 低估。' if _has_arrow_h else ''
        foot = (f'\n      <p class="lc-note">⚠ = 低置信度估算（{n_lc} 个模型存在服务端时段减免 / 配额，'
                '估算与实际计费偏差已知较大），不参与成本结论，请勿据此做预算。'
                + _legend_h + '</p>')
    return (
        f'    <div class="chart-bars">\n      <p><strong>{_esc(title)}</strong></p>\n'
        + "\n".join(rows)
        + foot
        + "\n    </div>"
    )
def _lc_bias(name, bias_map):
    """模型低置信度偏差方向：over/under/mixed/''（空=可信）。"""
    if not bias_map or not name:
        return ""
    return bias_map.get(name) or bias_map.get(str(name).lower()) or ""
def _lc_arrow(bias):
    """偏差方向 -> 报告标记：⚠↑ 高估 / ⚠↓ 低估 / ⚠ 方向不明或未知。"""
    if bias == "over":
        return "⚠↑"
    if bias == "under":
        return "⚠↓"
    return "⚠"
def _tier_rates_snippet(meta):
    """生成 mode_rates 的 JSON 片段（供可配置折叠块展示），逐行字符串列表。"""
    rates = meta.get("mode_rates") or {}
    lines = ['  "mode_rates": {', '    "auto_estimate": true,']
    for tier_name, t in rates.items():
        if not isinstance(t, dict):
            continue
        lines.append(
            f'    "{tier_name}": {{ "alias": "{t.get("alias")}", "label": "{t.get("label")}", '
            f'"multiplier": {t.get("multiplier")}, "input": {t.get("input")}, "output": {t.get("output")} }},'
        )
    lines.append('  }')
    return lines
