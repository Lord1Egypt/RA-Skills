"""市场数据：全球/中国规模与融资默认值、Chart.js 数据构建、本周市场信号与趋势洞察桥接。

从 generate_site.py 抽出（P1#1 Phase 2）。
- 国内数据单位为亿元人民币，全球为十亿美元；均为**静态快照**，随 `--data-snapshot` 标注截止日。
- `_extract_market_signals` / `_render_trend_insights_html` 负责「宏观图 ↔ 本周新闻」的桥接
  （计划第九章 M1/M2），全部服务端预渲染进静态 HTML，禁 JS 也可见。

快照外置（HON-2）：快照的读取、兜底常量与过期判定已拆到 `market_snapshot.py`
（该模块是 `_SNAPSHOT` 的唯一真身，本文件按属性读它）。拿不到快照文件时会回退
`_FALLBACK_*` 并把 `snapshot_stale()` 置True，页面显式标注「已过期」，绝不静默用旧数。
"""
from __future__ import annotations

import html
import json
import re
from datetime import date, datetime

from aiweekly.leaderboard import _collect_leaderboard_models
from aiweekly.market_snapshot import (
    SNAPSHOT_PATH,
    SNAPSHOT_STALE_DAYS,
    load_snapshot,
    snapshot_age_days,
    snapshot_stale,
    snapshot_status_text,
    run_snapshot_check,
)
from aiweekly.market_snapshot import (
    _FALLBACK_CN_CONCENTRATION_DATA,
    _FALLBACK_CN_CONCENTRATION_LABELS,
    _FALLBACK_CN_FUNDING_DATA,
    _FALLBACK_CN_FUNDING_LABELS,
    _FALLBACK_CN_FUNDING_SOURCE,
    _FALLBACK_CN_MARKET_DATA,
    _FALLBACK_CN_MARKET_LABELS,
    _FALLBACK_CN_MARKET_SOURCE,
    _FALLBACK_CN_STRUCTURE_DATA,
    _FALLBACK_CN_STRUCTURE_LABELS,
    _FALLBACK_FUNDING_DATA,
    _FALLBACK_FUNDING_LABELS,
    _FALLBACK_FUNDING_SOURCE,
    _FALLBACK_MARKET_DATA,
    _FALLBACK_MARKET_LABELS,
    _FALLBACK_MARKET_SOURCE,
    _FALLBACK_NOTE,
    _FALLBACK_SOURCES,
    _labels_values,
)
from aiweekly.utils import safe_href

# 快照状态的真身模块。必须以**模块对象**持有并按属性读`_SNAPSHOT`，
# 不可 `from ... import _SNAPSHOT`（那是值拷贝：调用方改真身后本模块仍读旧值）。
from aiweekly import market_snapshot as _snapshot_mod


def _e(v, quote: bool = False) -> str:
    """转义**外部可控**字段后拼进 HTML。

    与裸 ``html.escape`` 的区别：``None`` 归一为空串。
    信号字段（amount / bridge_* / source 等）来自 RSS 解析，缺字段时为 ``None``，
    裸转义会抛 ``AttributeError`` 把整期报告打挂；原实现直接插值只是渲染出 "None"。
    安全修复不应引入新的崩溃路径，故统一走这里。

    ``quote=True`` 用于**属性值**上下文（如 ``class="ms-type t-{...}"``），
    额外转义引号，避免值里含 ``"`` 时提前闭合属性。
    """
    return html.escape("" if v is None else str(v), quote=quote)


def _js_json(obj) -> str:
    """序列化 JSON 供 <script> 上下文内联（图表 labels/data 来自 CLI 用户可控字符串）。

    转义 < > & 为 \\u003c / \\u003e / \\u0026，阻止 </script> 突破脚本块（防 XSS，对应审查 L4）。
    ensure_ascii=False 保留中文可读性；数值/布尔/None 序列化不受影响。
    """
    return (json.dumps(obj, ensure_ascii=False)
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("&", "\\u0026"))




__all__ = [
    "DEFAULT_MARKET_LABELS", "DEFAULT_MARKET_DATA", "DEFAULT_FUNDING_LABELS", "DEFAULT_FUNDING_DATA",
    "DEFAULT_CN_MARKET_LABELS", "DEFAULT_CN_MARKET_DATA", "DEFAULT_CN_FUNDING_LABELS", "DEFAULT_CN_FUNDING_DATA",
    "DEFAULT_CN_STRUCTURE_LABELS", "DEFAULT_CN_STRUCTURE_DATA", "DEFAULT_CN_CONCENTRATION_LABELS", "DEFAULT_CN_CONCENTRATION_DATA",
    "DEFAULT_MARKET_SOURCE", "DEFAULT_FUNDING_SOURCE", "DEFAULT_CN_MARKET_SOURCE", "DEFAULT_CN_FUNDING_SOURCE",
    "ESTIMATE_NOTE", "build_charts", "BASE_SOURCES", "SIGNAL_WEIGHTS",
    "MODEL_HINTS", "CN_HINTS", "AMOUNT_RE", "_extract_market_signals",
    "_compute_weekly_stats", "_lb_name_map", "_render_market_signals_html", "TREND_INSIGHTS",
    "_match_insight_evidence", "_signal_theme", "_render_trend_insights_html", "_render_market_signals_html_with_theme",
    "SNAPSHOT_PATH", "SNAPSHOT_STALE_DAYS", "load_snapshot", "snapshot_stale",
    "snapshot_status_text", "run_snapshot_check",
]


