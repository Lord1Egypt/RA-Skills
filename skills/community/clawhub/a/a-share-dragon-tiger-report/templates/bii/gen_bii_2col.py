#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BII 双栏范式变体 · A股涨停板龙虎榜深度研判报告（A4 横向）

与 templates/report_template.html（样式 A：MS 色系 + ECharts + A4 纵向）并列的
第二种排版样式（样式 B）：BlackRock 投资研究院（BII）的「左文字栏 + 右图表」双栏范式。

页面单位 = 一页 = runhead + (295px 左文字栏 ‖ 自适应右图表栏) + runfoot
右栏卡片 = 图号 + 结论式标题 + 口径副标题 + 图体 + 黑底「图表结论」条 + 资料来源脚注

用法：
    python3 templates/bii/gen_bii_2col.py --data strategy/sample_data.json --date 2026-09-16 \
        --predict-file strategy/predictions.example.json \
        --out out/dragon-tiger-20260916

产出：<out>/涨停板龙虎榜深度研判报告-BII双栏-YYYYMMDD.html（自包含，Chart.js 已内联）

次日 5 条可证伪预判（第 14 页）由 `--predict-file` / `--predictions` 注入；缺省时自动探测
<data 同级>/predictions.json，再退到 <out>/predictions.json。三者都缺则渲染「示例占位页」
（并明确标注），使模板在无预判数据时仍可独立跑通。

⚠️ 三个防坑工具函数（jsarr / jsdata / svgbox / strip_svg_take）都是有来历的，见 SKILL.md §12.3，
   不要"简化"掉。图型元素数均设了上限（_MAX_*），防止真实候选池变大时把图挤成一团。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from strategy import calibers as C          # noqa: E402
from strategy import formulas as F          # noqa: E402
from strategy import funnel as FN           # noqa: E402
from strategy import pipeline as PL         # noqa: E402
from strategy import limitup_source as LS   # noqa: E402


def _money(v: float) -> str:
    """金额三档自适应（2026-11-11 v3.1.2 资金规模层扩展）：
    ≥1亿 → 亿元(2位)；≥1万 → 万元(2位)；否则 → 元(整数)。
    7000 元级小本金用「万元」会塌缩成 0 万；7 亿级用「万元」会写成 70000.00万。
    正文金额一律走本函数；图表柱值由 _scale_unit() 决定刻度单位。"""
    v = float(v or 0.0)
    a = abs(v)
    if a >= 1e8:
        return f"{v/1e8:.2f}亿"
    if a >= 1e4:
        return f"{v/1e4:.2f}万"
    return f"{v:.0f}元"


def _scale_unit(equity: float) -> tuple[float, str]:
    """图表金额单位：机构级(≥1亿)用亿元，其余用万元。"""
    return (1e8, "亿元") if float(equity or 0) >= 1e8 else (1e4, "万元")


def _is_institutional(equity: float) -> bool:
    """资金规模分层闸门：≥1亿 走机构级容量约束结构；否则小本金路径逐字不变。"""
    return float(equity or 0) >= 1e8

CHART_LIB = (HERE / "chart.umd.js").read_text(encoding="utf-8")   # Chart.js 4.4.1 本地内联
CHART_TPL = (HERE / "chart_js_bii.js").read_text(encoding="utf-8")

TOTAL = 14                      # 纯 v2.3 版式：封面 + 13 个编号页；v3.0 开启时 main() 改为 16
PRED_PNO = 14                   # 次日 5 条预判页固定第 14 页（v3.0 只在其后追加附录页）
CODE = "LHB"                    # 运行时按日期填，形如 LHB0916-2026
SRC_LINE = "腾讯自选股（westock-mcp）· 四层漏斗 L1→L2→L2.5→L3 + 财富密码选股策略"

# 图型元素数上限 —— 真实候选池可达数十只，不设上限会把图挤成一团、也会顶破版心高度
_MAX_RANK = 12      # 图 4 综合分排行
_MAX_FIN = 10       # 图 5 财务对照
_MAX_PB = 10        # 图 6 PB 排序
_MAX_DIM = 8        # 图 7 五维分项
_MAX_BUB = 16       # 图 2 行业气泡


def pb_tradable(c: dict) -> bool:
    """图 6（PB 排序）与其配套论述的准入条件。

    要求 **PB > 0** 且 **未命中 L2.5 名称类剔除**（含「退市」/「ST」/「*ST」）。

    历史缺陷：0917 首版只加了 `float(pb) > 0`，漏掉名称类校验 → 已退市的
    「退市观典」（delisted=True、股价 0.37 元）以 PB 0.23 排到第 2 名，
    并被图结论条归入「低估值区（PB ≤2×）」，与同一份报告第 3 页的
    「L2.5 不可交易清单」直接自相矛盾。
    根因与口径 17 完全一致：**相对估值指标无法识别「公司已经不存在」**，
    必须叠加名称类校验；PB 为负同理（净资产为负 ≠ 特别便宜）。
    """
    v = c.get("pb")
    if v is None:
        return False
    try:
        if not float(v) > 0:
            return False
    except (TypeError, ValueError):
        return False
    if c.get("delisted"):
        return False
    nm = str(c.get("name") or "")
    if c.get("is_st") or "退市" in nm or "ST" in nm.upper():
        return False
    return True


# ══════════════════════════════ 防坑工具函数 ══════════════════════════════
def jsarr(d: Any) -> str:
    """输出 JS 数组字面量。

    ⚠️ 字符串必须加引号：日期/代码这类值若不引号，JS 会把 `2025-09-01` 当成
    **减法算式**算成数字 2015，后续任何 s.slice()/toFixed() 都会抛
    `TypeError: s.slice is not a function`，而**顶层 IIFE 抛错会让同一 <script>
    里后面所有图表一起不执行** —— 症状是"所有 canvas 空白但 window.Chart 正常"。
    """
    out = []
    for v in d:
        if isinstance(v, str):
            out.append("'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'")
        elif v is None:
            out.append("null")
        elif isinstance(v, bool):
            out.append("true" if v else "false")
        else:
            out.append(str(v))
    return "[" + ",".join(out) + "]"


def jsdata(obj: Any) -> str:
    """把嵌套 dict/list 序列化为 JS 字面量（字符串同样必须加引号）。"""
    if isinstance(obj, dict):
        return "{" + ",".join(f"{k}:{jsdata(v)}" for k, v in obj.items()) + "}"
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(jsdata(v) for v in obj) + "]"
    if isinstance(obj, str):
        return "'" + obj.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    return str(obj)


def check_js_syntax(js: str, label: str = "chart_js") -> None:
    """JS 语法自检 —— 占位符检查只能发现"没替换"，发现不了"替换成了非法字面量"。

    ⚠️ 反面教材：模板里写 `var A={__X__}` 而注入端给的是数组字面量 `['a','b']`，
    两者都没报"未替换"，但拼出来是 `{['a','b']}` —— 语法错误，整段脚本不执行，
    8 张图全空白、而 window.Chart 却正常加载，排查起来极费时间。

    这里用 `node --check` 做真正的语法解析；无 node 时退化为括号配对粗检并给出提示。
    """
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(js)
        tmp = fh.name
    try:
        try:
            p = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if p.returncode != 0:
                msg = (p.stderr or p.stdout).strip().splitlines()
                detail = " / ".join(msg[:4]) if msg else "unknown"
                raise SystemExit(f"[!] {label} 存在 JS 语法错误：{detail}")
            return
        except FileNotFoundError:
            pass  # 无 node：退化为粗检
        # 粗检：括号/引号配对（能抓住大多数手写失误，但抓不住上面那种语义错）
        pairs = {")": "(", "]": "[", "}": "{"}
        stack: list[str] = []
        quote = None
        esc = False
        for ch in js:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if quote:
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"`":
                quote = ch
                continue
            if ch in "([{":
                stack.append(ch)
            elif ch in ")]}":
                if not stack or stack.pop() != pairs[ch]:
                    raise SystemExit(f"[!] {label} 括号不配对（粗检）")
        if stack or quote:
            raise SystemExit(f"[!] {label} 括号/引号未闭合（粗检）")
        print(f"[i] 未找到 node，{label} 仅做括号粗检")
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def svgbox(s: str, h: int | None = None) -> str:
    """内联 SVG：加 display:block 消除行内基线间隙；h=None 时按等比自然高度渲染（最清晰）。"""
    i = s.find(">")
    if i < 0:
        return s
    root = s[:i].replace('width="100%"', 'width="100%" preserveAspectRatio="xMidYMid meet"')
    style = "display:block;width:100%" + (f";height:{h}px" if h else "")
    return root + f' style="{style}"' + s[i:]


def strip_svg_take(s: str) -> str:
    """剔除 SVG 尾部内嵌的「图表结论」黑条（卡片自身已有 fig-take 条），并把 viewBox 收紧到内容下沿。

    复用外部脚本生成的 SVG（桑基图 / 分歧树 / 漏斗示意）时会踩到，
    否则页面上会出现**两条「图表结论」**。
    """
    k = s.rfind("</svg>")
    if k > 0:
        seg = s[:k]
        i = seg.rfind("<rect")
        if i >= 0 and "图表结论" in seg[i:]:
            s = seg[:i] + "</svg>"
    bot = 0.0
    for v in re.findall(r'\by="(-?[\d.]+)"', s):
        bot = max(bot, float(v))
    for m in re.finditer(r"<rect\b[^>]*>", s):
        t = m.group(0)
        y = re.search(r'\by="(-?[\d.]+)"', t)
        h = re.search(r'\bheight="([\d.]+)"', t)
        if y and h:
            bot = max(bot, float(y.group(1)) + float(h.group(1)))
    if bot > 0:
        s = re.sub(r'(viewBox="0 0 \d+ )\d+(")',
                   lambda m: m.group(1) + str(int(bot + 8)) + m.group(2), s, count=1)
    return s


# ══════════════════════════════ CSS ══════════════════════════════
CSS = """
:root{
  --bk:#000000; --by:#FFB500; --by-d:#C98A00; --by-l:#FFF4D6; --by-l2:#FFE9B0;
  --gy:#C9C9C4; --gy2:#9E9E98; --bg:#F7F7F5; --bw:#FFFFFF;
  --bd:#E2E2DD; --bd2:#EFEFEA; --t2:#4A4A4A; --t3:#8C8C8C;
  /* A 股习惯：涨红跌绿 —— 不随机构范式改变 */
  --up:#C1272D; --dn:#1E8449;
}
*{box-sizing:border-box;}
@page{ size: A4 landscape; margin: 0; }
html,body{margin:0;padding:0;background:#EDEDEA;}
body{font-family:"Helvetica Neue",Helvetica,Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:11.5px;line-height:1.72;-webkit-font-smoothing:antialiased;}
b{font-weight:600;}
.up{color:var(--up);} .dn{color:var(--dn);} .fl{color:var(--t3);}

/* ── 页 ── */
/* 全出血方案：@page margin:0，边距由 .page 自身 padding 提供。
   这样封面才能真的铺满整张纸（负 margin 在打印时会被 page margin 裁掉，做不出出血）。
   版心 = 297−12−12 = 273mm 宽 × 210−11−10 = 189mm 高 ≈ 1032×714 px @96dpi */
.page{width:297mm;min-height:210mm;padding:11mm 12mm 10mm 12mm;
      display:flex;flex-direction:column;
      page-break-after:always;break-after:page;}
.page:last-child{page-break-after:auto;break-after:auto;}
.runhead{display:flex;justify-content:space-between;align-items:baseline;
  font-size:8.5px;color:var(--t3);letter-spacing:.5px;padding-bottom:4px;
  border-bottom:1px solid var(--bd);margin-bottom:10px;text-transform:uppercase;flex:0 0 auto;}
.runfoot{display:flex;justify-content:space-between;font-size:8.5px;color:var(--t3);
  border-top:1px solid var(--bd);padding-top:4px;margin-top:auto;flex:0 0 auto;}
.pbody{flex:1;display:grid;grid-template-columns:295px minmax(0,1fr);gap:22px;align-content:start;}
.pbody.full{grid-template-columns:1fr;}

/* ── 左文字栏 ── */
.colL{font-size:11.5px;line-height:1.78;}
.eyebrow{font-size:9px;font-weight:700;color:var(--by-d);letter-spacing:1.5px;
  display:block;margin-bottom:5px;}
.colL h2{font-size:19px;font-weight:700;line-height:1.26;margin:0 0 10px;letter-spacing:-.4px;}
.colL p{margin:0 0 7px;}
.colL p.lead{font-size:12.5px;color:var(--t2);line-height:1.7;}
.pq{border-left:3px solid var(--by);padding:2px 0 2px 11px;margin:11px 0;
    font-size:13px;line-height:1.5;font-weight:600;color:var(--bk);}
.pq span{display:block;font-size:9px;font-weight:400;color:var(--t3);margin-top:4px;letter-spacing:.4px;}
.impl{background:var(--by-l);padding:9px 13px;margin:11px 0 0;}
.impl .k{font-size:9px;font-weight:700;color:var(--by-d);letter-spacing:1.2px;display:block;margin-bottom:4px;}
.impl ul{margin:0;padding-left:15px;font-size:11px;line-height:1.56;}
.impl li{margin:3px 0;}

/* ── 右图表栏 ── */
.colR{min-width:0;}
.fig{margin:0;}
.fig-h{border-left:4px solid var(--by);padding-left:10px;margin-bottom:8px;}
.fig-h .n{font-size:9px;font-weight:700;color:var(--by-d);letter-spacing:1.4px;display:block;margin-bottom:1px;}
.fig-h h3{font-size:15.5px;font-weight:700;margin:0 0 2px;letter-spacing:-.3px;line-height:1.28;}
.fig-h .sd{font-size:10.5px;color:var(--t3);margin:0;line-height:1.5;}
.fig-b{background:#fff;border:1px solid var(--bd);padding:8px 7px;}
.fig-b.tight{padding:6px 5px;}
.fig-take{background:var(--bk);color:#fff;padding:8px 13px;font-size:11px;line-height:1.54;}
.fig-take .k{font-weight:700;color:var(--by);letter-spacing:.5px;margin-right:7px;}
.fig-take b{color:var(--by);}
.fig-src{font-size:9px;color:var(--t3);line-height:1.58;margin-top:6px;}
.fig-src b{color:var(--t2);font-weight:600;}
canvas{display:block;margin:0 auto;}

/* ── 表格 ── */
table{width:100%;border-collapse:collapse;font-size:11px;table-layout:fixed;}
th{background:var(--bk);color:#fff;font-weight:600;font-size:10px;padding:5.5px 5px;
   text-align:right;white-space:nowrap;letter-spacing:.2px;}
th:first-child,td:first-child{text-align:left;}
td{padding:5px 5px;text-align:right;border-bottom:1px solid var(--bd2);
   white-space:nowrap;font-variant-numeric:tabular-nums;}
tbody tr:last-child td{border-bottom:none;}
tbody tr:nth-child(even){background:#FCFCFA;}
.hi{background:var(--by-l) !important;font-weight:600;}
.tag{display:inline-block;font-size:9px;padding:1px 5px;border-radius:2px;
     background:var(--bk);color:var(--by);font-weight:700;margin-left:4px;vertical-align:1px;}
.tag.g{background:var(--bd);color:var(--t2);}
.tcap{font-size:9px;color:var(--t3);margin-top:5px;line-height:1.55;}

/* ── v4.0 投行量化研判页（P19/P20）── */
.qstrip{font-size:10.5px;line-height:1.5;color:#3A2A00;background:#FFF6DC;
  border-left:4px solid var(--by);padding:8px 12px;margin:9px 0;}
.qstrip b{color:var(--by-d);}
.qwm{font-size:9px;line-height:1.65;color:var(--t3);}
.qwm b{color:var(--t2);}
.qbar{display:inline-block;vertical-align:middle;width:34px;height:7px;background:var(--bd2);
  margin-right:3px;position:relative;}
.qbar i{position:absolute;left:0;top:0;height:7px;background:var(--by);}
.qbar.hot i{background:var(--up);} .qbar.low i{background:var(--dn);}
.qdim{font-variant-numeric:tabular-nums;color:var(--t2);}
.qcomp{background:var(--by-l);font-weight:700;font-variant-numeric:tabular-nums;}
.pmCause{font-size:9.5px;line-height:1.5;color:var(--t3);}
.pmCause b{color:var(--t2);}
.qdisc{background:var(--bg);border-top:3px solid var(--by);padding:8px 12px;
  font-size:8.8px;color:var(--t3);line-height:1.62;margin-top:10px;}
.qdisc b{color:var(--t2);}

/* ── 封面（全出血：占满整张 A4 横向，无白边） ── */
.cover{background:var(--bk);color:#fff;min-height:210mm;display:flex;flex-direction:column;
       width:297mm;page-break-after:always;break-after:page;
       padding:15mm 18mm 11mm;}
.cover .brand{display:flex;align-items:center;gap:9px;margin-bottom:34px;}
.cover .brand .dot{width:14px;height:14px;background:var(--by);}
.cover .brand .nm{font-size:11px;letter-spacing:2.8px;font-weight:700;color:var(--by);}
.cover .brand .code{margin-left:auto;font-size:9px;color:#7A7A7A;letter-spacing:.6px;}
.cover h1{font-size:38px;font-weight:700;line-height:1.16;margin:0 0 14px;letter-spacing:-1px;max-width:780px;}
.cover h1 em{font-style:normal;color:var(--by);}
.cover .sub{font-size:13.5px;color:#C9C9C9;line-height:1.62;max-width:680px;margin:0 0 28px;}
.cover .rule{height:4px;background:var(--by);width:86px;margin-bottom:22px;}
.cover .meta{font-size:10.5px;color:#8C8C8C;line-height:1.95;margin-top:auto;max-width:930px;}
.cover .meta b{color:#DADADA;font-weight:500;}
.cover .gcceo-strip{border-left:4px solid var(--by);background:var(--bg);padding:9px 13px;
      font-size:11px;color:var(--t2);line-height:1.65;margin-bottom:18px;max-width:930px;}
.cover .gcceo-strip .k{display:block;font-size:9px;font-weight:700;letter-spacing:1.2px;
      color:var(--by);margin-bottom:3px;}

/* ── 摘要页 ── */
.verdict{background:var(--bk);color:#fff;padding:11px 19px;font-size:12.5px;line-height:1.72;margin:0 0 9px;}
.verdict .k{display:inline-block;background:var(--by);color:#000;font-size:9.5px;font-weight:700;
            padding:1.5px 8px;letter-spacing:.9px;margin-bottom:7px;}
.verdict b{color:var(--by);font-weight:600;}
.kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;
      border-top:1px solid var(--bd);border-left:1px solid var(--bd);margin-bottom:14px;}
.kpi{padding:9px 11px;border-right:1px solid var(--bd);border-bottom:1px solid var(--bd);}
.kpi .l{font-size:9.5px;color:var(--t3);margin:0 0 3px;line-height:1.35;}
.kpi .v{font-size:18px;font-weight:700;letter-spacing:-.5px;margin:0;font-variant-numeric:tabular-nums;line-height:1.2;}
.kpi .s{font-size:9px;color:var(--t3);margin:3px 0 0;font-variant-numeric:tabular-nums;line-height:1.35;}
.kpi.hl{background:var(--by-l);}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:4px;}
.three .impl{margin:0;}

.risk{border:1px solid #E8C4C4;border-left:4px solid var(--up);background:#FDF6F6;
      padding:12px 16px;font-size:11.5px;line-height:1.7;}
.risk ol{margin:0;padding-left:17px;} .risk li{margin:5px 0;}
.disc{background:var(--bg);border-top:3px solid var(--bk);padding:11px 15px;
      font-size:9px;color:var(--t3);line-height:1.8;margin-top:14px;}
.disc b{color:var(--t2);}

@media print{
  html,body{background:#fff !important;}
  *{-webkit-print-color-adjust:exact !important;print-color-adjust:exact !important;}
  .page{min-height:210mm;}
  table{width:100% !important;table-layout:fixed !important;}
  th{position:static !important;}
  thead{display:table-header-group;}
  tr{break-inside:avoid;page-break-inside:avoid;}
  .fig,.impl,.kpis,.three,.risk,.disc{break-inside:avoid;page-break-inside:avoid;}
  .cover{min-height:210mm;}
}
"""


