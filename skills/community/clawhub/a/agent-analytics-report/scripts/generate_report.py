#!/usr/bin/env python3
"""
generate_report.py — Agent 使用情况周报生成器

整合所有数据源，生成多种格式的报告，包含：
  一、概览统计
  二、Token 消耗可视化（含成本货币化）
  三、任务类型统计
  四、任务 Token 消耗统计
  五、技能使用统计
  六、自动化任务运行情况
  七、产出物清单
  八、核心洞察与建议
  九、下周展望

支持输出格式：markdown（默认）、html、json

用法:
  python generate_report.py [data.json] [--days N] [--output report.xxx] [--format markdown|html|json]
"""

import argparse
import html
import json
import math
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 会话标题语义常量与时区统一从 ca_core 导入（单一真相源，避免与 collect_usage_data 漂移）：
#   UNNAMED_LABEL = 本地库有该会话但无标题（真·无标题）
#   ORPHAN_LABEL  = trace 的 session_id 在本地库查不到（孤儿 trace）
from ca_core import (
    TZ,
    UNNAMED_LABEL,
    ORPHAN_LABEL,
    PER_MILLION,
    normalize_model,
    token_active_session_ids,
)
from report_charts import (
    _esc,
    _fmt_inline,
    format_number,
    _disp_width,
    _pad_label,
    _DONUT_PALETTE,
    build_donut_chart,
    build_session_cost_bar_md,
    build_task_type_chart_md,
    _lc_reason,
    build_model_cost_chart_md,
    build_model_cost_chart,
    _lc_bias,
    _lc_arrow,
    _tier_rates_snippet,
)


def _emit_table(rows, columns, fmt, md_sep=None):
    """渲染表格。rows: list[list[str]]；columns: list[str] 表头。
    md_sep: MD 分隔行原样字符串（保留历史手调分隔线，避免 golden diff 回归）。"""
    if fmt == "html":
        out = ["        <table>"]
        out.append(
            "            <tr>"
            + "".join(f"<th>{_esc(c)}</th>" for c in columns)
            + "</tr>"
        )
        for r in rows:
            out.append(
                "            <tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>"
            )
        out.append("        </table>")
        return out
    out = ["| " + " | ".join(columns) + " |"]
    out.append(md_sep if md_sep else "|" + "|".join("------" for _ in columns) + "|")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return out


def _emit_heading(level, text, fmt):
    if fmt == "html":
        return [f"        <h{level}>{_esc(text)}</h{level}>"]
    return ["#" * level + " " + text]


def _emit_note(text, fmt, cls=None):
    """渲染备注块：md 用 `> ` 引用；html 用 <p>（可选 class）。text 用中性内联标记。"""
    if fmt == "html":
        attr = f' class="{cls}"' if cls else ""
        return [f"        <p{attr}>{_fmt_inline(text, 'html')}</p>"]
    return ["> " + text]