# 模块加载：一次即可，后面的常量都从它派生
load_snapshot()

_m_labels, _m_values = _labels_values("market", _FALLBACK_MARKET_LABELS, _FALLBACK_MARKET_DATA)
_f_labels, _f_values = _labels_values("funding", _FALLBACK_FUNDING_LABELS, _FALLBACK_FUNDING_DATA)
_cm_labels, _cm_values = _labels_values("cn_market", _FALLBACK_CN_MARKET_LABELS, _FALLBACK_CN_MARKET_DATA)
_cf_labels, _cf_values = _labels_values("cn_funding", _FALLBACK_CN_FUNDING_LABELS, _FALLBACK_CN_FUNDING_DATA)
_cs_labels, _cs_values = _labels_values("cn_structure", _FALLBACK_CN_STRUCTURE_LABELS, _FALLBACK_CN_STRUCTURE_DATA)
_cc_labels, _cc_values = _labels_values("cn_concentration", _FALLBACK_CN_CONCENTRATION_LABELS,
                                       _FALLBACK_CN_CONCENTRATION_DATA)

# 图表默认值（未通过 CLI 提供真实数据时使用）。取自快照文件，缺失时回退 _FALLBACK_*。
DEFAULT_MARKET_LABELS = _m_labels
DEFAULT_MARKET_DATA = _m_values
DEFAULT_FUNDING_LABELS = _f_labels
DEFAULT_FUNDING_DATA = _f_values
DEFAULT_CN_MARKET_LABELS = _cm_labels
DEFAULT_CN_MARKET_DATA = _cm_values
DEFAULT_CN_FUNDING_LABELS = _cf_labels
DEFAULT_CN_FUNDING_DATA = _cf_values
DEFAULT_CN_STRUCTURE_LABELS = _cs_labels
DEFAULT_CN_STRUCTURE_DATA = _cs_values
DEFAULT_CN_CONCENTRATION_LABELS = _cc_labels
DEFAULT_CN_CONCENTRATION_DATA = _cc_values

# 图来源署名：取快照的 chart_sources；过期时统一追加显式标注
_stale_note = snapshot_status_text()
_chart_sources = _snapshot_mod._SNAPSHOT.get("chart_sources", {})
DEFAULT_MARKET_SOURCE = _chart_sources.get(
    "market", _FALLBACK_MARKET_SOURCE) + _stale_note
DEFAULT_FUNDING_SOURCE = _chart_sources.get(
    "funding", _FALLBACK_FUNDING_SOURCE) + _stale_note
DEFAULT_CN_MARKET_SOURCE = _chart_sources.get(
    "cn_market", _FALLBACK_CN_MARKET_SOURCE) + _stale_note
DEFAULT_CN_FUNDING_SOURCE = _chart_sources.get(
    "cn_funding", _FALLBACK_CN_FUNDING_SOURCE) + _stale_note
# 兜底免责（已不再默认触发；表述改为诚实的「静态快照」而非「示例/估算」）
ESTIMATE_NOTE = "数据快照（静态，非实时）"

def build_market_routing_note(region: str = "auto") -> str:
    """市场数据「口径路由」提示条（服务端预渲染，禁 JS 也可见）。

    国内适配性：国内用户应优先采信国内口径（信通院 / IT桔子，可自行核对），
    全球口径来自海外机构静态快照，作趋势对照而非主口径——这点必须说清楚，
    否则读者会误以为两套数字同等可靠。
    region 取白名单值，避免任何注入面。
    """
    if region == "cn":
        lead = "🇨🇳 当前口径：国内优先"
        body = ("中国口径（中国信通院·中商产业研究院 / 新浪创投Plus / IT桔子）为主——"
                "均为国内公开数据，可自行核对；全球口径（Grand View Research / Crunchbase）"
                "属海外机构静态快照，仅作趋势对照，国内无法一手核实。")
    elif region == "global":
        lead = "🌍 当前口径：全球为主"
        body = ("全球口径（Grand View Research / Crunchbase）为主；"
                "中国口径（信通院 / IT桔子）作区域对照。两者均为静态快照，非实时数据。")
    else:
        lead = "📊 两套口径并列"
        body = ("同一指标给出全球与中国两套口径，来源与快照日期见每张图下方。"
                "均为静态快照而非实时数据，引用前请核对快照日期。")
    return f'<div class="market-routing"><b>{lead}</b> — {body}</div>'