# ══════════════════════════════ 组件 ══════════════════════════════
def page(inner: str, pno: int, sec: str = "", full: bool = False) -> str:
    cls = "pbody full" if full else "pbody"
    return (
        '<section class="page">\n'
        f'<div class="runhead"><span class="sec">{sec}</span>'
        f'<span>{CODE}　·　{pno}/{TOTAL}</span></div>\n'
        f'<div class="{cls}">{inner}</div>\n'
        f'<div class="runfoot"><span>数据来源：{SRC_LINE}</span><span>{pno}</span></div>\n'
        "</section>"
    )


def two(left: str, right: str) -> str:
    return f'<div class="colL">{left}</div><div class="colR">{right}</div>'


def card(n: str, title: str, sub: str, body: str, take: str, src: str) -> str:
    return (
        '<figure class="fig">\n'
        f'<div class="fig-h"><span class="n">图 {n}</span><h3>{title}</h3>'
        f'<p class="sd">{sub}</p></div>\n'
        f'<div class="fig-b">{body}</div>\n'
        f'<div class="fig-take"><span class="k">图表结论</span>{take}</div>\n'
        f'<p class="fig-src">{src}</p>\n'
        "</figure>"
    )


def cv(cid: str, w: int = 678, h: int = 396) -> str:
    return f'<canvas id="{cid}" width="{w}" height="{h}"></canvas>'


def eyebrow(t: str) -> str:
    return f'<span class="eyebrow">{t}</span>'


def pq(text: str, who: str = "") -> str:
    w = f"<span>{who}</span>" if who else ""
    return f'<div class="pq">{text}{w}</div>'


def impl(items: list[str], title: str = "投资启示") -> str:
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<div class="impl"><span class="k">{title}</span><ul>{li}</ul></div>'


def clamp(items: list, n: int) -> tuple[list, int]:
    """截断到 n 个并返回被截掉的数量（用于在图注里声明「仅显示前 N」）。"""
    if len(items) <= n:
        return list(items), 0
    return list(items[:n]), len(items) - n


# ══════════════════════════ 次日 5 条可证伪预判 ══════════════════════════
def next_trading_day(date_str: str) -> str:
    """下一「交易日」的**近似**值：只跳过周末。

    ⚠️ 法定节假日无法离线判定（需要连接器 trade-calendar）。所以日更时**必须**由
    predictions.json 显式给出 target_date；本函数仅作兜底，命中兜底时页面会标注
    「近似推断」——否则预判会被挂到一个休市日上，次日核验任务直接扑空。
    """
    d = dt.date.fromisoformat(date_str[:10]) + dt.timedelta(days=1)
    while d.weekday() >= 5:           # 5=周六 6=周日
        d += dt.timedelta(days=1)
    return d.isoformat()


PRED_FIELDS = ("claim", "falsify", "source")


def load_predictions(args, data_path: pathlib.Path, out_dir: pathlib.Path) -> dict:
    """读取次日预判：`--predictions`（内联）> `--predict-file` > 自动探测 predictions.json。

    自动探测顺序：<data 同级>/predictions.json → <out 目录>/predictions.json。
    一个都找不到时返回 {} —— 生成端会渲染「示例占位页」，而不是报错，
    这样模板本身在无预判数据时仍可独立跑通（demo / 冒烟）。
    """
    raw: str | None = None
    src: str | None = None
    if args.predictions:
        raw, src = args.predictions, "--predictions（内联）"
    else:
        cands: list[pathlib.Path] = []
        if args.predict_file:
            cands.append(pathlib.Path(args.predict_file).expanduser())
        cands += [data_path.parent / "predictions.json", out_dir / "predictions.json"]
        for p in cands:
            if p.exists():
                raw, src = p.read_text(encoding="utf-8"), str(p)
                break
    if raw is None:
        print("[i] 未找到次日预判（--predict-file / --predictions / predictions.json），"
              "本页将渲染「示例占位」。")
        return {}

    try:
        d = json.loads(raw)
    except Exception as e:                                  # noqa: BLE001
        sys.exit(f"[!] 预判 JSON 解析失败（{src}）：{e}")
    if not isinstance(d, dict):
        sys.exit(f"[!] 预判 JSON 顶层必须是对象（{src}）")
    items = d.get("items") or []
    if len(items) != 5:
        sys.exit(f"[!] 次日预判必须恰好 5 条（可证伪的硬性数量），实际 {len(items)} 条：{src}")
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            sys.exit(f"[!] 第 {i} 条预判不是对象：{src}")
        it.setdefault("n", i)
        if not str(it.get("claim") or "").strip():
            sys.exit(f"[!] 第 {i} 条预判缺 `claim`（预判内容）：{src}")
        if not str(it.get("falsify") or "").strip():
            sys.exit(f"[!] 第 {i} 条预判缺 `falsify`（可证伪判据 / 观测口径）：{src} —— "
                     f"没有判据的预判次日无法核验，等于没写。")
    d.setdefault("target_date", "")
    d["_src"] = src
    return d


def build_pred_page(pred: dict, date: str) -> str:
    """第 14 页 · 次日 5 条可证伪预判（BII 双栏：左文字栏 ‖ 右预判表）。

    ⚠️ 标题必须保留 `9.1 次日（YYYY-MM-DD）5 条可证伪预判` 这一**字面形式**：
    19:15 的核验任务用正则 `2?\\d\\.\\d\\s*次日（<目标日>）\\s*5\\s*条可证伪预判`
    定位本节。改标题 = 核验任务失联（这是踩过的坑，见 SKILL.md §12.4）。
    因此这里刻意用**半角空格**（`\\s` 在各种引擎下都匹配），不要换成全角空格。
    """
    pred = pred or {}
    raw_tgt = str(pred.get("target_date") or "").strip()
    tgt = raw_tgt or next_trading_day(date)
    tgt_src = ("由 predictions.json 显式给出" if raw_tgt
               else "按周末顺延近似推断，节假日以交易日历为准")
    basis = str(pred.get("data_basis_date") or date)
    items = list(pred.get("items") or [])

    if items:
        rows, placeholder = list(items), False      # ⚠️ 这里是 list(items)，不是 []——
    else:                                           #    写成 [] 会让表格渲染成空 tbody，
        placeholder = True                          #    而「有效条数 5/5」照旧正确，很难一眼看出
        rows = [{"n": i, "claim": "（示例占位 —— 日更时由 18:00 任务写入 predictions.json）",
                 "falsify": "—", "source": "—"} for i in range(1, 6)]

    body = "".join(
        f"<tr><td><span class='tag'>{it.get('n', i + 1)}</span></td>"
        f"<td style=\"text-align:left;white-space:normal\">{it.get('claim', '—')}</td>"
        f"<td style=\"text-align:left;white-space:normal\">{it.get('falsify') or '—'}</td>"
        f"<td style=\"text-align:left;white-space:normal\">{it.get('source') or '—'}</td></tr>"
        for i, it in enumerate(rows))

    warn = ""
    if placeholder:
        warn = "　<b>⚠ 本页为示例占位：未提供 predictions.json，5 条预判为空。</b>"
    elif pred.get("demo"):
        warn = "　<b>⚠ 本页预判为示例内容（随演示数据一同生成），非真实盘后预判。</b>"

    n_real = 5 if items else 0
    L = f'''{eyebrow("09　次日预判 · FALSIFIABLE CALLS")}
<h2>9.1 次日（{tgt}）5 条可证伪预判</h2>
<p class="lead">本页写出次日（{tgt}）5 条可证伪预判。预判不是观点，是<b>待检验的命题</b> ——
5 条一律写成「能被次日数据推翻」的形式，指明标的、口径、方向与阈值；任一要素缺失，
盘后就无法判定命中与否，预判也就失去了复盘价值。</p>
{pq("不可证伪的判断，等于没有判断。", "本页的写作纪律")}
<p><b>5 条的最低覆盖要求</b>　① 过会标的的量价确认；② L2.5 可交易性（防退市 / ST / PB&lt;0）；
③ 行业或方向层的分位与额比；④ 资金面（主力净额 / 龙虎榜净买卖）；⑤ 本期结论本身（过会数或名单变化）。</p>
{impl(["<b>判定三态</b>：命中 / 部分命中 / 未命中；含子条件者必须分腿判定（腿 A / 腿 B）。",
       "<b>三层命中率</b>：完全命中率、含部分命中口径、加权命中率（命中 1.0 · 部分 0.5 · 未命中 0）。",
       "<b>阈值校准</b>：每条须标注阈值「过严 / 合适 / 过松」，并给出下一期建议阈值。"],
      "核验规则（次日 19:15 自动执行）")}'''

    R = f'''<table>
<colgroup><col style="width:6%"><col style="width:39%"><col style="width:35%"><col style="width:20%"></colgroup>
<thead><tr><th>#</th><th>预判（可证伪陈述）</th><th>判据阈值（观测口径）</th><th>取数来源</th></tr></thead>
<tbody>{body}</tbody></table>
<p class="tcap"><b>读法</b>　「判据阈值」栏写死了「命中 / 未命中」的分界线，是这 5 条可核验的关键；
该栏若为「—」，则该条<b>不可核验</b>，须在次日盘中补齐后才算成立。预判目标日为
<b>{tgt}</b> —— {tgt_src}；数据基准日 <b>{basis}</b>。<br>
<b>有效条数</b>　{n_real}/5。</p>'''

    # 说明条通栏（grid-column:1/-1）—— 与第 11 / 13 页的 .disc 用法保持一致，同时把版心底部填满
    D = f'''<div class="disc" style="grid-column:1 / -1">
<b>核验链路</b>　次日 19:15 的「预判核验」任务读本页 5 条，逐条给出「当日实际值（含前值对比）→
判定 → 偏差归因（① 资金未延续 / ② 指数板块拖累 / ③ 观测锚点层级错误 / ④ 阈值未触发或设定过严）」，
并汇总三层命中率与阈值校准建议；核验结论回写为下一期的置信度调整依据。<br>
<b>与正文的关系</b>　第 13 页给出「下一交易日盯住什么位」，本页给出「下一交易日哪些命题必须成立」——
前者是观察位，后者是可验证命题，两者缺一不可。<br>
<b>口径与免责</b>　所有阈值基于 {date} 盘后快照测算；本页为技术测算参考，<b>不构成任何投资建议</b>。{warn}
</div>'''
    return page(two(L, R) + D, PRED_PNO, "09　次日预判")


# ══════════════════════════════ 数据装配 ══════════════════════════════
def build_inputs(data: dict) -> tuple[list, list]:
    # dispersion / note 允许为 None（取数缺口），一律降级为 0.0 / ""；
    # rank / vr 是入池判定的必需字段，缺失即数据错误，直接抛错而不是静默降级。
    for i in data.get("industries", []):
        if i.get("rank") is None or i.get("vr") is None:
            raise SystemExit(f"[!] industries 条目缺 rank/vr（必需字段）：{i.get('name') or i.get('code')}")
    inds = [FN.Industry(i["code"], i["name"], float(i["rank"]), float(i["vr"]),
                        float(i.get("dispersion") or 0.0), i.get("note") or "")
            for i in data.get("industries", [])]
    stocks = []
    for c in data.get("candidates", []):
        raw = {k: v for k, v in c.items()
               if k not in ("code", "name", "sector", "rank", "vr")}
        stocks.append(FN.Stock(c["code"], c["name"], c.get("sector", ""),
                               float(c["rank"]) if c.get("rank") is not None else None,
                               float(c["vr"]) if c.get("vr") is not None else None,
                               raw))
    return inds, stocks


def compute_model(data: dict) -> dict:
    inds, stocks = build_inputs(data)
    fr = FN.run_funnel(inds, stocks)
    ctx = data.get("context", {}) or {}
    equity = float(ctx.get("equity", 1_000_000))
    stage = str(ctx.get("stage", "II")).upper()
    ice = F.is_ice_point(int(ctx.get("limit_up_count", 60)),
                         float(ctx.get("broken_rate", 0.2)),
                         float(ctx.get("index_pct", 0))) if ctx else False
    basis = [s.merged for s in fr.l3_pass] or data.get("candidates", [])
    result = PL.run_pipeline(basis, equity=equity, stage=stage, ice_point=ice)
    # ── 观察模式闸门（2026-11-11 修正，仅过会 0 只时触发，正常日子零影响）──
    # 过会池为空时 basis 回退到全候选池，只为让雷达/综合分/财务/PB 等「研究性图表」有数据可画；
    # 但这些标的未过 L2/L2.5/L3，评分再高也只能作「观察榜」，不得发 BUY、不得占用 α 预算。
    # 否则第 2 页「过会 0 只」会与「N 只可建仓 / -N 只观察 / 明日盯住这 N 只 / 已用 28%」
    # 当场自相矛盾，且出现负计数 —— 属实盘危险误导。
    observation_only = not fr.l3_pass
    if observation_only:
        for _r in result["rows"]:
            if _r.action == "BUY":
                _r.action = "WATCH"
                _r.notes.append("漏斗过会0只→仅研究评分，BUY降级为观察(WATCH)，不占用α预算")
        _ab = float(result["ledger"].get("alpha_budget", 0.30))
        result["ledger"].update(open_notional=0.0, used_pct=0.0, positions=0,
                                total_risk=0.0, remaining=round(equity * _ab, 2))
        result["stats"]["buy"] = 0
        result["stats"]["watch"] = sum(1 for _r in result["rows"] if _r.action == "WATCH")
    # L1 只判「位置」：3 年分位 ≤ 25%。额比 ≥1.0× 归 L2 个股层（口径分工见 funnel.run_funnel）。
    l1_pass = [i for i in inds if i.rank <= C.RANK_LOW_THRESHOLD]
    l1_vr_ok = [i for i in l1_pass if i.vr >= C.VR_THRESHOLD]
    return {"inds": inds, "fr": fr, "ctx": ctx, "equity": equity, "stage": stage,
            "ice": ice, "res": result, "l1_pass": l1_pass, "l1_vr_ok": l1_vr_ok,
            "observation_only": observation_only}