def _fmt_generated_at(dt=None):
    """生成时间展示格式：YYYY/MM/DD HH:MM:SS (UTC+08:00)，便于人类阅读。

    旧版曾用 ISO 8601 全精度（含微秒与 +08:00 后缀），对用户不友好；此处改回
    紧凑可读格式，时区以 UTC 偏移呈现（如 UTC+08:00）。
    """
    dt = dt or datetime.now(TZ)
    off = dt.utcoffset() or timedelta(0)
    total = int(off.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    hh, mm = divmod(total // 60, 60)
    tz = f"UTC{sign}{hh:02d}:{mm:02d}"
    return f"{dt.strftime('%Y/%m/%d %H:%M:%S')} ({tz})"


# 时间窗口标签（与 collect_usage_data.PERIOD_* 保持一致）
_PERIOD_LABEL = {
    "day": "日报",
    "week": "周报",
    "month": "月报",
    "year": "年报",
    "custom": "自定义报告",
}
_PERIOD_SHORT = {
    "day": "当日",
    "week": "本周",
    "month": "本月",
    "year": "本年",
    "custom": "本期",
}
_PERIOD_NEXT = {
    "day": "次日",
    "week": "下周",
    "month": "下月",
    "year": "明年",
    "custom": "下期",
}


def _period_labels(meta):
    """根据 meta.period 返回 (整期标签, 本期短标签, 下期短标签)。回退兼容旧数据（无 period 字段）。"""
    key = (meta or {}).get("period", "week")
    return (
        _PERIOD_LABEL.get(key, "周报"),
        _PERIOD_SHORT.get(key, "本周"),
        _PERIOD_NEXT.get(key, "下周"),
    )


def _calendar_period(meta):
    """将报告周期识别为 ISO 8601 日历日期标签。

    - 日报 · 2026-08-01
    - 周报 · 2026-W31（2026-07-27/2026-08-02）
    - 月报 · 2026-08
    - 年报 · 2026
    - 自定义报告 · 2026-07-26/2026-08-01
    """
    meta = meta or {}
    pk = meta.get("period", "week")
    start = meta.get("start_date", "")
    end = meta.get("end_date", "")
    try:
        if pk == "day":
            return f"日报 · {start}" if start else "日报"
        if pk == "week":
            d = datetime.strptime(end, "%Y-%m-%d")
            iso_year, iso_week, _ = d.isocalendar()
            return f"周报 · {iso_year}-W{iso_week:02d}（{start}/{end}）"
        if pk == "month":
            d = datetime.strptime(end, "%Y-%m-%d")
            return f"月报 · {d.year}-{d.month:02d}"
        if pk == "year":
            d = datetime.strptime(end, "%Y-%m-%d")
            return f"年报 · {d.year}"
    except (ValueError, TypeError):
        pass
    return f"自定义报告 · {start}/{end}" if (start or end) else "自定义报告"


def format_file_size(bytes_val):
    """文件大小格式化：B / KB / MB"""
    if bytes_val is None:
        return "0B"
    bytes_val = float(bytes_val)
    if bytes_val >= 1_000_000:
        return f"{bytes_val / 1_000_000:.1f}MB"
    elif bytes_val >= 1_000:
        return f"{bytes_val / 1_000:.1f}KB"
    return f"{int(bytes_val)}B"


def _timed_free_label(model, timed_free_map):
    """限免标签：优先用 pricing.json 里的真实截止日，缺失时退化为不带日期的通用说法。"""
    deadline = (timed_free_map or {}).get(model)
    return f"（限时免费至 {deadline}）" if deadline else "（限时免费）"


# GLM-5.2 家族裸模型名集合（与 collect_usage_data.py 保持一致）：用于 §3.1 合并为「glm-5.2」一行
GLM52_FAMILY = {"glm-5.2", "glm-5.2-x", "glm-5.2x"}


def merge_glm52_family(model_stats):
    """将 GLM-5.2 家族（glm-5.2 / glm-5.2-x / glm-5.2x）合并为「glm-5.2」一行。

    三者是同一官方模型在不同时段的计费形态（白天 0.79x、夜间 0.5x），合并后调用次数与
    计费均为二者之和。保留原排序位置（不再加粗）。
    """
    _fam = [m for m in model_stats if m["model"].strip().lower() in GLM52_FAMILY]
    if not _fam:
        return model_stats
    _idx = next(
        (
            i
            for i, m in enumerate(model_stats)
            if m["model"].strip().lower() in GLM52_FAMILY
        ),
        0,
    )
    _merged = {
        "model": "glm-5.2",
        "calls": sum(m.get("calls", 0) for m in _fam),
        "effective_tokens": sum(m.get("effective_tokens", 0) for m in _fam),
        "effective_cost": sum((m.get("effective_cost", 0) or 0) for m in _fam),
        "input_tokens": sum(m.get("input_tokens", 0) for m in _fam),
        "output_tokens": sum(m.get("output_tokens", 0) for m in _fam),
        "unit_price_input": (_fam[0].get("unit_price_input") or 8.0),
        "unit_price_output": (_fam[0].get("unit_price_output") or 28.0),
        "configured": _fam[0].get("configured", False),
    }
    model_stats = [
        m for m in model_stats if m["model"].strip().lower() not in GLM52_FAMILY
    ]
    model_stats.insert(_idx, _merged)
    return model_stats


def _build_model_block(
    fmt,
    model_stats,
    dim_label=None,
    is_exec=False,
    timed_free_map=None,
    compact=False,
    low_conf_map=None,
    low_conf_bias_map=None,
    hide_cost=False,
):
    """单一维度模型表格 + 洞察（MD / HTML 共用同一套数据计算，仅渲染层不同）。

    compact=True 时仅渲染「模型 / 调用次数 / 实际消耗Token」三列（用于本地模型使用统计，
    因本地推理零成本，单价/花费/占比列无意义）。
    hide_cost=True（tokens_only 计价模式）：等同 compact，且**连「最贵模型 / 高位告警 /
    模型成本图」这些金额结论一起不出**——没有单价时它们只会产出 ¥0.00 与「未配置」，
    读者容易把「没价可算」误读成「免费」。🏆 最常使用模型属调用维度，保留。
    GLM-5.2 家族合并已在调用方通过 merge_glm52_family() 完成。

    low_conf_map 为「成本置信度」配置（模型名 -> 偏差原因）。命中的模型在
    表格里加 ⚠ 标记并在表下说明，且**不参与「最贵模型」结论**（避免拿估算做决策）。
    """
    compact = compact or hide_cost
    configured = [m for m in model_stats if m.get("configured")]
    # 实际产生计费的行（含未配置单价的 auto 路由，其成本来自 trace 级汇总）——用于占比分母与图表
    priced = [m for m in model_stats if (m.get("effective_cost", 0) or 0) > 0]
    total_billable = sum(m.get("effective_cost", 0) for m in priced) or 1
    cost_header = "估算花费＊" if is_exec else "估算实际花费"
    if compact:
        columns = ["模型", "调用次数", "实际消耗Token"]
        md_sep = "|------|---------|-------------|"
    else:
        columns = [
            "模型",
            "调用次数",
            "实际消耗Token",
            "输入单价(元/1M)",
            "输出单价(元/1M)",
            cost_header,
            "占总花费比",
        ]
        md_sep = "|------|---------|-------------|--------------|--------------|------------|-----------|"
    rows = []
    for m in model_stats:
        cfg = m.get("configured")
        mname = m["model"]
        if m.get("is_delisted"):
            mname = f"{m['model']} 🗄️"
        elif m.get("is_local"):
            mname = f"{m['model']} 🔧🏠"
        elif m.get("is_router_api"):
            mname = f"{m['model']} 🔀"
        elif m.get("is_custom"):
            mname = f"{m['model']} 🔧"
        elif is_exec and m.get("is_router"):
            mname = f"{m['model']}（未解析具体模型）"
        elif m.get("timed_free"):
            mname = f"{m['model']}{_timed_free_label(m['model'], timed_free_map)}"
        # 低置信度（估算与实际计费存在已知系统性偏差）——与限免标记可共存
        _lc = _lc_reason(m["model"], low_conf_map)
        if _lc:
            _lc_mark = " " + _lc_arrow(_lc_bias(m["model"], low_conf_bias_map))
            mname = f"{mname}{_lc_mark}"
        eff = m.get("effective_cost", 0) or 0.0
        is_free = (
            cfg and m.get("unit_price_input") == 0 and m.get("unit_price_output") == 0
        )
        if m.get("timed_free"):
            ip = (
                f"{m['unit_price_input']:.2f}"
                if cfg and m.get("unit_price_input")
                else "限时免费"
            )
            op = (
                f"{m['unit_price_output']:.2f}"
                if cfg and m.get("unit_price_output")
                else "限时免费"
            )
            cost = "¥0.00"
        elif is_free:
            ip, op, cost = "免费", "免费", "¥0.00"
        elif eff > 0:
            ip = f"{m['unit_price_input']:.2f}" if cfg else "—"
            op = f"{m['unit_price_output']:.2f}" if cfg else "—"
            cost = f"¥{eff:.2f}"
        elif m.get("is_delisted") and cfg:
            ep = m.get("unit_price_input") or 0.0
            eo = m.get("unit_price_output") or 0.0
            est = (m.get("input_tokens", 0) / PER_MILLION) * ep + (
                m.get("output_tokens", 0) / PER_MILLION
            ) * eo
            eff = est
            ip = f"{ep:.2f}"
            op = f"{eo:.2f}"
            cost = f"¥{est:.2f}"
        else:
            ip = f"{m['unit_price_input']:.2f}" if cfg else "—"
            op = f"{m['unit_price_output']:.2f}" if cfg else "—"
            cost = "已下架·未知" if m.get("is_delisted") else "未配置"
        share = (eff / total_billable * 100) if eff > 0 else 0.0
        share_txt = f"{share:.1f}%" if eff > 0 else "—"
        if compact:
            rows.append(
                [mname, str(m["calls"]), format_number(m.get("effective_tokens", 0))]
            )
        else:
            rows.append(
                [
                    mname,
                    str(m["calls"]),
                    format_number(m.get("effective_tokens", 0)),
                    ip,
                    op,
                    cost,
                    share_txt,
                ]
            )
    out = []
    if fmt == "md":
        if dim_label:
            out.append(f"**{dim_label}**")
            out.append("")
        out.extend(_emit_table(rows, columns, "md", md_sep=md_sep))
        out.append("")
    else:
        out.extend(_emit_table(rows, columns, "html"))

    # 备注 / 免责声明（MD 用引用块，HTML 用 <p>）
    # tokens_only 模式下整段跳过：这些备注解释的全是「单价准不准、花费算不算账单」，
    # 金额维度缺席时留着只会自问自答。
    def _note(text, cls=None):
        return [] if hide_cost else _emit_note(text, fmt, cls=cls)

    if is_exec:
        _ie = (
            "＊本表为**使用量分布估算（非计费口径）**：已解析具体模型的调用按其真实单价估算；"
            "未能解析具体模型的调用（路由别名 `auto`）按本周期计费模型均价估算。"
            "**本表总额不代表真实账单，且不可与 3.1 相加**。"
        )
        out.extend(_note(_ie, "disclaimer" if fmt == "html" else None))
    if any(m.get("is_router") for m in model_stats):
        out.extend(
            _note(
                "ℹ️ `auto` / `fast-model` / `balanced-model` / `extreme-model` 等路由别名（含三档）执行时"
                "**不记录落到哪个底层模型**，报告无法解析其真实模型，故单独成组、**不计入「最贵模型」与省钱建议等成本结论**；"
                "其「单价 / 花费」为所有计费模型（单价>0）的**均价估算值**，仅供横向对比参考。"
            )
        )
    if any(m.get("is_delisted") for m in model_stats):
        out.extend(
            _note(
                "🗄️ = 曾在 WorkBuddy 提供、现已下架的官方模型；历史调用仍正常统计与计价，单价未知者不计入成本。"
            )
        )
    if any(m.get("is_local") for m in model_stats):
        out.extend(
            _note(
                "🔧🏠 = 你通过 Ollama 本地推理运行的模型（零 API 成本），**不计入账单总额**；"
                "其「花费」恒为 ¥0.00，仅作本地使用量统计。"
            )
        )
    if any(m.get("is_custom") and not m.get("is_local") for m in model_stats):
        out.extend(
            _note(
                "🔧 = 你通过外部 API 接口自建 / 接入的自定义模型（非 WorkBuddy 官方模型），与 🗄️ 官方已下架模型**分开统计**；"
                "单价仅作粗略参考，实际账单请往对应接口查看。"
            )
        )
    if any(m.get("is_router_api") for m in model_stats):
        out.extend(
            _note(
                "🔀 = 智能路由 / 聚合网关（外部 API，如 OpenRouter 免费档、Groq 等）：一次调用可能落到不同底层模型或上游 host，"
                "单价 / 花费为粗略参考，实际账单请往对应接口查看。"
            )
        )
    # 低置信度说明（只有本期真的命中时才出现，避免噪音）
    _lc_hits = {m["model"]: _lc_reason(m["model"], low_conf_map) for m in model_stats}
    _lc_hits = {k: v for k, v in _lc_hits.items() if v}
    if _lc_hits:
        out.extend(
            _note(
                "⚠ = **低置信度估算**：该模型存在服务端时段减免 / 用户配额，静态价表无法表达，"
                "估算与实际计费偏差已知较大；**不参与「最贵模型」结论，请勿据此做预算或对账**。"
            )
        )
        for _n, _r in sorted(_lc_hits.items()):
            _ar = _lc_arrow(_lc_bias(_n, low_conf_bias_map))
            out.extend(_note(f"　　`{_n} {_ar}`：{_r}"))
    # 洞察（🏆 最常使用 / 💸 最贵）——MD 与 HTML 结构不同
    if hide_cost:
        # tokens_only：只保留调用维度的 🏆，金额结论整段缺席
        if model_stats:
            _tc = max(model_stats, key=lambda x: x["calls"])
            if fmt == "md":
                out.append(
                    f"> 🏆 **最常使用模型**：`{_tc['model']}` —— 调用 {_tc['calls']} 次。"
                )
            else:
                out.append(
                    f"        <p>🏆 <strong>最常使用模型</strong>：<code>{_esc(_tc['model'])}</code>"
                    f"（调用 {_tc['calls']} 次）。</p>"
                )
        out.append("")
        return out
    if fmt == "md":
        if model_stats:
            top_calls = max(model_stats, key=lambda x: x["calls"])
            out.append(
                f"> 🏆 **最常使用模型**：`{top_calls['model']}` —— 调用 {top_calls['calls']} 次。"
            )
        if priced:
            # 低置信度模型不参与「最贵模型」结论（估算偏差已知较大）
            concrete = [
                m
                for m in priced
                if not m.get("is_router") and not _lc_reason(m["model"], low_conf_map)
            ]
            if not concrete and priced:
                concrete = [m for m in priced if not m.get("is_router")]
            top_cost = max(concrete or priced, key=lambda x: x.get("effective_cost", 0))
            share = (
                top_cost.get("effective_cost", 0) / total_billable * 100
                if total_billable
                else 0
            )
            # 仅当本期真的存在低置信度模型时才在标题里提它，避免无配置时的无谓噪音
            _lc_suffix = (
                "与 ⚠ 低置信度模型"
                if any(_lc_reason(m["model"], low_conf_map) for m in priced)
                else ""
            )
            out.append(
                f"> 💸 **最贵模型**（按花费，不含路由别名{_lc_suffix}）：`{top_cost['model']}` —— 估算花费 ¥{top_cost.get('effective_cost', 0):.2f}，"
                f"占总花费 {share:.1f}%。"
            )
            # 被剔除的低置信度模型不得悄悄消失：逐条列出金额，避免用一个误导替换另一个
            _skipped = sorted(
                (
                    m
                    for m in priced
                    if _lc_reason(m["model"], low_conf_map) and m is not top_cost
                ),
                key=lambda x: x.get("effective_cost", 0),
                reverse=True,
            )
            if _skipped:
                _sk = "、".join(
                    f"`{m['model']}` ¥{m.get('effective_cost', 0):.2f}"
                    for m in _skipped
                )
                out.append(
                    f"> ⚠ 未计入本结论的低置信度模型：{_sk} —— 估算偏差已知较大，不代表真实支出（见报告顶部「成本口径」）。"
                )
            # 高位告警：低置信度模型恰好是本期最贵（或 Top-3）时，单独醒目提示，
            # 避免用户照「最贵」去切换模型反而多花钱（这正是用户担心的「低置信度最贵」场景）。
            # 仅聚合本维度（model_stats）；low_conf 配置取自本函数入参，不可用外层 data/meta。
            _alert = _lc_top_alert(
                {
                    "model_stats": model_stats,
                    "model_exec_stats": [],
                    "meta": {
                        "low_confidence": low_conf_map or {},
                        "low_confidence_bias": low_conf_bias_map or {},
                    },
                }
            )
            if _alert:
                out.append(
                    f"> ⚠ **高位告警**：本期最贵模型 **`{_alert['model']}` {_alert['arrow']}**"
                    f"（¥{_alert['cost']:.2f}，第 {_alert['rank']} 贵，占付费花费 "
                    f"{_alert['share'] * 100:.0f}%）为低置信度估算"
                    f"（L2 偏差较大）；其真实花费请以官方账单为准，**不要据此切换模型**。"
                    f"（见报告顶部「成本口径」）"
                )
        elif configured:
            out.append(
                "> 💸 当前已配置单价的模型均为免费模型（花费 ¥0.00）；填入付费模型单价后此处显示最贵模型。"
            )
        out.append("")
    else:
        if configured:
            chart = build_model_cost_chart(
                configured,
                low_conf_map=low_conf_map,
                low_conf_bias_map=low_conf_bias_map,
            )
            if chart:
                out.append(chart)
            top_calls = max(model_stats, key=lambda x: x["calls"])
            if priced:
                # 低置信度模型不参与「最贵模型」结论
                concrete = [
                    m
                    for m in priced
                    if not m.get("is_router")
                    and not _lc_reason(m["model"], low_conf_map)
                ]
                if not concrete and priced:
                    concrete = [m for m in priced if not m.get("is_router")]
                top_cost = max(
                    concrete or priced, key=lambda x: x.get("effective_cost", 0)
                )
                share = (
                    top_cost.get("effective_cost", 0) / total_billable * 100
                    if total_billable
                    else 0
                )
                _lc_note = (
                    ' ⚠<span class="lc-note">（低置信度估算，仅供参考）</span>'
                    if _lc_reason(top_cost["model"], low_conf_map)
                    else ""
                )
                _lc_suffix = (
                    "与 ⚠ 低置信度模型"
                    if any(_lc_reason(m["model"], low_conf_map) for m in priced)
                    else ""
                )
                out.append(
                    f"        <p>🏆 <strong>最常使用模型</strong>：<code>{_esc(top_calls['model'])}</code>"
                    f"（调用 {top_calls['calls']} 次）；"
                    f"💸 <strong>最贵模型</strong>（按花费，不含路由别名{_lc_suffix}）："
                    f"<code>{_esc(top_cost['model'])}</code>"
                    f"（估算 ¥{top_cost.get('effective_cost', 0):.2f}，占 {share:.1f}%）。</p>"
                )
                _skipped = sorted(
                    (
                        m
                        for m in priced
                        if _lc_reason(m["model"], low_conf_map) and m is not top_cost
                    ),
                    key=lambda x: x.get("effective_cost", 0),
                    reverse=True,
                )
                if _skipped:
                    _sk = "、".join(
                        f"<code>{_esc(m['model'])}</code> ¥{m.get('effective_cost', 0):.2f}"
                        for m in _skipped
                    )
                    out.append(
                        f'        <p class="disclaimer">⚠ 未计入本结论的低置信度模型：{_sk}'
                        " —— 估算偏差已知较大，不代表真实支出（见报告顶部「成本口径」）。</p>"
                    )
                # 高位告警（HTML）：低置信度模型为本期最贵（或 Top-3）时醒目提示。
                # 注意：必须放在 if _skipped 之外——低置信度模型恰为 #1 最贵时 _skipped 为空，
                # 而这正是最需要告警的场景。
                _alert_h = _lc_top_alert(
                    {
                        "model_stats": model_stats,
                        "model_exec_stats": [],
                        "meta": {
                            "low_confidence": low_conf_map or {},
                            "low_confidence_bias": low_conf_bias_map or {},
                        },
                    }
                )
                if _alert_h:
                    out.append(
                        f'        <p class="warn-box">⚠ <b>高位告警</b>：本期最贵模型 '
                        f"<code>{_esc(_alert_h['model'])} {_alert_h['arrow']}</code>"
                        f"（¥{_alert_h['cost']:.2f}，第 {_alert_h['rank']} 贵，占付费花费 "
                        f"{_alert_h['share'] * 100:.0f}%）为低置信度估算"
                        f"（L2 偏差较大）；其真实花费请以官方账单为准，<b>不要据此切换模型</b>。</p>"
                    )
            else:
                out.append(
                    f"        <p>🏆 <strong>最常使用模型</strong>：<code>{_esc(top_calls['model'])}</code>"
                    f"（调用 {top_calls['calls']} 次）。当前已配置单价的模型均为免费模型，"
                    f"填入付费模型单价后显示最贵模型对比。</p>"
                )
    return out


def build_model_section(fmt, data):
    """章节 §三：模型使用与成本对比（双维度：接口/通道 + 实际执行模型）。
    MD / HTML 共用数据计算，仅渲染层不同；原 build_model_section_md / _html 合并产物。"""
    meta = data.get("meta", {})
    model_stats = data.get("model_stats", [])
    exec_stats = data.get("model_exec_stats", [])
    if not model_stats and not exec_stats:
        return []
    tf_map = meta.get("timed_free", {}) or {}
    lc_map = meta.get("low_confidence", {}) or {}
    lc_bias_map = meta.get("low_confidence_bias", {}) or {}
    hidden = _cost_hidden(data)  # tokens_only：隐藏金额维度
    # 单通道数据源（如千问办公：档位即入口）——§3.2「按入口/通道」必然与 §3.1 同构，
    # 由采集端显式声明 meta.single_channel，渲染端不靠「两表行数相等」隐式猜。
    _skip32 = bool(meta.get("single_channel"))
    if _skip32:
        exec_stats = []
    if fmt == "md":
        lines = []
        lines.append(
            "## 三、模型使用与成本对比" if not hidden else "## 三、模型使用对比"
        )
        lines.append("")
        if hidden:
            lines.append(
                "按模型统计调用次数与实际消耗 Token。**本报告为 tokens_only 计价模式："
                "本期没有任何模型命中单价，故金额、占比与「最贵模型」结论一律不出**"
                "（免得满屏 `¥0.00` 被读成「免费」）。"
                + (
                    "§3.1 按实际执行模型统计使用量。"
                    if _skip32
                    else "3.1 按实际执行模型、3.2 按入口 / 通道模型两个维度统计使用量。"
                )
            )
        else:
            lines.append(
                "按模型统计调用次数、实际消耗 Token 与单价（元 / 1M tokens，输入 / 输出分别计价）。"
                "本章节提供**两个维度**："
            )
            lines.append("")
            lines.append(
                "- **3.1 按实际计费模型（账单口径）**：按 API 实际计费的模型（即 trace 的 `exec_model`，含经 `auto`/限免入口路由到的付费模型）聚合，是费用结算依据；其各模型花费合计 = 报告概览「实际成本（计费等效）」总额。"
            )
            lines.append(
                "- **3.2 按入口 / 配置模型（使用维度）**：按你配置的入口 / 通道（如 `auto` 路由、`hy3`、`custom-local`）聚合，反映你实际请求 / 配置了哪些入口、各多少次——属「使用分布」而非「账单」；本维度总额不代表真实账单，且不可与 3.1 相加。"
            )
        lines.append("")
        if tf_map and not hidden:
            _tf_txt = "、".join(
                f"`{k}`（至 **{v}**）" for k, v in sorted(tf_map.items())
            )
            lines.append(
                f"> 🎁 **限时免费**：{_tf_txt} 在限免活动期间免费，相关调用花费记为 ¥0.00；"
                "表格中以「限时免费」标注，以区别于永久免费模型（`:free` 后缀）。"
                "若该模型有公开刊例价，表中仍会显示原单价，方便对比「原价 vs 实付」。"
            )
            lines.append("")
        if not hidden:
            lines.append(
                "> ⚠️ 以上计算只供参考，如果是外部自建接口（custom-local），请往接口相关网站查看账单。"
            )
            lines.append("")
        # 3.1 接口 / 通道（计费维度）
        lines.append(
            "### 3.1 按实际计费模型（账单口径）"
            if not hidden
            else "### 3.1 按实际执行模型"
        )
        lines.append("")
        if not hidden:
            lines.append(
                "> 备注：WorkBuddy 的 GLM-5.2 夜猫子计划折扣（2026 年 7 月 16 日开始）已计入 `glm-5.2` 的花费中。"
            )
            lines.append("")
        model_stats = merge_glm52_family(model_stats)
        lines += _build_model_block(
            "md",
            model_stats,
            "Token 维度明细" if hidden else "计费维度明细（费用结算依据）",
            timed_free_map=tf_map,
            low_conf_map=lc_map,
            low_conf_bias_map=lc_bias_map,
            hide_cost=hidden,
        )
        chart = (
            ""
            if hidden
            else build_model_cost_chart_md(
                [m for m in model_stats if m.get("configured")],
                low_conf_map=lc_map,
                low_conf_bias_map=lc_bias_map,
            )
        )
        if chart:
            lines.append(chart)
            lines.append("")
        # 3.2 按入口 / 配置模型（使用维度 · 非计费口径）
        if not _skip32:
            lines.append(
                "### 3.2 按入口 / 配置模型（使用维度 · 非计费口径）"
                if not hidden
                else "### 3.2 按入口 / 通道模型（使用维度）"
            )
            lines.append("")
        if not hidden and not _skip32:
            lines.append(
                "> 本维度按你配置的**入口 / 通道模型名**聚合（如 `auto` 路由、`hy3`、`custom-local`），"
                "反映你实际请求 / 配置了哪些入口、各多少次——是「使用分布」而非「账单」。"
                "经由 `auto` 路由或限免入口（如 `hy3`）实际执行的底层付费模型，其花费已计入 3.1 对应执行模型行，"
                "本表不直接展开；**本维度总额不代表真实账单，且不可与 3.1 相加**；自建接口（custom-local）实际单价请往接口网站查看。"
            )
            lines.append("")
        if exec_stats:
            official_exec = [m for m in exec_stats if not m.get("is_custom")]
            local_exec = [m for m in exec_stats if m.get("is_local")]
            external_exec = [
                m for m in exec_stats if m.get("is_custom") and not m.get("is_local")
            ]
            if official_exec:
                lines.append("#### 3.2.1 官方 / 网关入口模型")
                lines.append("")
                lines += _build_model_block(
                    "md",
                    official_exec,
                    "官方入口维度明细",
                    is_exec=True,
                    timed_free_map=tf_map,
                    low_conf_map=lc_map,
                    low_conf_bias_map=lc_bias_map,
                    hide_cost=hidden,
                )
                chart2 = (
                    ""
                    if hidden
                    else build_model_cost_chart_md(
                        [m for m in official_exec if m.get("configured")],
                        low_conf_map=lc_map,
                        low_conf_bias_map=lc_bias_map,
                    )
                )
                if chart2:
                    lines.append(chart2)
                    lines.append("")
            if local_exec:
                lines.append("#### 3.2.2 本地模型（Ollama 本地推理）🔧🏠")
                lines.append("")
                lines += _build_model_block(
                    "md",
                    local_exec,
                    "本地模型维度明细",
                    is_exec=True,
                    timed_free_map=tf_map,
                    low_conf_map=lc_map,
                    low_conf_bias_map=lc_bias_map,
                    compact=True,
                )
                chart3 = (
                    ""
                    if hidden
                    else build_model_cost_chart_md(
                        [m for m in local_exec if m.get("configured")],
                        low_conf_map=lc_map,
                        low_conf_bias_map=lc_bias_map,
                    )
                )
                if chart3:
                    lines.append(chart3)
                    lines.append("")
            if external_exec:
                lines.append("#### 3.2.3 外部 API 接口接入模型 🔧")
                lines.append("")
                lines += _build_model_block(
                    "md",
                    external_exec,
                    "外部API入口维度明细",
                    is_exec=True,
                    timed_free_map=tf_map,
                    low_conf_map=lc_map,
                    low_conf_bias_map=lc_bias_map,
                    hide_cost=hidden,
                )
                chart4 = (
                    ""
                    if hidden
                    else build_model_cost_chart_md(
                        [m for m in external_exec if m.get("configured")],
                        low_conf_map=lc_map,
                        low_conf_bias_map=lc_bias_map,
                    )
                )
                if chart4:
                    lines.append(chart4)
                    lines.append("")
        else:
            lines.append(
                "> ℹ️ 本数据源仅一层通道（档位即入口），§3.2 入口维度与 §3.1 必然同构，"
                "故不重复输出。"
                if _skip32
                else "（本期无模型调用数据）"
            )
            lines.append("")
        # 3.3 缺失单价模型（数据驱动）——tokens_only 或该源不支持计费时整块压制
        if _show_unconfigured_block(data):
            lines += _build_unconfigured_models_section("md", meta)
        return lines
    # HTML 渲染层
    lines = []
    lines.append('    <div class="section">')
    lines.append(
        '        <h2 class="section-title">三、模型使用与成本对比</h2>'
        if not hidden
        else '        <h2 class="section-title">三、模型使用对比</h2>'
    )
    if hidden:
        lines.append(
            "        <p>按模型统计调用次数与实际消耗 Token。<b>本报告为 tokens_only 计价模式："
            "本期没有任何模型命中单价，故金额、占比与「最贵模型」结论一律不出</b>"
            "（免得满屏 <code>¥0.00</code> 被读成「免费」）。</p>"
        )
    else:
        lines.append(
            "        <p>按模型统计调用次数、实际消耗 Token 与单价（元 / 1M tokens，输入 / 输出分别计价）。"
            "本章节提供<b>两个维度</b>：<b>3.1 按实际计费模型</b>（账单口径，与概览总额一致）与 <b>3.2 按入口 / 配置模型</b>（使用分布）。"
            "未配置单价的模型以「未配置」标注——在 <code>scripts/pricing.local.json</code> 的 <code>models</code> 里补上单价即可（无需改 Python 代码；该本地文件升级 Skill 时不丢失）。</p>"
        )
    if tf_map and not hidden:
        _tf_txt = "、".join(
            f"<code>{_esc(k)}</code>（至 <b>{_esc(v)}</b>）"
            for k, v in sorted(tf_map.items())
        )
        lines.append(
            f'        <p class="disclaimer">🎁 <b>限时免费</b>：{_tf_txt} 在限免活动期间免费，'
            "相关调用花费记为 ¥0.00，以区别于永久免费模型（<code>:free</code> 后缀）。"
            "若该模型有公开刊例价，表中仍显示原单价，方便对比「原价 vs 实付」。</p>"
        )
    lines.append(
        "        <h3>3.1 按实际计费模型（账单口径）</h3>"
        if not hidden
        else "        <h3>3.1 按实际执行模型</h3>"
    )
    if not hidden:
        lines.append(
            '        <p class="disclaimer">备注：WorkBuddy 的 GLM-5.2 夜猫子计划折扣（2026 年 7 月 16 日开始）已计入 <code>glm-5.2</code> 的花费中。</p>'
        )
    model_stats = merge_glm52_family(model_stats)
    lines += _build_model_block(
        "html",
        model_stats,
        timed_free_map=tf_map,
        low_conf_map=lc_map,
        low_conf_bias_map=lc_bias_map,
        hide_cost=hidden,
    )
    if not hidden:
        lines.append(
            '        <p class="disclaimer">⚠️ 以上计算只供参考，如果是外部自建接口（custom-local），请往接口相关网站查看账单。'
            "3.1 各模型花费合计 = 报告概览「实际成本（计费等效）」总额。</p>"
        )
    if not _skip32:
        lines.append(
            "        <h3>3.2 按入口 / 配置模型（使用维度 · 非计费口径）</h3>"
            if not hidden
            else "        <h3>3.2 按入口 / 通道模型（使用维度）</h3>"
        )
    if not hidden and not _skip32:
        lines.append(
            "        <p>本维度按你配置的<b>入口 / 通道模型名</b>（如 <code>auto</code> 路由、<code>hy3</code>、<code>custom-local</code>）聚合，"
            "反映实际请求 / 配置的入口分布（非账单）。经由 <code>auto</code> 或限免入口实际执行的底层付费模型，"
            "其花费已计入 3.1 对应执行模型行，本表不直接展开。"
            "<b>本维度总额不代表真实账单，且不可与 3.1 相加</b>。</p>"
        )
    if exec_stats:
        official_exec = [m for m in exec_stats if not m.get("is_custom")]
        local_exec = [m for m in exec_stats if m.get("is_local")]
        external_exec = [
            m for m in exec_stats if m.get("is_custom") and not m.get("is_local")
        ]
        if official_exec:
            lines.append("        <h4>3.2.1 官方 / 网关入口模型</h4>")
            lines += _build_model_block(
                "html",
                official_exec,
                is_exec=True,
                timed_free_map=tf_map,
                low_conf_map=lc_map,
                low_conf_bias_map=lc_bias_map,
                hide_cost=hidden,
            )
        if local_exec:
            lines.append("        <h4>3.2.2 本地模型（Ollama 本地推理）🔧🏠</h4>")
            lines += _build_model_block(
                "html",
                local_exec,
                is_exec=True,
                timed_free_map=tf_map,
                low_conf_map=lc_map,
                low_conf_bias_map=lc_bias_map,
                compact=True,
            )
        if external_exec:
            lines.append("        <h4>3.2.3 外部 API 接口接入模型 🔧</h4>")
            lines += _build_model_block(
                "html",
                external_exec,
                is_exec=True,
                timed_free_map=tf_map,
                low_conf_map=lc_map,
                low_conf_bias_map=lc_bias_map,
                hide_cost=hidden,
            )
    else:
        lines.append(
            "        <p>ℹ️ 本数据源仅一层通道（档位即入口），§3.2 入口维度与 §3.1 必然同构，"
            "故不重复输出。</p>"
            if _skip32
            else "        <p>（本期无模型调用数据）</p>"
        )
    if not hidden:
        lines.append(
            '        <p class="disclaimer">⚠️ 以上计算只供参考，如果是外部自建接口（custom-local），请往接口相关网站查看账单。</p>'
        )
    # 3.3 缺失单价模型（数据驱动）——tokens_only 或该源不支持计费时整块压制
    if _show_unconfigured_block(data):
        lines += _build_unconfigured_models_section("html", meta)
    lines.append("    </div>")
    return lines


def _build_unconfigured_models_section(fmt, meta):
    """渲染「缺失单价模型」提示块（MD / HTML 共用数据计算，仅渲染层不同）。"""
    unconfigured = meta.get("unconfigured_models") or []
    if not unconfigured:
        return []
    pricing_lookup = meta.get("pricing_lookup") or {}
    network_estimates = pricing_lookup.get("network_estimates") or {}
    search_links = pricing_lookup.get("search_links") or {}
    mode = pricing_lookup.get("mode", "offline")
    rows = []
    for m in unconfigured:
        est = network_estimates.get(m)
        link = search_links.get(m)
        if est:
            ip, op = f"{est['input']:.2f}", f"{est['output']:.2f}"
        else:
            ip, op = "—", "—"
        rows.append((m, ip, op, est, link))
    json_lines = []
    for m in unconfigured:
        json_lines.append(f'    "{m}": {{')
        json_lines.append(f'        "input": 0,   // 填入实际输入单价（元/1M tokens）')
        json_lines.append(f'        "output": 0   // 填入实际输出单价（元/1M tokens）')
        json_lines.append(f"    }},")
    if fmt == "md":
        out = [
            "> ⚠️ **本期有未配置单价的模型**（未计入账单总额，但调用仍发生）：",
            "",
            "| 模型 | 建议输入单价(元/1M) | 建议输出单价(元/1M) | 来源 |",
            "|------|---------------------|---------------------|------|",
        ]
        for m, ip, op, est, link in rows:
            if est:
                src = f"🌐 网络估算价，[搜索验证]({link})" if link else "🌐 网络估算价"
            elif link:
                src = f"[搜索定价]({link})"
            else:
                src = "未配置"
            out.append(f"| `{m}` | {ip} | {op} | {src} |")
        out.append("")
        out.append("<details>")
        out.append(
            "<summary>📝 复制下面片段到 <code>scripts/pricing.local.json</code> 的 <code>models</code> 节点补全单价（本地覆盖文件，<code>skillhub upgrade</code> 升级时不会被覆盖；仅供参考，请按实际账单核对）</summary>"
        )
        out.append("")
        out.append("```json")
        out.extend(json_lines)
        out.append("```")
        out.append("</details>")
        out.append("")
        if mode == "online":
            out.append(
                "> ℹ️ 已联网检索（`--lookup-pricing online`），上表「网络估算价」仅作参考，**不计入**报告任何成本总额，请以你实际账单为准。"
            )
            out.append("")
        return out
    out = [
        "        <h3>3.3 缺失单价模型（未计入账单总额）</h3>",
        '        <p class="disclaimer">⚠️ 以下模型本期被调用，但未在 <code>pricing.json</code>（或本地覆盖 <code>pricing.local.json</code>）中找到单价，因此未计入成本总额。请把单价补进 <code>scripts/pricing.local.json</code> 的 <code>models</code> 节点后重跑采集（该文件升级 Skill 时不会被覆盖）。</p>',
        "        <table>",
        "            <tr><th>模型</th><th>建议输入单价(元/1M)</th><th>建议输出单价(元/1M)</th><th>来源</th></tr>",
    ]
    for m, ip, op, est, link in rows:
        if est:
            src = (
                f'<a href="{_esc(link)}" target="_blank">🌐 网络估算价（点击验证）</a>'
                if link
                else "🌐 网络估算价"
            )
        elif link:
            src = f'<a href="{_esc(link)}" target="_blank">搜索定价</a>'
        else:
            src = "未配置"
        out.append(
            f"            <tr><td><code>{_esc(m)}</code></td><td>{ip}</td><td>{op}</td><td>{src}</td></tr>"
        )
    out.append("        </table>")
    out.append("        <details>")
    out.append(
        "            <summary>📝 点击展开：复制以下片段到 <code>scripts/pricing.local.json</code> 的 <code>models</code> 节点补全单价（本地覆盖，升级 Skill 时不丢失）</summary>"
    )
    out.append('            <pre><code class="language-json">')
    out.extend(json_lines)
    out.append("</code></pre>")
    out.append("        </details>")
    if mode == "online":
        out.append(
            '        <p class="disclaimer">ℹ️ 已联网检索（<code>--lookup-pricing online</code>），上表「网络估算价」仅作参考，<b>不计入</b>报告任何成本总额，请以你实际账单为准。</p>'
        )
    return out


# 档位规范 id → 中文档位名（与 collect_usage_data.TIER_LABELS 同源，报告层展示用）
TIER_LABELS = {
    "fast-model": "快速",
    "balanced-model": "均衡",
    "deep-model": "极致",
    "extreme-model": "极致",
}


def build_tier_section(fmt, data):
    """HTML 章节 §3.4 / Markdown §3.4：档位维度（快速 / 均衡 / 极致）。存在档位调用时才渲染。
    MD / HTML 共用数据计算，仅渲染层不同。

    新增分析维度。档位真实底层模型从不落盘，只能纯档位聚合；
    其单价为按积分倍率锚定的**估算值**（已在 meta 标注），不计入账单总额。
    """
    meta = data.get("meta", {})
    tier_stats = data.get("tier_stats") or []
    if not tier_stats:
        return []
    cache_loaded = meta.get("mode_config_cache_loaded", False)
    total_tier_cost = sum(m.get("effective_cost", 0) or 0 for m in tier_stats) or 1
    columns = [
        "档位",
        "调用次数",
        "实际消耗Token",
        "输入单价(估算,元/1M)",
        "输出单价(估算,元/1M)",
        "估算花费",
        "占总花费比",
    ]
    md_sep = "|------|---------|-------------|--------------|--------------|---------|-----------|"
    rows = []
    for m in tier_stats:
        label = TIER_LABELS.get(m["model"], m["model"])
        if m.get("is_router"):
            label += "（未解析具体模型）"
        eff = m.get("effective_cost", 0) or 0
        ip = f"{m['unit_price_input']:.2f}" if m.get("configured") else "—"
        op = f"{m['unit_price_output']:.2f}" if m.get("configured") else "—"
        share = (eff / total_tier_cost * 100) if eff > 0 else 0.0
        rows.append(
            [
                label,
                str(m["calls"]),
                format_number(m.get("effective_tokens", 0)),
                ip,
                op,
                f"¥{eff:.2f}",
                f"{share:.1f}%",
            ]
        )
    intro = (
        "WorkBuddy 的自动路由已拆为三档：**快速 / 均衡 / 极致**。它们在 trace 中以路由别名出现，"
        "真实底层模型**从不落盘**，故只能做纯档位聚合，无法做「档位 × 真实模型」交叉表。"
        "档位倍率是「积分维度」，与 ¥ 刊例价正交——本表单价仅作分析参考。"
    )
    disc = (
        "ℹ️ 档位为智能路由别名（执行时自动调配最适合模型，类似 openrouter/free），无单一单价；"
        "其「单价 / 花费」为按积分倍率锚定的**估算值**"
        + ("（倍率已用服务端配置缓存校准）" if cache_loaded else "")
        + "，仅供横向对比参考，**不计入**账单总额，请以实际积分账单为准。"
    )
    json_lines = _tier_rates_snippet(meta)
    if fmt == "md":
        out = [
            "### 3.4 档位维度（快速 / 均衡 / 极致）",
            "",
            intro,
            "",
            "| " + " | ".join(columns) + " |",
            md_sep,
        ]
        out.extend("| " + " | ".join(r) + " |" for r in rows)
        out.append("")
        out.append("> " + disc)
        out.append("")
        out.append("<details>")
        out.append(
            "<summary>📝 档位估算单价来源与如何调整为精确值（改 <code>scripts/pricing.json</code> 的 <code>mode_rates</code> 即可，无需改代码）</summary>"
        )
        out.append("")
        out.append("```json")
        out.extend(json_lines)
        out.append("```")
        out.append("</details>")
        out.append("")
        return out
    out = [
        '    <div class="section">',
        "        <h3>3.4 档位维度（快速 / 均衡 / 极致）</h3>",
        "        <p>" + _fmt_inline(intro, "html") + "</p>",
        "        <table>",
        "            <tr>" + "".join(f"<th>{_esc(c)}</th>" for c in columns) + "</tr>",
    ]
    out.extend(
        "            <tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>"
        for r in rows
    )
    out.append("        </table>")
    out.append('        <p class="disclaimer">' + _fmt_inline(disc, "html") + "</p>")
    out.append("        <details>")
    out.append(
        "            <summary>📝 点击展开：档位估算单价来源与如何调整为精确值（改 <code>scripts/pricing.json</code> 的 <code>mode_rates</code> 即可，无需改代码）</summary>"
    )
    out.append('            <pre><code class="language-json">')
    out.extend(json_lines)
    out.append("</code></pre>")
    out.append("        </details>")
    out.append("    </div>")
    return out


def build_reconciliation_section(fmt, data):
    """§3.5 双源对账（官方导出 L1 × 本地 trace L2）。

    仅在传入 `--import-official` 时渲染；未导入时返回 []，保证零回归。

    要回答的问题不是「谁数字大」，而是「**差在哪、差的是不是钱**」：
      - 官方有 / trace 无 → 真实计费但被 trace 漏记 → **成本被低估**（图像模型、minimax-m3）
      - trace 有 / 官方无 → 本地模型 / 免费额度 / 路由别名 → 通常不计费，不是漏记
      - 两边都有 → 给倍数，说明「一次请求 → 多次 generation」的粒度差，不是用量暴涨
    """
    rec = data.get("reconciliation")
    if not isinstance(rec, dict) or not rec.get("official_requests"):
        return []
    off = _official_import(data)
    if off is None:
        return []

    def _label(m):
        """基础模型名 + 已归并的收费版变体（如 hy3 ← hy3-x）。

        官方侧 `hy3-x` 会被 display_merge 归并到 `hy3`（与 trace 侧显示口径一致），
        这里把被归并掉的变体显式标出来，避免读者以为「官方有个 trace 没有的模型」。
        """
        vs = m.get("variants") or []
        return f"{m['model']}（含 {'、'.join(vs)}）" if vs else m["model"]

    w = off.get("meta", {}).get("window", {})
    ratio = rec.get("ratio", 0.0)
    missing = rec.get("missing_in_trace", []) or []
    trace_only = rec.get("trace_only", []) or []
    both = rec.get("both", []) or []

    if fmt == "md":
        lines = [
            "### 3.5 双源对账（官方导出 × 本地 Trace）",
            "",
            f"> 官方导出窗口 **{w.get('first', '')} ~ {w.get('last', '')}**（北京时间）；"
            f"本地 trace 已归一到同一时区后再比对，不存在 ±8h 错位。",
            "",
            "| 口径 | 数值 | 说明 |",
            "|------|------|------|",
            f"| 官方导出「请求数」 | {rec.get('official_requests', 0)} 次 | 一次用户提问 = 1 请求（账单口径）|",
            f"| 本地 trace「generation 数」 | {rec.get('trace_generations', 0)} 次 | 一次请求内部可含多轮生成（含工具调用续写）|",
            f"| 粒度倍数 | {ratio}x | **不是**用量暴涨，是统计粒度不同 |",
            f"| 官方积分合计 | {off.get('totals', {}).get('credits', 0):.2f} | L1 真值 |",
            "",
        ]

        if missing:
            lines += [
                f"**⚠️ 官方有、trace 无（{len(missing)} 项，共 {rec.get('missing_credits', 0):.2f} 积分）"
                f"—— 真实计费但被 trace 漏记，纯 trace 成本会低估**：",
                "",
                "| 模型 | 官方请求 | 官方积分 |",
                "|------|--------:|--------:|",
            ]
            for m in missing:
                lines.append(
                    f"| `{_label(m)}` | {m['official_requests']} | {m['official_credits']:.2f} |"
                )
            lines.append("")

        if trace_only:
            lines += [
                f"**trace 有、官方无（{len(trace_only)} 项）—— 本地模型 / 免费额度 / 路由别名，"
                f"不进官方账单，不是漏记**：",
                "",
                "| 模型 | trace generation | trace 估算成本 |",
                "|------|----------------:|--------------:|",
            ]
            for m in trace_only[:15]:
                lines.append(
                    f"| `{m['model']}` | {m['trace_generations']} | ¥{m['trace_est_cost']:.2f} |"
                )
            if len(trace_only) > 15:
                lines.append(f"| … 其余 {len(trace_only) - 15} 项 | | |")
            lines.append("")

        if both:
            lines += [
                "**两边都有（按官方积分降序）**：",
                "",
                "| 模型 | 官方请求 | trace generation | 官方积分 | trace 估算 |",
                "|------|--------:|-----------------:|--------:|-----------:|",
            ]
            for m in both[:15]:
                lines.append(
                    f"| `{_label(m)}` | {m['official_requests']} | {m['trace_generations']} | "
                    f"{m['official_credits']:.2f} | ¥{m['trace_est_cost']:.2f} |"
                )
            if len(both) > 15:
                lines.append(f"| … 其余 {len(both) - 15} 项 | | | | |")
            lines.append("")

        lines += [
            "> 读法：**官方积分 = 真金白银**；trace 估算只用来看结构（哪个模型在跑、跑了多少轮）。"
            "两者不可直接相加，也不该互相替换。",
            "",
        ]
        return lines

    out = [
        "        <h3>3.5 双源对账（官方导出 × 本地 Trace）</h3>",
        f"        <p>官方导出窗口 <b>{_esc(w.get('first', ''))} ~ {_esc(w.get('last', ''))}</b>"
        f"（北京时间）；本地 trace 已归一到同一时区后再比对，不存在 ±8h 错位。</p>",
        "        <table><thead><tr><th>口径</th><th>数值</th><th>说明</th></tr></thead><tbody>",
        f"        <tr><td>官方导出「请求数」</td><td>{rec.get('official_requests', 0)} 次</td>"
        f"<td>一次用户提问 = 1 请求（账单口径）</td></tr>",
        f"        <tr><td>本地 trace「generation 数」</td><td>{rec.get('trace_generations', 0)} 次</td>"
        f"<td>一次请求内部可含多轮生成（含工具调用续写）</td></tr>",
        f"        <tr><td>粒度倍数</td><td>{ratio}x</td><td><b>不是</b>用量暴涨，是统计粒度不同</td></tr>",
        f"        <tr><td>官方积分合计</td><td>{off.get('totals', {}).get('credits', 0):.2f}</td>"
        f"<td>L1 真值</td></tr>",
        "        </tbody></table>",
    ]

    if missing:
        out.append(
            f"        <p><b>⚠️ 官方有、trace 无（{len(missing)} 项，共 "
            f"{rec.get('missing_credits', 0):.2f} 积分）—— 真实计费但被 trace 漏记，"
            f"纯 trace 成本会低估</b></p>"
        )
        out.append(
            "        <table><thead><tr><th>模型</th><th>官方请求</th><th>官方积分</th></tr></thead><tbody>"
        )
        for m in missing:
            out.append(
                f"        <tr><td><code>{_esc(_label(m))}</code></td>"
                f"<td>{m['official_requests']}</td><td>{m['official_credits']:.2f}</td></tr>"
            )
        out.append("        </tbody></table>")

    if trace_only:
        out.append(
            f"        <p><b>trace 有、官方无（{len(trace_only)} 项）—— 本地模型 / 免费额度 / "
            f"路由别名，不进官方账单，不是漏记</b></p>"
        )
        out.append(
            "        <table><thead><tr><th>模型</th><th>trace generation</th>"
            "<th>trace 估算成本</th></tr></thead><tbody>"
        )
        for m in trace_only[:15]:
            out.append(
                f"        <tr><td><code>{_esc(m['model'])}</code></td>"
                f"<td>{m['trace_generations']}</td><td>¥{m['trace_est_cost']:.2f}</td></tr>"
            )
        out.append("        </tbody></table>")

    if both:
        out.append("        <p><b>两边都有（按官方积分降序）</b></p>")
        out.append(
            "        <table><thead><tr><th>模型</th><th>官方请求</th><th>trace generation</th>"
            "<th>官方积分</th><th>trace 估算</th></tr></thead><tbody>"
        )
        for m in both[:15]:
            out.append(
                f"        <tr><td><code>{_esc(_label(m))}</code></td>"
                f"<td>{m['official_requests']}</td><td>{m['trace_generations']}</td>"
                f"<td>{m['official_credits']:.2f}</td><td>¥{m['trace_est_cost']:.2f}</td></tr>"
            )
        out.append("        </tbody></table>")

    out.append(
        '        <p class="note">读法：<b>官方积分 = 真金白银</b>；trace 估算只用来看结构'
        "（哪个模型在跑、跑了多少轮）。两者不可直接相加，也不该互相替换。</p>"
    )
    return out


def _auto_is_active(run):
    """该运行所属自动化是否处于执行中（ACTIVE）。PAUSED/DELETED/UNKNOWN 均视为已停止。"""
    return (run.get("auto_status") or "UNKNOWN") == "ACTIVE"


def _auto_state_label(status):
    """把 automation 定义状态映射为中文标签（用于自动化详情表）。"""
    return {
        "ACTIVE": "执行中",
        "PAUSED": "已暂停",
        "DELETED": "已删除",
    }.get(status or "UNKNOWN", "未知")


def build_next_week_outlook(
    summary,
    daily_tokens,
    automation_runs,
    session_credits,
    period_key="week",
    cost_hidden=False,
    anomaly_days=None,
    background_runs=None,
):
    """基于本期实际数据，生成动态的下期用量预测 + 优先级行动建议。

    所有结论均由报告内真实数据驱动：花费预测来自日均花费，额度预测来自
    当前额度占用与本期 token 消耗，自动化告警带样本量门槛避免小样本误报。
    不再重复「十、核心洞察」已给出的最大成本来源（高峰日）。

    自动化相关建议**仅考虑「正在执行」的自动化（auto_status == ACTIVE）**：
    已停止（已暂停 PAUSED / 已删除 DELETED）的自动化任务不计入，其运行记录
    即便处于 PENDING_REVIEW 也不再视为需要人工处理的「待审核」项。

    tokens_only（`cost_hidden=True`）时金额恒为 0，原 `eff_cost > 0` 门槛会把预测整段
    静默吞掉、只剩一句「使用趋势平稳」兜底，故改按**日均 token** 推算；`anomaly_days`
    与 `background_runs` 用来让展望不再与 §4.3 的异常检测自相矛盾。
    """
    _short = _PERIOD_SHORT.get(period_key, "本周")
    _next = _PERIOD_NEXT.get(period_key, "下周")
    items = []

    # 0. 下期用量预测（真·展望，数据驱动）
    eff_cost = summary.get("total_effective_cost", 0)
    eff_tokens = summary.get("total_effective_tokens", 0)
    active_days = summary.get("active_day_count", 0)
    if daily_tokens and active_days > 0 and (eff_cost > 0 or cost_hidden):
        avg_daily_cost = eff_cost / active_days
        dates = sorted(daily_tokens.keys())
        try:
            d0 = datetime.strptime(dates[0], "%Y-%m-%d")
            d1 = datetime.strptime(dates[-1], "%Y-%m-%d")
            period_days = max((d1 - d0).days + 1, 1)
        except (ValueError, TypeError):
            period_days = PERIOD_DAYS.get(period_key, 7)
        if cost_hidden:
            # tokens_only：按日均 token 推算，单位与全文一致走 format_number，不提 ¥
            avg_daily_tok = eff_tokens / active_days
            peak_day_tok = max(
                (v.get("effective", 0) for v in daily_tokens.values()), default=0
            )
            tok_low = avg_daily_tok * period_days
            tok_high = (
                avg_daily_tok + max(peak_day_tok - avg_daily_tok, 0)
            ) * period_days
            items.append(
                f"- 📈 **下期用量预测（Token 口径）**：按本期日均 {format_number(avg_daily_tok)} token "
                f"推算，{_next}（约 {period_days} 天）预计 "
                f"**{format_number(tok_low)} ~ {format_number(tok_high)} token**。"
            )
        else:
            peak_day_cost = max(
                (v.get("effective_cost", 0) for v in daily_tokens.values()), default=0
            )
            forecast_low = avg_daily_cost * period_days
            forecast_high = (
                avg_daily_cost + max(peak_day_cost - avg_daily_cost, 0)
            ) * period_days
            items.append(
                f"- 📈 **下期用量预测**：按本期日均 ¥{avg_daily_cost:.2f} 推算，{_next}（约 {period_days} 天）"
                f"预计花费 **¥{forecast_low:.2f} ~ ¥{forecast_high:.2f}**。"
            )

    # 自动化相关建议：仅统计「正在执行（ACTIVE）」的自动化。
    # 已停止（PAUSED/DELETED）的自动化不计入——其 PENDING_REVIEW 运行不再视为待处理项。
    active_runs = [r for r in automation_runs if _auto_is_active(r)]
    total_runs = len(active_runs)

    # 1. 待审核任务（仅统计正在执行的自动化）
    pending = sum(1 for r in active_runs if r.get("status") == "PENDING_REVIEW")
    if pending:
        share = pending / total_runs * 100 if total_runs else 0
        items.append(
            f"- 🔔 **P0 处理待审核任务**：{pending} 个自动化运行处于 PENDING_REVIEW"
            f"（占本期执行中自动化 {share:.0f}%），卡在人工确认环节持续占用额度与资源，建议尽快审核或配置自动放行。"
        )

    # 2. 自动化稳定性（样本 ≥10 才告警，否则仅观察）
    if total_runs:
        success = sum(1 for r in active_runs if r.get("result_success"))
        fail = total_runs - success
        fail_rate = fail / total_runs * 100
        if total_runs >= 10 and fail_rate >= 30:
            items.append(
                f"- 🛠️ **P1 自动化成功率偏低**：{success}/{total_runs}（失败率 {fail_rate:.0f}%），"
                f"失败重试会重复消耗 token，建议检查任务配置与依赖环境。"
            )
        elif fail > 0:
            items.append(
                f"- 🛠️ **P1 自动化稳定性**：本期 {fail}/{total_runs} 次失败（失败率 {fail_rate:.0f}%），"
                f"样本偏小暂不作为告警，建议持续观察。"
            )

    # 3. Token 额度 → P2（数据驱动）
    if session_credits:
        latest = max(session_credits, key=lambda x: x.get("updated_at", 0))
        used = latest.get("used", 0)
        size = latest.get("size", 0)
        if size > 0:
            ratio = used / size * 100
            if ratio >= 70:
                items.append(
                    f"- 💳 **P2 检查 Token 额度**：已用约 {ratio:.0f}%，接近上限，"
                    f"建议规划{_next}用量避免高峰任务因额度不足中断。"
                )
            else:
                items.append(
                    f"- 💳 **P2 关注 Token 额度**：已用约 {ratio:.0f}%，"
                    f"建议定期核对防止高峰期任务因额度不足而失败。"
                )

    # 4. 本期有 Token 峰值日 → 展望必须承接 §4.3，不能再套「使用趋势平稳」的兜底话
    if anomaly_days:
        _peak = anomaly_days[0]
        items.append(
            f"- ⚠️ **P1 复盘 Token 峰值日**：{_peak.get('date', '')} 出现 "
            f"{'；'.join(_peak.get('reasons') or [])}（见 §4.3），"
            f"建议排查当日是否存在可精简的批量 / 重复调用，而不是等它在下期复现。"
        )

    # 5. 后台自动运行（千问办公这类源无 cron 自动化时的替代观察点）
    br = background_runs or {}
    if br.get("count"):
        _err = br.get("error_count") or 0
        _rate = (_err / br["count"] * 100) if br["count"] else 0
        if _rate >= 30:
            items.append(
                f"- 🤖 **P2 关注后台自动运行**：本期 {br['count']} 次后台运行（记忆整理 / 反思等）"
                f"失败 {_err} 次（{_rate:.0f}%）——虽不计入任务榜，但同样消耗额度且失败即空转，"
                f"建议在设置里核查相关后台能力是否被反复重试。"
            )
        else:
            items.append(
                f"- 🤖 **P3 后台自动运行**：本期 {br['count']} 次（失败 {_err} 次），运行正常。"
            )

    if not items:
        items.append("- 使用趋势平稳，建议继续保持并关注高峰时段任务调度。")

    return items


# ─────────────────────────────────────────────────────────────
# Markdown 格式
# ─────────────────────────────────────────────────────────────
def generate_markdown_report(data):
    meta = data.get("meta", {})
    summary = data.get("summary", {})
    daily_tokens = data.get("daily_tokens", {})
    task_dist = summary.get("task_type_distribution", {})
    skills = data.get("skill_usage", {}).get("skills", {})
    outputs = data.get("outputs", [])
    automation_runs = data.get("automation_runs", [])

    total_input = summary.get("total_input_tokens", 0)
    total_cached = summary.get("total_cached_tokens", 0)
    cache_rate = (total_cached / total_input * 100) if total_input else 0

    lines = []
    _key = meta.get("period", "week")
    _label, _short, _next = _period_labels(meta)
    # 标题按数据源给出（workbuddy 沿用历史文案，外部源不再冒充 WorkBuddy）
    lines.append("# %s" % _source_identity(data)[0])
    lines.append("")
    lines.append(f"> **报告类型**：{_calendar_period(meta)}")
    lines.append(
        f"> **报告周期**：{meta.get('start_date', '')} 至 {meta.get('end_date', '')}"
    )
    lines.append(f"> **生成时间**：{_fmt_generated_at()}")
    _src_list = _source_identity(data)[1]
    if _is_l1(data):
        _src_list += "、**官方用量导出（成本真值 L1，本地只读解析）**"
    lines.append(f"> **数据来源**：{_src_list}")
    lines.append("")
    lines += _source_caveat_lines("md", data)
    lines += _cost_confidence_banner("md", data)

    # 一、概览统计
    lines.append("## 一、概览统计")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(
        f"| 活跃天数 | {summary.get('active_day_count', 0)} 天（{', '.join(summary.get('active_days', []))}）|"
    )
    lines.append(
        f"| 会话总数 | {summary.get('total_sessions', 0)} 个{_session_count_note(data)} |"
    )
    _bd = _call_count_breakdown(data)
    _billable_calls = _bd["billable"]
    # 口径标注：粒度随数据源而变（WorkBuddy=generation，千问办公=逐次调用真值），
    # 不标注会被读成「用量暴涨」或「调用数 ≠ 请求数」。
    # 失败调用不计入有效调用；未知模型已按 0 计价，两类都逐项披露。
    _calls_note = _calls_note_md(data, _bd)
    lines.append(f"| 调用次数 | {_billable_calls} 次{_calls_note} |")
    _user_turns = _user_turn_count(data)
    if _user_turns is not None:
        lines.append(
            f"| 用户提问轮数（真实计数） | {_user_turns} 次"
            f"（仅统计本期有调用的会话；转录里可直接数出，非估算）|"
        )
    _bg_note = _background_runs_note(data)
    if _bg_note:
        lines.append(_bg_note)
    lines.append(f"| 使用技能 | {summary.get('skills_used', 0)} 个 |")
    lines.append(
        f"| 自动化任务运行 | {summary.get('total_automation_runs', 0)} 次（成功 {summary.get('successful_automation_runs', 0)} 次）|"
    )
    lines.append(f"| 产出文件 | {summary.get('total_outputs', 0)} 个 |")
    lines.append(
        f"| {_eff_token_label(data)} | {format_number(summary.get('total_effective_tokens', 0))}（原始 {format_number(summary.get('total_tokens', 0))}）|"
    )
    lines.append(
        f"| 缓存占比 | {cache_rate:.1f}%（缓存命中 token 占输入 token 的比例）|"
    )
    if _cost_hidden(data):
        lines.append(
            "| 计价状态 | 未计价（tokens_only：本期无模型命中单价，金额维度已从全篇移除）|"
        )
    else:
        lines.append(
            f"| 实际成本（计费等效） | ¥{summary.get('total_effective_cost', 0):.2f}（原始口径 ¥{summary.get('total_cost', 0):.2f}）|"
        )
    if _is_l1(data):
        lines.append(
            f"| 官方账单（L1 真值） | {summary.get('official_requests', 0)} 次请求 / "
            f"**{summary.get('total_cost_official', 0):.2f} 积分**"
            f"（其中 {summary.get('official_free_requests', 0)} 次免费）|"
        )
    # 档位名双口径注脚：概览金额按档位口径汇总，须显式给出hy3 刊例价对照，
    # 否则读者会把「倍率锚定估算价」当成真实账单单价。
    lines += _tier_pricing_note_lines("md", data)
    # 请求数反推：generation 聚类得到的「估算请求数」，与官方「请求数」口径不同，仅对照
    _est_req = summary.get("estimated_request_count")
    # 有真实提问轮数可数时不再摆估算值（两条并存会让人问「该信哪个」）；
    # WorkBuddy 等拿不到 _human_turns 的源走原路径，含 L1 对照行。
    if _est_req is not None and _user_turns is None:
        _gap = summary.get("request_estimate_gap_minutes", 15)
        lines.append(
            f"| 估算请求数（generation 反推） | {_est_req} 次"
            f"（按会话内 ≥{_gap} 分钟间隔聚类；**估算值**，口径与官方「请求数」不同，不可等同）|"
        )
        if _is_l1(data):
            _off_req = summary.get("official_requests", 0) or 0
            if _off_req:
                _ratio = _est_req / _off_req if _off_req else 0
                lines.append(
                    f"| 估算请求数 ↔ 官方请求数 | 估算 {_est_req} / 官方 {_off_req}（倍率 {_ratio:.1f}x）；"
                    f"差异较大通常因多轮 / 子 Agent 放大或聚类阈值差异，估算值仅供参考 |"
                )
    if any(
        m.get("timed_free")
        for m in data.get("model_stats", []) + data.get("model_exec_stats", [])
    ):
        tf_map = meta.get("timed_free", {}) or {}
        if tf_map:
            tf_desc = "、".join(f"{k} 至 {v} 免费" for k, v in tf_map.items())
            lines.append(
                f"> 🎁 实际成本已计「限时免费」模型（{tf_desc}），相关花费记为 ¥0.00。"
            )
        else:
            lines.append("> 🎁 实际成本已计「限时免费」模型，相关花费记为 ¥0.00。")
    _warn = _unresolved_warning_md(_unresolved_call_stats(data))
    if _warn:
        lines.append(_warn)
    lines.append("")

    # 二、Token 消耗可视化
    lines.append("## 二、Token 消耗可视化")
    lines.append("")
    lines.append("### 2.1 总体消耗")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(
        f"| 原始总 Token（含缓存命中） | {format_number(summary.get('total_tokens', 0))} |"
    )
    lines.append(
        f"| {_eff_token_label(data)} | {format_number(summary.get('total_effective_tokens', 0))} |"
    )
    lines.append(
        f"| 输入 Token | {format_number(summary.get('total_input_tokens', 0))} |"
    )
    lines.append(
        f"| 输出 Token | {format_number(summary.get('total_output_tokens', 0))} |"
    )
    lines.append(
        f"| 缓存命中 Token | {format_number(summary.get('total_cached_tokens', 0))} |"
    )
    lines.append(f"| 缓存占比 | {cache_rate:.1f}%（{_cache_rate_note(data)}）|")
    lines.append("")

    if not _cost_hidden(data):
        lines.append("### 2.2 成本货币化")
        lines.append("")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        lines.append(
            f"| 实际成本（计费等效） | ¥{summary.get('total_effective_cost', 0):.2f} |"
        )
        lines.append(
            f"| 原始总成本（含缓存全价） | ¥{summary.get('total_cost', 0):.2f} |"
        )
        lines.append(f"| 输入成本 | ¥{summary.get('total_input_cost', 0):.2f} |")
        lines.append(f"| 输出成本 | ¥{summary.get('total_output_cost', 0):.2f} |")
        lines.append("")

    lines.append("### 2.3 每日 Token 消耗趋势")
    lines.append("")
    if daily_tokens:
        max_tokens = max((v.get("total", 0) for v in daily_tokens.values()), default=1)
        lines.append("```")
        for date in sorted(daily_tokens.keys()):
            stats = daily_tokens[date]
            bar_len = (
                int(40 * stats.get("total", 0) / max_tokens) if max_tokens > 0 else 0
            )
            bar = "█" * bar_len
            lines.append(f"{date} |{bar} {format_number(stats.get('total', 0))}")
        lines.append("```")
        lines.append("")
        _hidden_daily = _cost_hidden(data)
        if _hidden_daily:
            lines.append(
                "| 日期 | 原始总Token | 实际消耗 | 输入 | 输出 | 缓存 | 调用 |"
            )
            lines.append("|------|-----------|---------|------|------|------|------|")
        else:
            lines.append(
                "| 日期 | 原始总Token | 实际消耗 | 输入 | 输出 | 缓存 | 调用 | 实际成本 |"
            )
            lines.append(
                "|------|-----------|---------|------|------|------|------|---------|"
            )
        for date in sorted(daily_tokens.keys()):
            stats = daily_tokens[date]
            lines.append(
                f"| {date} | {format_number(stats.get('total', 0))} | "
                f"{format_number(stats.get('effective', 0))} | "
                f"{format_number(stats.get('input', 0))} | {format_number(stats.get('output', 0))} | "
                f"{format_number(stats.get('cached', 0))} | {stats.get('calls', 0)} |"
                + ("" if _hidden_daily else f" ¥{stats.get('effective_cost', 0):.2f} |")
            )
        lines.append("")

    # （新增）三、模型使用与成本对比
    lines.extend(build_model_section("md", data))
    lines.extend(build_reconciliation_section("md", data))
    if not _cost_hidden(data):
        # 档位维度的价值全在「倍率 × 估算单价」，tokens_only 下没有可算的钱
        lines.extend(build_tier_section("md", data))

    # （新增）四、成本深度分析（每会话 / 异常 / 省钱）
    lines.extend(build_cost_analysis_section("md", data))

    # 五、任务类型统计
    lines.append("## 五、任务类型统计")
    lines.append("")
    lines.append(
        "> 统计口径：仅含本期有 trace（token 活动）的会话；历史空会话（无 token 活动）不计入，避免虚高。"
    )
    lines.append("")
    if task_dist:
        lines.append("| 任务类型 | 会话数 | 占比 |")
        lines.append("|----------|--------|------|")
        for task_type, count in sorted(
            task_dist.items(), key=lambda x: x[1], reverse=True
        ):
            pct = count / sum(task_dist.values()) * 100 if task_dist else 0
            lines.append(f"| {task_type} | {count} | {pct:.1f}% |")
        lines.append("")
        lines.append(
            "> ℹ️ 「其他」= 无法自动归类到已知任务类型的会话（含无标题且对话内容缺失的会话）。"
        )
        lines.append("")
        lines.append("### 任务类型分布图")
        lines.append("")
        lines.append("```")
        max_val = max(task_dist.values()) if task_dist else 1
        label_w = max((_disp_width(t) for t in task_dist), default=10)
        for task_type, count in sorted(
            task_dist.items(), key=lambda x: x[1], reverse=True
        ):
            bar = "█" * int(20 * count / max_val) if max_val > 0 else ""
            lines.append(f"{_pad_label(task_type, label_w)} |{bar} {count}")
        lines.append("```")
        lines.append("")

    # 五、任务 Token 消耗统计
    lines.append("## 六、任务 Token 消耗统计")
    lines.append("")
    lines.append(
        "按任务类型聚合的 Token 消耗，反映哪类任务最吃 token"
        + ("：" if _cost_hidden(data) else "（含估算成本）：")
    )
    lines.append("")
    task_token_stats = data.get("task_token_stats", [])
    # 过滤掉 0 token 的行（避免表格出现无意义的 0.0% 行）
    display_stats = [s for s in task_token_stats if s.get("effective_tokens", 0) > 0]
    if display_stats:
        total_eff = sum(s.get("effective_tokens", 0) for s in display_stats)
        total_tok = sum(s["total_tokens"] for s in display_stats)
        lines.append(_task_rank_note(data))
        lines.append("")
        _hidden_task = _cost_hidden(data)
        if _hidden_task:
            lines.append(
                "| 任务类型 | 会话数 | 实际消耗 | 原始总Token | 输入Token | 输出Token | 缓存占比 | 占比 |"
            )
            lines.append(
                "|---------|------|---------|-----------|----------|----------|---------|------|"
            )
        else:
            lines.append(
                "| 任务类型 | 会话数 | 实际消耗 | 原始总Token | 输入Token | 输出Token | 缓存占比 | 实际成本 | 占比 |"
            )
            lines.append(
                "|---------|------|---------|-----------|----------|----------|---------|---------|------|"
            )
        for s in display_stats:
            eff = s.get("effective_tokens", 0)
            pct = (eff / total_eff * 100) if total_eff else 0
            c_ratio = (
                (s["cached_tokens"] / s["input_tokens"] * 100)
                if s.get("input_tokens")
                else 0
            )
            lines.append(
                f"| {s['task_type']} | {s['session_count']} | {format_number(eff)} "
                f"| {format_number(s['total_tokens'])} "
                f"| {format_number(s['input_tokens'])} | {format_number(s['output_tokens'])} "
                f"| {c_ratio:.0f}% |"
                + ("" if _hidden_task else f" ¥{s.get('effective_cost', 0):.2f} |")
                + f" {pct:.1f}% |"
            )
        lines.append("")
        lines.append(
            "> ℹ️ 「未关联会话」= trace 的会话 ID 在本地会话库找不到（孤儿 trace，已合并为单一汇总行）；"
        )
        lines.append(
            "> 「未命名会话」= 本地会话库中确有但无标题的会话；「其他」= 任务类型无法自动归类或自动分类失败的 token。"
        )
        lines.append("")
        top = task_token_stats[0]
        top_pct = (top.get("effective_tokens", 0) / total_eff * 100) if total_eff else 0
        if _hidden_task:
            lines.append(
                f"> 🔥 **实际消耗最高的任务类型**：{top['task_type']} —— "
                f"{format_number(top.get('effective_tokens', 0))} token（原始 {format_number(top['total_tokens'])}），"
                f"占 {top_pct:.1f}%。"
            )
        else:
            lines.append(
                f"> 🔥 **实际消耗最高的任务类型**：{top['task_type']} —— "
                f"{format_number(top.get('effective_tokens', 0))} token（原始 {format_number(top['total_tokens'])}），"
                f"占 {top_pct:.1f}%，实际成本 ¥{top.get('effective_cost', 0):.2f}。"
            )
        # 占比图：各任务类型 实际消耗 token 占比（横向条形图，主题安全、不重叠）
        donut = build_task_type_chart_md(display_stats, title=_donut_title(data))
        if donut:
            lines.append("")
            lines.append("**各任务类型 实际消耗 Token 占比**：")
            lines.append("")
            lines.append(donut)
            lines.append("")
        # Top 10 最吃 token 的任务对话框（含自动化任务会话）
        top_tasks = data.get("top_tasks", [])
        if top_tasks:
            lines.append("")
            lines.append(
                "**实际消耗最高的 10 个任务对话框**（含自动化任务，按会话实际消耗排序）："
            )
            lines.append("")
            if _cost_hidden(data):
                lines.append(
                    "| 排名 | 任务名称 | 任务类型 | 实际消耗 | 原始总Token | 缓存占比 |"
                )
                lines.append(
                    "|------|----------|----------|---------|-----------|---------|"
                )
            else:
                lines.append(
                    "| 排名 | 任务名称 | 任务类型 | 实际消耗 | 原始总Token | 缓存占比 | 实际成本 |"
                )
                lines.append(
                    "|------|----------|----------|---------|-----------|---------|---------|"
                )
            for i, tk in enumerate(top_tasks, 1):
                c_ratio = (
                    (tk.get("cached_tokens", 0) / tk["input_tokens"] * 100)
                    if tk.get("input_tokens")
                    else 0
                )
                lines.append(
                    f"| {i} | {tk.get('title', '-')} | {tk.get('task_type', '-')} "
                    f"| {format_number(tk.get('effective_tokens', 0))} "
                    f"| {format_number(tk.get('total_tokens', 0))} "
                    f"| {c_ratio:.0f}% |"
                    + (
                        ""
                        if _cost_hidden(data)
                        else f" ¥{tk.get('effective_cost', 0):.2f} |"
                    )
                )
            lines.append("")
    else:
        lines.append(f"_{_short}无任务 Token 消耗数据_")
    lines.append("")

    # 六、技能使用统计
    lines.append("## 七、技能使用统计")
    lines.append("")
    if skills:
        lines.append("| 技能名称 | 使用次数 | 最近使用 |")
        lines.append("|----------|---------|---------|")
        for sid, sdata in sorted(
            skills.items(),
            key=lambda x: x[1].get("usage_count_in_range", 0),
            reverse=True,
        ):
            lines.append(
                f"| {sid} | {sdata.get('usage_count_in_range', 0)} | {sdata.get('last_used', '-')} |"
            )
        lines.append("")
    else:
        lines.append(f"_{_short}未使用技能_")
        lines.append("")

    # 七、自动化任务运行情况
    lines.append("## 八、自动化任务运行情况")
    lines.append("")
    if automation_runs:
        auto_groups = defaultdict(list)
        for run in automation_runs:
            auto_groups[run.get("automation_id", "unknown")].append(run)
        lines.append(
            "| 任务名称 | 状态 | 运行次数 | 成功 | 失败 | 最近一次结果 | 最近一次运行日期 |"
        )
        lines.append(
            "|---------|------|---------|------|------|----------|----------------|"
        )
        for auto_id, runs in sorted(
            auto_groups.items(), key=lambda x: len(x[1]), reverse=True
        ):
            success = sum(1 for r in runs if r.get("result_success"))
            fail = len(runs) - success
            if runs:
                latest_result = "成功" if runs[-1].get("result_success") else "失败"
            else:
                latest_result = "-"
            label = runs[0].get("automation_name") or auto_id
            auto_state = _auto_state_label(runs[0].get("auto_status"))
            dates = [r.get("created_date", "") for r in runs if r.get("created_date")]
            last_run_date = max(dates) if dates else "-"
            lines.append(
                f"| {label} | {auto_state} | {len(runs)} | {success} | {fail} | {latest_result} | {last_run_date} |"
            )
        lines.append("")
    else:
        lines.append(f"_{_short}无自动化任务运行记录_")
        lines.append("")

    # 八、产出物清单
    lines.append("## 九、产出物清单")
    lines.append("")
    if outputs:
        lines.append("| 文件 | 类型 | 日期 | 大小 |")
        lines.append("|------|------|------|------|")
        for out in outputs[:20]:
            ext = out.get("extension", "").lstrip(".")
            size = format_file_size(out.get("size_bytes", 0))
            lines.append(
                f"| {out.get('file_name', '-')} | {ext or '-'} | {out.get('date', '-')} | {size} |"
            )
        lines.append("")
    else:
        lines.append(f"_{_short}无产出文件_")
        lines.append("")

    # 十、核心洞察与建议（数据驱动：钱优先 + 判断 + 行动）
    lines.append("## 十、核心洞察与建议")
    lines.append("")
    eff_cost = summary.get("total_effective_cost", 0)
    raw_cost = summary.get("total_cost", 0)
    eff_tokens = summary.get("total_effective_tokens", 0)
    cache_saving = max(raw_cost - eff_cost, 0)

    # 💰 花费速览（钱头条，数据驱动）/ tokens_only 下换成用量速览
    if _cost_hidden(data):
        lines.append("### 📈 用量速览")
        lines.append("")
        lines.append(
            f"- 本期实际消耗 **{format_number(eff_tokens)} token**"
            f"（原始 {format_number(summary.get('total_tokens', 0))}），"
            f"计价模式 tokens_only：本期无模型命中单价，**不输出金额与省钱结论**。"
        )
        lines.append("")
    else:
        lines.append("### 💰 花费速览")
        lines.append("")
        lines.append(
            f"- 本期实际花费 **¥{eff_cost:.2f}**（原始口径 ¥{raw_cost:.2f}），缓存复用为你节省约 **¥{cache_saving:.2f}**。"
        )
        session_credits = data.get("session_credits", [])
        if session_credits:
            latest = max(session_credits, key=lambda x: x.get("updated_at", 0))
            used = latest.get("used", 0)
            size = latest.get("size", 0)
            if size > 0:
                lines.append(
                    f"- 当前会话额度已用 **{used / size * 100:.0f}%**（{format_number(used)} / {format_number(size)}）。"
                )
        lines.append("")

    # 🔍 最大成本来源（替代"高峰日"，带数据驱动判断）
    if daily_tokens and eff_tokens:
        peak_day, peak_stats = max(
            daily_tokens.items(), key=lambda x: x[1].get("effective", 0)
        )
        peak_cost = peak_stats.get("effective_cost", 0)
        peak_tok = peak_stats.get("effective", 0)
        peak_share = peak_tok / eff_tokens * 100
        verdict = (
            "占本期实际消耗比重偏高，建议复盘当日是否存在可精简的批量/重复任务"
            if peak_share >= 25
            else "占本期实际消耗比重正常，属单日波动"
        )
        lines.append(
            "### 🔍 最大成本来源" if not _cost_hidden(data) else "### 🔍 最大消耗日"
        )
        lines.append("")
        if _cost_hidden(data):
            lines.append(
                f"- **高峰日 {peak_day}**：{format_number(peak_tok)} token，"
                f"占本期实际消耗 **{peak_share:.1f}%**——{verdict}。"
            )
        else:
            lines.append(
                f"- **高峰日 {peak_day}**：实际花费 ¥{peak_cost:.2f}（{format_number(peak_tok)} token），"
                f"占本期实际消耗 **{peak_share:.1f}%**——{verdict}。"
            )
        lines.append("")

    # 📊 任务类型洞察（加分布形态判断）
    if task_dist:
        total_count = sum(task_dist.values())
        top_task, top_n = max(task_dist.items(), key=lambda x: x[1])
        top_pct = top_n / total_count * 100
        if top_pct >= 50:
            shape = "高度集中于单一类型，建议确认是否为预期工作流"
        elif top_pct >= 25:
            shape = "相对集中，为本期主力任务"
        else:
            shape = "分布较均衡，未见单一类型主导"
        lines.append("### 📊 任务类型洞察")
        lines.append("")
        # 分母只含有 token 活动的会话（§五 D5 口径），不交代会被拿来跟 §一 的会话总数对
        _scope = (
            ""
            if total_count == summary.get("total_sessions")
            else f"，仅统计本期有 token 活动的 {total_count} 个会话"
        )
        lines.append(
            f"- **主要任务类型**：{top_task}（{top_n} 次，{top_pct:.1f}%{_scope}）——{shape}。"
        )
        lines.append("")

    # ✅ 省钱成就（替代"缓存效率优秀"，翻成钱）——tokens_only 下无钱可翻
    if cache_rate > 0 and not _cost_hidden(data):
        lines.append("### ✅ 省钱成就")
        lines.append("")
        lines.append(
            f"- 缓存命中率达 **{cache_rate:.1f}%**，按原始全价计费你本应付约 ¥{raw_cost:.2f}，"
            f"实际仅 ¥{eff_cost:.2f}——**缓存为你省下 ¥{cache_saving:.2f}**，"
            f"是实际成本远低于原始账单的主因。"
        )
        lines.append("")

    # 十、下期展望（基于实际数据动态生成）
    lines.append(f"## 十一、{_next}展望")
    lines.append("")
    lines.append(f"基于{_short}实际数据，先预测下期用量，再按优先级给出行动建议：")
    lines.append("")
    for item in build_next_week_outlook(
        summary,
        daily_tokens,
        automation_runs,
        data.get("session_credits", []),
        period_key=_key,
        cost_hidden=_cost_hidden(data),
        anomaly_days=_token_anomaly_days(data),
        background_runs=(meta.get("background_runs") or {}),
    ):
        lines.append(item)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*%s*" % _footer_text(data))

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# HTML 格式
# ─────────────────────────────────────────────────────────────


# ── 四、成本深度分析（每会话 / 异常 / 省钱）────────────────
def _build_session_cwd_maps(data):
    """构建两个 session 映射：
      - sessions_by_cwd: cwd -> [session_id, ...]
      - session_cost_by_id: session_id -> effective_cost
    用于 §4.5 失败自动化成本归因（automation_runs 通过 source_cwd ↔ sessions.cwd 关联）。
    """
    sessions_by_cwd = {}
    for s in data.get("sessions") or []:
        cwd = s.get("cwd")
        if not cwd:
            continue
        sessions_by_cwd.setdefault(cwd, []).append(s.get("id"))
    session_cost_by_id = {}
    for r in (data.get("session_stats") or {}).get("rows") or []:
        sid = r.get("session_id")
        if sid:
            session_cost_by_id[sid] = r.get("effective_cost", 0.0)
    return sessions_by_cwd, session_cost_by_id


def _compute_failed_automation_cost(
    automation_runs, sessions_by_cwd, session_cost_by_id
):
    """按 automation_id 聚合失败自动化的浪费成本。

    数据模型说明：automation_runs.thread_id 是「run-{ts}-{n}」格式的内部 run ID，
    与 sessions.id（UUID）不是同一套标识系统，因此无法直接 1:1 关联。本函数采用
    cwd 作为桥接键：每个 automation 涉及一组唯一 source_cwd，匹配 sessions.cwd 后
    累加这些会话的有效成本，再除以运行次数得到「平均单次成本」。

    估算口径：
      - 单 cwd 单会话（如手动测试）：归因准确。
      - 多 cwd / 单 cwd 多会话：可能高估（混入了同工作区的交互会话成本）。
      - 失败重试场景下，实际失败成本可能略高于平均；本估算取平均属保守口径。
    只读，不写任何配置；apply 动作（F8/v2）不触发。
    """
    if not automation_runs or not sessions_by_cwd or not session_cost_by_id:
        return []
    groups = {}
    for r in automation_runs:
        groups.setdefault(r.get("automation_id") or "unknown", []).append(r)
    out = []
    for auto_id, runs in groups.items():
        fail = sum(1 for x in runs if not x.get("result_success"))
        if fail == 0:
            continue
        unique_cwds = {x.get("source_cwd") for x in runs if x.get("source_cwd")}
        total_cost = 0.0
        matched_session_count = 0
        matched_cwd_count = 0
        for cwd in unique_cwds:
            sids = sessions_by_cwd.get(cwd) or []
            if not sids:
                continue
            matched_cwd_count += 1
            matched_session_count += len(sids)
            for sid in sids:
                total_cost += session_cost_by_id.get(sid, 0.0)
        total_runs = len(runs)
        avg_cost = total_cost / total_runs if total_runs else 0.0
        waste = fail * avg_cost
        fail_rate = fail / total_runs * 100 if total_runs else 0
        # D3：匹配到会话但其成本全为 0（多为幽灵 / 空 trace）时，标记「成本未解析」，
        # 渲染层据此显示「无法估算」而非误导性的 ¥0.00。
        unresolved = matched_session_count > 0 and total_cost == 0
        out.append(
            {
                "name": runs[0].get("automation_name") or auto_id,
                "state": _auto_state_label(runs[0].get("auto_status")),
                "total_runs": total_runs,
                "fail": fail,
                "fail_rate": fail_rate,
                "avg_cost": avg_cost,
                "waste": waste,
                "cwd_count": len(unique_cwds),
                "matched_cwd_count": matched_cwd_count,
                "matched_session_count": matched_session_count,
                "unresolved": unresolved,
            }
        )
    out.sort(key=lambda x: x["waste"], reverse=True)
    return out


def _render_failed_automation(fmt, items):
    if not items:
        return []
    if fmt == "md":
        lines = []
        lines.append("### 4.5 失败自动化成本归因")
        lines.append("")
        lines.append(
            "> 💸 失败运行 = 消耗 token 但无产出。下列自动化本月存在失败运行，"
            "按「失败次数 × 该任务所在工作区平均单次成本」估算白白烧掉的成本。"
        )
        lines.append(
            "> ⚠️ 估算口径：通过 `automation.source_cwd ↔ sessions.cwd` 关联；"
            "若同一工作区下含多个会话（含交互），平均成本可能略高估。"
        )
        lines.append("")
        lines.append(
            "| 自动化任务 | 状态 | 运行 | 失败 | 失败率 | 平均单次成本 | 估算浪费 |"
        )
        lines.append(
            "|-----------|------|------|------|--------|-------------|---------|"
        )
        for r in items:
            warn = " ⚠️" if r["fail_rate"] >= 30 else ""
            if r.get("unresolved"):
                avg_disp = "¥—（成本未解析）"
                waste_disp = "¥—（成本未解析）"
            else:
                avg_disp = f"¥{r['avg_cost']:.2f}"
                waste_disp = f"¥{r['waste']:.2f}"
            lines.append(
                f"| {r['name']}{warn} | {r['state']} | {r['total_runs']} | {r['fail']} | "
                f"{r['fail_rate']:.0f}% | {avg_disp} | {waste_disp} |"
            )
        lines.append("")
        total_waste = sum(r["waste"] for r in items)
        lines.append(
            f"> 💸 **本月失败自动化总浪费估算：¥{total_waste:.2f}**"
            "（按失败次数 × 该任务所在工作区平均单次成本推算）。"
        )
        if any(r.get("unresolved") for r in items):
            lines.append(
                "> ⚠️ 部分失败任务的成本未解析（会话无 token 或模型未解析），其浪费无法估算，"
                "上表「总浪费」为可解析部分的下限，实际可能更高。"
            )
        lines.append(
            "> 建议：失败率 ≥ 30% 的任务优先排查依赖环境与配置，或暂停直至修复。"
            "（apply 动作属 F8/v2，本节仅提供洞察。）"
        )
        lines.append("")
        return lines
    # html
    L = []
    L.append("        <h3>4.5 失败自动化成本归因</h3>")
    L.append(
        "        <p>💸 失败运行 = 消耗 token 但无产出。"
        "按「失败次数 × 该任务所在工作区平均单次成本」估算白白烧掉的成本。</p>"
    )
    L.append(
        "        <p>⚠️ 估算口径：通过 automation.source_cwd ↔ sessions.cwd 关联；"
        "若同一工作区下含多个会话（含交互），平均成本可能略高估。</p>"
    )
    L.append("        <table>")
    L.append(
        "            <tr><th>自动化任务</th><th>状态</th><th>运行</th><th>失败</th>"
        "<th>失败率</th><th>平均单次成本</th><th>估算浪费</th></tr>"
    )
    for r in items:
        warn = " ⚠️" if r["fail_rate"] >= 30 else ""
        if r.get("unresolved"):
            avg_disp = "¥—（成本未解析）"
            waste_disp = "¥—（成本未解析）"
        else:
            avg_disp = f"¥{r['avg_cost']:.2f}"
            waste_disp = f"¥{r['waste']:.2f}"
        L.append(
            f"            <tr><td>{_esc(r['name'])}{warn}</td><td>{r['state']}</td>"
            f"<td>{r['total_runs']}</td><td>{r['fail']}</td>"
            f"<td>{r['fail_rate']:.0f}%</td><td>{avg_disp}</td>"
            f"<td>{waste_disp}</td></tr>"
        )
    L.append("        </table>")
    total_waste = sum(r["waste"] for r in items)
    L.append(
        f"        <p>💸 <b>本月失败自动化总浪费估算：¥{total_waste:.2f}</b>"
        f"（按失败次数 × 该任务所在工作区平均单次成本推算）。</p>"
    )
    if any(r.get("unresolved") for r in items):
        L.append(
            '        <p style="color:var(--disclaimer-fg)">⚠️ 部分失败任务的成本未解析（会话无 token 或模型未解析），'
            "其浪费无法估算，上表「总浪费」为可解析部分的下限，实际可能更高。</p>"
        )
    L.append(
        "        <p>建议：失败率 ≥ 30% 的任务优先排查依赖环境与配置，或暂停直至修复。"
        "（apply 动作属 F8/v2，本节仅洞察。）</p>"
    )
    return L


def _compute_session_size_anomalies(rows):
    """会话规模（调用次数）异常检测。纯只读。

    threshold = max(p95(calls), 200)，top 5 按 calls 降序。
    p95 用与 §4.3 顶部「会话级 p95（调用次数）」相同的线性插值百分位
    （ca_aggregate._percentile），且输入集合同为全部会话行——避免同一节里
    先报 436、后报 376 两个不一致的 p95。
    """
    if not rows:
        return None
    calls = sorted(r.get("calls", 0) for r in rows)
    if not calls:
        return None
    n = len(calls)
    idx = 0.95 * (n - 1)
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    p95_calls = calls[lo] * (1 - (idx - lo)) + calls[hi] * (idx - lo)
    threshold = max(p95_calls, 200)
    items = sorted(
        [r for r in rows if r.get("calls", 0) > threshold],
        key=lambda x: x.get("calls", 0),
        reverse=True,
    )
    return {"threshold": threshold, "p95": p95_calls, "items": items[:5]}


def _compute_cache_and_untitled(data, threshold_pct=60.0):
    """缓存健康度卡 + 未命名高成本会话提示。纯只读。

    O4：从 traces 聚合每会话 cache_rate，找出 < threshold 的会话，
       按「(全局缓存率 - 当前缓存率) × 当前成本 × 0.5」估算可省（保守口径）。
    O6：未命名 / 标题为「未命名会话」且成本 ≥ 会话级 p95 的会话。
    """
    summary = data.get("summary", {})
    total_cached = summary.get("total_cached_tokens", 0)
    total_input = summary.get("total_input_tokens", 0)
    global_cache_rate = (total_cached / total_input * 100) if total_input else 0

    traces = data.get("traces") or []
    sessions = data.get("sessions") or []
    known_session_ids = {s.get("id") for s in sessions}
    rows = (data.get("session_stats") or {}).get("rows", [])
    if not rows:
        return None

    sess_cache = defaultdict(lambda: {"cached": 0, "input": 0})
    for t in traces:
        sid = t.get("session_id")
        if not sid:
            continue
        sess_cache[sid]["cached"] += t.get("cached_tokens", 0) or 0
        sess_cache[sid]["input"] += t.get("input_tokens", 0) or 0

    sid_to_meta = {}
    for s in sessions:
        sid = s.get("id")
        if sid:
            sid_to_meta[sid] = {"title": s.get("title") or ""}
    for r in rows:
        sid = r.get("session_id")
        if sid:
            sid_to_meta.setdefault(sid, {"title": ""})
            sid_to_meta[sid].update(
                {
                    "cost": r.get("effective_cost", 0.0),
                    "calls": r.get("calls", 0),
                    "task_type": r.get("task_type", "其他"),
                    "first_date": r.get("first_date", ""),
                }
            )

    # O4：缓存健康度
    cache_items = []
    for sid, st in sess_cache.items():
        if st["input"] <= 0:
            continue
        cr = st["cached"] / st["input"] * 100
        if cr < threshold_pct:
            meta = sid_to_meta.get(sid, {})
            cost = meta.get("cost", 0.0)
            gap = max(global_cache_rate - cr, 0)
            saving = cost * (gap / 100) * 0.5  # 保守估算：差距一半可补
            cache_items.append(
                {
                    "title": (
                        meta.get("title")
                        or (
                            ORPHAN_LABEL
                            if sid not in known_session_ids
                            else UNNAMED_LABEL
                        )
                    )[:30],
                    "task_type": meta.get("task_type", "其他"),
                    "cache_rate": cr,
                    "calls": meta.get("calls", 0),
                    "cost": cost,
                    "potential_saving": saving,
                }
            )
    cache_items.sort(key=lambda x: x["potential_saving"], reverse=True)
    cache_health = {
        "global_rate": global_cache_rate,
        "threshold": threshold_pct,
        "items": cache_items[:5],
        "total_potential": sum(x["potential_saving"] for x in cache_items),
    }

    # O6：未命名高成本会话
    costs = sorted([r.get("effective_cost", 0) for r in rows])
    n = len(costs)
    cost_p95 = costs[max(0, int(n * 0.95) - 1)] if costs else 0
    untitled = []
    for r in rows:
        title = r.get("title", "")
        cost = r.get("effective_cost", 0)
        if (not title or title == UNNAMED_LABEL) and cost >= cost_p95 and cost > 0:
            untitled.append(
                {
                    "title": title or "未命名会话",
                    "task_type": r.get("task_type", "其他"),
                    "cost": cost,
                    "calls": r.get("calls", 0),
                    "first_date": r.get("first_date", ""),
                }
            )
    untitled.sort(key=lambda x: x["cost"], reverse=True)

    # D4：本期成本整体未解析（多为幽灵 / 空 trace）时，缓存可省金额无法量化，标记之。
    cost_unresolved = summary.get("total_effective_cost", 0) == 0
    return {
        "cache_health": cache_health,
        "untitled": untitled[:5],
        "cost_p95": cost_p95,
        "cost_unresolved": cost_unresolved,
    }


def _render_cache_untitled(fmt, payload):
    if not payload:
        return []
    ch = payload["cache_health"]
    if fmt == "md":
        lines = []
        lines.append("### 4.6 缓存健康度与未命名高成本会话")
        lines.append("")
        lines.append(
            f"> 💡 全局缓存命中率 **{ch['global_rate']:.1f}%**——"
            f"提升缓存复用是「零质量风险」的直接省钱杠杆。"
            f"下列会话缓存率 < {ch['threshold']}%。"
        )
        lines.append("")
        if ch["items"]:
            lines.append(
                "**📉 缓存健康度卡**（保守估算「差距 × 0.5 × 当前成本」为可省空间）："
            )
            lines.append("")
            lines.append(
                "| 任务名称 | 任务类型 | 缓存率 | 调用 | 当前成本 | 估算可省 |"
            )
            lines.append("|---------|---------|--------|------|---------|---------|")
            for r in ch["items"]:
                lines.append(
                    f"| {r['title']} | {r['task_type']} | {r['cache_rate']:.0f}% | "
                    f"{r['calls']} | ¥{r['cost']:.2f} | ¥{r['potential_saving']:.2f} |"
                )
            lines.append("")
            lines.append(
                f"> 💰 **缓存潜力总省：¥{ch['total_potential']:.2f}**"
                "（F8 prompt-caching 可承接）。"
            )
            lines.append("")
        else:
            lines.append(
                f"- 当前所有会话缓存率均 ≥ {ch['threshold']}%，暂无明显缓存优化空间。"
            )
            lines.append("")
        if payload.get("cost_unresolved"):
            lines.append(
                "> ⚠️ 缓存潜力估算不可用：本期成本未解析（多为幽灵 / 空 trace），无法量化可省金额；"
                "请先解决 §4 顶部的数据缺失提示。"
            )
            lines.append("")
        if payload["untitled"]:
            lines.append(
                f"**⚠️ 未命名高成本会话**（成本 ≥ ¥{payload['cost_p95']:.2f}"
                " = 会话级 p95，建议补标题便于归因）："
            )
            lines.append("")
            lines.append("| 标题 | 任务类型 | 实际成本 | 调用 | 日期 |")
            lines.append("|------|---------|---------|------|------|")
            for r in payload["untitled"]:
                lines.append(
                    f"| ⚠️ {r['title']} | {r['task_type']} | ¥{r['cost']:.2f} | "
                    f"{r['calls']} | {r['first_date']} |"
                )
            lines.append("")
        return lines
    # html
    L = []
    L.append("        <h3>4.6 缓存健康度与未命名高成本会话</h3>")
    L.append(
        f"        <p>💡 全局缓存命中率 <b>{ch['global_rate']:.1f}%</b>——"
        "提升缓存复用是「零质量风险」的直接省钱杠杆。"
        f"下列会话缓存率 &lt; {ch['threshold']}%。</p>"
    )
    if ch["items"]:
        L.append(
            "        <p><b>📉 缓存健康度卡</b>（保守估算「差距 × 0.5 × 当前成本」为可省空间）：</p>"
        )
        L.append("        <table>")
        L.append(
            "            <tr><th>任务名称</th><th>任务类型</th><th>缓存率</th>"
            "<th>调用</th><th>当前成本</th><th>估算可省</th></tr>"
        )
        for r in ch["items"]:
            L.append(
                f"            <tr><td>{_esc(r['title'])}</td><td>{_esc(r['task_type'])}</td>"
                f"<td>{r['cache_rate']:.0f}%</td><td>{r['calls']}</td>"
                f"<td>¥{r['cost']:.2f}</td><td>¥{r['potential_saving']:.2f}</td></tr>"
            )
        L.append("        </table>")
        L.append(
            f"        <p>💰 <b>缓存潜力总省：¥{ch['total_potential']:.2f}</b>"
            "（F8 prompt-caching 可承接）。</p>"
        )
    else:
        L.append(
            f"        <p>当前所有会话缓存率均 ≥ {ch['threshold']}%，"
            "暂无明显缓存优化空间。</p>"
        )
    if payload.get("cost_unresolved"):
        L.append(
            '        <p style="color:var(--disclaimer-fg)">⚠️ 缓存潜力估算不可用：本期成本未解析'
            "（多为幽灵 / 空 trace），无法量化可省金额；请先解决 §4 顶部的数据缺失提示。</p>"
        )
    if payload["untitled"]:
        L.append(
            f"        <p><b>⚠️ 未命名高成本会话</b>（成本 ≥ ¥{payload['cost_p95']:.2f}"
            " = 会话级 p95，建议补标题便于归因）：</p>"
        )
        L.append("        <table>")
        L.append(
            "            <tr><th>标题</th><th>任务类型</th><th>实际成本</th>"
            "<th>调用</th><th>日期</th></tr>"
        )
        for r in payload["untitled"]:
            L.append(
                f"            <tr><td>⚠️ {_esc(r['title'])}</td><td>{_esc(r['task_type'])}</td>"
                f"<td>¥{r['cost']:.2f}</td><td>{r['calls']}</td>"
                f"<td>{r['first_date']}</td></tr>"
            )
        L.append("        </table>")
    return L


def _unresolved_call_stats(data):
    """统计「未解析 / 幽灵」调用，供 §1 / §4 警告卡使用。

    早期 WorkBuddy trace 可能同时缺失 sessionId、modelInfo（被 collect 兜底记为字面量
    'default' 且 token 全 0），这类调用无法归属到模型 / 会话 / 成本——须显式提示，
    而非静默记为 ¥0.00。
    """
    traces = data.get("traces", [])
    n_default = sum(1 for t in traces if (t.get("raw_model") or "") == "default")
    n_no_session = sum(1 for t in traces if not t.get("session_id"))
    n_no_tokens = sum(
        1
        for t in traces
        if (t.get("input_tokens", 0) or 0) + (t.get("output_tokens", 0) or 0) == 0
    )
    return {
        "total": len(traces),
        "default": n_default,
        "no_session": n_no_session,
        "no_tokens": n_no_tokens,
    }


def _unresolved_warning_md(stats):
    """Markdown 警告卡：列出未解析 / 幽灵调用的占比与影响。无异常时返回空串。"""
    if stats["default"] == 0 and stats["no_session"] == 0 and stats["no_tokens"] == 0:
        return ""
    try:
        from collect_usage_data import DEFAULT_MODEL
    except (ImportError, AttributeError):
        DEFAULT_MODEL = "（未配置）"
    parts = []
    if stats["default"]:
        parts.append(
            f"{stats['default']} 次调用模型未解析（记为 `default`，缺 modelInfo 无真实模型名），"
            f"已按默认模型 `{DEFAULT_MODEL}` 口径估算；若不符请改 collect 脚本的 DEFAULT_MODEL 常量"
        )
    if stats["no_session"]:
        parts.append(
            f"{stats['no_session']} 次调用缺 sessionId，未计入「每会话成本」分析"
        )
    if stats["no_tokens"]:
        parts.append(f"{stats['no_tokens']} 次调用无 token 数据，未计入成本")
    pct = ""
    if stats["total"]:
        unresolved = stats["default"] or stats["no_tokens"]
        if unresolved:
            pct = f"（占本期 {stats['total']} 次调用的约 {round(unresolved / stats['total'] * 100)}%）"
    return (
        "> ⚠️ **未解析 / 幽灵调用提示**" + pct + "：" + "；".join(parts) + "。\n"
        "> 这些调用并非「免费」，而是数据缺失导致无法计费——请结合上方各章节交叉核对。\n"
    )


def _fmt_anom_val(v, is_cost):
    return f"¥{v:.2f}" if is_cost else f"{v:,.0f} token"


def _compute_free_token_share(data):
    """估算本期「有效 Token 中来自零成本（免费 / 限时免费 / 未计费）调用」的比例。

    用于判断本期是否为免费主导期，从而给出 §4 免责声明。优先用逐 trace 数据（精确）；
    退化到每日统计（日级，免费+付费可能同日记一日，略粗略）。
    """
    traces = data.get("traces") or []
    if traces:
        total_eff = sum(t.get("effective_tokens", 0) for t in traces)
        if not total_eff:
            return 1.0
        free_eff = sum(
            t.get("effective_tokens", 0)
            for t in traces
            if t.get("effective_cost", 0) == 0
        )
        return free_eff / total_eff
    daily = data.get("daily_tokens", {}) or {}
    total_eff = sum(d.get("effective", 0) for d in daily.values())
    if not total_eff:
        return 1.0
    free_eff = sum(
        d.get("effective", 0) for d in daily.values() if d.get("effective_cost", 0) == 0
    )
    return free_eff / total_eff


def _free_period_disclaimer(fmt, data):
    """若本期为免费 / 限时免费主导期，返回免责声明段落；否则返回 []。"""
    free_share = _compute_free_token_share(data)
    total_eff_cost = (data.get("summary", {}) or {}).get("total_effective_cost", 0) or 0
    free_dominant = (free_share >= 0.8) or (total_eff_cost == 0)
    if not free_dominant:
        return []
    pct = round(free_share * 100)
    if fmt == "md":
        return [
            f"> 🎁 **本期以免费 / 限时免费模型为主**（约 {pct}% 的有效 Token 来自零成本调用）。",
            ">",
            "> 成本相关洞察（§4.4 省钱杠杆、§4.5 失败自动化成本归因、§4.6 未命名高成本会话）在免费期参考意义有限；",
            "> 请重点参考 **§4.3 Token 口径异常**（捕捉免费日的高 Token 峰值）与 **§4.6 缓存健康度**（与计费无关，始终有效）。",
            "",
        ]
    return [
        '        <div class="disclaimer-box">',
        f"            <b>🎁 本期以免费 / 限时免费模型为主</b>（约 {pct}% 的有效 Token 来自零成本调用）。",
        "            <p>成本相关洞察（§4.4 省钱杠杆、§4.5 失败自动化成本归因、§4.6 未命名高成本会话）在免费期参考意义有限；"
        "请重点参考 <b>§4.3 Token 口径异常</b>（捕捉免费日的高 Token 峰值）与 <b>§4.6 缓存健康度</b>（与计费无关，始终有效）。</p>",
        "        </div>",
    ]


# —— 成本置信度 ——
# 背景：静态价表（pricing.json）在数学上无法表达「服务端时段减免 / 用户免费额度」，
# 导致部分模型（如 hy4-preview 夜间免费）的估算严重高于实际账单。
# 对策不是让价表变准（做不到），而是让报告**明确告诉用户你在看哪一级**：
#   L1 真值 —— 导入官方用量导出后的「积分」字段
#   L2 估算 —— 未导入（默认路径），静态价表推算，仅供参考
_COST_SOURCE_LABEL = {
    "official": ("L1 真值", "✅"),
    "estimate": ("L2 估算", "⚠️"),
}


def _low_conf_map(data):
    """本期 meta 里的成本置信度配置：模型名 -> 偏差原因。"""
    return (data.get("meta", {}) or {}).get("low_confidence", {}) or {}


def _low_conf_bias_map(data):
    """本期 meta 里的成本置信度偏差方向：模型名 -> over/under/mixed。"""
    return (data.get("meta", {}) or {}).get("low_confidence_bias", {}) or {}


# 低置信度模型要「够贵」才值得高位告警：既在 Top-N 里，又占总花费 ≥ 该比例。
# 否则 ¥0.01 的促销模型也会因为「第 2 贵」而弹告警，纯粹是噪音。
LC_ALERT_TOP_N = 3
LC_ALERT_MIN_SHARE = 0.05


def _lc_top_alert(data):
    """判断低置信度模型是否「贵到值得高位告警」。

    条件（同时满足）：
      - 该模型在本期付费模型中排名 Top-3（含并列）
      - 且其花费占付费总额 ≥ 5%（避免 ¥0.01 的模型也弹告警）

    返回 dict(model, cost, rank, arrow, share) 或 None。
    """
    lc_map = _low_conf_map(data)
    if not lc_map:
        return None
    bias_map = _low_conf_bias_map(data)
    stats = (data.get("model_stats") or []) + (data.get("model_exec_stats") or [])
    # 同一模型可能同时出现在两个维度，先按模型名归并取最大花费，避免重复计数
    agg = {}
    for m in stats:
        name = (m.get("model") or "").strip()
        if not name:
            continue
        cost = m.get("effective_cost", 0) or 0
        if cost > agg.get(name, 0):
            agg[name] = cost
    paid = {n: c for n, c in agg.items() if c > 0}
    if not paid:
        return None
    total = sum(paid.values())
    if total <= 0:
        return None
    lc_paid = {n: c for n, c in paid.items() if _lc_reason(n, lc_map)}
    if not lc_paid:
        return None
    rank = sorted(paid.items(), key=lambda kv: kv[1], reverse=True)
    top_lc = max(lc_paid.items(), key=lambda kv: kv[1])
    idx = next((i for i, (n, _) in enumerate(rank, 1) if n == top_lc[0]), None)
    if idx is None or idx > LC_ALERT_TOP_N:
        return None
    share = top_lc[1] / total
    if share < LC_ALERT_MIN_SHARE:
        return None
    return {
        "model": top_lc[0],
        "cost": top_lc[1],
        "rank": idx,
        "arrow": _lc_arrow(_lc_bias(top_lc[0], bias_map)),
        "share": share,
    }


def _low_conf_hits(data):
    """本期实际出现、且被标为低置信度的模型 -> 原因（按模型名排序）。"""
    lc = _low_conf_map(data)
    if not lc:
        return {}
    hits = {}
    for m in (data.get("model_stats") or []) + (data.get("model_exec_stats") or []):
        name = (m.get("model") or "").strip()
        if not name or (m.get("calls", 0) or 0) <= 0:
            continue
        reason = lc.get(name) or lc.get(name.lower())
        if reason:
            hits.setdefault(name, reason)
    return dict(sorted(hits.items()))


def _official_import(data):
    """本期导入的官方用量导出（未导入返回 None）。"""
    off = data.get("official_usage")
    return off if isinstance(off, dict) and off.get("by_model") is not None else None


def _cost_mode(data):
    """计价模式：'tokens_only' 或 'priced'。

    缺失该字段的历史 JSON 一律按 'priced' 处理——报告口径不得因为升级而回头改变
    既有数据文件的呈现（也让 §四/§三 的既有测试断言零漂移）。
    """
    meta = (data or {}).get("meta", {}) or {}
    return (
        "tokens_only"
        if str(meta.get("cost_mode") or "priced") == "tokens_only"
        else "priced"
    )


def _cost_hidden(data):
    """本报告是否应隐藏金额维度（Tokens-only 口径）。"""
    return _cost_mode(data) == "tokens_only"


def _is_l1(data):
    """成本是否为 L1 真值（已导入官方用量导出）。"""
    meta = data.get("meta", {}) or {}
    return str(meta.get("cost_source") or "estimate").lower() == "official" and bool(
        _official_import(data)
    )


# 数据源 → (报告标题, 数据来源一行文案, 数据来源清单[JSON 用])。
# workbuddy / 缺失 source 一律沿用历史文案，既有报告与测试断言零漂移；
# 外部适配器（claude-code / codex / qwenwork）用自己的名字，不再冒充 WorkBuddy。
_SOURCE_LABELS = {
    "workbuddy": (
        "Workbuddy使用情况报告",
        "WorkBuddy 会话历史、Traces、workbuddy.db、技能使用记录、自动化配置",
        ["WorkBuddy 会话历史", "Traces", "workbuddy.db", "技能使用记录", "自动化配置"],
    ),
    "claude-code": (
        "Claude Code 使用情况报告",
        "Claude Code 会话 JSONL（~/.claude/projects/**/*.jsonl）",
        ["Claude Code 会话 JSONL"],
    ),
    "codex": (
        "Codex CLI 使用情况报告",
        "Codex CLI rollout JSONL（~/.codex/sessions/**/rollout-*.jsonl）",
        ["Codex CLI rollout JSONL"],
    ),
    "qwenwork": (
        "千问办公使用情况报告",
        "千问办公会话转录（~/.qwenworkcn/projects）、逐次调用日志（logs/runs）、"
        "agents.db 会话元信息",
        [
            "千问办公会话转录 projects/*.jsonl",
            "逐次调用日志 logs/runs/qodercli.log",
            "agents.db 会话元信息",
        ],
    ),
    "dumate": (
        # 数据源名为 dumate，但 ~/.workbuddy 数据布局里没有任何字段能区分它到底
        # 来自百度搭子还是 WorkBuddy ——归属未证实（实测 217 会话里
        # qianfan/dumate 命中 0 行）。故标题用中性措辞、不暗示确认的百度搭子归属，
        # 并在数据来源行与清单里强制标注「归属未证实、勿据此当作百度搭子用量」，
        # 避免把某产品的用量误标成另一产品（SDI-4）。
        "Dumate 数据源使用情况报告（数据归属未证实）",
        "通用 WorkBuddy 布局数据源（数据位于 ~/.workbuddy）：会话历史、Traces、"
        "workbuddy.db、技能使用记录、自动化配置。⚠️ 归属未证实——记录中无任何字段"
        "能区分数据来自百度搭子还是 WorkBuddy，内容可能完全是 WorkBuddy 的，"
        "请勿将其作为百度搭子用量引用或对外发布。",
        ["通用 WorkBuddy 布局数据（会话历史）", "Traces", "workbuddy.db",
         "技能使用记录", "自动化配置",
         "⚠️ 数据归属未证实，勿当作百度搭子用量引用"],
    ),
}


def _source_key(data):
    """本次报告的数据源标识（缺失时按历史默认 workbuddy 处理）。"""
    meta = (data or {}).get("meta", {}) or {}
    return str(meta.get("source") or "workbuddy").strip().lower()


def _source_identity(data):
    """返回 (报告标题, 数据来源文案, 数据来源清单)；未知源给出通用兜底。"""
    src = _source_key(data)
    if src in _SOURCE_LABELS:
        return _SOURCE_LABELS[src]
    return ("%s 使用情况报告" % src, "%s 数据源适配器" % src, ["%s 数据源适配器" % src])


def _cost_supported(data):
    """该数据源在语义上是否支持「计费」维度（由适配器显式声明，不由单价是否为 0 推断）。

    千问办公是积分订阅制、账号级积分无法归因到单个会话，适配器里写死
    `SUPPORTS_COST = False`：即便将来用户在 pricing.local.json 填了单价，
    算出来的 ¥ 也是无法对账的虚构值，因此「缺失单价模型 + 补价 stub」整块
    对该源永远不该出现（真要金额请显式 --cost-mode priced 并接受其口径）。
    历史 JSON 没有 meta.cost_supported 字段 → 按 True 处理，WorkBuddy 呈现零变化。
    """
    meta = (data or {}).get("meta", {}) or {}
    return meta.get("cost_supported", True) is not False


def _show_unconfigured_block(data):
    """「本期有未配置单价的模型」整块（含 pricing.local.json 复制 stub）是否输出。

    压制条件（任一成立即压掉）：
      1. tokens_only —— 顶部横幅已说明「为什么没金额、怎么强制出」，正文再摆一张
         未配置表 + 补价 stub，与「不出计费口径」自相矛盾；
      2. 数据源不支持计费（SUPPORTS_COST=False）—— 给了 stub 也是引导用户造
         无法对账的虚构金额。
    priced 且该源支持计费、且只是**部分**模型缺价时保留 —— 那时它真有用。
    """
    return _cost_supported(data) and not _cost_hidden(data)


# ── token-only 口径下的措辞（与 priced 分支一一对应，MD / HTML 共用）────────


def _eff_token_label(data):
    """「实际消耗 Token」标签：tokens_only 下不带「（计费等效）」后缀。"""
    return "实际消耗 Token" if _cost_hidden(data) else "实际消耗 Token（计费等效）"


def _cache_rate_note(data):
    """缓存占比的解释：tokens_only 下不提「按 1/10 价计费」这种计费细节。"""
    if _cost_hidden(data):
        return "缓存命中 token 占输入 token 的比例"
    return "缓存命中按约 1/10 价计费，不计入实际消耗全价"


def _task_rank_note(data):
    """§六 表前说明（MD 引用块版）。"""
    if _cost_hidden(data):
        return (
            "> 排名按「实际消耗」排序；「缓存占比」高说明该任务大量复用同一段上下文"
            "（如连续多轮生成）。"
        )
    return (
        "> 排名按「实际消耗（计费等效）」排序：缓存命中 token 按约 1/10 价计费，不按全价，"
        "故不虚高；「缓存占比」高说明该任务大量复用同一段上下文（如连续多轮生成），"
        "看起来 token 多但实际便宜。"
    )


def _donut_title(data):
    return (
        "实际消耗 Token 占比（按任务类型）"
        if _cost_hidden(data)
        else "实际消耗 Token 占比（按任务类型，计费等效）"
    )


def _calls_granularity_note(data):
    """§一 调用次数的粒度括注（MD 版，不含外层括号）。

    WorkBuddy 的 trace 是 generation 粒度（一次请求内含多轮生成），
    千问办公的 trace 是**逐次模型调用**（按 requestId 归并、来自调用日志），
    两者量级与含义都不同——套同一句话会把真值说成"不等于请求数"。
    """
    if _source_key(data) == "qwenwork":
        return (
            "**逐次模型调用粒度**：按 `requestId` 归并，取自逐次调用日志，"
            "与「请求数」同一量级"
        )
    return "**generation 粒度**：一次请求内部可含多轮生成，**不等于**官方「请求数」"


def _calls_granularity_short(data):
    """HTML 统计卡用的短标签（纯文本、无 markdown 星号）。"""
    return "逐次模型调用" if _source_key(data) == "qwenwork" else "generation 粒度"


def _is_unknown_model_trace(t):
    """该 trace 是否属于「未知模型」——采集层已把这类 cost 强制记 0。

    判据必须与 ca_sources.collect_traces 的 `is_unknown_model` 严格一致：
    `exec_model` 与 `raw_model` **都**归一为 default 才算未知。只看其中一个会漏判——
    会话声明了 default 但 trace 记录了真模型名时，模型是已知的，费用照实计。
    """
    return (
        normalize_model(t.get("exec_model") or "") == "default"
        and normalize_model(t.get("raw_model") or "") == "default"
    )


def _call_count_breakdown(data):
    """§一 调用次数的完整口径分解（MD / HTML 共用，避免两版渲染漂移）。

    返回 dict：
      billable    有效调用次数（概览「调用次数」用它）
      unresolved  未解析/幽灵次数（未知模型 或 token 全 0）——不计费
      unknown     其中「未知模型」次数——已按 0 计价，需在文案里说明
      error       失败调用次数——不计入 billable
      granularity 粒度说明（MD 版带 markdown）
      granularity_short 粒度说明（纯文本，给 HTML 统计卡）
    """
    summary = (data or {}).get("summary", {}) or {}
    traces = (data or {}).get("traces", []) or []
    unknown = sum(1 for t in traces if _is_unknown_model_trace(t))
    # 幽灵：模型名能解析但 token 全 0 —— 与「未知模型」是两种不同的不计费原因
    ghost = sum(
        1
        for t in traces
        if not _is_unknown_model_trace(t)
        and ((t.get("input_tokens", 0) or 0) + (t.get("output_tokens", 0) or 0)) == 0
    )
    # 失败调用：优先用采集层打的 is_error，回退到 status（外部数据源可能没这个标记）
    error = sum(
        1
        for t in traces
        if t.get("is_error") is True or t.get("status") == "error"
    )
    unresolved = unknown + ghost
    # 有效调用 = 总 trace - 失败 - 未解析。summary.total_effective_traces 是采集层
    # 已算好的值（只扣 error），但它不扣未解析；这里以本地分解为准，
    # 保证「概览调用次数」与括注里的两笔扣减自洽（否则读者加不出这个数）。
    billable = max(len(traces) - unresolved - error, 0)
    return {
        "billable": billable,
        "unresolved": unresolved,
        "unknown": unknown,
        "ghost": ghost,
        "error": error,
        "granularity": _calls_granularity_note(data),
        "granularity_short": _calls_granularity_short(data),
    }


def _calls_note_md(data, bd):
    """§一 调用次数的口径括注（MD 版，含外层括号）。"""
    parts = []
    if bd["error"]:
        parts.append(f"{bd['error']} 次失败调用未计入有效调用")
    if bd["unknown"]:
        parts.append(f"{bd['unknown']} 次未知模型未计入费用")
    if bd["ghost"]:
        parts.append(f"{bd['ghost']} 次未解析不计费")
    parts.append(bd["granularity"])
    note = "（" + "；".join(parts) + "）"
    if _is_l1(data):
        note += f"；官方导出同期 **{data['summary'].get('official_requests', 0)} 次请求**"
    return note


def _tier_pricing_note_lines(fmt, data):
    """档位名（fast-model 等）双计价口径注脚；无档位调用返回 []。

    档位名是「路由档位」而非真模型名，单价来自倍率锚定估算，与官方刊例价不是一回事。
    同一批调用在两种口径下金额不同，必须同时给出，否则读者会把估算价当成真实账单。
    `total_cost` 不改——这里只补充口径说明。
    """
    meta = (data or {}).get("meta", {}) or {}
    tp = meta.get("tier_pricing_basis") or {}
    n = tp.get("tier_traces") or 0
    if not n:
        return []
    tier_cost = tp.get("tier_cost") or 0.0
    alt_cost = tp.get("alt_hy3_cost")
    diff_txt = ""
    if alt_cost is not None:
        try:
            delta = float(tier_cost) - float(alt_cost)
            diff_txt = f"，较hy3 刊例价口径{'高' if delta >= 0 else '低'} ¥{abs(delta):.2f}"
        except (TypeError, ValueError):
            diff_txt = ""
    body = (
        f"本期 {n} 条调用的 `raw_model` 是**档位名**（如 `fast-model`）而非真实模型名，"
        f"其单价为倍率锚定**估算值**：档位口径 ¥{float(tier_cost):.2f}"
        + (f"，hy3 刊例价口径 ¥{float(alt_cost):.2f}{diff_txt}" if alt_cost is not None else "")
        + "。两个金额对应同一批 token，差异来自「档位估算单价 vs 官方刊例单价」，"
        "不代表账单差额；概览金额按档位口径汇总。"
    )
    if fmt == "html":
        return [
            '        <div class="disclaimer-box">',
            "            <p>🏷️ <b>档位名计价口径</b></p>",
            f"            <p>{_esc(body.replace('**', ''))}</p>",
            "        </div>",
        ]
    return [f"> 🏷️ **档位名计价口径**：{body}", ""]


def _user_turn_count(data):
    """真实用户提问轮数（仅统计本期有调用的会话）；拿不到返回 None 走回退。

    千问办公转录里 `humanInput` 可直接数出来（适配器落在 sessions[]._human_turns），
    比 15 分钟聚类反推的「估算请求数」更准，不该被估算值顶掉。
    WorkBuddy / claude-code / codex 没有这个字段 → 返回 None，报告保留原估算行。
    """
    traced = {
        t.get("session_id")
        for t in (data or {}).get("traces", [])
        if t.get("session_id")
    }
    if not traced:
        return None
    total, has_field = 0, False
    for s in (data or {}).get("sessions", []):
        if s.get("id") not in traced:
            continue
        n = s.get("_human_turns")
        if isinstance(n, int):
            has_field = True
            total += n
    return total if has_field else None


def _background_runs_note(data):
    """千问办公的后台自动运行摘要（记忆整理 / 反思等），无则返回 ""。"""
    br = ((data or {}).get("meta", {}) or {}).get("background_runs") or {}
    count = br.get("count") or 0
    if not count:
        return ""
    err = br.get("error_count") or 0
    note = f"| 后台自动运行 | {count} 次（记忆整理 / 反思等，非用户任务）"
    note += f"，其中失败 {err} 次 |" if err else " |"
    return note


def _token_anomaly_days(data):
    """§4.3 已判定的 Token 异常日列表（供 §十一 展望承接，别自相矛盾）。"""
    block = ((data or {}).get("cost_anomalies") or {}).get("token") or {}
    return block.get("daily") or []


def _session_count_note(data):
    """§一「会话总数」的口径补充：总数含空会话，与后文「N 个会话进入统计」自洽。

    只在两者确实不等时才追加说明，避免给 WorkBuddy 那种全有活动的窗口添噪音。
    """
    summary = (data or {}).get("summary", {}) or {}
    total = summary.get("total_sessions", 0) or 0
    rows = ((data or {}).get("session_stats") or {}).get("rows") or []
    traced = len(rows)
    if not traced or traced >= total:
        return ""
    return f"（含空会话；其中 {traced} 个有 token 活动，其余为无调用的空会话）"


def _footer_text(data):
    """页脚署名：workbuddy 沿用历史文案（既有测试断言它），其余源标清来源与计价模式。"""
    src = _source_key(data)
    if src == "workbuddy":
        return "本报告基于 WorkBuddy 数据自动生成。"
    label = (
        _SOURCE_LABELS[src][0].replace("使用情况报告", "").strip()
        if src in _SOURCE_LABELS
        else src
    )
    # 纯中文标签两侧不加空格（中英混排才需要），ASCII 标签（Codex CLI 等）保留空格
    pad = "" if any("\u4e00" <= ch <= "\u9fff" for ch in label) else " "
    return (
        f"本报告基于{pad}{label}{pad}本机数据自动生成（计价模式 {_cost_mode(data)}）。"
    )


def _source_caveat_lines(fmt, data):
    """数据源专属口径横幅（无特殊口径的来源返回空列表）。

    千问办公需要单独声明：它的 **token 本身也是估算**（服务端不回传用量），
    与 WorkBuddy / Claude Code / Codex 的「token 真值 + 成本估算」是两种口径。
    不写清楚就会被当成账单引用。
    """
    if _source_key(data) != "qwenwork":
        return []
    text = (
        "千问办公服务端<b>不回传 token 用量</b>（实测 <code>model.response.completed</code> "
        "的四个 token 字段恒为 0），本报告 token 由转录内容按「CJK 1 字 ≈ 1 token、"
        "其余 4 字符 ≈ 1 token」字符估算，输入 token 按逐请求<b>上下文重发</b>累加；"
        "<b>调用次数、请求耗时、模型档位、会话标题为真实值</b>。"
        "千问办公按积分订阅计费、账号级积分无法归因到单个会话，故<b>金额未计价</b>。"
    )
    plain = (
        text.replace("<b>", "**")
        .replace("</b>", "**")
        .replace("<code>", "`")
        .replace("</code>", "`")
    )
    if fmt == "html":
        return [
            '        <div class="disclaimer-box">',
            f"            <p>⚠️ <b>token 口径：本地字符估算</b> —— {text}</p>",
            "        </div>",
        ]
    return [f"> ⚠️ **token 口径：本地字符估算** —— {plain}", ""]


def _l2_cost_note(data):
    """L2 成本横幅的（标题后缀, MD 正文, HTML 正文）。

    「未导入官方用量导出」「本地 trace 盲区漏记 8.7%」只对 WorkBuddy 成立
    ——只有它有官方积分导出可对账。把这句话套到 claude-code / codex / qwenwork
    上会让读者以为存在一个没去导的账单，故按数据源分文案。
    """
    src = _source_key(data)
    if src == "workbuddy":
        return (
            "（未导入官方用量导出）",
            "成本 = `pricing.json` 静态单价 × token 量**估算**，不含服务端时段减免 / 用户免费额度；"
            "图像模型等本地 trace 盲区也无法覆盖（实测漏记约 8.7%）。**请勿据此做预算或账单对账。**",
            "成本 = <code>pricing.json</code> 静态单价 × token 量<b>估算</b>，"
            "不含服务端时段减免 / 用户免费额度；图像模型等本地 trace 盲区也无法覆盖"
            "（实测漏记约 8.7%）。<b>请勿据此做预算或账单对账。</b>",
        )
    # 外部数据源：压根没有「官方积分导出」这回事，别拿 WorkBuddy 的话术糊弄读者
    tail = "；本报告 token 本身亦为本地字符估算" if src == "qwenwork" else ""
    md = (
        "成本 = `pricing.json` 静态单价 × token 量**估算**%s。"
        "该数据源没有可对账的官方积分账单，**金额仅供趋势参考**。" % tail
    )
    html = (
        "成本 = <code>pricing.json</code> 静态单价 × token 量<b>估算</b>%s。"
        "该数据源没有可对账的官方积分账单，<b>金额仅供趋势参考</b>。" % tail
    )
    return ("（外部数据源，无官方账单可对账）", md, html)


def _cost_hidden_banner(fmt, data):
    """tokens_only 模式的口径横幅：说明金额维度为何缺席、怎么打开。"""
    meta = data.get("meta", {}) or {}
    unc = meta.get("unconfigured_models") or []
    _unc_txt = "、".join("`%s`" % m for m in unc[:6]) + ("…" if len(unc) > 6 else "")
    body = (
        "本报告**不提供金额（¥）与花费结论**：本期所有调用都没有命中"
        "`pricing.json` 里的单价（未配置：%s），继续渲染只会得到满屏 "
        "`¥0.00` 与「未配置」，反而容易被误读成「免费」或「采集失败」。"
        "Token / 调用次数 / 耗时 / 任务维度不受影响。"
        % (_unc_txt or "（本期无模型名记录）")
    )
    howto = (
        "要出金额：在 `scripts/pricing.local.json` 补上这些模型的单价后重跑，"
        "或加 `--cost-mode priced` 强制保留成本章节。"
    )
    if fmt == "html":
        return [
            '        <div class="disclaimer-box">',
            "            <p>ℹ️ <b>计价模式：tokens_only（仅用量，不计价）</b></p>",
            f"            <p>{body.replace('**', '')}</p>",
            f"            <p>{howto.replace('`', '')}</p>",
            "        </div>",
        ]
    return [
        f"> ℹ️ **计价模式：tokens_only（仅用量，不计价）**",
        ">",
        f"> {body}",
        ">",
        f"> {howto}",
        "",
    ]


def _cost_confidence_banner(fmt, data):
    """成本口径横幅：默认 L2 估算；导入官方导出后自动切 L1 真值。"""
    meta = data.get("meta", {}) or {}
    # tokens_only：连单价都没有，L1/L2 这套「成本置信度」话术无从谈起，换专属横幅
    if _cost_hidden(data):
        return _cost_hidden_banner(fmt, data)
    # 口径级别以「是否真拿到了官方数据」为准，而不是 meta 里的标记：
    # 若 meta 标了 official 但数据缺失（脏数据 / 手工编辑的 JSON），必须回落 L2，
    # 否则会渲染出「L1 真值（未导入官方用量导出）」这种自相矛盾的横幅。
    is_est = not _is_l1(data)
    src = "official" if not is_est else "estimate"
    label, icon = _COST_SOURCE_LABEL.get(src, _COST_SOURCE_LABEL["estimate"])
    hits = _low_conf_hits(data)
    off = _official_import(data)

    if fmt == "md":
        if is_est:
            _suffix, _body_md, _ = _l2_cost_note(data)
            lines = [f"> {icon} **成本口径：{label}**{_suffix}", ">", f"> {_body_md}"]
            if hits:
                lines.append(">")
                lines.append("> **低置信度模型（估算偏差已知较大，不参与成本结论）**：")
                for name, reason in hits.items():
                    _ar = _lc_arrow(_lc_bias(name, _low_conf_bias_map(data)))
                    lines.append(f"> - `{name} {_ar}` —— {reason}")
                lines.append(">")
                lines.append(
                    "> 取真值：加 `--import-official <官方用量导出.xlsx>` 重跑，本横幅自动切换为 L1。"
                )
            lines.append("")
            return lines

        # ── L1 真值 ──
        t = off.get("totals", {})
        w = off.get("meta", {}).get("window", {})
        lines = [
            f"> {icon} **成本口径：{label}**（已导入官方用量导出，成本取「积分」字段）",
            ">",
            f"> 本期官方账单：**{t.get('requests', 0)} 次请求 / {t.get('credits', 0):.2f} 积分**"
            f"（窗口 {w.get('first', '')} ~ {w.get('last', '')}，北京时间）。"
            f"其中 {t.get('free_requests', 0)} 次免费、{t.get('paid_requests', 0)} 次计费。",
            ">",
            "> §3 模型成本表仍是 trace 静态估算（L2），**仅供结构参考**；"
            "真实账单以本节积分与 §3.5 双源对账为准。",
        ]
        lines.append("")
        return lines

    if is_est:
        _suffix_h, _, _body_h = _l2_cost_note(data)
        rows = [
            f"            <b>{icon} 成本口径：{label}</b>{_suffix_h}",
            f"<p>{_body_h}</p>",
        ]
        if hits:
            rows.append(
                "<p><b>低置信度模型（估算偏差已知较大，不参与成本结论）：</b></p><ul>"
            )
            for name, reason in hits.items():
                _ar = _lc_arrow(_lc_bias(name, _low_conf_bias_map(data)))
                rows.append(
                    f"            <li><code>{_esc(name)} {_ar}</code> —— {_esc(reason)}</li>"
                )
            rows.append("        </ul>")
            rows.append(
                "<p>取真值：加 <code>--import-official &lt;官方用量导出.xlsx&gt;</code> 重跑，"
                "本横幅自动切换为 L1。</p>"
            )
        return ['        <div class="disclaimer-box">'] + rows + ["        </div>"]

    t = off.get("totals", {})
    w = off.get("meta", {}).get("window", {})
    rows = [
        f"            <b>{icon} 成本口径：{label}</b>（已导入官方用量导出，成本取「积分」字段）",
        f"<p>本期官方账单：<b>{t.get('requests', 0)} 次请求 / "
        f"{t.get('credits', 0):.2f} 积分</b>（窗口 {_esc(w.get('first', ''))} ~ "
        f"{_esc(w.get('last', ''))}，北京时间）。其中 {t.get('free_requests', 0)} 次免费、"
        f"{t.get('paid_requests', 0)} 次计费。</p>",
        "<p>§3 模型成本表仍是 trace 静态估算（L2），<b>仅供结构参考</b>；"
        "真实账单以本节积分与 §3.5 双源对账为准。</p>",
    ]
    return ['        <div class="disclaimer-box">'] + rows + ["        </div>"]


def _render_anomaly_block(fmt, title, block, kind):
    """渲染单口径（cost / token）异常块。"""
    thr = block.get("thresholds", {})
    if fmt == "md":
        lines = []
        if kind == "cost":
            lines.append(
                f"**💰 {title}**：日级成本阈值 p50 = ¥{thr.get('p50', 0):.2f}、"
                f"p95 = ¥{thr.get('p95', 0):.2f}；会话级 p95 = ¥{thr.get('session_p95', 0):.2f}。"
            )
        else:
            lines.append(
                f"**📊 {title}**：日级有效 Token 阈值 p50 = {thr.get('p50', 0):,.0f}、"
                f"p95 = {thr.get('p95', 0):,.0f}；会话级 p95（调用次数）= {thr.get('session_p95', 0):,.0f}。"
            )
        lines.append("")
        daily = block.get("daily", [])
        if daily:
            lines.append("**异常日**：")
            lines.append("")
            for a in daily:
                v = _fmt_anom_val(a["value"], kind == "cost")
                lines.append(f"- 🔺 **{_esc(a['date'])}**：{v} —— {'；'.join(_esc(r) for r in a['reasons'])}")
            lines.append("")
        else:
            label = "成本" if kind == "cost" else "Token 消耗"
            lines.append(f"- 日级{label}平稳，无超过 p95 或环比突增的异常日。")
            lines.append("")
        sess = block.get("session", [])
        if sess:
            if kind == "cost":
                lines.append("**异常高成本会话（超过会话级 p95）**：")
            else:
                lines.append("**异常高调用会话（调用次数超过 p95）**：")
            lines.append("")
        for a in sess:
            models = "、".join(_esc(x) for x in a.get("models", [])[:3]) or "—"
            if kind == "cost":
                lines.append(
                    f"- 💰 **{_esc(a['title'])}**：¥{a['value']:.2f}（主要模型：{models}）"
                )
            else:
                # token 口径不是钱，沿用 💰 会让 tokens_only 报告自己打自己脸
                lines.append(
                    f"- 📈 **{_esc(a['title'])}**：实际消耗 {a['value']:,.0f} token、"
                    f"调用 {a.get('calls', 0)} 次（主要模型：{models}）"
                )
            lines.append("")
        return lines
    # html
    L = []
    if kind == "cost":
        L.append(
            f"        <p><b>💰 {title}</b>：日级成本阈值 p50 = ¥{thr.get('p50', 0):.2f}、"
            f"p95 = ¥{thr.get('p95', 0):.2f}；会话级 p95 = ¥{thr.get('session_p95', 0):.2f}。</p>"
        )
    else:
        L.append(
            f"        <p><b>📊 {title}</b>：日级有效 Token 阈值 p50 = {thr.get('p50', 0):,.0f}、"
            f"p95 = {thr.get('p95', 0):,.0f}；会话级 p95（调用次数）= {thr.get('session_p95', 0):,.0f}。</p>"
        )
    daily = block.get("daily", [])
    if daily:
        L.append("        <p><b>异常日</b>：</p><ul>")
        for a in daily:
            v = _fmt_anom_val(a["value"], kind == "cost")
            L.append(
                f"            <li>🔺 <b>{_esc(a['date'])}</b>：{v} —— {'；'.join(_esc(r) for r in a['reasons'])}</li>"
            )
        L.append("        </ul>")
    else:
        label = "成本" if kind == "cost" else "Token 消耗"
        L.append(f"        <p>日级{label}平稳，无超过 p95 或环比突增的异常日。</p>")
    sess = block.get("session", [])
    if sess:
        if kind == "cost":
            L.append("        <p><b>异常高成本会话（超过会话级 p95）</b>：</p><ul>")
        else:
            L.append("        <p><b>异常高调用会话（调用次数超过 p95）</b>：</p><ul>")
        for a in sess:
            models = "、".join(_esc(x) for x in a.get("models", [])[:3]) or "—"
            if kind == "cost":
                L.append(
                    f"            <li>💰 <b>{_esc(a['title'])}</b>：¥{a['value']:.2f}（主要模型：{models}）</li>"
                )
            else:
                L.append(
                    f"            <li>📈 <b>{_esc(a['title'])}</b>：实际消耗 {a['value']:,.0f} token、"
                    f"调用 {a.get('calls', 0)} 次（主要模型：{models}）</li>"
                )
        L.append("        </ul>")
    return L


def _token_buckets(rows):
    """tokens_only 模式下的「每会话 Token 消耗」分桶（替代成本分桶）。

    区间按数量级切，末档为 ≥1M；返回 [(label, 会话数, 合计 token)]，
    仅保留有会话的区间，避免整表 0 噪音。
    """
    edges = [
        (0, 10_000, "< 10K"),
        (10_000, 100_000, "10K–100K"),
        (100_000, 1_000_000, "100K–1M"),
        (1_000_000, float("inf"), "≥ 1M"),
    ]
    out = []
    for lo, hi, label in edges:
        sel = [r for r in rows if lo <= (r.get("effective_tokens") or 0) < hi]
        if sel:
            out.append(
                (label, len(sel), sum(r.get("effective_tokens") or 0 for r in sel))
            )
    return out


def _build_tokens_only_analysis(fmt, data):
    """tokens_only 模式的 §四：只讲 Token 与调用，不讲钱。

    独立成章而不是往成本章节里塞十几个 if：既有 §四 的渲染路径与 20+ 条断言
    一行不动（零回归），新口径的可读性也由这一处承载。
    """
    session_stats = data.get("session_stats") or {}
    rows = session_stats.get("rows", [])
    ca = data.get("cost_anomalies") or {}
    if not rows:
        return []
    total_tokens = sum(r.get("effective_tokens") or 0 for r in rows)
    top = rows[:10]
    buckets = _token_buckets(rows)
    size_anom = _compute_session_size_anomalies(rows)

    if fmt == "md":
        lines = ["## 四、Token 与调用深度分析（每会话 / 异常）", ""]
        lines.append(
            "> 本报告为 **tokens_only 计价模式**（本期无模型命中单价），"
            "故本章按「每会话 Token 消耗、调用次数、异常峰值」拆解；"
            "省钱杠杆、失败自动化成本归因、缓存可省测算等金额结论整章缺席。"
        )
        lines.append("")
        _warn = _unresolved_warning_md(_unresolved_call_stats(data))
        if _warn:
            lines.append(_warn)
            lines.append("")
        lines.append("### 4.1 每会话 Token 消耗 Top 10")
        lines.append("")
        lines.append("| 排名 | 任务名称 | 任务类型 | 实际消耗 | 调用 | 主要模型 |")
        lines.append("|------|---------|---------|---------|------|---------|")
        for i, r in enumerate(top, 1):
            models = "、".join(r.get("models", [])[:3]) or "—"
            lines.append(
                f"| {i} | {r['title']} | {r['task_type']} | "
                f"{format_number(r.get('effective_tokens', 0))} | {r.get('calls', 0)} | {models} |"
            )
        lines.append("")
        lines.append("### 4.2 每会话 Token 消耗分布")
        lines.append("")
        lines.append(
            f"本期共 {len(rows)} 个会话进入统计，合计实际消耗 {format_number(total_tokens)} token。"
        )
        lines.append("")
        lines.append("| Token 区间 | 会话数 | 合计 Token | 占比 |")
        lines.append("|-----------|--------|-----------|------|")
        for label, cnt, tk in buckets:
            pct = (tk / total_tokens * 100) if total_tokens else 0
            lines.append(f"| {label} | {cnt} | {format_number(tk)} | {pct:.1f}% |")
        lines.append("")
        lines.append("### 4.3 Token 异常与飙升检测")
        lines.append("")
        if ca.get("token") is not None:
            lines.extend(
                _render_anomaly_block("md", "Token 口径", ca["token"], "token")
            )
        else:
            lines.append("- 日级 Token 消耗平稳，无超过 p95 或环比突增的异常日。")
            lines.append("")
        if size_anom and size_anom["items"]:
            lines.append(
                f"**📊 会话规模异常**（调用次数 > {size_anom['threshold']}，"
                f"取 max(会话 p95={size_anom['p95']}, 200)，疑似 fan-out / 长链路）："
            )
            lines.append("")
            lines.append("| 任务名称 | 任务类型 | 调用 | 实际消耗 |")
            lines.append("|---------|---------|------|---------|")
            for r in size_anom["items"]:
                lines.append(
                    f"| {r['title'][:30]} | {r['task_type']} | {r['calls']} | "
                    f"{format_number(r.get('effective_tokens', 0))} |"
                )
            lines.append("")
        return lines

    L = [
        '    <div class="section">',
        '        <h2 class="section-title">四、Token 与调用深度分析（每会话 / 异常）</h2>',
        "        <p>本报告为 <b>tokens_only 计价模式</b>（本期无模型命中单价），本章按"
        "「每会话 Token 消耗、调用次数、异常峰值」拆解；省钱杠杆、失败自动化成本归因、"
        "缓存可省测算等金额结论整章缺席。</p>",
    ]
    _warn_h = _unresolved_warning_md(_unresolved_call_stats(data))
    if _warn_h:
        L.append(
            f"        <p class='disclaimer'>{_warn_h.replace(chr(10), ' ').replace('&gt; ', '')}</p>"
        )
    L.append("        <h3>4.1 每会话 Token 消耗 Top 10</h3>")
    L.append("        <table>")
    L.append(
        "            <thead><tr><th>排名</th><th>任务名称</th><th>任务类型</th>"
        "<th>实际消耗</th><th>调用</th><th>主要模型</th></tr></thead>"
    )
    L.append("            <tbody>")
    for i, r in enumerate(top, 1):
        models = "、".join(r.get("models", [])[:3]) or "—"
        L.append(
            f"                <tr><td>{i}</td><td>{_esc(r['title'])}</td>"
            f"<td>{_esc(r['task_type'])}</td>"
            f"<td>{format_number(r.get('effective_tokens', 0))}</td>"
            f"<td>{r.get('calls', 0)}</td><td>{_esc(models)}</td></tr>"
        )
    L.append("            </tbody>")
    L.append("        </table>")
    L.append("        <h3>4.2 每会话 Token 消耗分布</h3>")
    L.append(
        f"        <p>本期共 {len(rows)} 个会话进入统计，合计实际消耗 "
        f"{format_number(total_tokens)} token。</p>"
    )
    L.append("        <table>")
    L.append(
        "            <thead><tr><th>Token 区间</th><th>会话数</th><th>合计 Token</th><th>占比</th></tr></thead>"
    )
    L.append("            <tbody>")
    for label, cnt, tk in buckets:
        pct = (tk / total_tokens * 100) if total_tokens else 0
        L.append(
            f"                <tr><td>{_esc(label)}</td><td>{cnt}</td>"
            f"<td>{format_number(tk)}</td><td>{pct:.1f}%</td></tr>"
        )
    L.append("            </tbody>")
    L.append("        </table>")
    L.append("        <h3>4.3 Token 异常与飙升检测</h3>")
    if ca.get("token") is not None:
        L.extend(_render_anomaly_block("html", "Token 口径", ca["token"], "token"))
    else:
        L.append("        <p>日级 Token 消耗平稳，无超过 p95 或环比突增的异常日。</p>")
    if size_anom and size_anom["items"]:
        L.append(
            f"        <p><b>📊 会话规模异常</b>（调用次数 &gt; {size_anom['threshold']}，"
            f"取 max(会话 p95={size_anom['p95']}, 200)，疑似 fan-out / 长链路）：</p>"
        )
        L.append(
            "        <table><thead><tr><th>任务名称</th><th>任务类型</th><th>调用</th>"
            "<th>实际消耗</th></tr></thead><tbody>"
        )
        for r in size_anom["items"]:
            L.append(
                f"            <tr><td>{_esc(r['title'][:30])}</td><td>{_esc(r['task_type'])}</td>"
                f"<td>{r['calls']}</td><td>{format_number(r.get('effective_tokens', 0))}</td></tr>"
            )
        L.append("        </tbody></table>")
    L.append("    </div>")
    return L


def build_cost_analysis_section(fmt, data):
    """章节：四、成本深度分析（每会话 / 异常 / 省钱）。MD / HTML 共用一份数据与逻辑。"""
    if _cost_hidden(data):
        # tokens_only：换用「Token 与调用」版章节，既有成本渲染路径一行不动
        return _build_tokens_only_analysis(fmt, data)
    session_stats = data.get("session_stats") or {}
    rows = session_stats.get("rows", [])
    buckets = session_stats.get("buckets", [])
    ca = data.get("cost_anomalies") or {}
    si = data.get("savings_insights") or {}
    automation_runs = data.get("automation_runs") or []
    if not rows:
        return []
    if fmt == "md":
        lines = []
        lines.append("## 四、成本深度分析（每会话 / 异常 / 省钱）")
        lines.append("")
        lines.append(
            "> 行业调研显示：Agent 使用者最关心「**每任务 / 每会话成本**」——token 成本往往只占 AI Agent 总成本的 30–70%，"
            "真正烧钱的是「每个会话跑几次调用、几次重试」。以下从会话维度拆解你的花费。"
        )
        lines.append("")
        _warn = _unresolved_warning_md(_unresolved_call_stats(data))
        if _warn:
            lines.append(_warn)
            lines.append("")
        _disc = _free_period_disclaimer("md", data)
        if _disc:
            lines.extend(_disc)
        lines.append("### 4.1 每会话成本 Top 10")
        lines.append("")
        lines.append(
            "| 排名 | 任务名称 | 任务类型 | 实际成本 | 实际消耗 | 调用 | 主要模型 |"
        )
        lines.append(
            "|------|---------|---------|---------|---------|------|---------|"
        )
        for i, r in enumerate(rows[:10], 1):
            models = "、".join(r.get("models", [])[:3]) or "—"
            lines.append(
                f"| {i} | {r['title']} | {r['task_type']} | ¥{r['effective_cost']:.2f} | "
                f"{format_number(r['effective_tokens'])} | {r['calls']} | {models} |"
            )
        lines.append("")
        lines.append("### 4.2 每会话成本分布")
        lines.append("")
        total_cost = sum(b["cost"] for b in buckets) or 0
        lines.append(
            f"本期共 {len(rows)} 个会话，合计实际成本 ¥{total_cost:.2f}。按单会话成本分桶（图表按会话数，明细含合计成本）："
        )
        lines.append("")
        bar = build_session_cost_bar_md(buckets)
        if bar:
            lines.append(bar)
            lines.append("")
        lines.append("**明细**（成本区间 | 会话数 | 合计成本 | 占成本比）：")
        lines.append("")
        lines.append("| 成本区间 | 会话数 | 合计成本 | 占比 |")
        lines.append("|---------|--------|---------|------|")
        for b in buckets:
            pct = (b["cost"] / total_cost * 100) if total_cost else 0
            lines.append(
                f"| {b['label']} | {b['count']} | ¥{b['cost']:.2f} | {pct:.1f}% |"
            )
        lines.append("")
        lines.append("### 4.3 成本 / Token 异常与飙升检测（双口径）")
        lines.append("")
        lines.append(
            "> 本节同时以「成本」与「Token 消耗」两个**独立**口径检测异常日，"
            "避免免费 / 限时免费模型拉低成本口径而漏报 Token 峰值。"
        )
        lines.append("")
        cost_block = ca.get("cost")
        if cost_block is None:
            lines.append(f"> ⚠️ {ca.get('cost_note', '')}")
            lines.append("")
        else:
            lines.extend(_render_anomaly_block("md", "成本口径", cost_block, "cost"))
        # 防御：cost_anomalies 缺 token 子块时不阻塞整章（单源缺失不扩散，见 metadata 错误处理策略）
        if ca.get("token") is not None:
            lines.extend(
                _render_anomaly_block("md", "Token 口径", ca["token"], "token")
            )
        size_anom = _compute_session_size_anomalies(rows)
        if size_anom and size_anom["items"]:
            lines.append(
                f"**📊 会话规模异常**（调用次数 > {size_anom['threshold']}，"
                f"取 max(会话 p95={size_anom['p95']}, 200)，疑似 fan-out / 长链路）："
            )
            lines.append("")
            lines.append("| 任务名称 | 任务类型 | 调用 | 实际成本 |")
            lines.append("|---------|---------|------|---------|")
            for r in size_anom["items"]:
                lines.append(
                    f"| {r['title'][:30]} | {r['task_type']} | {r['calls']} | ¥{r['effective_cost']:.2f} |"
                )
            lines.append("")
        lines.append("### 4.4 省钱杠杆（自动洞察）")
        lines.append("")
        items = si.get("items", [])
        if items:
            if _is_l1(data):
                lines.append(
                    "基于官方用量导出（成本真值 L1）按模型分析，以下高占比付费模型存在更便宜的替代方案"
                    "（假设 30% 的简单任务可迁移，真值口径，仅供参考）："
                )
            else:
                lines.append(
                    "基于「实际执行模型」维度分析，以下高占比付费模型存在更便宜的替代方案"
                    "（假设 30% 的简单任务可迁移，估算口径，仅供参考）："
                )
            lines.append("")
            for it in items:
                lines.append(
                    f"- **{it['model']}** 当前花费 ¥{it['cost']:.2f}（占付费成本 {it['cost_share']:.1f}%）；"
                    f"若简单任务迁移至 **{it['alternative']}**（{it['note']}），"
                    f"预计月省 **¥{it['estimated_monthly_save']:.2f}**。"
                )
            lines.append("")
            lines.append(
                f"> 💡 **合计预计月省 ¥{si.get('total_estimated_monthly_save', 0):.2f}**"
                f"（保守估算，实际取决于你可迁移的任务比例）。"
            )
        else:
            lines.append(
                "- 当前付费模型均已是最优性价比，暂无明确可迁移的更便宜替代；"
                "后续若引入更便宜模型或提升缓存复用率，可进一步降本。"
            )
        # 省钱杠杆已排除低置信度模型；此处显式提示折扣/时段模型，避免用户自行「迁走」
        # 低置信度模型恰好是最贵（Top-3）时，在省钱章节顶部也给出高位告警
        # L1 真值模式：官方积分已是真值，不再渲染低置信度标记（折扣/时段模型在 L1 不构成误导）
        _lc_models = sorted(
            {
                m["model"]
                for m in (
                    data.get("model_stats", []) + data.get("model_exec_stats", [])
                )
                if _lc_reason(m["model"], _low_conf_map(data))
                and (m.get("effective_cost", 0) or 0) > 0
            }
        )
        if _lc_models and not _is_l1(data):
            _lc_txt = "、".join(
                f"`{n} {_lc_arrow(_lc_bias(n, _low_conf_bias_map(data)))}`"
                for n in _lc_models
            )
            lines.append(
                f"> ℹ️ **折扣 / 时段模型提示**：{_lc_txt} 在 L2 被高估（夜间免费 / 促销 / 峰谷），"
                f"真实花费请以官方账单为准；本报告不就此给出「迁走」建议，避免你反而多花钱。"
            )
            _alert = _lc_top_alert(data)
            if _alert:
                lines.append(
                    f"> ⚠ **高位告警**：本期最贵模型 **`{_alert['model']}` {_alert['arrow']}**"
                    f"（¥{_alert['cost']:.2f}，第 {_alert['rank']} 贵，占付费花费 "
                    f"{_alert['share'] * 100:.0f}%）为低置信度估算；"
                    f"真实花费以官方账单为准，**不要据此切换模型**。（见报告顶部「成本口径」）"
                )
        lines.append("")
        sessions_by_cwd, session_cost_by_id = _build_session_cwd_maps(data)
        failed_items = _compute_failed_automation_cost(
            automation_runs, sessions_by_cwd, session_cost_by_id
        )
        lines.extend(_render_failed_automation("md", failed_items))
        cache_untitled = _compute_cache_and_untitled(data, threshold_pct=60.0)
        lines.extend(_render_cache_untitled("md", cache_untitled))
        return lines
    # html
    L = []
    L.append('    <div class="section">')
    L.append(
        '        <h2 class="section-title">四、成本深度分析（每会话 / 异常 / 省钱）</h2>'
    )
    L.append(
        "        <p>行业调研显示：Agent 使用者最关心「<b>每任务 / 每会话成本</b>」——token 成本往往只占 "
        "AI Agent 总成本的 30–70%，真正烧钱的是「每个会话跑几次调用、几次重试」。以下从会话维度拆解你的花费。</p>"
    )
    _warn = _unresolved_warning_md(_unresolved_call_stats(data))
    if _warn:
        _warn_html = _warn.replace("\n", " ").replace("⚠️", "").strip()
        L.append(
            f'        <div class="warn-box"><b>⚠️ 未解析 / 幽灵调用提示</b>：{_esc(_warn_html)}</div>'
        )
    L.extend(_free_period_disclaimer("html", data))
    L.append("        <h3>4.1 每会话成本 Top 10</h3>")
    L.append("        <table>")
    L.append(
        "            <tr><th>排名</th><th>任务名称</th><th>任务类型</th><th>实际成本</th>"
        "<th>实际消耗</th><th>调用</th><th>主要模型</th></tr>"
    )
    for i, r in enumerate(rows[:10], 1):
        models = "、".join(r.get("models", [])[:3]) or "—"
        L.append(
            f"            <tr><td>{i}</td><td>{_esc(r['title'])}</td><td>{_esc(r['task_type'])}</td>"
            f"<td>¥{r['effective_cost']:.2f}</td><td>{format_number(r['effective_tokens'])}</td>"
            f"<td>{r['calls']}</td><td>{models}</td></tr>"
        )
    L.append("        </table>")
    L.append("        <h3>4.2 每会话成本分布</h3>")
    total_cost = sum(b["cost"] for b in buckets) or 0
    L.append(
        f"        <p>本期共 {len(rows)} 个会话，合计实际成本 ¥{total_cost:.2f}。按单会话成本分桶（环形图按会话数）：</p>"
    )
    bucket_stats = [
        {"task_type": b["label"], "count": b["count"], "cost": b["cost"]}
        for b in buckets
    ]
    donut = build_donut_chart(
        bucket_stats,
        title="每会话成本分布（按会话数）",
        center_label="会话数",
        value_key="count",
        unit=" 会话",
    )
    if donut:
        L.append(donut)
    L.append("        <table>")
    L.append(
        "            <tr><th>成本区间</th><th>会话数</th><th>合计成本</th><th>占比</th></tr>"
    )
    for b in buckets:
        pct = (b["cost"] / total_cost * 100) if total_cost else 0
        L.append(
            f"            <tr><td>{b['label']}</td><td>{b['count']}</td>"
            f"<td>¥{b['cost']:.2f}</td><td>{pct:.1f}%</td></tr>"
        )
    L.append("        </table>")
    L.append("        <h3>4.3 成本 / Token 异常与飙升检测（双口径）</h3>")
    L.append(
        "        <p>本节同时以「成本」与「Token 消耗」两个<b>独立</b>口径检测异常日，"
        "避免免费 / 限时免费模型拉低成本口径而漏报 Token 峰值。</p>"
    )
    cost_block = ca.get("cost")
    if cost_block is None:
        L.append(
            f'        <p style="color:var(--disclaimer-fg)">⚠️ {ca.get("cost_note", "")}</p>'
        )
    else:
        L.extend(_render_anomaly_block("html", "成本口径", cost_block, "cost"))
    if ca.get("token") is not None:
        L.extend(_render_anomaly_block("html", "Token 口径", ca["token"], "token"))
    size_anom = _compute_session_size_anomalies(rows)
    if size_anom and size_anom["items"]:
        L.append(
            f"        <p><b>📊 会话规模异常</b>（调用次数 &gt; {size_anom['threshold']}，"
            f"取 max(会话 p95={size_anom['p95']}, 200)，疑似 fan-out / 长链路）：</p>"
        )
        L.append("        <table>")
        L.append(
            "            <tr><th>任务名称</th><th>任务类型</th><th>调用</th><th>实际成本</th></tr>"
        )
        for r in size_anom["items"]:
            L.append(
                f"            <tr><td>{_esc(r['title'][:30])}</td><td>{_esc(r['task_type'])}</td>"
                f"<td>{r['calls']}</td><td>¥{r['effective_cost']:.2f}</td></tr>"
            )
        L.append("        </table>")
    L.append("        <h3>4.4 省钱杠杆（自动洞察）</h3>")
    items = si.get("items", [])
    if items:
        if _is_l1(data):
            L.append(
                "        <p>基于官方用量导出（成本真值 L1）按模型分析，以下高占比付费模型存在更便宜的替代方案"
                "（假设 30% 的简单任务可迁移，真值口径，仅供参考）：</p><ul>"
            )
        else:
            L.append(
                "        <p>基于「实际执行模型」维度分析，以下高占比付费模型存在更便宜的替代方案"
                "（假设 30% 的简单任务可迁移，估算口径，仅供参考）：</p><ul>"
            )
        for it in items:
            L.append(
                f"            <li><b>{it['model']}</b> 当前花费 ¥{it['cost']:.2f}（占付费成本 {it['cost_share']:.1f}%）；"
                f"若简单任务迁移至 <b>{it['alternative']}</b>（{it['note']}），"
                f"预计月省 <b>¥{it['estimated_monthly_save']:.2f}</b>。</li>"
            )
        L.append("        </ul>")
        L.append(
            f"        <p>💡 <b>合计预计月省 ¥{si.get('total_estimated_monthly_save', 0):.2f}</b>"
            f"（保守估算，实际取决于你可迁移的任务比例）。</p>"
        )
    else:
        L.append(
            "        <p>当前付费模型均已是最优性价比，暂无明确可迁移的更便宜替代；"
            "后续若引入更便宜模型或提升缓存复用率，可进一步降本。</p>"
        )
    # 折扣/时段模型提示；低置信度最贵高位告警（HTML）
    # L1 真值模式：官方积分已是真值，不再渲染低置信度标记
    _lc_models_h = sorted(
        {
            m["model"]
            for m in (data.get("model_stats", []) + data.get("model_exec_stats", []))
            if _lc_reason(m["model"], _low_conf_map(data))
            and (m.get("effective_cost", 0) or 0) > 0
        }
    )
    if _lc_models_h and not _is_l1(data):
        _lc_txt_h = "、".join(
            f"<code>{_esc(n)} {_lc_arrow(_lc_bias(n, _low_conf_bias_map(data)))}</code>"
            for n in _lc_models_h
        )
        L.append(
            f"        <p>ℹ️ <b>折扣 / 时段模型提示</b>：{_lc_txt_h} 在 L2 被高估（夜间免费 / 促销 / 峰谷），"
            "真实花费请以官方账单为准；本报告不就此给出「迁走」建议，避免你反而多花钱。</p>"
        )
        _alert_h = _lc_top_alert(data)
        if _alert_h:
            L.append(
                f'        <p class="warn-box">⚠ <b>高位告警</b>：本期最贵模型 '
                f"<code>{_esc(_alert_h['model'])} {_alert_h['arrow']}</code>"
                f"（¥{_alert_h['cost']:.2f}，第 {_alert_h['rank']} 贵，占付费花费 "
                f"{_alert_h['share'] * 100:.0f}%）为低置信度估算；"
                f"真实花费以官方账单为准，<b>不要据此切换模型</b>。</p>"
            )
    sessions_by_cwd, session_cost_by_id = _build_session_cwd_maps(data)
    failed_items = _compute_failed_automation_cost(
        automation_runs, sessions_by_cwd, session_cost_by_id
    )
    L.extend(_render_failed_automation("html", failed_items))
    cache_untitled = _compute_cache_and_untitled(data, threshold_pct=60.0)
    L.extend(_render_cache_untitled("html", cache_untitled))
    L.append("    </div>")
    return L


def generate_html_report(data):
    meta = data.get("meta", {})
    summary = data.get("summary", {})
    daily_tokens = data.get("daily_tokens", {})
    task_dist = summary.get("task_type_distribution", {})
    skills = data.get("skill_usage", {}).get("skills", {})
    outputs = data.get("outputs", [])
    automation_runs = data.get("automation_runs", [])

    total_input = summary.get("total_input_tokens", 0)
    total_cached = summary.get("total_cached_tokens", 0)
    cache_rate = (total_cached / total_input * 100) if total_input else 0

    # CSS 作为普通字符串，花括号即字面量，无需转义
    css = """
        :root {
            --bg: #ffffff; --fg: #333333; --muted: #6c757d;
            --card-bg: #f8f9fa; --card-border: #dee2e6; --table-border: #dee2e6;
            --th-bg: #f8f9fa; --accent: #3498db; --accent-fg: #2c3e50;
            --chart-bg: #f8f9fa; --bar-track: #e9ecef; --bar-fill: #3498db;
            --link: #3498db;
            --disclaimer-bg: #fff8e6; --disclaimer-border: #e0a800; --disclaimer-fg: #b8860b;
        }
        /* 显式深色：通过 <html data-theme="dark"> 强制 */
        :root[data-theme="dark"] {
            --bg: #16181d; --fg: #e6e6e6; --muted: #9aa0a6;
            --card-bg: #21242b; --card-border: #343a45; --table-border: #343a45;
            --th-bg: #262a32; --accent: #58b6ec; --accent-fg: #9fd3f3;
            --chart-bg: #21242b; --bar-track: #343a45; --bar-fill: #58b6ec;
            --link: #58b6ec;
            --disclaimer-bg: #3a2f12; --disclaimer-border: #c79a2e; --disclaimer-fg: #f0c75a;
        }
        /* 系统深色：未显式选择「浅色」时跟随系统配色 */
        @media (prefers-color-scheme: dark) {
            :root:not([data-theme="light"]) {
                --bg: #16181d; --fg: #e6e6e6; --muted: #9aa0a6;
                --card-bg: #21242b; --card-border: #343a45; --table-border: #343a45;
                --th-bg: #262a32; --accent: #58b6ec; --accent-fg: #9fd3f3;
                --chart-bg: #21242b; --bar-track: #343a45; --bar-fill: #58b6ec;
                --link: #58b6ec;
                --disclaimer-bg: #3a2f12; --disclaimer-border: #c79a2e; --disclaimer-fg: #f0c75a;
            }
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: var(--fg); background: var(--bg); max-width: 1200px; margin: 0 auto; padding: 20px; transition: background .3s ease, color .3s ease; }
        .header { background: var(--card-bg); padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--card-border); transition: background .3s ease, border-color .3s ease; }
        .section { margin-bottom: 30px; }
        .section-title { color: var(--accent-fg); border-bottom: 2px solid var(--accent); padding-bottom: 10px; margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid var(--table-border); padding: 8px 12px; text-align: left; }
        th { background-color: var(--th-bg); font-weight: 600; }
        .chart-pie { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; background: var(--chart-bg); padding: 15px; border-radius: 5px; }
        .chart-pie svg { flex-shrink: 0; }
        .chart-pie .legend { font-size: 13px; line-height: 1.5; color: var(--fg); }
        .chart-pie .legend-item { display: flex; align-items: center; margin: 4px 0; }
        .chart-pie .swatch { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; display: inline-block; }
        .chart-pie .pct { color: var(--muted); margin-left: 4px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin: 15px 0; }
        .stat-card { background: var(--card-bg); padding: 15px; border-radius: 8px; border: 1px solid var(--card-border); }
        .stat-value { font-size: 24px; font-weight: bold; color: var(--accent-fg); }
        .stat-label { color: var(--muted); font-size: 14px; }
        .chart-bars { background: var(--chart-bg); padding: 15px; border-radius: 5px; margin: 10px 0; }
        .bar-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; font-size: 13px; }
        .bar-label { width: 220px; text-align: right; font-family: monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .bar-track { flex: 1; background: var(--bar-track); border-radius: 4px; height: 14px; overflow: hidden; min-width: 60px; }
        .bar-fill { display: block; height: 100%; background: var(--bar-fill); }
        .bar-val { width: 80px; text-align: right; font-family: monospace; }
        .disclaimer { color: var(--disclaimer-fg); font-size: 13px; background: var(--disclaimer-bg); border-left: 4px solid var(--disclaimer-border); padding: 8px 12px; border-radius: 4px; margin: 12px 0; }
        .warn-box { color: var(--disclaimer-fg); background: var(--disclaimer-bg); border: 1px solid var(--disclaimer-border); border-left: 4px solid var(--disclaimer-border); padding: 10px 14px; border-radius: 6px; margin: 12px 0; font-size: 13px; }
        .disclaimer-box { color: var(--disclaimer-fg); background: var(--disclaimer-bg); border: 1px solid var(--disclaimer-border); border-left: 4px solid var(--disclaimer-border); padding: 10px 14px; border-radius: 6px; margin: 12px 0; font-size: 13px; }
        .disclaimer-box p { margin: 6px 0 0; }
        .disclaimer-box ul { margin: 6px 0 0; padding-left: 20px; }
        .disclaimer-box li { margin: 4px 0; }
        /* 成本置信度：低置信度估算标记 */
        .lc-note { color: var(--disclaimer-fg); font-size: 12px; }
        .chart-bars .lc-note { margin: 8px 0 0; }
        /* 双源对账（§3.5） */
        .note { color: var(--disclaimer-fg); font-size: 13px; background: var(--disclaimer-bg); border-left: 4px solid var(--disclaimer-border); padding: 8px 12px; border-radius: 4px; margin: 12px 0; }
        a { color: var(--link); }
        /* 主题切换控件 */
        .theme-toggle { display: inline-flex; gap: 6px; margin-top: 14px; flex-wrap: wrap; }
        .theme-toggle button {
            font-size: 13px; padding: 6px 14px; border-radius: 999px;
            border: 1px solid var(--table-border); background: var(--bg);
            color: var(--fg); cursor: pointer; transition: all .2s ease;
        }
        .theme-toggle button:hover { border-color: var(--accent); color: var(--accent-fg); }
        .theme-toggle button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
    """

    lines = []
    _key = meta.get("period", "week")
    _label, _short, _next = _period_labels(meta)
    lines.append("<!DOCTYPE html>")
    lines.append('<html lang="zh-CN">')
    lines.append("<head>")
    lines.append('    <meta charset="UTF-8">')
    lines.append(
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
    )
    lines.append("    <script>")
    lines.append(
        '        (function(){try{var t=localStorage.getItem("aurs-theme")||"system";if(t&&t!=="system"){document.documentElement.setAttribute("data-theme",t);}}catch(e){}})();'
    )
    lines.append("    </script>")
    _title_h, _src_h, _ = _source_identity(data)
    lines.append(f"    <title>{_title_h}</title>")
    lines.append("    <style>")
    lines.append(css)
    lines.append("    </style>")
    lines.append("</head>")
    lines.append("<body>")
    lines.append('    <div class="header">')
    lines.append(f"        <h1>{_title_h}</h1>")
    lines.append(f"        <p><strong>报告类型</strong>：{_calendar_period(meta)}</p>")
    lines.append(
        f"        <p><strong>报告周期</strong>：{meta.get('start_date', '')} 至 {meta.get('end_date', '')}</p>"
    )
    lines.append(f"        <p><strong>生成时间</strong>：{_fmt_generated_at()}</p>")
    _src_list_h = _src_h
    if _is_l1(data):
        _src_list_h += "、<strong>官方用量导出（成本真值 L1，本地只读解析）</strong>"
    lines.append(f"        <p><strong>数据来源</strong>：{_src_list_h}</p>")
    lines.append(
        '        <div class="theme-toggle" role="group" aria-label="主题切换">'
    )
    lines.append(
        '            <button type="button" data-set-theme="light">☀ 浅色</button>'
    )
    lines.append(
        '            <button type="button" data-set-theme="dark">🌙 深色</button>'
    )
    lines.append(
        '            <button type="button" data-set-theme="system">🖥 系统</button>'
    )
    lines.append("        </div>")
    lines.append("    </div>")
    lines += _source_caveat_lines("html", data)
    lines += _cost_confidence_banner("html", data)

    # 一、概览统计
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">一、概览统计</h2>')
    lines.append('        <div class="stats-grid">')
    _bd_h = _call_count_breakdown(data)
    _billable_calls_h = _bd_h["billable"]
    # 统计卡空间有限，括注压到最短：失败 + 未知模型两类关键扣减，粒度用短标签
    _calls_label_parts = [_bd_h["granularity_short"]]
    if _bd_h["error"]:
        _calls_label_parts.append(f"{_bd_h['error']} 失败")
    if _bd_h["unknown"]:
        _calls_label_parts.append(f"{_bd_h['unknown']} 未知模型")
    if _bd_h["ghost"]:
        _calls_label_parts.append(f"{_bd_h['ghost']} 未解析")
    _calls_label_h = "调用次数·" + "·".join(_calls_label_parts)
    _user_turns_h = _user_turn_count(data)
    _hidden_h = _cost_hidden(data)  # tokens_only：隐藏金额维度
    stat_cards = [
        (summary.get("active_day_count", 0), "活跃天数"),
        (summary.get("total_sessions", 0), f"会话总数{_session_count_note(data)}"),
        (_billable_calls_h, _calls_label_h),
        (summary.get("skills_used", 0), "使用技能"),
        (summary.get("total_automation_runs", 0), "自动化任务运行"),
        (format_number(summary.get("total_effective_tokens", 0)), "实际消耗 Token"),
    ]
    if _hidden_h:
        stat_cards.append(("tokens_only", "计价模式（不计价）"))
    else:
        stat_cards.append(
            (f"¥{summary.get('total_effective_cost', 0):.2f}", "实际成本（估算）")
        )
    if _is_l1(data):
        stat_cards.insert(3, (summary.get("official_requests", 0), "官方请求数（L1）"))
        stat_cards.append(
            (f"{summary.get('total_cost_official', 0):.2f}", "官方积分合计（L1 真值）")
        )
    # 请求数：有真实提问轮数就用真值卡片，否则保留聚类反推的估算卡片
    _est_req_h = summary.get("estimated_request_count")
    if _user_turns_h is not None:
        stat_cards.append((_user_turns_h, "用户提问轮数（真实计数）"))
    elif _est_req_h is not None:
        stat_cards.append((_est_req_h, "估算请求数（反推·估算）"))
    _br = ((data or {}).get("meta", {}) or {}).get("background_runs") or {}
    if _br.get("count"):
        stat_cards.append((_br["count"], "后台自动运行（次）"))
    for val, label in stat_cards:
        lines.append('            <div class="stat-card">')
        lines.append(f'                <div class="stat-value">{val}</div>')
        lines.append(f'                <div class="stat-label">{label}</div>')
        lines.append("            </div>")
    lines.append("        </div>")
    lines.append("    </div>")

    # 二、Token 消耗可视化
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">二、Token 消耗可视化</h2>')
    lines.append("        <table>")
    lines.append("            <tr><th>指标</th><th>数值</th></tr>")
    token_rows = [
        ("原始总 Token（含缓存命中）", format_number(summary.get("total_tokens", 0))),
        (
            _eff_token_label(data),
            format_number(summary.get("total_effective_tokens", 0)),
        ),
        ("输入 Token", format_number(summary.get("total_input_tokens", 0))),
        ("输出 Token", format_number(summary.get("total_output_tokens", 0))),
        ("缓存命中 Token", format_number(summary.get("total_cached_tokens", 0))),
        ("缓存占比", f"{cache_rate:.1f}%"),
    ]
    if _hidden_h:
        token_rows.append(
            (
                "计价状态",
                "未计价（tokens_only：本期无模型命中单价，金额维度已从全篇移除）",
            )
        )
    else:
        token_rows.append(
            ("实际成本（计费等效）", f"¥{summary.get('total_effective_cost', 0):.2f}")
        )
        token_rows.append(
            ("原始总成本（含缓存全价）", f"¥{summary.get('total_cost', 0):.2f}")
        )
    for name, val in token_rows:
        lines.append(f"            <tr><td>{name}</td><td>{val}</td></tr>")
    lines.append("        </table>")
    # 档位名双口径注脚：与 MD 版 §一 同源（共用 _tier_pricing_note_lines）
    lines += _tier_pricing_note_lines("html", data)
    lines.append("    </div>")

    # 每日趋势（横向条形图，与报告内其他横条图表一致）
    if daily_tokens:
        max_tokens = (
            max((v.get("total", 0) for v in daily_tokens.values()), default=1) or 1
        )
        rows = []
        for date in sorted(daily_tokens.keys()):
            stats = daily_tokens[date]
            tok = stats.get("total", 0)
            w = max(int(220 * tok / max_tokens), 1)
            rows.append(
                f'        <div class="bar-row"><span class="bar-label" title="{_esc(date)}">{_esc(date)}</span>'
                f'<span class="bar-track"><span class="bar-fill" style="width:{w}px"></span></span>'
                f'<span class="bar-val">{format_number(tok)}</span></div>'
            )
        lines.append('    <div class="section">')
        lines.append('        <h2 class="section-title">每日 Token 消耗趋势</h2>')
        lines.append('        <div class="chart-bars">')
        lines.append("            <p><strong>每日 Token 消耗（原始总计）</strong></p>")
        lines.extend(rows)
        lines.append("        </div>")
        lines.append("    </div>")

    # （新增）三、模型使用与成本对比
    lines.extend(build_model_section("html", data))
    lines.extend(build_reconciliation_section("html", data))
    if not _hidden_h:
        # 档位维度的价值全在「倍率 × 估算单价」，tokens_only 下没有可算的钱
        lines.extend(build_tier_section("html", data))

    # （新增）四、成本深度分析（每会话 / 异常 / 省钱）
    lines.extend(build_cost_analysis_section("html", data))

    # 五、任务类型统计
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">五、任务类型统计</h2>')
    lines.append(
        '        <p style="font-size:.85em;opacity:.75;margin:.4em 0">统计口径：仅含本期有 trace（token 活动）的会话；历史空会话（无 token 活动）不计入，避免虚高。</p>'
    )
    lines.append("        <table>")
    lines.append("            <tr><th>任务类型</th><th>会话数</th><th>占比</th></tr>")
    if task_dist:
        total_tasks = sum(task_dist.values())
        for task_type, count in sorted(
            task_dist.items(), key=lambda x: x[1], reverse=True
        ):
            pct = count / total_tasks * 100 if total_tasks else 0
            lines.append(
                f"            <tr><td>{_esc(task_type)}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
            )
    else:
        lines.append("            <tr><td colspan='3'>暂无任务数据</td></tr>")
    lines.append("        </table>")
    lines.append(
        '        <p style="font-size:.85em;opacity:.75;margin:.4em 0">ℹ️ 「其他」= 无法自动归类到已知任务类型的会话（含无标题且对话内容缺失的会话）。</p>'
    )
    lines.append("    </div>")

    # 五、任务 Token 消耗统计
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">六、任务 Token 消耗统计</h2>')
    task_token_stats = data.get("task_token_stats", [])
    # 过滤掉 0 token 的行（避免表格出现无意义的 0.0% 行）
    display_stats = [s for s in task_token_stats if s.get("effective_tokens", 0) > 0]
    if _hidden_h:
        lines.append(
            "        <p>按任务类型聚合的 Token 消耗，反映哪类任务最吃 token。"
            "排名按「实际消耗」排序；缓存占比高说明该任务大量复用同一段上下文。</p>"
        )
    else:
        lines.append(
            "        <p>按任务类型聚合的 Token 消耗，排名按「实际消耗（计费等效）」排序；"
            "缓存命中 token 按约 1/10 价计费，不虚高。缓存占比高说明该任务大量复用同一段上下文。</p>"
        )
    if display_stats:
        total_eff = sum(s.get("effective_tokens", 0) for s in display_stats)
        total_tok = sum(s["total_tokens"] for s in display_stats)
        lines.append("        <table>")
        if _hidden_h:
            lines.append(
                "            <tr><th>任务类型</th><th>会话数</th><th>实际消耗</th><th>原始总Token</th><th>输入</th><th>输出</th><th>缓存占比</th><th>占比</th></tr>"
            )
        else:
            lines.append(
                "            <tr><th>任务类型</th><th>会话数</th><th>实际消耗</th><th>原始总Token</th><th>输入</th><th>输出</th><th>缓存占比</th><th>实际成本</th><th>占比</th></tr>"
            )
        for s in display_stats:
            eff = s.get("effective_tokens", 0)
            pct = (eff / total_eff * 100) if total_eff else 0
            c_ratio = (
                (s["cached_tokens"] / s["input_tokens"] * 100)
                if s.get("input_tokens")
                else 0
            )
            lines.append(
                f"            <tr><td>{_esc(s['task_type'])}</td><td>{s['session_count']}</td>"
                f"<td>{format_number(eff)}</td><td>{format_number(s['total_tokens'])}</td>"
                f"<td>{format_number(s['input_tokens'])}</td><td>{format_number(s['output_tokens'])}</td>"
                f"<td>{c_ratio:.0f}%</td>"
                + ("" if _hidden_h else f"<td>¥{s.get('effective_cost', 0):.2f}</td>")
                + f"<td>{pct:.1f}%</td></tr>"
            )
        lines.append("        </table>")
        lines.append(
            '        <p style="font-size:.85em;opacity:.75;margin:.4em 0">ℹ️ 「未关联会话」= trace 的会话 ID 在本地会话库找不到（孤儿 trace，已合并为单一汇总行）；「未命名会话」= 本地会话库中确有但无标题的会话；「其他」= 任务类型无法自动归类或自动分类失败的 token。</p>'
        )
        top = task_token_stats[0]
        top_pct = (top.get("effective_tokens", 0) / total_eff * 100) if total_eff else 0
        lines.append(
            f"        <p>🔥 <strong>实际消耗最高的任务类型</strong>：{top['task_type']} —— "
            f"{format_number(top.get('effective_tokens', 0))} token（原始 {format_number(top['total_tokens'])}），"
            f"占 {top_pct:.1f}%"
            + ("" if _hidden_h else f"，实际成本 ¥{top.get('effective_cost', 0):.2f}")
            + "。</p>"
        )
        # 环形图：各任务类型 实际消耗 token 占比
        donut = build_donut_chart(display_stats, title=_donut_title(data))
        if donut:
            lines.append(
                "        <p><strong>各任务类型 实际消耗 Token 占比</strong>：</p>"
            )
            lines.append(donut)
        # Top 10 最吃 token 的任务对话框（含自动化任务会话）
        top_tasks = data.get("top_tasks", [])
        if top_tasks:
            lines.append(
                "        <p><strong>实际消耗最高的 10 个任务对话框</strong>（含自动化任务，按会话实际消耗排序）：</p>"
            )
            lines.append("        <table>")
            if _hidden_h:
                lines.append(
                    "            <tr><th>排名</th><th>任务名称</th><th>任务类型</th><th>实际消耗</th><th>原始总Token</th><th>缓存占比</th></tr>"
                )
            else:
                lines.append(
                    "            <tr><th>排名</th><th>任务名称</th><th>任务类型</th><th>实际消耗</th><th>原始总Token</th><th>缓存占比</th><th>实际成本</th></tr>"
                )
            for i, tk in enumerate(top_tasks, 1):
                c_ratio = (
                    (tk.get("cached_tokens", 0) / tk["input_tokens"] * 100)
                    if tk.get("input_tokens")
                    else 0
                )
                lines.append(
                    f"            <tr><td>{i}</td><td>{_esc(tk.get('title', '-'))}</td>"
                    f"<td>{_esc(tk.get('task_type', '-'))}</td>"
                    f"<td>{format_number(tk.get('effective_tokens', 0))}</td>"
                    f"<td>{format_number(tk.get('total_tokens', 0))}</td>"
                    f"<td>{c_ratio:.0f}%</td>"
                    + (
                        ""
                        if _hidden_h
                        else f"<td>¥{tk.get('effective_cost', 0):.2f}</td>"
                    )
                    + "</tr>"
                )
            lines.append("        </table>")
    else:
        lines.append(f"        <p>{_short}无任务 Token 消耗数据</p>")
    lines.append("    </div>")

    # 六、技能使用统计
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">七、技能使用统计</h2>')
    lines.append("        <table>")
    lines.append(
        "            <tr><th>技能名称</th><th>使用次数</th><th>最近使用</th></tr>"
    )
    if skills:
        for sid, sdata in sorted(
            skills.items(),
            key=lambda x: x[1].get("usage_count_in_range", 0),
            reverse=True,
        ):
            lines.append(
                f"            <tr><td>{_esc(sid)}</td><td>{sdata.get('usage_count_in_range', 0)}</td><td>{sdata.get('last_used', '-')}</td></tr>"
            )
    else:
        lines.append(f"            <tr><td colspan='3'>{_short}未使用技能</td></tr>")
    lines.append("        </table>")
    lines.append("    </div>")

    # 七、自动化任务运行情况
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">八、自动化任务运行情况</h2>')
    lines.append("        <table>")
    lines.append(
        "            <tr><th>任务名称</th><th>状态</th><th>运行次数</th><th>成功</th><th>失败</th><th>最近一次结果</th><th>最近一次运行日期</th></tr>"
    )
    if automation_runs:
        auto_groups = defaultdict(list)
        for run in automation_runs:
            auto_groups[run.get("automation_id", "unknown")].append(run)
        for auto_id, runs in sorted(
            auto_groups.items(), key=lambda x: len(x[1]), reverse=True
        ):
            success = sum(1 for r in runs if r.get("result_success"))
            fail = len(runs) - success
            if runs:
                latest_result = "成功" if runs[-1].get("result_success") else "失败"
            else:
                latest_result = "-"
            label = runs[0].get("automation_name") or auto_id
            auto_state = _auto_state_label(runs[0].get("auto_status"))
            dates = [r.get("created_date", "") for r in runs if r.get("created_date")]
            last_run_date = max(dates) if dates else "-"
            lines.append(
                f"            <tr><td>{_esc(label)}</td><td>{auto_state}</td><td>{len(runs)}</td><td>{success}</td><td>{fail}</td><td>{latest_result}</td><td>{last_run_date}</td></tr>"
            )
    else:
        lines.append(
            f"            <tr><td colspan='7'>{_short}无自动化任务运行记录</td></tr>"
        )
    lines.append("        </table>")
    lines.append("    </div>")

    # 八、产出物清单
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">九、产出物清单</h2>')
    lines.append("        <table>")
    lines.append(
        "            <tr><th>文件</th><th>类型</th><th>日期</th><th>大小</th></tr>"
    )
    if outputs:
        for out in outputs[:20]:
            ext = out.get("extension", "").lstrip(".")
            size = format_file_size(out.get("size_bytes", 0))
            fname = out.get("file_name", "-")
            lines.append(
                f"            <tr><td>{_esc(fname)}</td><td>{_esc(ext or '-')}</td><td>{out.get('date', '-')}</td><td>{size}</td></tr>"
            )
    else:
        lines.append(f"            <tr><td colspan='4'>{_short}无产出文件</td></tr>")
    lines.append("        </table>")
    lines.append("    </div>")

    # 十、核心洞察与建议（数据驱动：钱优先 + 判断 + 行动）
    lines.append('    <div class="section">')
    lines.append('        <h2 class="section-title">十、核心洞察与建议</h2>')
    eff_cost = summary.get("total_effective_cost", 0)
    raw_cost = summary.get("total_cost", 0)
    eff_tokens = summary.get("total_effective_tokens", 0)
    cache_saving = max(raw_cost - eff_cost, 0)
    session_credits = data.get("session_credits", [])

    # 💰 花费速览 / tokens_only 下为 📈 用量速览
    if _hidden_h:
        lines.append("        <h3>📈 用量速览</h3>")
        lines.append(
            f"        <p>本期实际消耗 <strong>{format_number(eff_tokens)} token</strong>"
            f"（原始 {format_number(summary.get('total_tokens', 0))}）。"
            f"计价模式 <code>tokens_only</code>：本期无模型命中单价，"
            f"<strong>不输出金额与省钱结论</strong>。</p>"
        )
    else:
        lines.append("        <h3>💰 花费速览</h3>")
        lines.append(
            f"        <p>本期实际花费 <strong>¥{eff_cost:.2f}</strong>（原始口径 ¥{raw_cost:.2f}），"
            f"缓存复用为你节省约 <strong>¥{cache_saving:.2f}</strong>。</p>"
        )
        if session_credits:
            latest = max(session_credits, key=lambda x: x.get("updated_at", 0))
            used = latest.get("used", 0)
            size = latest.get("size", 0)
            if size > 0:
                lines.append(
                    f"        <p>当前会话额度已用 <strong>{used / size * 100:.0f}%</strong>"
                    f"（{format_number(used)} / {format_number(size)}）。</p>"
                )

    # 🔍 最大成本来源
    if daily_tokens and eff_tokens:
        peak_day, peak_stats = max(
            daily_tokens.items(), key=lambda x: x[1].get("effective", 0)
        )
        peak_cost = peak_stats.get("effective_cost", 0)
        peak_tok = peak_stats.get("effective", 0)
        peak_share = peak_tok / eff_tokens * 100
        verdict = (
            "占本期实际消耗比重偏高，建议复盘当日是否存在可精简的批量/重复任务"
            if peak_share >= 25
            else "占本期实际消耗比重正常，属单日波动"
        )
        lines.append(
            "        <h3>🔍 最大成本来源</h3>"
            if not _hidden_h
            else "        <h3>🔍 最大消耗日</h3>"
        )
        if _hidden_h:
            lines.append(
                f"        <p><strong>高峰日 {peak_day}</strong>：{format_number(peak_tok)} token，"
                f"占本期实际消耗 <strong>{peak_share:.1f}%</strong>——{verdict}。</p>"
            )
        else:
            lines.append(
                f"        <p><strong>高峰日 {peak_day}</strong>：实际花费 ¥{peak_cost:.2f}"
                f"（{format_number(peak_tok)} token），占本期实际消耗 <strong>{peak_share:.1f}%</strong>——{verdict}。</p>"
            )

    # 📊 任务类型洞察
    if task_dist:
        total_count = sum(task_dist.values())
        top_task, top_n = max(task_dist.items(), key=lambda x: x[1])
        top_pct = top_n / total_count * 100
        if top_pct >= 50:
            shape = "高度集中于单一类型，建议确认是否为预期工作流"
        elif top_pct >= 25:
            shape = "相对集中，为本期主力任务"
        else:
            shape = "分布较均衡，未见单一类型主导"
        lines.append("        <h3>📊 任务类型洞察</h3>")
        _scope_h = (
            ""
            if total_count == summary.get("total_sessions")
            else f"，仅统计本期有 token 活动的 {total_count} 个会话"
        )
        lines.append(
            f"        <p><strong>主要任务类型</strong>：{_esc(top_task)}（{top_n} 次，{top_pct:.1f}%{_scope_h}）——{shape}。</p>"
        )

    # ✅ 省钱成就 —— tokens_only 下无钱可翻
    if cache_rate > 0 and not _hidden_h:
        lines.append("        <h3>✅ 省钱成就</h3>")
        lines.append(
            f"        <p>缓存命中率达 <strong>{cache_rate:.1f}%</strong>，按原始全价计费你本应付约 ¥{raw_cost:.2f}，"
            f"实际仅 ¥{eff_cost:.2f}——<strong>缓存为你省下 ¥{cache_saving:.2f}</strong>，"
            f"是实际成本远低于原始账单的主因。</p>"
        )
    lines.append("    </div>")

    # 十、下期展望（基于实际数据动态生成）
    lines.append('    <div class="section">')
    lines.append(f'        <h2 class="section-title">十一、{_next}展望</h2>')
    lines.append(
        f"        <p>基于{_short}实际数据，先预测下期用量，再按优先级给出行动建议：</p>"
    )
    lines.append("        <ul>")
    for item in build_next_week_outlook(
        summary,
        daily_tokens,
        automation_runs,
        data.get("session_credits", []),
        period_key=_key,
        cost_hidden=_cost_hidden(data),
        anomaly_days=_token_anomaly_days(data),
        background_runs=(meta.get("background_runs") or {}),
    ):
        raw = item[2:].strip() if item.startswith("- ") else item
        escaped = _esc(raw)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        lines.append(f"            <li>{text}</li>")
    lines.append("        </ul>")
    lines.append("    </div>")

    lines.append("    <footer>")
    lines.append(
        f'        <p style="text-align: center; color: var(--muted); margin-top: 40px;">{_footer_text(data)}</p>'
    )
    lines.append("    </footer>")
    lines.append("    <script>")
    lines.append("        (function(){")
    lines.append("            var root = document.documentElement;")
    lines.append(
        '            var btns = document.querySelectorAll(".theme-toggle button");'
    )
    lines.append("            function applyTheme(t){")
    lines.append(
        '                if(t==="system"){ root.removeAttribute("data-theme"); }'
    )
    lines.append('                else { root.setAttribute("data-theme", t); }')
    lines.append(
        '                try { localStorage.setItem("aurs-theme", t); } catch(e){}'
    )
    lines.append(
        '                btns.forEach(function(b){ b.classList.toggle("active", b.getAttribute("data-set-theme")===t); });'
    )
    lines.append("            }")
    lines.append(
        '            btns.forEach(function(b){ b.addEventListener("click", function(){ applyTheme(b.getAttribute("data-set-theme")); }); });'
    )
    lines.append('            var saved = "system";')
    lines.append(
        '            try { saved = localStorage.getItem("aurs-theme") || "system"; } catch(e){}'
    )
    lines.append("            applyTheme(saved);")
    lines.append("        })();")
    lines.append("    </script>")
    lines.append("</body>")
    lines.append("</html>")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# JSON 格式
# ─────────────────────────────────────────────────────────────
def generate_json_report(data):
    meta = data.get("meta", {})
    summary = data.get("summary", {})
    traces = data.get("traces", [])
    sessions = data.get("sessions", [])
    automation_runs = data.get("automation_runs", [])
    session_credits = data.get("session_credits", [])
    skill_usage = data.get("skill_usage", {})
    outputs = data.get("outputs", [])
    daily_tokens = data.get("daily_tokens", {})

    task_dist = summary.get("task_type_distribution", {})
    total_input = summary.get("total_input_tokens", 0)
    total_cached = summary.get("total_cached_tokens", 0)
    cache_rate = (total_cached / total_input * 100) if total_input else 0

    model_stats = data.get("model_stats", [])
    exec_stats = data.get("model_exec_stats", [])
    # 最常使用模型：基于「实际执行模型」维度，且排除路由别名（auto），取最具体的真实模型
    _calls_src = (
        [m for m in exec_stats if not m.get("is_router")]
        or [m for m in model_stats if not m.get("is_router")]
        or (exec_stats or model_stats)
    )
    top_model_by_calls = (
        max(_calls_src, key=lambda x: x["calls"])["model"] if _calls_src else None
    )
    configured = [m for m in model_stats if m.get("configured")]
    priced_models = [m for m in configured if m.get("effective_cost", 0) > 0]
    concrete_priced = [m for m in priced_models if not m.get("is_router")]
    _cost_src = concrete_priced or priced_models
    top_model_by_cost = (
        max(_cost_src, key=lambda x: x.get("effective_cost", 0))["model"]
        if _cost_src
        else None
    )

    _title_j, _, _sources_j = _source_identity(data)
    report = {
        "meta": {
            "report_title": _title_j,
            "start_date": meta.get("start_date", ""),
            "end_date": meta.get("end_date", ""),
            "generated_at": _fmt_generated_at(),
            "data_sources": _sources_j,
            "source": _source_key(data),
            "cost_mode": _cost_mode(data),
            "tokens_source": meta.get("tokens_source", "reported"),
            "mode_rates": meta.get("mode_rates"),
            "mode_cost_estimated": meta.get("mode_cost_estimated"),
            "mode_config_cache_loaded": meta.get("mode_config_cache_loaded"),
            "mode_config_cache_path": meta.get("mode_config_cache_path"),
            "mode_config_cache_mtime": meta.get("mode_config_cache_mtime"),
        },
        "summary": {
            "overview": {
                "active_days": summary.get("active_days", []),
                "active_day_count": summary.get("active_day_count", 0),
                "total_sessions": summary.get("total_sessions", 0),
                "total_traces": summary.get("total_traces", 0),
                "total_automation_runs": summary.get("total_automation_runs", 0),
                "successful_automation_runs": summary.get(
                    "successful_automation_runs", 0
                ),
                "total_outputs": summary.get("total_outputs", 0),
                "skills_used": summary.get("skills_used", 0),
                "total_cost": summary.get("total_cost", 0),
                "total_input_cost": summary.get("total_input_cost", 0),
                "total_output_cost": summary.get("total_output_cost", 0),
            },
            "token_usage": {
                "total_tokens": summary.get("total_tokens", 0),
                "total_effective_tokens": summary.get("total_effective_tokens", 0),
                "total_input_tokens": summary.get("total_input_tokens", 0),
                "total_output_tokens": summary.get("total_output_tokens", 0),
                "total_cached_tokens": summary.get("total_cached_tokens", 0),
                "cache_rate": round(cache_rate, 1),
                "total_cost": summary.get("total_cost", 0),
                "total_effective_cost": summary.get("total_effective_cost", 0),
            },
            "task_types": task_dist,
            "daily_tokens": daily_tokens,
            "skill_usage": skill_usage.get("skills", {}),
            "automation_summary": {
                "total_runs": len(automation_runs),
                "successful_runs": sum(
                    1 for r in automation_runs if r.get("result_success")
                ),
                "failed_runs": len(automation_runs)
                - sum(1 for r in automation_runs if r.get("result_success")),
            },
            "model_breakdown": model_stats,
            "model_exec_breakdown": exec_stats,
        },
        "details": {
            "sessions": sessions,
            "automation_runs": automation_runs,
            "outputs": outputs,
            "session_credits": session_credits,
            "full_traces": traces,
        },
        "insights": {
            "peak_usage": {
                "day": max(daily_tokens.items(), key=lambda x: x[1].get("total", 0))[0]
                if daily_tokens
                else None,
                "tokens": max(
                    (v.get("total", 0) for v in daily_tokens.values()), default=0
                )
                if daily_tokens
                else 0,
            },
            "dominant_task_type": max(task_dist.items(), key=lambda x: x[1])
            if task_dist
            else None,
            "cache_efficiency": "优秀"
            if cache_rate > 80
            else "良好"
            if cache_rate > 60
            else "一般",
            "top_model_by_calls": top_model_by_calls,
            "top_model_by_cost": top_model_by_cost,
            "cost_analysis": {
                "top_sessions": [
                    {
                        "title": r["title"],
                        "task_type": r["task_type"],
                        "effective_cost": r["effective_cost"],
                        "effective_tokens": r["effective_tokens"],
                        "calls": r["calls"],
                        "models": r["models"],
                    }
                    for r in (data.get("session_stats") or {}).get("rows", [])[:10]
                ],
                "distribution": (data.get("session_stats") or {}).get("buckets", []),
                "anomalies": data.get("cost_anomalies", {}),
                "savings": data.get("savings_insights", {}),
            },
        },
    }

    return json.dumps(report, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Agent 使用情况报告生成器")
    parser.add_argument(
        "data_file", nargs="?", help="数据 JSON 文件路径（未提供则实时采集）"
    )
    parser.add_argument(
        "--period",
        choices=["day", "week", "month", "year"],
        default="week",
        help="时间窗口预设（实时采集时使用，默认 week）："
        "day=今天 / week=当前日历周(YYYY年第WW周，周一至周日，不论生成日在周中或周末) / "
        "month=当前自然月(MM月，1日至月底) / year=当前自然年(YYYY年全年)",
    )
    parser.add_argument(
        "--days", type=int, help="自定义滚动天数，覆盖 --period（实时采集时使用）"
    )
    parser.add_argument(
        "--start", type=str, help="绝对起始日期 YYYY-MM-DD（实时采集时使用）"
    )
    parser.add_argument(
        "--end", type=str, help="绝对结束日期 YYYY-MM-DD（实时采集时使用）"
    )
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument(
        "--format",
        type=str,
        default="markdown",
        choices=["markdown", "html", "json"],
        help="输出格式",
    )
    args = parser.parse_args()

    if args.data_file:
        data = json.loads(Path(args.data_file).read_text(encoding="utf-8"))
    else:
        import collect_usage_data as collector

        start_date, end_date, period_key, period_label = collector.resolve_date_range(
            period=args.period, days=args.days, start=args.start, end=args.end
        )
        db_data = collector.collect_db_data(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        traces = collector.collect_traces(start_date, end_date, sid_to_rawmodel)
        skill_usage = collector.collect_skill_usage(start_date, end_date)
        outputs, memory_logs = collector.collect_session_outputs(start_date, end_date)
        collector.collect_task_types(db_data["sessions"])

        total_tokens = sum(t["total_tokens"] for t in traces)
        total_input = sum(t["input_tokens"] for t in traces)
        total_output = sum(t["output_tokens"] for t in traces)
        total_cached = sum(t["cached_tokens"] for t in traces)
        total_effective = sum(t.get("effective_tokens", 0) for t in traces)
        total_effective_cost = round(
            sum(t.get("effective_cost", 0.0) for t in traces), 2
        )
        cache_rate = (total_cached / total_input * 100) if total_input else 0

        daily_tokens = {}
        for t in traces:
            d = t["date"]
            if d not in daily_tokens:
                daily_tokens[d] = {
                    "total": 0,
                    "input": 0,
                    "output": 0,
                    "cached": 0,
                    "calls": 0,
                    "total_cost": 0.0,
                    "effective": 0,
                    "effective_cost": 0,
                }
            daily_tokens[d]["total"] += t["total_tokens"]
            daily_tokens[d]["input"] += t["input_tokens"]
            daily_tokens[d]["output"] += t["output_tokens"]
            daily_tokens[d]["cached"] += t["cached_tokens"]
            daily_tokens[d]["calls"] += t["call_count"]
            daily_tokens[d]["total_cost"] += t.get("cost", 0.0)
            daily_tokens[d]["effective"] += t.get("effective_tokens", 0)
            daily_tokens[d]["effective_cost"] += t.get("effective_cost", 0.0)

        # 活跃天数 = 窗口内产生 token 活动的日期（仅 trace 日期，避免会话创建日虚高）
        active_days = set(t["date"] for t in traces)

        # §5 任务类型分布（D5：仅统计「真正产生 token 活动」的会话）
        # 与 §一「N 个有 token 活动」、§4.2、§六 口径一致：不再把「有 trace 但估算
        # token 为 0」的会话算进来——否则 §5 计数会与全文打架（千问办公字符估算口径下
        # 偶发 0-token 会话，会让 §5=8 而 §1/§4.2/§6=7）。
        token_active_ids = token_active_session_ids(traces)
        task_dist = {}
        for s in db_data["sessions"]:
            if s.get("id") not in token_active_ids:
                continue
            tt = s.get("task_type", "其他")
            task_dist[tt] = task_dist.get(tt, 0) + 1

        _session_stats = collector.aggregate_by_session(traces, db_data["sessions"])
        data = {
            "meta": {
                "start_date": start_date,
                "end_date": end_date,
                "period": period_key,
                "period_label": period_label,
                "days": args.days
                if args.days is not None
                else collector.PERIOD_DAYS.get(period_key, 7),
            },
            "traces": traces,
            "sessions": db_data["sessions"],
            "automation_runs": db_data["automation_runs"],
            "session_credits": db_data["session_credits"],
            "skill_usage": skill_usage,
            "outputs": outputs,
            "daily_tokens": daily_tokens,
            "summary": {
                "total_traces": len(traces),
                "total_sessions": len(db_data["sessions"]),
                "total_tokens": total_tokens,
                "total_input_tokens": total_input,
                "total_output_tokens": total_output,
                "total_cached_tokens": total_cached,
                "total_effective_tokens": total_effective,
                "cache_rate": round(cache_rate, 1),
                "active_days": sorted(active_days),
                "active_day_count": len(active_days),
                "total_automation_runs": len(db_data["automation_runs"]),
                "successful_automation_runs": sum(
                    1 for r in db_data["automation_runs"] if r["result_success"]
                ),
                "total_outputs": len(outputs),
                "skills_used": len(skill_usage.get("skills", {})),
                "task_type_distribution": task_dist,
                "total_cost": sum(t.get("total_cost", 0.0) for t in traces),
                "total_input_cost": sum(t.get("input_cost", 0.0) for t in traces),
                "total_output_cost": sum(t.get("output_cost", 0.0) for t in traces),
                "total_effective_cost": round(total_effective_cost, 2),
            },
            "task_token_stats": collector.aggregate_task_token_stats(
                traces, db_data["sessions"]
            ),
            "top_tasks": collector.aggregate_top_tasks(
                traces, db_data["sessions"], top_n=10
            ),
            # §3.1 改为「实际计费模型」维度（exec_model，与头条/账单一致），
            # §3.2 改为「入口/配置」维度（model_key，使用分布）。对调两节数据源以消除 §3.1 与头条矛盾。
            "model_stats": collector.aggregate_by_exec_model(traces),
            "model_exec_stats": collector.aggregate_by_model(traces),
            "session_stats": _session_stats,
            "cost_anomalies": collector.detect_cost_anomalies(
                daily_tokens, _session_stats
            ),
            "savings_insights": collector.build_savings_insights(
                collector.aggregate_by_exec_model(traces)
            ),
            # 档位维度（快速/均衡/极致）。与 §3.1/§3.2 同源、金额口径一致。
            "tier_stats": collector.aggregate_by_tier(traces),
        }
        # 将档位估算倍率的「配置缓存校准」状态注入 meta，供 §3.4 与 JSON 输出展示。
        _mode_meta = getattr(collector, "MODE_RATES_META", {}) or {}
        data["meta"]["mode_rates"] = dict(_mode_meta.get("rates", {}) or {})
        data["meta"]["mode_cost_estimated"] = bool(
            _mode_meta.get("auto_estimate", False)
        )
        data["meta"]["mode_config_cache_loaded"] = bool(
            _mode_meta.get("config_cache_loaded", False)
        )
        data["meta"]["mode_config_cache_path"] = _mode_meta.get("config_cache_path")
        data["meta"]["mode_config_cache_mtime"] = _mode_meta.get("config_cache_mtime")

    if args.format == "markdown":
        report = generate_markdown_report(data)
    elif args.format == "html":
        report = generate_html_report(data)
    else:
        report = generate_json_report(data)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        _pl = _PERIOD_LABEL.get((data.get("meta", {}).get("period", "week")), "周报")
        print(f"[OK] {_pl}已保存到 {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