def resolve_chart_data(market_data=None, market_labels=None,
                       funding_data=None, funding_labels=None,
                       cn_market_data=None, cn_market_labels=None,
                       cn_funding_data=None, cn_funding_labels=None,
                       cn_structure_data=None, cn_structure_labels=None,
                       cn_concentration_data=None, cn_concentration_labels=None) -> dict:
    """把 6 张市场图的序列与标签统一解析（None 回退到标注清晰的默认/估算值）。

    单一事实源：Chart.js 轨（`build_charts`）与服务端 SVG 轨（`charts_svg.build_svg_charts`）
    都从这里取数，避免两轨默认值各写一份、日后漂移不一致。
    """
    return {
        "market": {"labels": market_labels or DEFAULT_MARKET_LABELS,
                   "values": market_data or DEFAULT_MARKET_DATA},
        "funding": {"labels": funding_labels or DEFAULT_FUNDING_LABELS,
                    "values": funding_data or DEFAULT_FUNDING_DATA},
        "cn_market": {"labels": cn_market_labels or DEFAULT_CN_MARKET_LABELS,
                      "values": cn_market_data or DEFAULT_CN_MARKET_DATA},
        "cn_funding": {"labels": cn_funding_labels or DEFAULT_CN_FUNDING_LABELS,
                       "values": cn_funding_data or DEFAULT_CN_FUNDING_DATA},
        "cn_structure": {"labels": cn_structure_labels or DEFAULT_CN_STRUCTURE_LABELS,
                         "values": cn_structure_data or DEFAULT_CN_STRUCTURE_DATA},
        "cn_concentration": {"labels": cn_concentration_labels or DEFAULT_CN_CONCENTRATION_LABELS,
                             "values": cn_concentration_data or DEFAULT_CN_CONCENTRATION_DATA},
    }