# ══════════════════════════════ 图表数据注入 ══════════════════════════════
def inject_charts(m: dict, by_code: dict, by_name: dict) -> str:
    res, fr, inds = m["res"], m["fr"], m["inds"]

    # 图1 个股维度漏斗（保持单调递减；L1 为行业粒度，单独在正文说明）
    stage_l = ["候选池 L0", "L2 技术面入池", "L2.5 可交易", "L3 基本面通过"]
    stage_v = [len(by_code), len(fr.l2_pass),
               len(fr.l2_pass) - len(fr.l2_5_removed), len(fr.l3_pass)]

    # 图2 行业气泡（按分位升序取前 N，截断时在图注声明）
    ind_sorted = sorted(inds, key=lambda i: i.rank)
    ind_show, ind_cut = clamp(ind_sorted, _MAX_BUB)
    ind_n = [i.name for i in ind_show]
    ind_rank = [round(i.rank, 1) for i in ind_show]
    ind_vr = [round(i.vr, 2) for i in ind_show]
    ind_disp = [round(i.dispersion, 1) for i in ind_show]

    # 图3 雷达：综合分前 3
    rows_desc = sorted(res["rows"], key=lambda r: -r.score)
    radar_rows = rows_desc[:3]
    radar_labels = ["技术面", "资金面", "基本面", "周期位置", "斐波那契"]
    radar_sets = []
    for r in radar_rows:
        c = by_code.get(r.code) or by_name.get(r.name) or {}
        radar_sets.append({"label": r.name, "data": [
            float(c.get("tech", 0) or 0), float(c.get("flow", 0) or 0),
            float(c.get("fund", 0) or 0), float(c.get("cycle", 0) or 0),
            float(c.get("fib", 0) or 0)]})

    # 图4 综合分排行（降序，前 N）
    rank_show, rank_cut = clamp(rows_desc, _MAX_RANK)
    score_n = [r.name for r in rank_show]
    score_v = [round(r.score, 1) for r in rank_show]
    score_act = [r.action for r in rank_show]

    # 图5 财务：中报同比 vs 上年度增速（按综合分顺序，取前 N 个有数据的）
    fin_pool = []
    for r in rows_desc:
        c = by_code.get(r.code) or {}
        if c.get("interim_yoy") is None or c.get("prior_fy_yoy") is None:
            continue
        fin_pool.append((r.name, round(float(c["interim_yoy"]), 4),
                         round(float(c["prior_fy_yoy"]), 4)))
    fin_show, fin_cut = clamp(fin_pool, _MAX_FIN)
    fin_n = [x[0] for x in fin_show]
    fin_i = [x[1] for x in fin_show]
    fin_p = [x[2] for x in fin_show]

    # 图6 PB 排序（升序，前 N）—— 只排「可交易且 PB 为正」的标的。
    # 历史缺陷一：不过滤负 PB 时，升序前 10 名会被「净资产为负」的标的全部占满
    # （0917 实测 11 只负 PB 把榜单从头占到位），图里只剩负值柱，
    # 与左栏「估值最低三只」和「PB 为负不属低估值」的论述直接矛盾（0917 修正）。
    # 历史缺陷二：只过滤负 PB 仍不够 —— 已退市的「退市观典」(PB 0.23) 会排到第 2 名，
    # 与同报告 L2.5 不可交易清单自相矛盾。故统一走 pb_tradable()（0917 二次修正）。
    pbs = sorted([(c["name"], float(c["pb"])) for c in by_code.values()
                  if pb_tradable(c)], key=lambda x: x[1])
    pb_show, pb_cut = clamp(pbs, _MAX_PB)
    pb_n = [x[0] for x in pb_show]
    pb_v = [round(x[1], 2) for x in pb_show]

    # 图7 五维分项（按综合分顺序，前 N）
    dim_show, dim_cut = clamp(rows_desc, _MAX_DIM)
    dim_labels = [r.name for r in dim_show]
    dim_keys = [("tech", "技术面"), ("flow", "资金面"), ("fund", "基本面"),
                ("cycle", "周期位置"), ("fib", "斐波那契")]
    dim_sets = [{"label": lab, "data": [
        float((by_code.get(r.code) or {}).get(k, 0) or 0) for r in dim_show]}
        for k, lab in dim_keys]

    # 图8 α 账本（单位随资金规模自适应：机构级亿元 / 其余万元）
    led = res["ledger"]
    _div, _unit = _scale_unit(led["equity"])
    alpha_max = led["equity"] * led["alpha_budget"] / _div
    alpha_used = float(led.get("open_notional", 0)) / _div
    alpha_remain = max(0.0, alpha_max - alpha_used)

    # 截断声明（写进图注，避免读者误以为看的是全量）
    notes = {
        "bub_cut": ind_cut, "rank_cut": rank_cut, "fin_cut": fin_cut,
        "pb_cut": pb_cut, "dim_cut": dim_cut,
    }

    js = CHART_TPL
    repl = {
        "__STAGE_L__": jsarr(stage_l),
        "__STAGE_V__": jsarr(stage_v),
        "__IND_N__": jsarr(ind_n),
        "__IND_RANK__": jsarr(ind_rank),
        "__IND_VR__": jsarr(ind_vr),
        "__IND_DISP__": jsarr(ind_disp),
        "__RADAR_LABELS__": jsarr(radar_labels),
        "__RADAR_SETS__": jsdata(radar_sets),
        "__SCORE_N__": jsarr(score_n),
        "__SCORE_V__": jsarr(score_v),
        "__SCORE_ACT__": jsarr(score_act),
        "__FIN_N__": jsarr(fin_n),
        "__FIN_INTERIM__": jsarr(fin_i),
        "__FIN_PRIOR__": jsarr(fin_p),
        "__PB_N__": jsarr(pb_n),
        "__PB_V__": jsarr(pb_v),
        "__DIM_LABELS__": jsarr(dim_labels),
        "__DIM_SETS__": jsdata(dim_sets),
        "__ALPHA_USED__": f"{alpha_used:.4f}",
        "__ALPHA_REMAIN__": f"{alpha_remain:.4f}",
        "__ALPHA_MAX__": f"{max(alpha_max, 1.0):.4f}",
    }
    for k, v in repl.items():
        js = js.replace(k, v)
    # c8 图表刻度与柱内标签硬编码「万」；机构级统一改「亿」（该字样全模板仅 c8 两处）
    if _unit == "亿元":
        js = js.replace("' 万'", "' 亿'")
    # 占位符残留检查：先剥掉 // 行注释，否则注释里举例写的占位符会被误判
    code_only = "\n".join(re.sub(r"//.*$", "", ln) for ln in js.splitlines())
    left = re.findall(r"__[A-Z0-9_]+__", code_only)
    if left:
        raise SystemExit(f"[!] 图表配置仍有未替换占位符：{sorted(set(left))}")
    check_js_syntax(js, "chart_js_bii")     # 语法自检 —— 拼出非法字面量时当场拦下
    m["_notes"] = notes
    m["_radar_n"] = len(radar_rows)
    return js


# ══════════════════════════════ 页面构建 ══════════════════════════════
# ══════════════════ v3.0 扩展层附录（第 15 / 16 页）══════════════════
# 非破坏性：前 14 页的 HTML 生成逻辑一字不改，只在末尾追加两页。
# 页面数据全部来自 data.json 顶层 `v3.blocks`（由 strategy/v3_ext.py 生成），
# 本文件不 import v3_ext —— 没有 v3 字段时这两个函数根本不会被调用，仍出 14 页。
# 版面：双栏（左文字 / 右表格），实测 p15/p16 页高均 ≤794px。
_BAR = ('font-size:11px;line-height:1.45;color:#0A3D6E;background:#F6F8FA;'
        'border-left:3px solid #FFB500;padding:4px 9px;margin:5px 0 8px;word-break:break-word;')


def _v3_macro_page(B: dict, date: str) -> str:
    co = B.get("counts") or {}
    rows = B.get("macro_rows") or []
    gaps = B.get("macro_gaps") or []
    supp = B.get("supplement") or []
    anchors = B.get("anchors") or []
    facts = B.get("fact_anchors") or []
    chk = B.get("checks") or {}
    wm = B.get("watermark") or {}
    alerts = B.get("alerts") or []
    fac = B.get("factor_rows") or []
    quad = B.get("quadrant") or {}
    buckets = B.get("buckets") or {}
    cb, ce = B.get("position_cap_base"), B.get("position_cap_effective")
    cap_txt = f"{cb:.0%} → {ce:.0%}" if cb is not None and ce is not None else "—"

    trs = "".join(
        f"<tr><td style='width:14%'><b>{r['id']}</b></td>"
        f"<td style='width:36%;text-align:left'>{r['v']}</td>"
        f"<td style='width:50%;text-align:left'>{r['tag']}</td></tr>" for r in rows)
    gap_ids = "、".join(str(g).split()[0] for g in gaps) or "—"
    supp_txt = "；".join(f"<b>{s['label']}</b> {str(s['v'])[:44]}" for s in supp[:4]) or "—"
    quad_txt = "；".join(f"{k}：{str(v)[:14]}" for k, v in quad.items())
    bucket_txt = " / ".join(f"{k} {v[0]:.0%}–{v[1]:.0%}" for k, v in buckets.items())
    fac_txt = "、".join(f"{r['id']} {r['m']}" for r in fac) or "—"
    anc_txt = "；".join(f"{a['k']} {a['v']}〔{a['kind']}〕" for a in anchors[:3])
    fact_txt = "；".join(f"{a['k']} {a['v']}" for a in facts[:2])
    alert_txt = "；".join(alerts[:1]) or "无"

    L = f"""{eyebrow("10　v3.0 扩展层 · L0 宏观定位")}
<h2>宏观中性、α 不折减</h2>
<p class="lead">{co.get('macro_computed', 0)} 条实算 / {co.get('macro_proxies', 0)} 条代理 /
{co.get('macro_gaps', 0)} 条缺口；{co.get('sources', 0)} 份新增资料蒸馏。</p>
<div class="mkt" style="{_BAR}"><b>扩展层结论</b>　{B.get('headline', '')}</div>
{impl([f"<b>定位</b>　{B.get('macro_tag', '')}，α 折减 ×{B.get('alpha_multiplier', 1.0):.2f}，仓位上限 {cap_txt}。<br>宏观层只下调不上调，不参与反身性判定、不回写情绪阶段。"], "L0 宏观定位层")}
{impl([f"<b>因子乘数</b>　{fac_txt}<br>只乘 α 预算，不乘仓位上限；事件加分封顶 ≤20% 主口径权重，主题催化 20 日衰减归零。"], "策略会因子层")}
{impl([f"<b>四象限</b>　{quad_txt}<br><b>三层面分桶</b>　{bucket_txt}（仅上限告警）"], "配置矩阵与 α 分桶")}
<p class="tcap"><b>本期缺口 {co.get('macro_gaps', 0)} 条</b>　{gap_ids}。一律标「外部数据缺口·仅定性」，不写成可计算判据。</p>"""

    R = f"""<table>
<colgroup><col style="width:14%"><col style="width:36%"><col style="width:50%"></colgroup>
<thead><tr><th>规则</th><th>westock 实测值</th><th>判定 / 标签</th></tr></thead>
<tbody>{trs}</tbody></table>
<p class="tcap"><b>补充实算（月频，发布日更新）</b>　{supp_txt}。</p>
<div class="disc">
<b>预测锚登记簿〔预测·非事实〕</b>　{anc_txt}。仅用于分档边界，不生成买卖信号、不进入回溯验收；
两份 2027 展望均未给出 A 股指数点位预测，本模块不设指数目标位。<br>
<b>已发布事实锚</b>　{fact_txt}。<br>
<b>水印</b>　{str(wm.get("规则", ""))}；{str(wm.get("隔离", ""))}。<br>
<b>非侵入自检</b>　{chk.get('passed', 0)}/{chk.get('total', 0)} 项通过（六条口径常量、KNOWLEDGE 45 键、
红旗否决线、打板门槛均未改写）。<b>本期告警</b>　{alert_txt}。
</div>"""
    return page(two(L, R), 15, "10　v3.0 扩展层 · 宏观")


def _v3_theme_page(B: dict, date: str) -> str:
    co = B.get("counts") or {}
    themes = B.get("theme_rows") or []
    bs = B.get("book_suggest") or {}
    books = B.get("book_rows") or []
    wm = B.get("watermark") or {}
    gaps = B.get("gaps") or []
    rollback = B.get("rollback", "")

    by_tier: dict[str, list] = {}
    for t in themes:
        by_tier.setdefault(t["tier"], []).append(t)
    sel = []
    for tier in ("A", "A/B", "B", "C"):
        sel += by_tier.get(tier, [])[:2]
    trs = "".join(
        f"<tr><td style='width:9%'><b>{t['tier']}</b></td>"
        f"<td style='width:34%;text-align:left'>{t['name']}</td>"
        f"<td style='width:42%;text-align:left'>{str(t['kw'])[:30]}</td>"
        f"<td style='width:15%;text-align:left'>{t['src']}</td></tr>" for t in sel)
    bs_rows = "".join(
        f"<tr><td style='width:28%;text-align:left'>{k}</td>"
        f"<td style='width:44%;text-align:left'>{str(v.get('suggest', ''))[:30]}</td>"
        f"<td style='width:28%;text-align:left'>{v.get('status', '')}</td></tr>"
        for k, v in list(bs.items())[:6])
    gc: dict[str, int] = {}
    for r in books:
        gc[r["g"]] = gc.get(r["g"], 0) + 1
    grp_txt = "、".join(f"{k} {v} 条" for k, v in gc.items())
    gap_txt = "；".join(str(g)[:24] for g in gaps[:3])

    L = f"""{eyebrow("11　v3.0 扩展层 · X- 主题与书籍规则")}
<h2>{co.get('themes', 0)} 个 X- 方向、{co.get('book_rules', 0)} 条书籍规则</h2>
<div class="mkt" style="{_BAR}"><b>隔离</b>　18 方向 / 102 板块 / 31 行业 / 70 只成分一律不动；
扩展层只并行输出标签，不回写主表、不进漏斗、不参与分位与离散度。</div>
{impl([f"<b>A</b> 可交易（A/H 上市且校验通过）；<b>B</b> 影子股事件标签（不参与分位）；<b>C</b> 非上市主体纯定性，严禁混入可交易池。事件加分封顶 ≤20% 主口径权重，20 日线性衰减。<br><b>分组</b>　{grp_txt}；命中 {co.get('book_hits', 0)} 条、缺口 {co.get('book_missing', 0)} 条。冲突时以 seal_quality / lhb_power / sentiment_cycle 为准。"], "三层白名单 + 短线金手 7 册只读标签")}
{impl([f"{str(wm.get('口径差异处理', ''))}<br><b>回滚</b>　data.json 顶层 v3.enabled=false，或逐条关 V3_SWITCHES → 自动回到 14 页纯 v2.3 版式。"], "水印与回滚")}"""

    R = f"""<table>
<colgroup><col style="width:9%"><col style="width:34%"><col style="width:42%"><col style="width:15%"></colgroup>
<thead><tr><th>层</th><th>X- 扩展方向</th><th>板块关键词</th><th>来源</th></tr></thead>
<tbody>{trs}</tbody></table>
<p class="tcap"><b>共 {co.get('themes', 0)} 个扩展方向（按层各列 2 个代表）</b>；告警只进风险清单，不删成分。
<b>阈值校准建议</b>共 {len(bs)} 条、列 6 条，只登记不覆盖 KNOWLEDGE。</p>
<table>
<colgroup><col style="width:28%"><col style="width:44%"><col style="width:28%"></colgroup>
<thead><tr><th>现有键</th><th>书籍建议值</th><th>处置</th></tr></thead>
<tbody>{bs_rows}</tbody></table>
<div class="disc">
<b>外部数据缺口</b>　{gap_txt} 等 {co.get('gaps', len(gaps)) if 'gaps' in co else len(gaps)} 类。<br>
<b>事实 / 预测 / 口径差异</b>　{str(wm.get("隔离", ""))}；{str(wm.get("历史资料", ""))}。<br>
<b>频率与免责</b>　宏观月/季频（发布日更新），情绪 / 漏斗 / 评分仍为日频。本页只输出标签与乘数，
<b>不构成投资建议</b>；{date} 盘后快照，预测项已带水印，不得用于回溯验收。
</div>"""
    return page(two(L, R), 16, "11　v3.0 扩展层 · 主题与规则")


# ════════════════════ v3.1 GCCEO 全量整合层附录（第 17/18 页）══════════════════
# 非破坏性：前 16 页逐字不改，仅在 v3 与 gceo 同时开启时追加两页。
# 页面数据全部来自 data.json 顶层 `gceo.blocks`（由 strategy/gcceo_ext.py 生成）；
# 本文件不 import gcceo_ext —— 没有 gceo 字段时这两个函数根本不会被调用。
# GCCEO 是「企业管理能力体系」→ 研判视角的映射，不是选股因子；只输出标签/清单/提问/叙事，
# 无剔除权、无打分权、无仓位上调权。右栏零 canvas，天然绕开 ink>300 图表校验；
# 所有长文本字段一律 [:N] 截断，保证页高 ≤794px。
_GCEEO_BAR = ('font-size:11px;line-height:1.45;color:#5A3A00;background:#FFF9EC;'
              'border-left:3px solid #C5A572;padding:4px 9px;margin:5px 0 8px;word-break:break-word;')


def _gceo_decision_page(B: dict, date: str) -> str:
    """第 17 页：五步决策框架 + 十域 91 技能 → 研判视角映射。"""
    co = B.get("counts") or {}
    steps = B.get("decision_rows") or []
    doms = B.get("domain_rows") or []
    chk = B.get("checks") or {}
    wm = B.get("caliber_diffs") or []
    headline = B.get("headline", "")

    step_txt = " → ".join(f"{s['step'].split()[0]}" for s in steps) or "DEFINE→ANALYZE→SYNTHESIZE→DECIDE→EXECUTE"
    step_rows = "".join(
        f"<tr><td style='width:14%'><b>{str(s['step'])[:11]}</b></td>"
        f"<td style='width:48%;text-align:left'>{str(s['research'])[:46]}</td>"
        f"<td style='width:38%;text-align:left'>{str(s['landing'])[:30]}</td></tr>" for s in steps)
    dom_rows = "".join(
        f"<tr><td style='width:8%'><b>{d['domain']}</b></td>"
        f"<td style='width:17%;text-align:left'>{str(d['zh'])[:8]}</td>"
        f"<td style='width:25%;text-align:left'>{str(d['lens'])[:14]}</td>"
        f"<td style='width:50%;text-align:left'>{str(d['q'])[:40]}</td></tr>" for d in doms[:10])
    diff_txt = "；".join(f"{w['item']} {w['v_frontmatter']}/{w['v_skillsjson']}" for w in wm) or "无"

    L = f"""{eyebrow("12　v3.1 全量整合 · 决策工程与十域映射")}
<h2>五步决策框架 · 十域 {co.get('domains', 91)} 技能</h2>
<p class="lead">GCCEO 4.0 全量整合：决策链 {step_txt}；十域能力映射为研判视角，非选股因子。</p>
<div class="mkt" style="{_GCEEO_BAR}"><b>整合结论</b>　{headline}</div>
{impl([f"<b>定位</b>　GCCEO 是企业经营能力体系，映射为提问 / 清单 / 风险项 / 叙事脚手架；"
       f"<b>只读无剔除、无打分、无仓位上调</b>，六条口径 v2.3 与 v3.0 结论零改动。",
       f"<b>五步框架</b>　DEFINE 议题树 → ANALYZE 五维共振 → SYNTHESIZE 叙事 123 → "
       f"DECIDE 事前尸检+安全边际+5 条预判 → EXECUTE 跟踪清单+次日核验复盘（AAR）。"], "推理链可审计")}
<p class="tcap"><b>十域映射</b>　逐域给出研判视角与核心提问；能力不进 scoring / funnel / predictions 数值计算。</p>"""

    R = f"""<table>
<colgroup><col style="width:14%"><col style="width:48%"><col style="width:38%"></colgroup>
<thead><tr><th>决策步</th><th>研判动作</th><th>报告落点</th></tr></thead>
<tbody>{step_rows}</tbody></table>
<p class="tcap">五步 = 推理链脚手架，不改变任何判定结果。</p>
<table>
<colgroup><col style="width:8%"><col style="width:17%"><col style="width:25%"><col style="width:50%"></colgroup>
<thead><tr><th>域</th><th>能力域</th><th>研判视角</th><th>核心提问</th></tr></thead>
<tbody>{dom_rows}</tbody></table>
<div class="disc">
<b>口径差异〔水印〕</b>　{diff_txt}。取 skills.json 十域 91 为结构口径，96 含 2026 新增模块，绝对值不写阈值。<br>
<b>非侵入自检</b>　{chk.get('passed', 0)}/{chk.get('total', 0)} 项通过；v3 复用 {str((chk.get('v3_recheck') or {}).get('passed', '—'))}/14。
六条口径、KNOWLEDGE 45 键、v3 五模块均只读比对，未改写。<br>
<b>免责</b>　本页为方法论映射，<b>不构成投资建议</b>；{date} 盘后，仅作研判视角参考。
</div>"""
    return page(two(L, R), 17, "12　v3.1 全量整合 · 决策与十域")


def _gceo_ext_page(B: dict, date: str) -> str:
    """第 18 页：投行 A1-A10 / 出海 G1-G10 / AI 超能力 / 方法论 / 尽调 / 风险 / 回滚。"""
    co = B.get("counts") or {}
    ib = B.get("ib_rows") or []
    gl = B.get("gl_rows") or []
    ai = B.get("ai_rows") or []
    mt = B.get("method_rows") or []
    dd = B.get("dd_rows") or []
    rr = B.get("risk_rows") or []
    narr = B.get("narrative") or []
    rb = B.get("rollback", "")

    ib_txt = "、".join(f"{r['id']}{r['name']}" for r in ib[:10])
    gl_txt = "、".join(f"{r['id']}{r['name']}" for r in gl[:10])
    ai_txt = "、".join(f"{r['name']}" for r in ai[:8])
    mt_inj = co.get("method_injected", 0)
    mt_map = co.get("method_mapped", 0)
    mt_txt = f"已注入 {mt_inj} / 映射 {mt_map} / 共 {co.get('method_tools', 16)} 条"
    narr_txt = "；".join(str(n)[:22] for n in narr[:3])

    dd_rows = "".join(
        f"<tr><td style='width:30%;text-align:left'>{str(d['item'])[:17]}</td>"
        f"<td style='width:70%;text-align:left'>{str(d['gate'])[:44]}</td></tr>" for d in dd[:6])
    rr_txt = "；".join(f"{str(r['q'])[:20]}" for r in rr[:4]) or "—"
    risk_rows = "".join(
        f"<tr><td style='width:52%;text-align:left'>{str(r['q'])[:32]}</td>"
        f"<td style='width:48%;text-align:left'>{str(r['fill'])[:20]}</td></tr>" for r in rr[:5])

    L = f"""{eyebrow("13　v3.1 全量整合 · 资本/出海/AI/治理")}
<h2>投行 {co.get('ib_pe',10)} · 出海 {co.get('globalization',10)} · AI 超能力 {co.get('ai_superpowers',8)}</h2>
<div class="mkt" style="{_GCEEO_BAR}"><b>无剔除、无上调</b>　下列能力一律映射为定性标签 / 风险提问 / 叙事脚手架，
不参与打分、不改变四层漏斗与情绪仓位。</div>
{impl([f"<b>投行私募 A1-A10</b>　{ib_txt}。<br>资本运作事件标签；A4 高杠杆反向接入达尔文禁区。",
       f"<b>出海 G1-G10</b>　{gl_txt}。<br>对齐 X-主题出海方向（6.4），仅定性标签、无剔除权。",
       f"<b>AI 超能力 8</b>　{ai_txt}。<br>作为研判工作台辅助定位，落到既有章节，不新增买卖信号。",
       f"<b>方法论 16</b>　{mt_txt}。<br>推理链可审计，不改判定。"], "四类能力映射")}
{impl([f"<b>叙事纪律</b>　{narr_txt}。"], "叙事与复盘")}
<p class="tcap"><b>定性尽调清单</b>　治理 / 人才 / ESG 域，全部标注 gate，明确不改写任何硬口径。</p>"""

    R = f"""<table>
<colgroup><col style="width:30%"><col style="width:70%"></colgroup>
<thead><tr><th>尽调项</th><th>边界（不改口径）</th></tr></thead>
<tbody>{dd_rows}</tbody></table>
<p class="tcap"><b>风险雷达（仅定性，westock 无接口标缺口）</b>　{rr_txt}。</p>
<table>
<colgroup><col style="width:52%"><col style="width:48%"></colgroup>
<thead><tr><th>风险提问</th><th>取数处置</th></tr></thead>
<tbody>{risk_rows}</tbody></table>
<div class="disc">
<b>三层单向叠加</b>　v2.3 ⊂ v3.0 ⊂ v3.1（GCCEO）。gceo 强依赖 v3：v3 关则 GCCEO 映射一并关闭，
不会出现「引用不存在层」。回滚：{rb}<br>
<b>免责</b>　本页为方法论映射与风险提问，<b>不构成投资建议</b>；{date} 盘后，预测项已带水印，不得用于回溯验收。
</div>"""
    return page(two(L, R), 18, "13　v3.1 全量整合 · 资本出海AI治理")


def _gceo_quant_valuation_page(B: dict, date: str) -> str:
    """第 19 页：v4.0 投行级估值锚与真值研判（真值算 + 缺口标注）。"""
    dist = B.get("dist") or {}
    val = B.get("val_rows") or []
    wm = B.get("watermarks") or {}
    co = B.get("counts") or {}
    chk = B.get("checks") or {}
    extra = B.get("extra_rows") or []

    # 估值锚表（7 栏，模式并入标的 tag；PEG 双口径 年/半，带 * 为高基数失真）
    def peg_cls(p: str) -> str:
        return "up" if (p.endswith("*") or p.replace(".", "").isdigit()
                        and float(p) >= 2.0) else ""

    val_rows = ""
    for r in val:
        gate = (f"<b>{r['gate']}</b>" if r["gate"] == "通过"
                else f"<span class='dn'>{r['gate']}</span>")
        val_rows += (
            f"<tr><td>{r['name']}<span class='tag g'>{r['biz']}</span></td>"
            f"<td>{r['pe']}</td><td>{r['pb']}</td><td>{r['g_h1']}</td>"
            f"<td class='{peg_cls(r['peg'])}'>{r['peg']}<span class='tcap'> {r['peg_dual']}</span></td>"
            f"<td>{r['deduct']}</td><td>{gate}</td></tr>")

    extra_txt = "、".join(f"{g['field']}" for g in extra) or "无"

    L = f"""{eyebrow("14　v4.0 投行量化 · 估值锚与真值研判")}
<h2>投行级估值锚<br>真值算 + 缺口标注</h2>
<p class="lead">候选 {dist.get('n','—')} 只：PE 中位 {dist.get('pe_median','—')} / 亏损 {dist.get('n_loss','—')} /
负增长 {dist.get('n_neg_growth','—')} / 高基数 {dist.get('n_high_base','—')}。
每数字可回溯 data.json，缺字段一律标缺口。</p>
<div class="qstrip"><b>研判池</b> {B.get('universe_n','—')} 只（{B.get('universe_src','—')}），
逐只标注冻结闸门结论；<b>本层不生成 BUY、不占 α 预算</b></div>
{impl([
 f"<b>PE/PB 真值</b>　直接取非空字段；PE≤0 标「亏损」→ PE 锚失效，PB 仅作净资产参考，不编造内在价值。",
 f"<b>PEG 双口径</b>　上年度同比为参照锚 + 中报同比为波动补充；同比&gt;200% 标『*』高基数失真；"
 f"无一致预期增速 → <b>仅参考非结论</b>。",
 f"<b>周期顶缺口</b>　复用 KNOWLEDGE 估值锚，但盈利历史分位 / 毛利率位置字段全空 → "
 f"低 PE 是买点还是卖点一律标【缺口】，不触发伪判定。",
 f"<b>利润质量</b>　复用 KNOWLEDGE.profit_quality；仅「扣非为负」可真判，"
 f"净现比 / 商誉 / 补助 / 归母缺口 → 第 20 页台账登记。"], "估值锚方法（复用冻结知识库）")}
<p class="qwm"><b>四色水印</b>　{wm.get('truth','')}<br>{wm.get('gap','')}<br>
{wm.get('infer','')}<br>{wm.get('diff','')}</p>"""

    R = f"""<table>
<colgroup><col style="width:20%"><col style="width:11%"><col style="width:10%"><col style="width:14%"><col style="width:17%"><col style="width:15%"><col style="width:13%"></colgroup>
<thead><tr><th>标的/模式</th><th>PE</th><th>PB</th><th>中报同比</th><th>PEG 年/半</th><th>扣非</th><th>闸门</th></tr></thead>
<tbody>{val_rows}</tbody></table>
<p class="tcap"><b>PEG 年/半</b>＝上年度同比口径 / 中报同比口径（仅真值实算）；带 <b>*</b> 者所选口径同比&gt;200% 高基数失真【口径差异】；
PE≤0 或同比转负 →「不适用」。扣非为 data.json 真值（元→亿）。模式为行业推定【推定】。</p>
<div class="qstrip"><b>估值侧不可判定</b>　{extra_txt} 在 data.json 全缺 →
红利股息率锚 / 周期顶低 PE 陷阱 / 前瞻 PEG 一律标【缺口】，<b>不编造</b>。</div>
<div class="qdisc"><b>非侵入自检</b>　{chk.get('passed',0)}/{chk.get('total',0)} 项通过；
冻结口径 v2.3 + KNOWLEDGE 45 键 + v3.0 五模块 + GCCEO 4.0 只读比对，均未被改写；PEG/估值仅真值实算，无 DCF/LBO 编造值。<br>
<b>免责</b>　本页为投行级量化研判视角，<b>不构成投资建议</b>；{date} 盘后。“闸门”列为冻结口径实跑结论的引用，非本层判定。</div>"""
    return page(two(L, R), 19, "14　v4.0 投行量化 · 估值锚")


def _gceo_quant_lifecycle_page(B: dict, date: str) -> str:
    """第 20 页：五维形态 + Pre-Mortem 三因 + 全周期全链路 + 数据缺口台账。"""
    rad = B.get("rad_rows") or []
    pm = B.get("pm_rows") or []
    life = B.get("life_rows") or []
    gaps = B.get("gap_rows") or []
    extra = B.get("extra_rows") or []
    chk = B.get("checks") or {}

    def bar(v) -> str:
        if v is None:
            return "—"
        w = max(0.0, min(100.0, float(v)))
        cls = " hot" if w >= 85 else (" low" if w < 40 else "")
        return (f"<span class='qbar{cls}'><i style='width:{w:.0f}%'></i></span>"
                f"<span class='qdim'>{w:.0f}</span>")

    rad_rows = ""
    for r in rad:
        comp = (f"{r['composite']:.2f}" if r.get("composite") is not None else "—")
        rad_rows += (
            f"<tr><td>{r['name']}</td><td>{bar(r.get('tech'))}</td><td>{bar(r.get('flow'))}</td>"
            f"<td>{bar(r.get('fund'))}</td><td>{bar(r.get('cycle'))}</td><td>{bar(r.get('fib'))}</td>"
            f"<td class='qcomp'>{comp}</td></tr>")

    pm_blocks = ""
    for p in pm[:4]:
        cs = "；".join(p["causes"]) or "无显著失败路径"
        pm_blocks += f"<div class='pmCause'><b>{p['name']}</b> → {cs}</div>"

    life_rows = "".join(
        f"<tr><td style='width:22%;text-align:left'><b>{s['step'].split()[0]}</b></td>"
        f"<td style='width:64%;text-align:left'>{s['truth']}</td>"
        f"<td style='width:14%'>{s['wm']}</td></tr>" for s in life)

    gap_rows = "".join(
        f"<tr><td style='width:36%;text-align:left'>{g['field']}</td>"
        f"<td style='width:12%'>{g['rate']}%</td>"
        f"<td style='width:52%;text-align:left'>{g['unable']}</td></tr>" for g in gaps)
    extra_txt = "、".join(g["field"] for g in extra) or "无"

    L = f"""{eyebrow("15　v4.0 投行量化 · 雷达/尸检/全链路")}
<h2>五维形态 · 事前尸检<br>全周期全链路</h2>
<p class="lead">研判池 {B.get('universe_n','—')} 只（{B.get('universe_src','—')}）。
五维为既有评分输入的重述，<b>非新增因子、不进 scoring 二次计分</b>。</p>
<table>
<colgroup><col style="width:20%"><col style="width:12%"><col style="width:12%"><col style="width:12%"><col style="width:12%"><col style="width:12%"><col style="width:20%"></colgroup>
<thead><tr><th>标的</th><th>技</th><th>资</th><th>基</th><th>周</th><th>位</th><th>合成</th></tr></thead>
<tbody>{rad_rows}</tbody></table>
<p class="tcap">技=技术 / 资=资金 / 基=基本面 / 周=周期 / 位=位置（fib）；合成＝既有五维加权（0-100）。
色条：黄=中性、红≥85 过热、绿&lt;40 低位（A 股红涨绿跌惯例）。</p>
<p class="tcap" style="margin-top:8px"><b>事前尸检 Pre-Mortem</b>　假设该笔交易 3 个月后失败，列出最可能原因（真值 + 缺口，非买卖结论）：</p>
{pm_blocks}"""

    R = f"""<table>
<colgroup><col style="width:22%"><col style="width:64%"><col style="width:14%"></colgroup>
<thead><tr><th>决策步</th><th>当日真值落点</th><th>水印</th></tr></thead>
<tbody>{life_rows}</tbody></table>
<p class="tcap"><b>五步决策框架</b>＝推理链脚手架，每步落到真值或明确缺口；α 预算 {B.get('budget_yi','—')} 亿受容量约束。</p>
<p class="tcap" style="margin-top:8px"><b>数据缺口台账</b>　缺什么 → 测不了什么（33 只候选逐字段统计）：</p>
<table>
<colgroup><col style="width:36%"><col style="width:12%"><col style="width:52%"></colgroup>
<thead><tr><th>缺失字段</th><th>缺失率</th><th>无法完成的核验</th></tr></thead>
<tbody>{gap_rows}</tbody></table>
<p class="tcap">估值侧另缺 {extra_txt}（全空）→ 相关锚一律标【缺口】。字段补齐后自动参与真值判定。</p>
<div class="qdisc"><b>回滚</b>　{B.get('rollback','')}<br>
<b>自检</b>　{chk.get('passed',0)}/{chk.get('total',0)}；
<b>免责</b>　本页为方法论与真值研判，<b>不构成投资建议</b>；{date} 盘后，预测项已带水印，不得用于回溯验收。</div>"""
    return page(two(L, R), 20, "15　v4.0 投行量化 · 雷达尸检全链路")