def build_charts(market_data=None, market_labels=None,
                 funding_data=None, funding_labels=None,
                 cn_market_data=None, cn_market_labels=None,
                 cn_funding_data=None, cn_funding_labels=None,
                 cn_structure_data=None, cn_structure_labels=None,
                 cn_concentration_data=None, cn_concentration_labels=None) -> str:
    """生成 Chart.js 初始化代码。未提供真实数据时回退到标注清晰的估算值。
    支持全球(Global)与中国(CN)双来源：每类含市场规模与融资趋势，各自独立来源。
    M2：中国融资补 2026H1 当期点，并新增「赛道结构」与「头部集中度」两张分析图。"""
    _d = resolve_chart_data(
        market_data, market_labels, funding_data, funding_labels,
        cn_market_data, cn_market_labels, cn_funding_data, cn_funding_labels,
        cn_structure_data, cn_structure_labels,
        cn_concentration_data, cn_concentration_labels)
    m_data, m_labels = _d["market"]["values"], _d["market"]["labels"]
    f_data, f_labels = _d["funding"]["values"], _d["funding"]["labels"]
    cm_data, cm_labels = _d["cn_market"]["values"], _d["cn_market"]["labels"]
    cf_data, cf_labels = _d["cn_funding"]["values"], _d["cn_funding"]["labels"]
    cs_data, cs_labels = _d["cn_structure"]["values"], _d["cn_structure"]["labels"]
    cc_data, cc_labels = _d["cn_concentration"]["values"], _d["cn_concentration"]["labels"]
    return f"""
// Market size chart（M3 #11：实测 vs CAGR 外推 诚实区分）
const marketCtx = document.getElementById('marketSizeChart').getContext('2d');
// 标签以 F 结尾视为「预测/外推」（如 2027F/2028F），浅色虚线感；其余为实测/机构估算，实色
const marketIsForecast = {_js_json([(l.strip().endswith('F')) for l in m_labels])};
const marketBarColors = marketIsForecast.map(f => f ? 'rgba(37,99,235,0.32)' : 'rgba(37,99,235,0.7)');
const marketBarBorders = marketIsForecast.map(f => f ? 'rgba(37,99,235,0.6)' : 'rgba(37,99,235,1)');
marketChart = new Chart(marketCtx, {{
  type: 'bar',
  data: {{
    labels: {_js_json(m_labels)},
    datasets: [{{
      label: '市场规模（$B，约 ¥7.2/$）',
      data: {_js_json(m_data)},
      backgroundColor: marketBarColors,
      borderColor: marketBarBorders,
      borderWidth: 1, borderRadius: 6,
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: c => {{
        const f = marketIsForecast[c.dataIndex];
        return '$'+c.parsed.y+'B' + (f ? '（CAGR 外推，非实测）' : '（实测/机构估算）');
      }} }} }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b' }} }},
      y: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => '$'+v+'B' }} }}
    }}
  }}
}});

// Funding trend chart
const fundCtx = document.getElementById('fundingChart').getContext('2d');
fundingChart = new Chart(fundCtx, {{
  type: 'line',
  data: {{
    labels: {_js_json(f_labels)},
    datasets: [{{
      label: '融资额（$B，约 ¥7.2/$）',
      data: {_js_json(f_data)},
      borderColor: 'rgba(124,58,237,1)',
      backgroundColor: 'rgba(124,58,237,0.1)',
      fill: true, tension: 0.3,
      pointRadius: 4, pointBackgroundColor: 'rgba(124,58,237,1)',
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b' }} }},
      y: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => '$'+v+'B' }} }}
    }}
  }}
}});

// --- 中国 AI 核心产业规模（亿元，RMB）--- M3 #10：叠加 YoY% 折线
const cnMarketCtx = document.getElementById('cnMarketChart').getContext('2d');
// 由数据自动算同比：第 i 年 = data[i]/data[i-1]-1（首年无）
const cnYoY = {_js_json([None] + [round((cm_data[i]/cm_data[i-1]-1)*100, 1) for i in range(1, len(cm_data))])};
cnMarketChart = new Chart(cnMarketCtx, {{
  type: 'bar',
  data: {{
    labels: {_js_json(cm_labels)},
    datasets: [
      {{
        label: '核心产业规模（亿元，RMB）',
        data: {_js_json(cm_data)},
        backgroundColor: 'rgba(220,38,38,0.7)',
        borderColor: 'rgba(220,38,38,1)',
        borderWidth: 1, borderRadius: 6,
        yAxisID: 'y',
        order: 2,
      }},
      {{
        label: '同比增速 YoY（%）',
        data: cnYoY,
        type: 'line',
        borderColor: 'rgba(22,163,74,1)',
        backgroundColor: 'rgba(22,163,74,1)',
        borderWidth: 2, tension: 0.3,
        pointRadius: 4, pointBackgroundColor: 'rgba(22,163,74,1)',
        yAxisID: 'y2',
        order: 1,
      }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: true, labels: {{ color: '#64748b', boxWidth: 12, font: {{ size: 11 }} }} }},
      tooltip: {{ callbacks: {{ label: c => {{
        if (c.dataset.yAxisID === 'y2') {{
          return c.parsed.y == null ? 'YoY：—' : 'YoY：+'+c.parsed.y+'%';
        }}
        return c.parsed.y+'亿（RMB）' + (cnYoY[c.dataIndex] != null ? '  同比 +'+cnYoY[c.dataIndex]+'%' : '');
      }} }} }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b' }} }},
      y: {{ position: 'left', grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => v+'亿' }} }},
      y2: {{ position: 'right', grid: {{ display: false }}, ticks: {{ color: '#16a34a', callback: v => v+'%' }}, suggestedMin: 0 }}
    }}
  }}
}});

// --- 中国 AI 融资趋势（亿元，RMB，年度）---
const cnFundCtx = document.getElementById('cnFundingChart').getContext('2d');
cnFundingChart = new Chart(cnFundCtx, {{
  type: 'line',
  data: {{
    labels: {_js_json(cf_labels)},
    datasets: [{{
      label: '融资额（亿元，RMB）',
      data: {_js_json(cf_data)},
      borderColor: 'rgba(220,38,38,1)',
      backgroundColor: 'rgba(220,38,38,0.1)',
      fill: true, tension: 0.3,
      pointRadius: 4, pointBackgroundColor: 'rgba(220,38,38,1)',
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b' }} }},
      y: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => v+'亿' }} }}
    }}
  }}
}});

// --- 中国 2026H1 AI 融资赛道结构（亿元，RMB）--- M2 #7
const cnStructCtx = document.getElementById('cnStructureChart').getContext('2d');
cnStructureChart = new Chart(cnStructCtx, {{
  type: 'bar',
  data: {{
    labels: {_js_json(cs_labels)},
    datasets: [{{
      label: '融资额（亿元，RMB）',
      data: {_js_json(cs_data)},
      backgroundColor: ['rgba(220,38,38,0.78)','rgba(234,88,12,0.78)','rgba(217,119,6,0.78)','rgba(100,116,139,0.78)'],
      borderRadius: 6,
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: c => c.parsed.x + ' 亿（RMB）' }} }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => v+'亿' }} }},
      y: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b' }} }}
    }}
  }}
}});

// --- 中国 AI 融资头部集中度（亿元，RMB）--- M2 #9
const cnConcCtx = document.getElementById('cnConcentrationChart').getContext('2d');
cnConcentrationChart = new Chart(cnConcCtx, {{
  type: 'bar',
  data: {{
    labels: {_js_json(cc_labels)},
    datasets: [{{
      label: '融资额（亿元，RMB）',
      data: {_js_json(cc_data)},
      backgroundColor: ['rgba(220,38,38,0.85)','rgba(234,88,12,0.7)','rgba(148,163,184,0.7)'],
      borderRadius: 6,
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: c => c.parsed.x + ' 亿（占 3076 亿的 ' + (c.parsed.x/3076.82*100).toFixed(1) + '%）' }} }} }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(0,0,0,0.06)' }}, ticks: {{ color: '#64748b', callback: v => v+'亿' }} }},
      y: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b' }} }}
    }}
  }}
}});
"""