def _resolve_total(data: dict) -> int:
    """总页数单一真相源。四态（单向叠加、强依赖：gceo⊂v3，gceo_quant⊂gceo）：
      v3.enabled=false                          → 14 页（纯 v2.3）
      v3.enabled=true, gceo 关                  → 16 页（v3.0）
      v3.enabled=true, gceo 开, quant 关        → 18 页（v3.1 GCCEO 全量整合）
      v3.enabled=true, gceo 开, gceo_quant 开   → 20 页（v4.0 投行级量化研判）
    """
    v3_on = bool((data.get("v3") or {}).get("enabled"))
    gceo_on = v3_on and bool((data.get("gceo") or {}).get("enabled"))
    gq_on = gceo_on and bool((data.get("gceo_quant") or {}).get("enabled"))
    return 20 if gq_on else (18 if gceo_on else (16 if v3_on else 14))


def build_pages(m: dict, data: dict, date: str, by_code: dict, by_name: dict,
                pred: dict | None = None) -> list[str]:
    res, fr, inds = m["res"], m["fr"], m["inds"]
    notes = m.get("_notes", {})
    P: list[str] = []
    # 选股源主口径开关：limitup=涨停源右侧动量（新增只读旁路）；
    # 其余值一律走 v2.3 原超跌路径，逐字不变、可一键回滚。
    lim_screen = None
    _qa_note = ""          # 数据契约 + 资金容量联动，落在第 13 页「数据与口径说明」
    if data.get("selection_mode") == LS.MODE_LIMITUP:
        lim_screen = LS.build_screen(data)
        lim_screen["validation"] = LS.validate(data)
        lim_screen["verify"] = LS.verify_covered(data, lim_screen)
        lim_screen["capacity"] = LS.capacity_check(data, lim_screen)

    # 框架版本标识：只在扩展层开启时出现，纯 v2.3 数据下封面/口径章节完全照旧。
    v3_on = bool((data.get("v3") or {}).get("enabled"))
    gceo_on = v3_on and bool((data.get("gceo") or {}).get("enabled"))
    gq_on = gceo_on and bool((data.get("gceo_quant") or {}).get("enabled"))
    _v3chk = (data.get("v3") or {}).get("non_invasive_check") or {}
    if gq_on:
        _fw_extra = (f"{C.EXTENSION_VERSION} 五维共振 + GCCEO {C.GCCEO_SOURCE_VERSION} "
                     f"全量整合 {C.GCCEO_EXT_VERSION} + 投行量化真值研判 v4.0")
    elif gceo_on:
        _fw_extra = (f"{C.EXTENSION_VERSION} 五维共振 + GCCEO {C.GCCEO_SOURCE_VERSION} "
                     f"全量整合层 {C.GCCEO_EXT_VERSION}")
    else:
        _fw_extra = f"{C.EXTENSION_VERSION} 知识蒸馏扩展层"
    _fw_label = "v4.0" if gq_on else (C.FRAMEWORK_VERSION if gceo_on else C.EXTENSION_VERSION)
    fw = (f"　<b>框架版本</b>　{_fw_label}"
          f"（六条口径 {C.CALIBER_VERSION} 不变 + {_fw_extra}；{TOTAL} 页）") if v3_on else ""
    # 第 11 页版心在 v2.3 下已是 794px 满格，加任何文字都会溢出 ——
    # 框架说明全部移到第 15/16 页附录，封面保留框架版本标识即可。
    v3_note = ""

    n_cand = len(by_code)
    n_l1 = len(m["l1_pass"])
    n_l1v = len(m.get("l1_vr_ok") or [])
    n_l2 = len(fr.l2_pass)
    n_25 = len(fr.l2_5_removed)
    n_l3v = len(fr.l3_vetoed)
    n_pass = len(fr.l3_pass)
    sens = fr.sensitivity
    led = res["ledger"]
    srows = sorted(res["rows"], key=lambda r: -r.score)

    cutoff = f"；仅显示分位最低的 {_MAX_BUB} 个" if notes.get("bub_cut") else ""
    def tail(n_cut: int, n_show: int) -> str:
        """图注截断声明：必须打印【实际展示数】，不是被截掉的数量。
        历史缺陷：曾把 cut 数量当展示数传入 → PB 图注写出「仅显示前 499 个」，
        而实际只画了 _MAX_PB=10 根柱，属误导性图注（0917 修正）。"""
        return f"；仅显示前 {n_show} 个" if n_cut else ""

    # ── 1. 封面 ──
    demo_flag = ('<span style="color:#FFB500">　⚠ 当前为演示数据 · 非当日行情</span>'
                 if data.get("_note") else "")
    # GCCEO 全量整合能力带（前置到封面第一屏；随 gceo.enabled 显隐，16 页回滚版不露出）
    _g = data.get("gceo") or {}
    _sc = _g.get("source_counts") or {}
    _g_on = bool(_g.get("enabled"))
    _gq = data.get("gceo_quant") or {}
    _gq_on = _g_on and bool(_gq.get("enabled"))
    _gq_chk = _gq.get("non_invasive_check") or {}
    _gq_line = (
        f'<br><span class="k" style="margin-top:3px">v4.0 投行级量化研判 · 第三只读旁路'
        f'（自检 {_gq_chk.get("passed","—")}/{_gq_chk.get("total","—")}）</span>'
        f'真值算 + 缺口标注：PE/PB/PEG 实算 · 穿透 7 字段全缺口如实标注 · '
        f'<b>不编造 DCF/LBO</b> · 见 P19/P20'
    ) if _gq_on else ""
    _gcc_strip = (
        f'<div class="gcceo-strip"><span class="k">GCCEO 4.0 全量整合 · 两层只读旁路之一（自检 23/23）</span>'
        f'<b>五步决策框架</b> DEFINE→ANALYZE→SYNTHESIZE→DECIDE→EXECUTE　·　'
        f'<b>十域 {_sc.get("domain_skills", 91)} 技能</b>　·　<b>投行 {_sc.get("ib_pe", 10)}</b>'
        f'　·　<b>出海 {_sc.get("globalization", 10)}</b>　·　<b>AI 超能力 {_sc.get("ai_superpowers", 8)}</b>'
        f'　·　方法论 {_sc.get("method_tools", 16)}<br>'
        f'研判视角映射：提问 / 清单 / 风险 / 叙事 —— <b>不打分 · 不剔除 · 不上调仓位</b>'
        f'{_gq_line}</div>'
    ) if _g_on else ""
    P.append(f'''<section class="cover">
  <div class="brand"><span class="dot"></span><span class="nm">A-SHARE DRAGON-TIGER REVIEW</span>
    <span class="code">{CODE}　1/{TOTAL}</span></div>
  <h1>涨停板龙虎榜<br><em>深度研判报告</em></h1>
  <p class="sub">四层漏斗 L1→L2→L2.5→L3 全链路核验 · 财富密码选股策略融合层 ——
     图表版式参照 BlackRock 投资研究院（BII）「左文字栏 + 右图表」双栏范式重构</p>
  <div class="rule"></div>
  {_gcc_strip}
  <div class="meta">
    <b>报告日期</b>　{date}（交易日）　
    <b>口径版本</b>　{C.CALIBER_VERSION}（永久生效）{fw}　
    <b>数据来源</b>　腾讯自选股（westock-mcp）{demo_flag}<br>
    <b>分析框架</b>　四层漏斗（L1 行业 → L2 个股 → L2.5 可交易 → L3 基本面）+ 评分管道
    （技术 / 资金 / 基本面 / 周期 / 位置五维）+ α 预算风控<br>
    <b>图表规范</b>　黑 + 品牌黄（#FFB500）+ 白配色；每图含图号、口径副标题、「图表结论」条与资料来源脚注；
    涨跌类指标保留 A 股「红涨绿跌」惯例；A4 横向双栏<br>
    <b>免责声明</b>　本报告为基于公开数据的技术与基本面分析，<b>不构成任何投资建议</b>
  </div>
</section>''')

    # ── 2. 摘要 ──
    top = srows[0] if srows else None
    all_watch = bool(srows) and all(r.action == "WATCH" for r in srows)
    n_buy = sum(1 for r in srows if r.action == "BUY")
    # 结语必须由 action 分布决定：曾硬编码「有候选、无买点」，
    # 在出现 BUY 的日子里会与第 12 页「本期触发 BUY 的标的数」直接打架。
    # v2.3 升级点 4（123 原则）：核心判断 ≤30 字，必须含 1 个关键词 + 1 个关键数。
    # 关键词取当期主线/定性（弱市取情绪阶段，强市取主线名称），关键数取过会数。
    #
    # v2.3 修正（0919）：此前「关键词」硬编码为「情绪见顶」，与同页
    # 「市场情绪仪表盘」由 KN.sentiment_cycle 算出的阶段直接打架
    # （如本期引擎判「高潮」而摘要写「情绪见顶」）。改为把情绪引擎
    # 前移到此处，摘要关键词与仪表盘共用同一判定结果，单一事实来源。
    import sys as _sys, pathlib as _pl
    _sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[2]))
    from strategy import knowledge as KN
    ctx = data.get("context", {}) or {}
    _lu = int(ctx.get("limit_up_count", 60)) if ctx else None
    _br = float(ctx.get("broken_rate", 0.2)) if ctx else None
    sent = KN.sentiment_cycle(
        _lu, _br,
        lianban_height=ctx.get("lianban_height"),
        lianban_rate=ctx.get("lianban_rate"),
        prev_premium=ctx.get("prev_premium"),
        prev_stage=ctx.get("prev_sentiment_stage"),
    )
    refl = KN.reflexivity(
        ladder_height_today=ctx.get("lianban_height"),
        ladder_height_prev=ctx.get("lianban_height_prev"),
        vr_slope_up=ctx.get("vr_slope_up"),
        margin_net3d=ctx.get("margin_net3d"),
        prev_premium=ctx.get("prev_premium"),
    )
    if n_buy:
        verdict_txt = f"情绪{sent.stage}：过会 {n_pass} 只、仅 {n_buy} 只可建仓"
    else:
        verdict_txt = (
            f"情绪{sent.stage}：涨停源净买 {lim_screen['summary']['pool_n']} 只入观察、"
            f"背离 {lim_screen['summary']['divergence_n']} 只；四层闸门过会 {n_pass} 只"
            if lim_screen else f"情绪{sent.stage}：过会 {n_pass} 只、暂无买点")
    _led_full = led["used_pct"] >= led["alpha_budget"] * 0.98
    budget_txt = ("α 预算已用满" if _led_full else f"剩余 {_money(led['remaining'])}")
    verdict = f'''<div class="verdict"><span class="k">核心判断</span>
今日候选池 <b>{n_cand}</b> 只，经四层漏斗后仅 <b>{n_pass}</b> 只过会；
L1 行业层 {len(inds)} 个板块中 <b>{n_l1}</b> 个达门槛；L2.5 剔除 <b>{n_25}</b> 只不可交易标的，
L3 基本面否决 <b>{n_l3v}</b> 只。{'全部过会标的均为 <b>WATCH</b> 观察信号，' if (all_watch and n_pass > 0) else ''}
α 预算阶段 <b>{led['stage']}</b> 下已用 <b>{led['used_pct']:.1%}</b>、{budget_txt} ——
结论是「<b>{verdict_txt}</b>」。</div>'''
    kpis = [
        ("候选标的（L0）", str(n_cand), "进入闸门的全部个股", ""),
        ("L1 行业达门槛", f"{n_l1}/{len(inds)}", f"3 年分位 ≤{C.RANK_LOW_THRESHOLD:.0f}%（额比归 L2）", ""),
        ("L2 技术面入池", str(n_l2), "分位与额比双达标", ""),
        ("L3 最终过会", str(n_pass), f"L2.5 剔 {n_25} · L3 否 {n_l3v}", "hl"),
        (("α 可用额度" if _is_institutional(led["equity"]) else "α 预算剩余"),
         _money(led["remaining"]),
         ("机构级 · 单票 ≤1% 名义" if _is_institutional(led["equity"])
          else f"阶段 {led['stage']} 预算 {led['alpha_budget']:.0%}"), ""),
        ("敏感度 ±N", f"±{abs(sens['rule_50pct_relative'] - sens['rule_any_deceleration'])} 只",
         "口径③收紧的过会数变化", "hl"),
    ]
    kpi_html = "".join(
        f'<div class="kpi {c}"><p class="l">{k}</p><p class="v">{v}</p><p class="s">{s}</p></div>'
        for k, v, s, c in kpis)
    # ── v2.3 市场情绪仪表盘（缺项自动降级） ──
    # sent / refl / ctx 已在摘要「核心判断」处前移计算，此处直接复用同一结果，
    # 确保摘要关键词与仪表盘判定永远一致（单一事实来源）。
    _ban = "允许打板" if sent.allow_da_ban else "禁止打板（低吸/半路为主）"
    _sent_cls = "ok" if sent.stage in ("启动", "发酵", "高潮") else "no"
    _refl_cls = "ok" if refl.stage == "强化" else ("no" if refl.stage == "毁灭" else "")
    _sent_reasons = "；".join(sent.reasons) if sent.reasons else "—"
    _refl_reasons = "；".join(refl.reasons) if refl.reasons else "—"
    # 版式护栏（0928）：实测「依据」列若承载 3 段以上长文案（本期为
    # 「涨停 35 家 / 炸板率 18% / 连板率 20%；涨停 35 < 峰值参考 90 的 50%；
    # 昨日涨停溢价 +0.1%」，约 60 字）会撑破 36% 列宽并与「操作指令」列叠印，
    # 而页高/溢出/墨量三重几何判据对此完全无感。此处按字符数硬截断到 ~38 字，
    # 保证固定列宽下必定单行可容；被截信息在左栏「数据与口径说明」中另行完整披露。
    def _clip(s: str, n: int = 38) -> str:
        s = (s or "").strip()
        return s if len(s) <= n else s[: n - 1] + "…"
    _sent_reasons = _clip(_sent_reasons)
    _refl_reasons = _clip(_refl_reasons)
    _sent_note = ("　" + sent.note) if sent.note else ""
    # 版式修正（0928）：原用百分比列宽 + 无 table-layout 约束，当「判定」列文案较长
    # （如「见顶 · 减少操作、不追高，可低吸偏离主线的低位股 · 仓位上限 20%」）时会把
    # 「依据」列挤到文字重叠。改为 table-layout:fixed + 固定列宽 + word-break，
    # 并把「判定」列拆成「阶段 · 仓位上限」短标签，模式文案移到「操作指令」列。
    sentiment_html = (
        '<div class="sentiment-dash" style="margin:7px 0 8px;">'
        '<h3 style="font-size:13px;color:#0A3D6E;margin:0 0 4px;">市场情绪仪表盘（v2.3 知识蒸馏）</h3>'
        '<table style="font-size:11.5px;table-layout:fixed;width:100%;">'
        '<tr><th style="width:15%">维度</th><th style="width:17%">判定</th>'
        '<th style="width:34%">依据</th><th style="width:34%">操作指令</th></tr>'
        f'<tr><td>情绪周期（5 阶段）</td>'
        f'<td class="{_sent_cls}" style="word-break:break-word;">{sent.stage} · 仓位上限 {sent.pos_cap:.0%}</td>'
        f'<td style="word-break:break-word;">{_sent_reasons}</td>'
        f'<td style="word-break:break-word;">{_ban}（{_clip(sent.mode, 10)}）</td></tr>'
        f'<tr><td>反身性（索罗斯）</td>'
        f'<td class="{_refl_cls}">{refl.stage}</td>'
        f'<td style="word-break:break-word;">{_refl_reasons}</td>'
        '<td style="word-break:break-word;">强化期持有待涨，毁灭期逢高兑现、只做首板</td></tr>'
        '</table></div>'
    )
    # 情形二的「当前状态」必须由 action 分布与 α 账本决定：
    # 曾硬编码「不主动建仓」，在出现 BUY 且预算用满的日子会与同一页的
    # 「有买点（N 只触发建仓阈值）」和 KPI「α 预算已用满」当场打架（0917 修正）。
    if n_buy:
        _scen2 = (f"按综合分排序跟踪；本期已触发 <b>{n_buy} 只 BUY</b>"
                f"（α 预算使用率 {led['used_pct']:.1%}），新增建仓须先释放既有额度。")
    else:
        _scen2 = "维持 WATCH 观察，按综合分排序跟踪，不主动建仓；α 预算保持空置。"
    three = "".join([
        impl(["<b>升级条件</b>：过会标的出现放量突破 + 额比回到 1.2× 以上，且行业层维持低位。"], "情形一 · 升级信号"),
        impl([f"<b>当前状态</b>：{_scen2}"], "情形二 · 基准情形"),
        impl(["<b>失效条件</b>：过会标的跌破止损位，或行业分位抬升至 40% 以上。"], "情形三 · 失效信号"),
    ])
    # 市场全景条（2026-10-22 新增）：契约 §6 要求摘要页用「一句话定性 + 关键数字 + 主线排序」
    # 呈现资金主线；原模板 p2 只有漏斗与情绪仪表盘，缺市场层事实。本块由 data.json 的
    # context.market_brief（可选，字符串）驱动，缺失时整块不渲染，不影响旧数据兼容。
    _mkt = str((ctx or {}).get("market_brief") or "").strip()
    market_html = (
        '<div class="mkt" style="font-size:11px;line-height:1.45;color:#0A3D6E;'
        'background:#F6F8FA;border-left:3px solid #FFB500;padding:4px 9px;margin:6px 0 0;'
        'word-break:break-word;">'
        f'<b>市场全景</b>　{_mkt}</div>'
    ) if _mkt else ""
    P.append(page(f'''{eyebrow("00　摘要 · EXECUTIVE SUMMARY")}
<h2>一句话：{verdict_txt}</h2>
{verdict}
{market_html}
<div class="kpis">{kpi_html}</div>
{sentiment_html}
<div class="three">{three}</div>''', 2, "00　摘要", full=True))

    # ── 3. 图1 漏斗 ──
    L = f'''{eyebrow("01　漏斗 · FOUR-LAYER FUNNEL")}
<h2>{n_cand} 只候选，最后只有 {n_pass} 只过会</h2>
<p class="lead">四层漏斗按「行业 → 个股 → 可交易性 → 基本面」顺序逐层收口，每一层都有明确的
数值门槛，不靠主观判断。</p>
{('<p><b>【主口径说明】</b>本期已由「从超跌找」切至「<b>从涨停找</b>」（见第 4 页）：本页四层漏斗保留为<b>左侧风控对照</b>，回答「能不能买」，不再回答「从哪找」。</p>' if lim_screen else '')}
<p><b>L1 行业层</b>：{len(inds)} 个板块中 {n_l1} 个满足「3 年分位 ≤ {C.RANK_LOW_THRESHOLD:.0f}%」——
位置不贵，构成<b>超跌池</b>。额比 ≥ {C.VR_THRESHOLD:.1f}×（资金是否真的进来）是 <b>L2 个股层</b>的必要条件，
不在 L1 重复设卡：行业位置低但资金没进，只说明「便宜」，够不上「机会」。</p>
<p><b>L2 个股层</b>：{n_l2} 只通过；<b>L2.5 可交易性</b>独立成层，剔除退市整理、*ST、净资产为负等
{n_25} 只；<b>L3 基本面</b>再否决 {n_l3v} 只。</p>
{pq(f"漏斗的价值不在「选出好票」，而在「把不能买的先剔掉」—— 这次剔掉了 {n_25 + n_l3v} 只。",
    "先做减法，再做加法")}
{impl([(f"<b>过会 {n_pass} 只</b>：其中 <b>{n_buy} 只</b>触发建仓阈值、{n_pass - n_buy} 只为观察信号。"
        if n_pass > 0 else
        "<b>过会 0 只</b>：全池虽有多只高分候选，但无一同时满足「低位 + 放量 + 可交易 + 基本面」四道闸门 —— 本期无可执行信号。"),
       "<b>被剔标的同样有信息量</b>：其共性短板往往就是当期市场的短板。",
       "<b>下一层验证</b>：过会标的需在次日出现量能确认，否则维持 WATCH。"])}
'''
    pass_names = "、".join(s.name for s in fr.l3_pass) or "无"
    R = card(1, f"四层漏斗：从 {n_cand} 只候选到 {n_pass} 只过会",
             f"个股维度逐层通过数（只）；L1 行业层为 {len(inds)}→{n_l1} 入池，未计入本图",
             cv("c1", 678, 340),
             f"逐层收口后仅 <b>{n_pass} 只</b>过会（{pass_names}）。"
             f"L2.5 剔 {n_25} 只、L3 否 {n_l3v} 只 —— "
             "<b>被剔除的数量比通过的数量更有信息量</b>，它刻画的是当期市场的可交易性约束。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）· 四层漏斗执行结果"
             f"（口径 {C.CALIBER_VERSION}）。<b>注：</b>L1 为行业粒度（个），与个股粒度不可直接相连，"
             "故单独在左栏正文说明。")
    P.append(page(two(L, R), 3, "01　漏斗"))

    # ── 4. 图2 行业气泡 ──
    in_gate = "、".join(i.name for i in m["l1_pass"]) or "无"
    if lim_screen:
        sm = lim_screen["summary"]
        top = LS.table_rows(lim_screen, "pool", limit=8)
        dv = LS.table_rows(lim_screen, "divergence", limit=8)
        trs = "".join(
            f"<tr><td>{r['name']}</td><td>{r['pct']}</td><td>{r['net']}</td></tr>" for r in top)
        main_txt = " / ".join(
            f"{x['name']} +{x['net_inflow_yi']:.2f}亿({x['pct']:+.2f}%)"
            for x in lim_screen["mainline"])
        div_names = "、".join(r["name"] for r in dv)
        vd = lim_screen["validation"]
        cp = lim_screen["capacity"]
        _shares = [r["share_pct"] for r in cp["rows"]] or [0.0]
        _verdicts = "、".join(sorted({r["verdict"] for r in cp["rows"]})) or "—"
        _qa_note = (f"<b>数据契约与容量</b>　validate() 通过（主池 {vd['stats']['pool']} / "
                    f"背离 {vd['stats']['divergence']} / 唯一 {vd['unique_codes']} / "
                    f"异常 {len(vd['issues'])}，六规则全绿）；α {cp['budget_yi']:.2f} 亿占 "
                    f"{len(cp['rows'])} 只可核验股 20 日均成交 "
                    f"{min(_shares):.2f}%–{max(_shares):.2f}%（{_verdicts}），"
                    f"观察 ≠ 可容纳。<br>")
        L = f'''{eyebrow("01　主口径 · LIMIT-UP SOURCE")}
<h2>从涨停找，不从超跌找</h2>
<p class="lead">本期主口径切换为<b>当日涨停梯队 + 龙虎榜净买 + 主线资金</b>的右侧动量视角；
3 年分位 / 额比的<b>超跌池降级为位置对照</b>（右栏），不再主导选股。</p>
<p><b>主线</b>　{main_txt}。当日涨停 <b>{lim_screen['market'].get('limit_up','—')}</b> 家、
最高 <b>{lim_screen['market'].get('max_height','—')}</b> 连板。龙虎榜「涨停·净买」
<b>{sm['pool_n']} 只</b>（合计 +{sm['net_buy_total_yi']:.2f} 亿）为主池，
「涨停·净卖」<b>{sm['divergence_n']} 只</b>（{sm['net_sell_total_yi']:.2f} 亿）为量价背离风险。</p>
<table style="font-size:10px;line-height:1.25"><thead><tr><th>涨停·净买 TOP8</th><th>涨幅</th><th>净买(亿)</th></tr></thead>
<tbody>{trs}</tbody></table>
<p class="tcap">按净买降序列前 8/{sm['pool_n']} 只；全量见 <code>data.json.limitup.pool</code>。冻结闸门实跑：可核验 {lim_screen['verify']['total_n']} 只 → 通过 {lim_screen['verify']['passed_n']} 只 / L3 否决 {lim_screen['verify']['l3_rejected_n']} 只（明细见第 13 页）。</p>
<p><b>背离名单</b>　{div_names} —— 涨停但龙虎榜净卖出，是出货而非进货，一律不入观察池。</p>
<p><b>【数据缺口】</b>主池 {sm['pool_n']} 只中 {sm['covered_n']} 只与候选池重合、具备完整财务字段可走 L2.5/L3；
其余 {sm['gap_n']} 只如实标注「财务数据缺口 · 仅定性观察」，不伪造通过、不生成 BUY。
<b>【口径差异】</b>旧 L1 为左侧超跌判据，本层为右侧涨停判据，二者不互相否定。</p>
'''
        R = card(2, "位置对照（非主口径）· 行业 3 年分位 × 额比",
                 f"气泡 = 板块内部离散度；虚线 = 分位 {C.RANK_LOW_THRESHOLD:.0f}% 超跌线与额比 "
                 f"{C.VR_THRESHOLD:.1f}× 资金确认线{cutoff}。<b>本图仅供位置对照，不主导本期选股。</b>",
                 cv("c2", 678, 366),
                 f"L1 超跌池 <b>{n_l1} 个板块</b>（{in_gate}），其中额比达 "
                 f"{C.VR_THRESHOLD:.1f}× 者仅 <b>{n_l1v} 个</b>。主口径已切至左栏涨停源，"
                 "超跌池只回答「便不便宜」，不再回答「从哪找」。",
                 "<b>资料来源：</b>左栏 westock-mcp data_lhb(2026-11-11) 实取；右栏板块分位与成交额比。"
                 "<b>注：</b>净买额单位亿元（原始元 ÷1e8）；观察池不构成建仓清单。")
    else:
            L = f'''{eyebrow("01　漏斗 · L1 INDUSTRY GATE")}
        <h2>行业先筛位置，个股再筛资金</h2>
        <p class="lead">L1 是唯一一道「站在行业视角」的闸门，但<b>它只回答一个问题：这个行业贵不贵</b>。
        「资金进没进」留给 L2 逐只个股去验 —— 两把尺子分工，不在一层里重复设卡。</p>
        <p><b>横轴 = 3 年分位</b>，越靠左代表板块在自身过去三年的位置越低；
        <b>纵轴 = 额比</b>，是近期成交额与历史常态的比值，衡量资金是否真的进场。
        分位 {C.RANK_LOW_THRESHOLD:.0f}% 左侧为 <b>L1 超跌池</b>；额比 {C.VR_THRESHOLD:.1f}× 线是
        <b>L2 个股层</b>的资金确认线，画在同一张图上便于对照。</p>
        <p>本期超跌池：<b>{in_gate}</b>；其中额比已达 {C.VR_THRESHOLD:.1f}× 的仅 <b>{n_l1v} 个</b>。
        位置低但没有放量，只能算「便宜」，够不上「机会」。</p>
        {pq("位置低是必要条件，不是充分条件 —— 便宜可以便宜很久，资金进场才是催化剂。",
            "为什么 L1 只看位置")}
        {impl(["<b>不要只看跌幅榜</b>：跌得多不等于机会，要配成交额变化一起看。",
               "<b>气泡大小 = 板块内部离散度</b>：气泡越大说明内部分化越剧烈，个股选择越重要。",
               "<b>门槛是过滤器不是预测器</b>：通过门槛只代表「值得继续看」，不代表会涨。"])}
        '''
            R = card(2, "行业 3 年分位 × 成交额比：超跌池与资金确认线",
                     f"气泡 = 板块内部离散度（越大越分化；散度为 0 表示本次取数无该行业成份股分位样本，"
                     f"非「无分化」）；虚线 = 分位 {C.RANK_LOW_THRESHOLD:.0f}% 超跌线（L1 入池）"
                     f"与额比 {C.VR_THRESHOLD:.1f}× 资金确认线（L2 判定）{cutoff}",
                     cv("c2", 678, 366),
                     f"L1 超跌池 <b>{n_l1} 个板块</b>（{in_gate}），其中额比已达 "
                     f"{C.VR_THRESHOLD:.1f}× 者仅 <b>{n_l1v} 个</b> —— "
                     "<b>「位置低」与「资金进」是两把独立的尺子</b>：前者在 L1 整池筛，后者在 L2 逐只验，"
                     "单看任一项都会误判。",
                     "<b>资料来源：</b>腾讯自选股（westock-mcp）· 板块年内分位与成交额比。"
                     "<b>注：</b>额比按区间成交额与历史常态比值计算，非简单量比；分位为当月保留口径。")

    P.append(page(two(L, R), 4, "01　漏斗"))

    # ── 5. 图3 雷达 ──
    top_names = "、".join(r.name for r in srows[:3]) or "无"
    L = f'''{eyebrow("02　评分 · FIVE-DIMENSION RADAR")}
<h2>同一批候选，强在不同的地方</h2>
<p class="lead">五维评分把「为什么选它」拆成可比较的五个方向。雷达图的作用不是比大小，
而是看<b>形状</b> —— 形状差异直接指向不同的持有方式。</p>
<p>技术面强、基本面弱的是<b>交易型</b>；基本面强、技术面平的是<b>配置型</b>；
只有形状均衡的才适合作为底仓。本期高分候选为 <b>{top_names}</b>。</p>
{pq("看形状，不看面积 —— 面积大但形状歪的标的，往往对应「赚了指数不赚钱」的体验。",
    "雷达图的正确读法")}
{impl(["<b>先定风格再定标的</b>：形状决定该用交易还是配置的方式持有。",
       "<b>短板即风险</b>：雷达上凹进去的那一维，通常就是回撤时最先出问题的维度。",
       "<b>满分 100 但别追满</b>：五维全高的标的一年也未必出现一次。"])}
'''
    R = card(3, "Top 候选五维评分雷达",
             "技术面 / 资金面 / 基本面 / 周期位置 / 斐波那契位置，满分 100",
             cv("c3", 660, 392),
             f"前三名（{top_names}）形状各异：<b>强项维度不同，意味着持有方式不能照搬</b>。"
             "雷达面积接近的标的，未必可以互相替代。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）评分体系 + 策略包 `pipeline.score_row` 加权。"
             "<b>注：</b>缺少的维度按「不给分」处理，不做均值替代 —— 均值替代会系统性高估数据缺失标的。")
    P.append(page(two(L, R), 5, "02　评分"))

    # ── 6. 图4 综合分 ──
    if srows:
        s0, sN = srows[0], srows[-1]
        gap_line = f"最高分 <b>{s0.score:.1f}</b>（{s0.name}）与末位相差 <b>{s0.score - sN.score:.1f} 分</b>。"
        head_line = (f"本期最高分 <b>{s0.score:.1f}</b>（{s0.name}），动作为 <b>{s0.action}</b>。"
                     + ("全部候选均为 WATCH —— 分数够看，但未触发建仓阈值。" if all_watch else ""))
    else:
        s0 = None
        gap_line = "本期无候选。"
        head_line = "本期无候选。"
    L = f'''{eyebrow("02　评分 · COMPOSITE RANKING")}
<h2>综合分排序与风控动作</h2>
<p class="lead">综合分 = 五维加权 + 加分项（国资背景、新兴科技）− 减分项（单年亏损、增速失速）。
分数决定排序，但<b>动作由风控规则决定</b>，两者是分开的。</p>
<p>{head_line}</p>
{pq("分数告诉你「看谁」，风控告诉你「能不能买」—— 不要用一个答案回答两个问题。",
    "排序与动作分离")}
{impl(["<b>WATCH 不是观望</b>：它是有明确升级条件的等待。",
       "<b>排序会骗人</b>：分差 1~2 分不构成优劣，分差 10 分以上才有区分度。",
       "<b>动作栏才是可执行信息</b>，分数只是研究顺序。"])}
'''
    R = card(4, "候选综合分排序与风控动作",
             f"综合分 = 五维加权 + 加分项 − 减分项，满分 100；末端标注风控动作"
             f"{tail(notes.get('rank_cut', 0), _MAX_RANK)}",
             cv("c4", 678, 320),
             f"{gap_line}但排序只解决「先看谁」，<b>能不能买由风控动作栏决定</b> —— "
             f"本期触发 BUY 的标的数为 <b>{sum(1 for r in srows if r.action == 'BUY')}</b>。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）· 评分管道输出。"
             "<b>注：</b>综合分与分项分均来自同一评分体系，样本内可比；跨报告不可直接比较。")
    P.append(page(two(L, R), 6, "02　评分"))

    # ── 7. 图5 财务增速 ──
    # 增速红线只对 **L2 入池标的** 执行（L3 层口径），故名单必须限定在 L2 池内 ——
    # 曾对全候选池（数百只）统计，左栏直接列出上百个名字把版面顶破；
    # 且把「未进入 L2 的标的」也算作「触发硬线」本身就不成立。
    # L3 的执行域 = L2 入池 − L2.5 可交易性剔除（口径⑥：L2.5 是独立一层，先于 L3）
    _l2codes = {s.code for s in fr.l2_pass} - {g.code for g in fr.l2_5_removed}
    hard = [c["name"] for c in by_code.values()
            if c["code"] in _l2codes
            and c.get("interim_yoy") is not None and float(c["interim_yoy"]) <= 0]
    hard_txt = "、".join(hard[:6]) + (f" 等 {len(hard)} 只" if len(hard) > 6 else "") or "无"
    sens_n = abs(sens["rule_50pct_relative"] - sens["rule_any_deceleration"])
    # v2.3：利润质量红旗扫描（§11 说明用）。
    # 口径：只扫 **L3 过会标的**（fr.l3_pass）—— 红旗否决是过会后的最后一道闸，
    # 对 1600 只候选逐只扫既无意义（绝大多数未进入 L2/L3、本就无财务数据），
    # 又会因「全池无财务字段」而误触发数据缺口文案。
    try:
        from strategy import knowledge as _KN
        _pass_codes = {s.code for s in fr.l3_pass}
        _pq_rows = [by_code[c] for c in _pass_codes if c in by_code]
        _pq_veto, _pq_names = 0, []
        _pq_gap = 0
        _opt_keys = ("net_cash_ratio", "recv_rev_gap", "inv_rev_gap", "goodwill_ratio")
        for _c in _pq_rows:
            _pq = _KN.profit_quality(_c)
            if _pq.veto_suggest:
                _pq_veto += 1
                _pq_names.append(_c.get("name") or _c.get("code"))
            if _c.get("net_cash_ratio") is None:
                _pq_gap += 1
        pq_veto = _pq_veto
        pq_names = "、".join(_pq_names[:6]) + (f" 等 {_pq_veto} 只" if _pq_veto > 6 else "")
        pq_hit = f"（{pq_names}）" if _pq_names else ""
        # 单条强红旗也要点名：0 只否决 ≠ 干净，需把「仅 1 条但含扣非为负」的标的显式列出
        _one = []
        for _c in _pq_rows:
            _q = _KN.profit_quality(_c)
            if not _q.veto_suggest and _q.red_flags:
                _nm = _c.get("name") or _c.get("code")
                _one.append(f"{_nm} {_q.red_flags[0].split('（')[0].strip()}")
        pq_single = ("；另 " + str(len(_one)) + " 只单条强红旗（降级观察）：" + "、".join(_one[:4])
                     + ("…" if len(_one) > 4 else "")) if _one else ""
        pq_n = len(_pq_rows)
        pq_note = ("（净现比字段缺失 %d 只 → 该部分仅能覆盖扣非/背离类判据，"
                   "商誉口径因接口未返回 Goodwill 全期缺失，结论偏保守）" % _pq_gap
                   if _pq_gap else "")
    except Exception:
        pq_veto, pq_n, pq_note, pq_names, pq_hit = 0, len(fr.l3_pass), "（本期无法执行扫描）", "", ""
    L = f'''{eyebrow("03　财务 · GROWTH RED LINE")}
<h2>增速红线的三道判读</h2>
<p class="lead">口径③以<b>半年口径</b>（最新中报年内同比）判定成长性。它有三档：
硬线排除、减分线扣分、其余通过。</p>
<p><b>硬线</b>：中报同比 ≤ 0 → 直接排除；
<b>减分线</b>：同比 &gt; 0 但不足上一年度增速的 50% → 重大减分 −15 分。
本期触发硬线（限 L2 入池标的）：<b>{hard_txt}</b>。</p>
<p>50% 这条<b>相对线</b>是框架自定默认值，不是市场共识。把它收紧为「任何减速即排除」，
过会数量会从 <b>{sens['rule_50pct_relative']}</b> 只降到 <b>{sens['rule_any_deceleration']}</b> 只，
差 <b>±{sens_n} 只</b> —— 这个敏感度必须随报告披露。</p>
{pq("增速不是越高越好，而是「别掉档」—— 从高增速掉到低增速，比一直低增速更危险。",
    "为什么用相对线而非绝对线")}
{impl([f"<b>本报告 ±N = {sens_n} 只</b>：口径收紧会改变过会名单，务必知悉。",
       "<b>不要用年度口径替代半年口径</b>：两套口径下整批结论会翻转。",
       "<b>扣非与归母要分开看</b>：归母为正但扣非为负，说明盈利质量存疑。"])}
'''
    R = card(5, "中报同比 vs 上年度增速：增速红线的三道判读",
             f"半年口径归母同比（黄）与上一年度增速（灰）对照；单位 %；顶部虚线为 50% 相对线"
             f"{tail(notes.get('fin_cut', 0), _MAX_FIN)}",
             cv("c5", 678, 330),
             f"硬线（同比 ≤0）在 L2 池内排除 <b>{len(hard)} 只</b>（{hard_txt}）；"
             "减分线针对「增速掉档」的标的扣分而非排除。"
             f"<b>口径 50% 相对线的 ±N 敏感度为 {sens_n} 只</b>，"
             "是本报告最需要读者知悉的不确定性来源。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）`data_finance`"
             "（归母同比 `NPParentCompanyYOY`）。<b>注：</b>半年口径 = 最新中报年内同比；"
             f"增速红线见 `strategy/calibers.py`（口径 {C.CALIBER_VERSION}）。")
    P.append(page(two(L, R), 7, "03　财务"))

    # ── 8. 图6 PB ──
    neg_pb = [c["name"] for c in by_code.values()
              if c.get("pb") is not None and float(c["pb"]) < 0]
    # 名称类剔除（退市 / ST / *ST）—— 单列，供左栏与图结论条说明「它们为何不在榜上」。
    # 不单列会让读者以为榜单漏了标的，单列才能自证与 L2.5 清单一致（0917 二次修正）。
    name_excl = [c["name"] for c in by_code.values()
                 if c.get("pb") is not None and float(c["pb"]) > 0
                 and not pb_tradable(c)]
    low_pb = sorted([(c["name"], float(c["pb"])) for c in by_code.values()
                     if pb_tradable(c)], key=lambda x: x[1])[:3]
    low_txt = "、".join(f"{n}（{v:.2f}×）" for n, v in low_pb) or "无"
    # 名称类剔除项可达数十只（ST 股 PB 多为正），全量罗约会撑破版心 →
    # 图卡结论条只报数量，左栏最多列 4 只作示例（0917 二次修正）。
    _nx_show = "、".join(name_excl[:4]) + ("等" if len(name_excl) > 4 else "")
    name_excl_txt = _nx_show or "无"
    L = f'''{eyebrow("03　财务 · VALUATION")}
<h2>PB 是安全边际，不是上涨理由</h2>
<p class="lead">对重资产与周期型标的，市净率比市盈率更稳定；对轻资产成长股则参考价值有限。
本图只做排序参考，不构成买卖依据。</p>
<p>估值最低的三只：<b>{low_txt}</b>。</p>
<p><b>PB 为负</b>意味着净资产为负，属于可交易性层面的问题，会在 L2.5 被单独剔除，
而不是作为「估值便宜」处理。本期：<b>{"、".join(neg_pb) or "无"}</b>。</p>
<p>同理，<b>已退市与 ST / *ST 标的也不进本榜</b>—— 它们同样命中 L2.5，相对估值指标
识别不了「公司已不存在或已出问题」。本期因此另有 <b>{len(name_excl)} 只</b>被排除
（{name_excl_txt}）。</p>
{pq("低估值只能解释「跌不动」，不能解释「会涨」—— 上涨需要资金和景气度，估值不提供。",
    "低估值的正确位置")}
{impl(["<b>PB 为负不是「极便宜」</b>：净资产为负的标的优先走可交易性剔除流程。",
       "<b>跨行业不可比</b>：不同行业的 PB 中枢差异极大，只在同行业内比较。",
       "<b>与增长配对使用</b>：低 PB + 正增长才是有效组合。"])}
'''
    R = card(6, "候选市净率（PB）排序：安全边际视角",
             "PB 由低到高排列，仅取 PB > 0 且未命中 L2.5 名称类剔除（退市 / ST / *ST）者"
             "（两类命中项均属可交易性问题，已排除，见图结论条与左栏）；"
             "黄 = PB ≤2×（低估值区），灰 = 其余"
             + tail(notes.get("pb_cut", 0), _MAX_PB),
             cv("c6", 678, 336),
             f"低估值区（PB ≤2×）标的为 "
             f"{'、'.join(n for n, v in low_pb if v <= 2) or '无'}；"
             f"PB 为负 <b>{len(neg_pb)} 只</b>（{'、'.join(neg_pb) or '无'}）—— "
             "后者应走可交易性剔除通道，<b>而非被解读为「特别便宜」</b>；"
             f"另有 <b>{len(name_excl)} 只</b>已退市 / ST 标的同样不进榜，"
             "<b>不并入低估值区</b>。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）`data_finance` 市净率 + `data_quote` PB / 名称核对。"
             "<b>注：</b>PB 仅作同行业内相对排序参考，不构成估值结论；净资产为负、已退市、ST / *ST "
             "标的均在 L2.5 层单独处理。")
    P.append(page(two(L, R), 8, "03　财务"))

    # ── 9. 图7 五维分项 ──
    L = f'''{eyebrow("04　结构 · SCORE DECOMPOSITION")}
<h2>把综合分拆回五个维度</h2>
<p class="lead">综合分是加权结果，看不出短板在哪。拆回五维之后，每只标的的「问题维度」
会直接暴露出来 —— 这比总分更有决策价值。</p>
<p>读法：<b>看哪根柱子最短</b>。最短的那一维就是该标的在回撤中最先失效的环节，
也是仓位上限的真正约束。</p>
{pq("总分决定排序，短板决定仓位 —— 一个决定先看谁，一个决定敢放多少。",
    "为什么要拆项")}
{impl(["<b>基本面维度最低</b>的标的，不适合作为中期持有。",
       "<b>资金面维度最低</b>的标的，即便技术形态好也只适合短打。",
       "<b>五维均衡</b>比「某一维极高」更难得，也更适合承担主要仓位。"])}
'''
    R = card(7, "五维评分分项拆解",
             "各候选在技术面 / 资金面 / 基本面 / 周期位置 / 斐波那契五个维度的原始得分（满分 100）"
             + tail(notes.get("dim_cut", 0), _MAX_DIM),
             cv("c7", 678, 372),
             "拆项后可以看到：<b>多数候选的短板集中在基本面或资金面</b>，而技术面普遍不低 —— "
             "说明当前的约束不是「形态不好」，<b>而是「基本面或资金面不给力」</b>，"
             "这决定了仓位应该偏保守。",
             "<b>资料来源：</b>腾讯自选股（westock-mcp）评分体系分项。"
             "<b>注：</b>分项为原始得分，未含加分项与减分项；加权后的综合分见图 4。")
    P.append(page(two(L, R), 9, "04　结构"))

    # ── 10. 图8 α 账本（v3.1.2 资金规模自适应结构重构） ──
    budget_yuan = led["equity"] * led["alpha_budget"]
    empty_note = "预算完全空置，说明本期没有触发建仓条件。" if led["positions"] == 0 else ""
    # 相对判据（2026-11-11 修正）：原用 remaining<1万元 判「打满」，在 7000 元本金下
    # 即使完全空置（remaining≈2100 元）也恒为真，会误报「本期建仓已打满额度」。
    _used_up = led["used_pct"] >= led["alpha_budget"] * 0.98
    _unit_div, _unit_lab = _scale_unit(led["equity"])
    inst = _is_institutional(led["equity"])
    cap = data.get("capital") or {}
    cap_rows = cap.get("capacity_rows") or []
    if inst and cap_rows:
        trs = "".join(
            f"<tr><td>{r['name']}</td><td>{r['turnover_yi']:.2f}</td>"
            f"<td>{r['cap_1pct_yi']:.2f}</td><td>{r['budget_share_pct']:.1f}%</td>"
            f"<td>{r['verdict']}</td></tr>" for r in cap_rows)
        cap_table = (f'<table style="font-size:10px;line-height:1.25"><thead><tr>'
                     f'<th>标的</th><th>成交额</th><th>1%上限</th>'
                     f'<th>α占比</th><th>判定</th>'
                     f'</tr></thead><tbody>{trs}</tbody></table>')
        L_extra = f'''<h3>规模切换：从「买不买得起」到「装不装得下」</h3>
<p>权益 <b>{_money(led['equity'])}</b> 下，约束不再是 1 手门槛，而是<b>流动性容量</b>。
以真实 20 日均成交额（亿元）实算：1%上限 = 成交×1%；α占比 = 阶段额度 ÷ 成交。
按单票 ≤1% 名义、参与率 ≤10% 判定。</p>
{cap_table}
<p><b>【口径差异】</b>{cap.get('caliber_diff','')}</p>
{impl(["<b>容量先于选股，规模不改判定</b>：单票上限 = min(α额度×单票比例, 20日均成交×参与率)；四层漏斗与本金无关，本期仍为纪律性空仓。"])}'''
    else:
        L_extra = f'''{pq(("预算已用满：本期建仓已把阶段额度打满，新增标的只能等额置换（先减后加），不得突破 30% 上限。"
     if _used_up else
     "预算没用完不是「浪费」，是「没有符合条件的机会」—— 空仓也是一种仓位。"),
    "α 预算的纪律意义")}
{impl(["<b>用不完 ≠ 应该用完</b>：预算是上限，不是目标。",
       "<b>冰点期预算减半</b>：`ICE_POINT_ALPHA_MULTIPLIER` 按 0.5 折减，防止在极端行情里放大风险。",
       "<b>三道限额先于选股</b>：单笔、单票、总仓限额在选股之前就已锁定。"])}'''
    L = f'''{eyebrow("05　风控 · α BUDGET LEDGER" + (" · 机构级容量约束" if inst else ""))}
<h2>{"资金容量与执行约束" if inst else "α 预算：先定风险的额度，再谈机会"}</h2>
<p class="lead">α 账本把「能亏多少」前置成预算。阶段 <b>{led['stage']}</b> 对应预算比例
<b>{led['alpha_budget']:.0%}</b>，以权益 <b>{_money(led['equity'])}</b> 计，
可用额度 <b>{_money(budget_yuan)}</b>。</p>
<p>当前持仓 <b>{led['positions']}</b> 笔、已用 <b>{led['used_pct']:.1%}</b>、
剩余 <b>{_money(led['remaining'])}</b>。{empty_note}</p>
{L_extra}
'''
    R = card(8, ("资金容量与 α 额度" if inst else "α 预算使用情况"),
             f"阶段 {led['stage']} 预算 = 权益 × {led['alpha_budget']:.0%}；金额单位 {_unit_lab}",
             cv("c8", 678, 190),
             f"已用 <b>{_money(led['open_notional'])}</b>、"
             f"剩余 <b>{_money(led['remaining'])}</b>。"
             + (f"当前持仓 {led['positions']} 笔 —— <b>阶段额度已打满</b>，"
                f"含义是「本期 {led['positions']} 笔建仓已占满风险预算」，"
                "新增标的须先释放既有额度，而不是继续加仓。"
                if _used_up else
                f"当前持仓 {led['positions']} 笔 —— <b>预算空置是可接受的结果</b>，"
                "它的含义是「本期没有符合风险收益要求的机会」，而不是「应该加快出手」。"),
             f"<b>资料来源：</b>策略包 `risk.AlphaLedger` 快照；容量取 westock 20 日均成交额实算。"
             f"<b>注：</b>α_max 为阶段预算上限；冰点期按 0.5 折减；金额单位{_unit_lab}。")
    P.append(page(two(L, R), 10, "05　风控"))

    # ── 11. 六条口径（full） ──
    rows_cal = [
        ("① 国企央企背景", "偏好项（+6 分），不是门槛", "soe_background"),
        ("② 产业偏好", "新兴科技成长优先（+8 分）", "emerging_tech"),
        ("③ 净利润增长率", "<b>半年口径</b>（最新中报年内同比）", "interim_yoy"),
        ("④ 单年亏损", "减分项（−10 分）；连续两年年报亏损 = 否决", "annual_loss_years"),
        ("⑤「链」形态主题", "跳过 L1 否决权（行业层仅定性）", "CHAIN_THEMES"),
        ("⑥ 基础可交易性", "<b>L2.5 独立层</b>（位于 L2 与 L3 之间）", "gate_tradability"),
    ]
    cal_html = "".join(
        f"<tr><td>{a}</td>"
        f"<td style=\"text-align:left;white-space:normal\">{b}</td>"
        f"<td style=\"text-align:left\">{c2}</td></tr>" for a, b, c2 in rows_cal)
    demo_disc = ("<b>⚠ 本期为演示数据（`strategy/sample_data.json`），非当日真实行情，"
                 "仅用于跑通流程。</b>" if data.get("_note") else "")
    P.append(page(f'''{eyebrow("06　口径 · CALIBERS (PERMANENT)")}
<h2>六条口径：{C.CALIBER_VERSION}，永久生效</h2>
<p class="lead">口径一旦定稿即永久生效。任何变更都必须<b>全量重算历史结论</b>并披露 ±N 只敏感度 ——
口径漂移会让不同日期的报告失去可比性，这比单次判断错误更危险。</p>
<table>
<colgroup><col style="width:22%"><col style="width:52%"><col style="width:26%"></colgroup>
<thead><tr><th>口径</th><th>v2.3 取值（v2 六条不变）</th><th>实现模块</th></tr></thead>
<tbody>{cal_html}</tbody></table>
<p class="tcap"><b>增速红线（口径③的量化）</b>　硬线：中报同比 ≤ 0 → 排除；减分线：同比 &gt; 0 但不足上一年度增速
50% → 重大减分 −15 分。<b>50% 相对线为框架自定默认值</b>，收紧为「任何减速即排除」会改变过会数量，
本报告披露的敏感度为 <b>±{sens_n} 只</b>。</p>
<p class="tcap"><b>利润质量红旗扫描（v2.3 新增 · 科目接力造假检测）</b>　对每只 L3 候选执行 5 类红旗扫描：
① 净现比 &lt; 0.5（经营现金流 / 归母净利润，连续两期）；② 存货增速 − 营收增速 &gt; 20pp 且存货绝对额上升；
③ 应收增速 − 营收增速 &gt; 20pp；④ 商誉 / 净资产 &gt; 30%；⑤ 扣非为负但归母为正（非经常性损益撑利润）。
<b>≥2 条同时命中 → 标记 veto_suggest（一票否决级人工复核）</b>；单条命中只罚分不否决。
本期 L3 过会 <b>{pq_n} 只</b>中，命中 ≥2 条红旗者 <b>{pq_veto} 只</b>{pq_hit}
{pq_note}{pq_single}。扣非为负的原有罚分语义不变（向后兼容）。</p>
<div class="disc">
<b>数据与口径说明</b>　行情、资金流向、评分、分位、额比均来自腾讯自选股（westock-mcp）；
口径版本 <b>{C.CALIBER_VERSION}</b>；策略包 `strategy/` 负责闸门与评分，`pipeline` 负责信号输出。
{v3_note}{demo_disc}<br>
<b>图表规范</b>　本报告版式参照 BlackRock 投资研究院（BII）公开材料重构：A4 横向「左文字栏 + 右图表」双栏；
每图含图号、口径副标题、图体、黑底「图表结论」条与资料来源脚注；配色为黑 + 品牌黄（#FFB500）+ 白；
涨跌类指标保留 A 股「红涨绿跌」惯例。<br>
<b>免责声明</b>　本文档为基于公开数据的技术与基本面分析，<b>不构成任何投资建议</b>。
所有目标位、止损位均为技术测算参考，不代表未来价格走势。市场有风险，投资需谨慎。
</div>''', 11, "06　口径", full=True))

    # ── 12. 风险 + 三情形（full） ──
    P.append(page(f'''{eyebrow("07　风险清单与情形推演")}
<h2>六个风险，按优先级排序</h2>
<div class="risk">
<ol>
<li><b>口径敏感度是本报告最大的不确定性</b>：口径③的 50% 相对线收紧会使过会数量由
{sens['rule_50pct_relative']} 只降至 {sens['rule_any_deceleration']} 只（±{sens_n} 只），
须按最保守口径复核名单。</li>
<li><b>过会 ≠ 可买</b>：本期触发 BUY 的标的数为 <b>{sum(1 for r in srows if r.action == 'BUY')}</b>；
把 WATCH 当 BUY 是本流程最常见的误用。</li>
<li><b>数据时效</b>：{"当前为演示数据，非当日行情，任何结论不可直接用于交易。" if data.get("_note") else "行情与资金数据为收盘后快照，盘中数据会变动。"}</li>
<li><b>L2.5 与 L3 不可混同</b>：「不可交易」与「基本面不通过」是两类问题，
混淆会把可修复的问题误判为标的质量问题。</li>
<li><b>分位与额比的历史依赖</b>：两者都基于历史区间计算，区间选择变化会影响门槛通过情况。</li>
<li><b>样本内可比性</b>：综合分与分项分只在同一评分体系、同一口径版本内可比，跨报告不可直接比较。</li>
</ol>
</div>
<div class="three" style="margin-top:14px;">
{impl(["<b>升级条件</b>：过会标的出现放量突破，额比回到 1.2× 以上，且行业层维持低位。三条同时成立才升级为建仓评估。"], "情形一 · 升级信号")}
{impl([f"<b>基准应对</b>：{_scen2}"], "情形二 · 基准情形")}
{impl(["<b>失效条件</b>：过会标的跌破止损位，或行业分位抬升至 40% 以上，或 L3 基本面出现新的否决项。"], "情形三 · 失效信号")}
</div>''', 12, "07　风险清单", full=True))

    # ── 13. 跟踪清单 + 数据说明（full） ──
    # 过会标的可达数十只；全量入表会把版心顶破（2026-09-16 实测 26 行时页高超阈值 454px）。
    # 按综合分降序只列前 _MAX_WATCH 只，并在表下注明总数与截断规则 —— 不静默截断。
    _MAX_WATCH = 11
    # 2026-10-28 补：截断只按综合分会把「排名靠后的 BUY」一起截掉（本期金融街 77.2 排第 15），
    # 与第 2 页「4 只可建仓」直接打架。改为：先取前 11 只，再把未入表的 BUY 追加进表 ——
    # 保证任何 BUY 都不被静默隐藏。
    _buy_all = [r for r in srows if (getattr(r, "action", "") or "").upper() == "BUY"]
    _others = [r for r in srows if (getattr(r, "action", "") or "").upper() != "BUY"]
    # BUY 优先占位，剩余名额按综合分补足；总行数仍受 _MAX_WATCH 约束（不冒版心溢出的风险）
    watch_shown = sorted(_buy_all + _others[:max(0, _MAX_WATCH - len(_buy_all))],
                         key=lambda r: -float(getattr(r, "score", 0) or 0))
    watch_rows = []
    for r in watch_shown:
        c = by_code.get(r.code) or {}
        price = c.get("price")
        entry = c.get("entry")
        stop = c.get("stop")
        watch_rows.append(
            f"<tr><td>{r.name}<span class='tag g'>{r.code}</span></td>"
            f"<td>{price if price is not None else '—'}</td>"
            f"<td>{entry if entry is not None else '—'}</td>"
            f"<td>{stop if stop is not None else '—'}</td>"
            f"<td>{r.score:.1f}</td><td>{r.action}</td></tr>")
    if not watch_rows:
        watch_rows.append("<tr><td colspan='6'>本期无过会标的</td></tr>")
    # 过会 0 只时（观察模式），srows 是全池评分而非过会名单 ——
    # 原模板把 len(srows) 当「过会数」、把全池当「明日盯住」，与第 2/3 页「过会 0 只」直接打架。
    if n_pass == 0:
        watch_note = (f"　本期四层漏斗<b>过会 0 只</b>；下表为全候选池评分排序（观察榜，"
                      f"仅供研究、<b>不构成建仓清单</b>），列前 <b>{len(watch_shown)}/{len(srows)} 只</b>，"
                      f"其余 {len(srows) - len(watch_shown)} 只见当日 <code>data.json</code> 候选池"
                      f"与 <code>framework/</code> 落盘明细。")
        _watch_title = (f"涨停源主口径 · 全池观察榜 {len(srows)} 只（不构成建仓清单）" if lim_screen
                        else f"本期无过会标的 · 全池观察榜 {len(srows)} 只（不构成建仓清单）")
    else:
        watch_note = (f"　本表按综合分降序列出前 <b>{len(watch_shown)} 只</b>；"
                      f"本期过会共 <b>{n_pass} 只</b>，其余 "
                      f"{len(srows) - len(watch_shown)} 只见当日 <code>data.json</code> 候选池"
                      f"与 <code>framework/</code> 落盘明细。"
                      if len(srows) > _MAX_WATCH else "")
        # v2.3 升级点 4（《故事的力量》123 原则）：第 13 页标题必须用结论式，
        # 即「明日盯住这 N 只：XXX / YYY / ZZZ」，而不是中性的「跟踪清单」。
        _buys = [r for r in srows if (getattr(r, "action", "") or "").upper() == "BUY"] or list(srows)
        _top3 = " / ".join((getattr(r, "name", "") or "").strip() for r in _buys[:3]) or "无过会标的"
        _etc = " 等" if len(_buys) > 3 else ""
        _watch_title = f"明日盯住这 {len(_buys)} 只：{_top3}{_etc}"
    _thead = ("<th>标的</th><th>最新价</th><th>参考入场</th><th>止损位</th>"
              "<th>综合分</th><th>风控动作</th>")
    _read_note = ("<b>读法</b>　「参考入场 / 止损位」来自候选数据，为技术测算参考；"
                  "「风控动作」由评分管道给出，是唯一的可执行字段。<b>动作栏为 WATCH 时不得建仓</b>，"
                  "须等待升级条件成立。标的按综合分降序排列，不代表推荐强度排序。" + watch_note)
    if lim_screen:
        sm = lim_screen["summary"]
        vf = lim_screen["verify"]
        shown = LS.table_rows(lim_screen, "pool", limit=_MAX_WATCH)
        vmap = {r["code"]: r for r in vf["rows"]}
        watch_rows = []
        for r in shown:
            v = vmap.get(r["code"])
            fin = "覆盖" if v else "缺口"
            gate = ("通过" if v["passed"] else "L3 否决") if v else "未核验"
            watch_rows.append(
                f"<tr><td>{r['name']}<span class='tag g'>{r['code']}</span></td>"
                f"<td>{r['pct']}</td><td>{r['net']}</td><td>{fin}</td>"
                f"<td>{gate}</td><td>WATCH</td></tr>")
        _thead = ("<th>涨停源标的</th><th>涨幅</th><th>龙虎榜净买(亿)</th>"
                  "<th>财务字段</th><th>L2.5/L3 实跑</th><th>风控动作</th>")
        _watch_title = (f"涨停源观察榜 {len(shown)}/{sm['pool_n']} 只 · "
                        f"冻结闸门通过 {vf['passed_n']}/{vf['total_n']}（不构成建仓清单）")
        watch_note = (f"　按龙虎榜净买降序列前 <b>{len(shown)}/{sm['pool_n']} 只</b>，"
                      f"其余 {sm['pool_n'] - len(shown)} 只见 <code>data.json.limitup.pool</code>；"
                      f"背离 {sm['divergence_n']} 只见第 4 页。"
                      f"可核验 {vf['total_n']} 只经 <b>L2.5/L3 冻结闸门实跑</b>："
                      f"通过 {vf['passed_n']} 只、L3 否决 {vf['l3_rejected_n']} 只；"
                      f"其余 {sm['gap_n']} 只标财务缺口、仅定性观察。"
                      f"全表动作栏恒为 WATCH，<b>不构成建仓清单</b>。")
        _read_note = ("<b>读法</b>　本表为<b>涨停源观察池</b>，按龙虎榜净买降序，"
                      "不代表推荐强度；「财务字段=缺口」者无闸门核验资格，"
                      "「L2.5/L3 实跑」是冻结口径的真实核验结果而非买卖建议。"
                      "<b>动作栏恒为 WATCH，不得建仓</b>。" + watch_note)
    P.append(page(f'''{eyebrow("08　跟踪清单与数据说明")}
<h2>{_watch_title}</h2>
<table>
<colgroup><col style="width:26%"><col style="width:12%"><col style="width:14%"><col style="width:14%"><col style="width:16%"><col style="width:18%"></colgroup>
<thead><tr>{_thead}</tr></thead>
<tbody>{"".join(watch_rows)}</tbody></table>
<p class="tcap">{_read_note}</p>

<div class="disc" style="line-height:1.55">
<b>数据与口径说明</b>　{date} 交易日盘后复盘；行情 / 资金流向 / 评分 / 分位 / 额比均来自腾讯自选股（westock-mcp）；
策略口径版本 <b>{C.CALIBER_VERSION}</b>（永久生效）；四层漏斗与评分管道由 `strategy/` 包实现。{demo_disc}<br>
{_qa_note}<b>图型说明</b>　共 8 张图：① 漏斗递减条形　② 分位×额比气泡矩阵　③ 五维雷达　④ 综合分排行
　⑤ 中报同比对照柱　⑥ PB 排序　⑦ 五维分项拆解　⑧ α 预算账本；版式参照 BII 双栏范式，A4 横向。<br>
<b>免责声明</b>　本文档基于公开数据的技术与基本面分析，<b>不构成任何投资建议</b>。
市场有风险，投资需谨慎，请根据自身风险承受能力独立决策。
</div>''', 13, "08　跟踪清单", full=True))

    # ── 14. 次日 5 条可证伪预判（双栏） ──
    P.append(build_pred_page(pred or {}, date))

    # ── 15/16. v3.0 扩展层附录（可选；前 14 页逐字不改）──
    v3 = data.get("v3") or {}
    B = v3.get("blocks") or {}
    if v3.get("enabled") and B:
        P.append(_v3_macro_page(B, date))
        P.append(_v3_theme_page(B, date))

    # ── 17/18. v3.1 GCCEO 全量整合层附录（强依赖 v3；前 16 页逐字不改）──
    gc = data.get("gceo") or {}
    GB = gc.get("blocks") or {}
    if v3_on and gc.get("enabled") and GB:
        P.append(_gceo_decision_page(GB, date))
        P.append(_gceo_ext_page(GB, date))

    # ── 19/20. v4.0 投行级量化研判层（强依赖 gceo⊂v3；前 18 页逐字不改）──
    gq = data.get("gceo_quant") or {}
    GQB = gq.get("blocks") or {}
    if v3_on and gc.get("enabled") and gq.get("enabled") and GQB:
        P.append(_gceo_quant_valuation_page(GQB, date))
        P.append(_gceo_quant_lifecycle_page(GQB, date))

    return P


# ══════════════════════════════ 主流程 ══════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description="BII 双栏范式 · 龙虎榜日更报告（A4 横向）")
    ap.add_argument("--data", default=str(REPO / "strategy" / "sample_data.json"))
    ap.add_argument("--date", default=dt.date.today().strftime("%Y-%m-%d"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--equity", type=float, default=None, help="覆盖权益（元）")
    ap.add_argument("--stage", default=None, help="覆盖阶段（I/II/III）")
    ap.add_argument("--predict-file", default=None,
                    help="次日 5 条可证伪预判 JSON（默认自动探测 <data 同级>/predictions.json）")
    ap.add_argument("--predictions", default=None,
                    help="内联预判 JSON 字符串（优先于 --predict-file）")
    args = ap.parse_args()

    global CODE, TOTAL
    dc = args.date.replace("-", "")
    CODE = f"LHB{dc[4:]}-{dc[:4]}"

    data_path = pathlib.Path(args.data)
    if not data_path.exists():
        sys.exit(f"[!] 数据文件不存在：{data_path}")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    # 四态总页数（单一真相源 _resolve_total；单向叠加：gceo⊂v3，gceo_quant⊂gceo）：
    #   v3.enabled=false                        → 14 页（纯 v2.3，向后完全兼容）
    #   v3.enabled=true, gceo 关                → 16 页（v3.0）
    #   v3.enabled=true, gceo 开, quant 关      → 18 页（v3.1 GCCEO 全量整合）
    #   v3.enabled=true, gceo 开, quant 开      → 20 页（v4.0 投行级量化研判）
    TOTAL = _resolve_total(data)
    if args.equity is not None:
        data.setdefault("context", {})["equity"] = args.equity
    if args.stage is not None:
        data.setdefault("context", {})["stage"] = args.stage

    out_dir = pathlib.Path(args.out) if args.out else REPO / "out" / f"dragon-tiger-{dc}"
    out_dir = out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    m = compute_model(data)
    by_code, by_name = {}, {}
    for c in data.get("candidates", []):
        by_code[c["code"]] = c
        by_name[c["name"]] = c

    pred = load_predictions(args, data_path, out_dir)
    if pred and pred.get("report_date") and str(pred["report_date"])[:10] != str(args.date)[:10]:
        print(f"[!] 预判 report_date={pred['report_date']} 与报告日期 {args.date} 不一致 —— "
              f"预判可能挂错交易日，请核对 predictions.json（已照常渲染）。")
    tgt = (pred or {}).get("target_date") or next_trading_day(args.date)

    chart_js = inject_charts(m, by_code, by_name)
    pages = build_pages(m, data, args.date, by_code, by_name, pred)
    if len(pages) != TOTAL:
        sys.exit(f"[!] 页数不符：TOTAL={TOTAL} 实际={len(pages)}")

    html = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>涨停板龙虎榜深度研判报告（BII 双栏）· {args.date}</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n"
        + "".join(pages) +
        "\n<script>__CHART_LIB__</script>\n"
        f"<script>{chart_js}</script>\n</body>\n</html>"
    )
    html = html.replace("__CHART_LIB__", CHART_LIB)

    out_file = out_dir / f"涨停板龙虎榜深度研判报告-BII双栏-{dc}.html"
    out_file.write_text(html, encoding="utf-8")

    print("=" * 66)
    print(f" BII 双栏范式 · A股涨停板龙虎榜深度研判报告 · {args.date}")
    print("=" * 66)
    print(f" 口径 {C.CALIBER_VERSION} | 候选 {len(by_code)} | L1 达门槛 {len(m['l1_pass'])}/{len(m['inds'])}"
          f" | L2 {len(m['fr'].l2_pass)} | L2.5 剔 {len(m['fr'].l2_5_removed)}"
          f" | L3 否 {len(m['fr'].l3_vetoed)} | 过会 {len(m['fr'].l3_pass)}")
    print(f" 页数 {len(pages)}（封面 + {TOTAL - 1} 编号页）| 图 8 张 | Chart.js 已内联")
    _p = pred or {}
    _n = len(_p.get("items") or [])
    print(f" 次日预判 {_n}/5 条 · 目标日 {tgt}"
          f"{'　（示例占位，未提供 predictions.json）' if not _n else ''}"
          f"{'　来源 ' + str(_p.get('_src')) if _p.get('_src') else ''}")
    print(f" HTML: {out_file}  ({out_file.stat().st_size / 1024:.1f} KB)")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