# 页脚「静态快照引用」署名名单 —— 数据来自 assets/market_snapshot.json 的 sources。
#
# 诚实性约定（HON-1/HON-2）：这一组是**人工誊录的静态基线**，不是本周抓取结果。
# 曾经此处的 8 家被渲染成与真实来源混排的「数据来源」，读者会误以为数据来自它们，
# 而全仓从未抓取过其中任何一家。现改为：
#   * 每家带 retrieved_at（誊录时间）与 used_for（被哪张图引用）；
#   * used_for 为空者在渲染层标注「未引用」，不再与真正被引用的机构混为一谈。
# 保留 Stanford HAI / LMMarketCap 两个条目是为了不擅自丢弃用户可能想用的署名，
# 但它们在快照里已显式标注为「未引用任何数字」——见 snapshot.json 的 uncited_reason。
def _load_base_sources() -> list:
    """从快照取署名名单；快照不可用时回退 _FALLBACK_SOURCES（并由 stale 标注兜住）。"""
    items = []
    # 按属性读真身，使「调用方改了 market_snapshot._SNAPSHOT 后立刻重建 BASE_SOURCES」
    # 生效（回归测试test_snapshot_block_rejects_unsafe_url 依赖这一点）。
    snapshot = _snapshot_mod._SNAPSHOT
    for s in snapshot.get("sources", []):
        if not isinstance(s, dict):
            continue
        name = (s.get("name") or "").strip()
        if not name:
            continue
        items.append({
            "name": name,
            "url": (s.get("url") or "").strip(),
            "used_for": (s.get("used_for") or "").strip(),
            "retrieved_at": (s.get("retrieved_at") or snapshot.get("retrieved_at") or "").strip(),
        })
    if items:
        return items
    return [{"name": n, "url": u, "used_for": uf, "retrieved_at": ""}
            for n, u, uf in _FALLBACK_SOURCES]


BASE_SOURCES = _load_base_sources()


# ============ M1：本周市场信号（新闻 ↔ 宏观图 桥接）============
# 从本周新闻抽取融资 / 并购 / IPO / 大额融资轮 / 模型发布事件，做成「关于本周」的桥接卡，
# 让市场板块不再只是静态宏观百科，而是真正呼应本周发生的事（计划第九章 M1 #4/#5/#6）。
SIGNAL_WEIGHTS = {
    "融资": [("融资", 3), ("募资", 3), ("轮融资", 3), ("融资轮", 3),
             ("funding", 3), ("raised", 3), ("raise", 2), ("round", 2)],
    "并购": [("收购", 3), ("并购", 3), ("acqui", 3), ("merger", 3)],
    "IPO": [("ipo", 3), ("招股", 3), ("敲钟", 3), ("上市", 2)],
    "估值": [("估值", 2), ("valuation", 2), ("独角兽", 3), ("unicorn", 3)],
    "模型发布": [("新模型", 2), ("模型发布", 2), ("发布模型", 2)],
}
# 模型发布类信号词（须与「模型」同现才计入，避免「发布报告」误触发）
MODEL_HINTS = ["发布", "推出", "开源", "上线"]
# 中国 / 国内机构或币种关键词 -> 桥接到中国融资图
CN_HINTS = ["中国", "国内", "人民币", "亿元", "阿里", "腾讯", "字节", "月之暗面", "kimi",
            "deepseek", "阶跃", "智谱", "百度", "商汤", "科大讯飞", "minimax", "百川",
            "零一万物", "蚂蚁", "华为", "美团", "京东"]
AMOUNT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(亿美金|亿美元|亿人民币|亿元人民币|亿元|亿|万美金|万美元|万元|万|"
    r"trillion|billion|\bn\b|\$b|\$\s*\d[\d.,]*\s*(?:b|bn|k|m)?)", re.I)


def _extract_market_signals(news_items, top_n=5):
    """从本周新闻抽取资本 / 模型发布信号，按信号强度打分取 Top N。

    返回每条：title / url / source / amount / types[] / bridge_label / bridge_region / score。
    桥接目标：中国机构或币种 -> 中国融资趋势；并购/IPO -> 全球融资趋势；纯模型发布 -> 能力榜。
    """
    signals = []
    for it in news_items:
        title = it.get("title", "") or ""
        summary = it.get("summary", "") or ""
        text = f"{title} {summary}"
        low = text.lower()
        score = 0
        types = set()
        for t, kws in SIGNAL_WEIGHTS.items():
            for kw, w in kws:
                if kw.lower() in low:
                    score += w
                    types.add(t)
        # 模型发布须与「模型」同现
        if "模型" in low and any(h in low for h in MODEL_HINTS):
            score += 2
            types.add("模型发布")
        if score < 2:
            continue
        am = AMOUNT_RE.search(text)
        amount = am.group(0).strip() if am else ""
        is_cn = any(h.lower() in low for h in CN_HINTS)
        if "并购" in types or "IPO" in types:
            bridge = ("全球融资趋势", "🌍 全球")
        elif is_cn:
            bridge = ("中国融资趋势", "🇨🇳 中国")
        elif types == {"模型发布"}:
            bridge = ("大模型排行榜", "🏆 能力榜")
        else:
            bridge = ("全球融资趋势", "🌍 全球")
        signals.append({
            "title": title,
            "url": it.get("url", "") or "",
            "source": it.get("source", "") or "",
            "lang": it.get("lang", "") or "",
            "cn_summary": it.get("cn_summary", "") or "",
            "amount": amount,
            "types": sorted(types),
            "bridge_label": bridge[0],
            "bridge_region": bridge[1],
            "score": score + (it.get("score", 0) or 0) * 0.1,
        })
    signals.sort(key=lambda x: x["score"], reverse=True)
    return signals[:top_n]


def _compute_weekly_stats(news_items, market_signals, leaderboard_data):
    """聚合「本周数字看板」：新闻总量 / 国内外比 / 模型相关+新发布 / 融资&发布事件 / 在榜模型数 / 必读 Top3。

    - news_items 已含 mustRead / score / category / lang / title / url
    - market_signals 来自 _extract_market_signals（types 标记融资/并购/IPO/模型发布）
    - 全部为派生指标，不引入新外部数据源；失败场景（空数据）兜底返回零值结构。
    """
    items = news_items or []
    sigs = market_signals or []
    total = len(items)
    zh = sum(1 for n in items if n.get("lang") == "zh")
    en = total - zh
    # 兼容 ai-models / model 两种历史 category 写法
    _MODEL_CATS = {"ai-models", "model"}
    model_news = [n for n in items if n.get("category") in _MODEL_CATS]
    _rel_re = re.compile(r"发布|推出|开源|上线|preview|launch|released|open.?source", re.I)
    releases = [
        n for n in model_news
        if _rel_re.search(f"{n.get('title','')} {n.get('summary','')}")
    ]
    fund_events = [
        s for s in sigs
        if s.get("types") and (
            set(s.get("types", [])) & {"融资", "并购", "IPO", "模型发布"}
            or s.get("amount")
        )
    ]
    must = sorted(
        [n for n in items if n.get("mustRead")],
        key=lambda x: x.get("score", 0) or 0,
        reverse=True,
    )[:3]
    lb_models = _collect_leaderboard_models(leaderboard_data)
    return {
        "total": total,
        "zh": zh,
        "en": en,
        "model_news": len(model_news),
        "releases": len(releases),
        "fund_events": len(fund_events),
        "lb_models": len(lb_models),
        "must_read": [
            {"title": (n.get("title") or "").strip(),
             "url": n.get("url") or "#"}
            for n in must
        ],
    }


def _lb_name_map(leaderboard):
    """构建 模型名/机构名(小写) -> (名次, 源) 映射，供资本↔能力联动标注。"""
    m = {}
    if not isinstance(leaderboard, dict):
        return m
    for grp in ("comprehensive", "open_source"):
        block = leaderboard.get(grp, {})
        if not isinstance(block, dict):
            continue
        for src, payload in block.items():
            rows = payload.get("rows", []) if isinstance(payload, dict) else []
            for i, r in enumerate(rows):
                if not isinstance(r, dict):
                    continue
                for key in ("model", "name", "org", "organization"):
                    v = (r.get(key) or "").lower().strip()
                    if v and v not in m:
                        m[v] = (i + 1, src)
    return m


def _render_market_signals_html(signals, lb_map):
    """服务端预渲染「本周市场信号」区块（即使 JS 不执行也可见）。"""
    if not signals:
        return ('<p class="ms-empty">本周新闻中未检出重大融资 / 并购 / IPO / 模型发布事件'
                '——市场板块维持宏观背景视角。</p>')
    cards = []
    for s in signals:
        types_html = " ".join(
            f'<span class="ms-type t-{_e(t, quote=True)}">{_e(t)}</span>' for t in s["types"])
        amt = f'<span class="ms-amount">{_e(s["amount"])}</span>' if s["amount"] else ""
        # 资本↔能力：检测标题是否含上榜模型/机构名
        title_low = s["title"].lower()
        on_lb = None
        for nm, (rk, src) in lb_map.items():
            if nm and nm in title_low:
                on_lb = (rk, src)
                break
        if on_lb:
            cap = f'<span class="ms-cap">↔ 能力榜 #{_e(on_lb[0])}（{_e(on_lb[1])}）</span>'
        else:
            cap = '<span class="ms-cap ms-cap-off">↔ 能力榜：未上榜</span>'
        cards.append(
            f'<div class="ms-card">'
            f'<div class="ms-top">{types_html}{amt}</div>'
            f'<a class="ms-title" href="{safe_href(s["url"])}" target="_blank" rel="noopener">{_e(s["title"])}</a>'
            f'<div class="ms-meta"><span class="ms-bridge">{_e(s["bridge_region"])} ↔ {_e(s["bridge_label"])}</span>'
            f'{cap}<span class="ms-src">{_e(s["source"])}</span></div>'
            f'</div>')
    head = (f'<p class="ms-head">从本周 <b>{len(signals)}</b> 条资本 / 模型发布信号看，'
            f'钱与能力正往这些方向集中（桥接下方宏观图）：</p>')
    return head + '<div class="ms-grid">' + "".join(cards) + '</div>'


# ============ 「AI 行业趋势洞察」×「关于本周」合作（计划第九章 用户议题）============
# 原本「趋势洞察」面板是模板写死的宏观百科，与本周新闻零联动。
# 做法：把 4 条宏观洞察上提到 Python，按周从本周信号 / 新闻抽「本周印证」证据行，
# 让每条宏观趋势都挂着本周真实发生的事；同时给 M1 信号卡加「印证趋势」标签，双向桥接。
TREND_INSIGHTS = [
    {
        "theme": "规模红利",
        "ico": "🌍→🇨🇳",
        "head": "规模：全球高速扩张，中国增速更快",
        "body": "全球 AI 市场 CAGR <b>30.6%</b>（Grand View Research），约每 2.5 年翻番；中国核心产业规模 "
                "<b>9188亿→1.2万亿→1.7万亿</b>（2024→2026E，中国信通院），三年近乎翻倍。",
        "tag": "PM / 开发者：国内仍是增量红利，优先盯本土落地场景",
        "tag_cls": "tag-pm",
        "keys": ["规模", "市场", "增速", "扩张", "信通院", "万亿", "增长", "产业"],
    },
    {
        "theme": "钱去哪了",
        "ico": "💰",
        "head": "钱去哪了：极端头部集中，但结构在变",
        "body": "全球 2026H1 融资 <b>$510B</b> 已超 2025 全年；中国 2026H1 AI 融资 <b>3076 亿</b>"
                "（占一级市场 48.6%），但 TOP3 大模型（DeepSeek/阶跃/Kimi）独揽 930 亿（30%），"
                "TOP30 超 1700 亿（过半）。",
        "tag": "开发者：通用大模型已是巨头决赛圈，别硬刚 base model",
        "tag_cls": "tag-dev",
        "keys": ["融资", "并购", "头部", "集中", "独角兽", "估值", "轮", "募资", "收购", "IPO"],
    },
    {
        "theme": "成本塌方",
        "ico": "💸",
        "head": "成本：推理价格年内腰斩，开源比闭源便宜 5 倍",
        "body": "企业级推理均价从 <b>$2.04</b> 跌到 <b>$1.16–1.18 / M token</b>（年内低点）；"
                "开源 vs 闭源价差约 <b>5 倍</b>（<b>$0.66</b> vs <b>$3.07</b>）。"
                "成本已不是应用落地门槛，瓶颈回到「场景与 PMF」。",
        "tag": "开发者：优先验证场景，别再为「模型太贵」找借口",
        "tag_cls": "tag-dev",
        "keys": ["成本", "降价", "价格", "推理", "GLM", "定价", "开源", "token"],
    },
    {
        "theme": "中国模型出海",
        "ico": "🇨🇳→🌐",
        "head": "势能：中国模型海外调用占比冲到 61%",
        "body": "OpenRouter 上中国模型调用量占比 <b>61%</b>；"
                "Ox Alpha 上线 6 天吃掉 <b>23.2 万亿 token</b> 登顶，"
                "国产模型从「追赶」转向「被全球用」。",
        "tag": "自媒体：国产登顶 / 出海占比 = 高情绪传播选题",
        "tag_cls": "tag-media",
        "keys": ["中国模型", "ox alpha", "openrouter", "出海", "登顶", "占比", "海外"],
    },
    {
        "theme": "具身智能",
        "ico": "🤖",
        "head": "机会窗口：具身智能成第二增长极",
        "body": "中国 2026H1 具身智能（人形机器人）融资 <b>906 亿</b>（29.5%），“七武士”单家超 20 亿；"
                "世界模型成早期第一共识（6 家早期合计 97 亿）；AIGC 应用 596 亿（图片/视频生成最成熟）。"
                "端侧拐点已现：MiniMax H3 移动端 <b>2400 万</b>下载、宇树冲刺 IPO，"
                "具身 / 端侧从 demo 走向规模化收入。",
        "tag": "开发者：现实机会在具身智能、AIGC 应用层、端侧 / 机器人",
        "tag_cls": "tag-dev",
        "keys": ["具身", "机器人", "人形", "AIGC", "应用", "agent", "世界模型", "视频生成", "智能体", "宇树", "minimax", "端侧"],
    },
    {
        "theme": "行动建议",
        "ico": "🎯",
        "head": "给三类读者的行动建议",
        "body": "<b>独立开发者</b>：用开源/免费 API（Hy3、Qwen、DeepSeek）做垂直场景应用。<br>"
                "<b>产品经理</b>：需求在“AI+传统行业”（制造/医疗/金融），用低成本模型验证 PMF。<br>"
                "<b>自媒体</b>：具身智能 + 应用层爆发是 2026 最强叙事，原始口径可向 IT桔子/信通院取。",
        "tag": "媒体：具身智能元年 / 应用层爆发 = 高传播选题",
        "tag_cls": "tag-media",
        "keys": [],  # 行动建议不挂本周印证（它是结论，不是可印证的事实趋势）
    },
]


def _match_insight_evidence(theme_keys, signals, news_items, top_k=2):
    """从本周信号 / 新闻中，为本条宏观趋势抽取「本周印证」证据。

    优先用 M1 信号（已带金额 / 链接），其次用本周新闻标题；按与主题词的重合度打分取 Top-K。
    返回 [{title, url, amount}]。
    """
    if not theme_keys:
        return []
    cands = []
    # 信号优先（已有金额与链接）
    for s in (signals or []):
        t = (s.get("title", "") or "").lower()
        hit = sum(1 for k in theme_keys if k.lower() in t)
        if hit:
            cands.append((hit, s.get("title", ""), s.get("url", "") or "", s.get("amount", "")))
    # 普通新闻补充（仅标题，无金额）
    for it in (news_items or []):
        t = (it.get("title", "") or "").lower()
        hit = sum(1 for k in theme_keys if k.lower() in t)
        if hit:
            cands.append((hit, it.get("title", ""), it.get("url", "") or "", ""))
    # 去重（按标题），按命中数降序
    seen = set()
    uniq = []
    for hit, title, url, amt in sorted(cands, key=lambda x: x[0], reverse=True):
        if not title or title in seen:
            continue
        seen.add(title)
        uniq.append({"title": title, "url": url, "amount": amt})
        if len(uniq) >= top_k:
            break
    return uniq


def _signal_theme(signal):
    """给 M1 信号卡标注它「印证」了哪条宏观趋势（双向桥接）。无匹配返回空串。"""
    t = (signal.get("title", "") or "").lower()
    best, best_hit = "", 0
    for th in TREND_INSIGHTS:
        if not th["keys"]:
            continue
        hit = sum(1 for k in th["keys"] if k.lower() in t)
        if hit > best_hit:
            best_hit, best = hit, th["theme"]
    # 标题无中文关键词命中时，回退到信号类型（融资/并购/IPO → 钱去哪了）
    if best_hit == 0:
        types = signal.get("types", []) or []
        if "并购" in types or "IPO" in types or "融资" in types:
            best = "钱去哪了"
    return best


def _render_trend_insights_html(signals, news_items):
    """服务端预渲染「AI 行业趋势洞察」面板（含本周印证行），注入 [TREND_INSIGHTS] 占位符。"""
    items = []
    for th in TREND_INSIGHTS:
        ev = _match_insight_evidence(th["keys"], signals, news_items)
        if ev:
            ev_parts = []
            for e in ev:
                amt = f' <b>{_e(e["amount"])}</b>' if e["amount"] else ""
                if e["url"]:
                    ev_parts.append(
                        f'<a href="{safe_href(e["url"])}" target="_blank" rel="noopener">{_e(e["title"])}</a>{amt}')
                else:
                    ev_parts.append(f'{_e(e["title"])}{amt}')
            ev_html = (f'<div class="insight-evidence">📌 本周印证：'
                       f'{"；".join(ev_parts)}</div>')
        else:
            ev_html = ""
        items.append(
            f'<div class="insight-item">'
            f'<div class="insight-head"><span class="insight-ico">{th["ico"]}</span>'
            f'<b>{th["head"]}</b></div>'
            f'<p>{th["body"]}</p>'
            f'{ev_html}'
            f'<span class="insight-tag {th["tag_cls"]}">{th["tag"]}</span>'
            f'</div>')
    return '<div class="insight-grid">' + "".join(items) + '</div>'


def _render_market_signals_html_with_theme(signals, lb_map):
    """M1 信号卡渲染（带「印证趋势」标签，与趋势洞察面板双向桥接）。"""
    if not signals:
        return ('<p class="ms-empty">本周新闻中未检出重大融资 / 并购 / IPO / 模型发布事件'
                '——市场板块维持宏观背景视角。</p>')
    cards = []
    for s in signals:
        types_html = " ".join(
            f'<span class="ms-type t-{_e(t, quote=True)}">{_e(t)}</span>' for t in s["types"])
        amt = f'<span class="ms-amount">{_e(s["amount"])}</span>' if s["amount"] else ""
        theme = _signal_theme(s)
        theme_html = (f'<span class="ms-theme">印证趋势：{_e(theme)}</span>'
                      if theme else '<span class="ms-theme ms-theme-off">印证趋势：—</span>')
        title_low = s["title"].lower()
        on_lb = None
        for nm, (rk, src) in lb_map.items():
            if nm and nm in title_low:
                on_lb = (rk, src)
                break
        if on_lb:
            cap = f'<span class="ms-cap">↔ 能力榜 #{_e(on_lb[0])}（{_e(on_lb[1])}）</span>'
        else:
            cap = '<span class="ms-cap ms-cap-off">↔ 能力榜：未上榜</span>'
        # 英文信号卡：补中文注解（与新闻卡一致，方便英文不好的中文读者）
        cn_html = ""
        if s.get("lang") == "en" and s.get("cn_summary"):
            cn_html = (f'<div class="ms-cn"><span class="cn-badge">中文</span> '
                       f'{html.escape(s["cn_summary"])}</div>')
        cards.append(
            f'<div class="ms-card">'
            f'<div class="ms-top">{types_html}{amt}</div>'
            f'<a class="ms-title" href="{safe_href(s["url"])}" target="_blank" rel="noopener">{html.escape(s["title"])}</a>'
            f'{cn_html}'
            f'<div class="ms-meta"><span class="ms-bridge">{_e(s["bridge_region"])} ↔ {_e(s["bridge_label"])}</span>'
            f'{cap}{theme_html}<span class="ms-src">{_e(s["source"])}</span></div>'
            f'</div>')
    head = (f'<p class="ms-head">从本周 <b>{len(signals)}</b> 条资本 / 模型发布信号看，'
            f'钱与能力正往这些方向集中（桥接下方宏观图）：</p>')
    return head + '<div class="ms-grid">' + "".join(cards) + '</div>'

