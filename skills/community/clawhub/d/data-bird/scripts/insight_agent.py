"""
InsightAgent: 生成咨询式短报告结构，兼容旧 conclusions/anomalies/suggestions 字段。
默认不发送原始行样本，优先依赖字段画像、统计摘要和图表结论。
"""
import json
import os
from typing import Any, Callable, Dict, List, Optional


def _trim(items: List[str], limit: int, max_len: int = 58) -> List[str]:
    out: List[str] = []
    for item in items:
        s = " ".join(str(item or "").split())
        if not s:
            continue
        if len(s) > max_len:
            s = s[: max_len - 1].rstrip() + "…"
        out.append(s)
        if len(out) >= limit:
            break
    return out


def _analysis_brief(analysis: Dict[str, Any]) -> str:
    parts: List[str] = []
    for r in (analysis.get("results") or [])[:10]:
        if r.get("error"):
            continue
        hint = str(r.get("title_hint") or r.get("type") or "").strip()
        takeaway = str(r.get("takeaway_hint") or "").strip()
        if takeaway:
            parts.append(f"{hint}: {takeaway}")
        elif hint:
            parts.append(hint)
    return "；".join(parts) if parts else "（无可用图表摘要）"


def _profile_brief(schema: Dict[str, Any], max_cols: int = 12) -> str:
    prof = (schema.get("profile") or {}).get("columns") or []
    lines: List[str] = []
    for p in prof[:max_cols]:
        lines.append(
            f"{p.get('name', '')}({p.get('semanticType', '')}) 缺失{p.get('null_pct', 0)}% 唯一值{p.get('unique_count', 0)}"
        )
    if len(prof) > max_cols:
        lines.append(f"...共 {len(prof)} 列")
    return "\n".join(lines)


def _default_insight(context: Dict[str, Any], data_summary: str) -> Dict[str, Any]:
    schema = context.get("schema") or {}
    analysis = context.get("analysis") or {}
    query = str(context.get("query") or "").strip() or "通用业务分析"
    row_count = int(schema.get("row_count") or 0)
    scenario_label = str(schema.get("scenario_label") or "通用数据分析")
    time_col = schema.get("detected_time_column") or "未识别"
    takeaways = _trim(
        [str(r.get("takeaway_hint") or "") for r in (analysis.get("results") or []) if r.get("takeaway_hint")],
        8,
        max_len=54,
    )
    high_missing = list(((schema.get("data_quality") or {}).get("high_missing_columns") or []))[:3]
    metrics = list(schema.get("metric_columns") or [])
    dims = list(schema.get("dimension_columns") or [])
    generated_chart_count = int(analysis.get("generated_chart_count") or len(analysis.get("results") or []))

    executive = _trim(
        [
            f"本次报告围绕“{query}”生成，数据规模为 {row_count} 行，当前识别为{scenario_label}场景。",
            f"报告已覆盖 {generated_chart_count} 张图，优先从趋势、结构、对比、分布和异常五类证据归纳结论。",
            takeaways[0] if takeaways else f"当前可重点关注字段“{(metrics or dims or ['核心指标'])[0]}”的变化表现。",
        ],
        3,
        60,
    )

    findings = _trim(
        takeaways[:4]
        or [
            f"当前数据已识别 {len(metrics)} 个数值字段与 {len(dims)} 个维度字段。",
            f"时间字段识别结果为：{time_col}。",
        ],
        4,
        56,
    )

    drivers = _trim(
        [
            f"建议优先从“{dims[0]}”维度拆解核心指标，区分头部集中与尾部拖累。" if dims else "",
            f"如需解释波动来源，可联动“{metrics[0]}”与“{metrics[1]}”判断联动关系。" if len(metrics) >= 2 else "",
            f"若存在时间维度，应优先判断阶段波动与结构变化，而非仅看总量高低。" if schema.get("detected_time_column") else "",
        ],
        3,
        58,
    )

    risks = _trim(
        [
            f"字段 {', '.join(str(c) for c in high_missing)} 缺失较高，可能影响结论稳定性。" if high_missing else "",
            "若缺少时间、成本或主键字段，趋势、利润与复购类判断应保持谨慎。",
        ],
        3,
        58,
    )

    opportunities = _trim(
        [
            "建议优先围绕头部贡献维度做资源聚焦，再验证尾部是否存在低效投入。",
            "若相关性图显示联动明显，可进一步设计分层经营或交叉销售动作。",
        ],
        2,
        58,
    )

    action_plan = _trim(
        [
            "先确认最重要的业务目标字段，再按区域/品类/客户等维度做二次拆解。",
            "对高缺失字段补齐口径，并对异常点做样本核查，避免被噪声误导。",
            "围绕头部贡献项与尾部风险项各形成一条短期执行动作，便于业务闭环。",
        ],
        3,
        58,
    )

    return {
        "style": "consulting",
        "scenario": schema.get("scenario") or "generic_profile",
        "scenarioLabel": scenario_label,
        "executiveSummary": executive,
        "keyFindings": findings,
        "driverAnalysis": drivers,
        "risks": risks,
        "opportunities": opportunities,
        "actionPlan": action_plan,
        "chartTakeaways": takeaways[:8],
        "conclusions": _trim(executive[:1] + findings[:2], 3, 56),
        "anomalies": _trim(risks, 3, 56),
        "suggestions": _trim(action_plan, 3, 56),
        "reportMeta": {
            "maxChars": 1000,
            "targetChars": 900,
            "chartCount": generated_chart_count,
            "dataSummary": data_summary[:500],
        },
    }


def _normalize_llm_insight(payload: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(fallback)
    for key in (
        "style",
        "scenario",
        "scenarioLabel",
        "executiveSummary",
        "keyFindings",
        "driverAnalysis",
        "risks",
        "opportunities",
        "actionPlan",
        "chartTakeaways",
        "conclusions",
        "anomalies",
        "suggestions",
        "reportMeta",
    ):
        if key in payload:
            out[key] = payload.get(key)
    out["executiveSummary"] = _trim(list(out.get("executiveSummary") or []), 3, 60)
    out["keyFindings"] = _trim(list(out.get("keyFindings") or []), 4, 58)
    out["driverAnalysis"] = _trim(list(out.get("driverAnalysis") or []), 3, 58)
    out["risks"] = _trim(list(out.get("risks") or []), 3, 58)
    out["opportunities"] = _trim(list(out.get("opportunities") or []), 2, 58)
    out["actionPlan"] = _trim(list(out.get("actionPlan") or []), 3, 58)
    out["chartTakeaways"] = _trim(list(out.get("chartTakeaways") or []), 8, 54)
    out["conclusions"] = _trim(list(out.get("conclusions") or []) or out["executiveSummary"][:1] + out["keyFindings"][:2], 3, 56)
    out["anomalies"] = _trim(list(out.get("anomalies") or []) or out["risks"][:3], 3, 56)
    out["suggestions"] = _trim(list(out.get("suggestions") or []) or out["actionPlan"][:3], 3, 56)
    return out


def run(
    context: Dict[str, Any],
    llm_call: Optional[Callable[[str, str], str]] = None,
) -> Dict[str, Any]:
    schema = context.get("schema") or {}
    df = context.get("df")
    query = str(context.get("query") or "").strip()
    analysis = context.get("analysis") or {}
    opts = context.get("options") if isinstance(context.get("options"), dict) else {}

    include_samples = bool(opts.get("llm_include_row_samples"))
    if os.environ.get("CLAW_BI_LLM_INCLUDE_SAMPLES", "").strip().lower() in ("1", "true", "yes"):
        include_samples = True

    row_count = schema.get("row_count") or (len(df) if df is not None else 0)
    col_meta = schema.get("columns") or []
    column_names = [c.get("name", "") for c in col_meta]

    stats_block = ""
    if df is not None and len(df) > 0:
        try:
            num_df = df.select_dtypes(include=["number"])
            if num_df.shape[1] > 0:
                stats_block = num_df.describe().head(20).to_string()[:1200]
        except Exception:
            stats_block = "（数值统计略）"

    sample_block = ""
    if include_samples and df is not None and len(df) > 0:
        try:
            sample_block = df.head(3).to_string()[:600]
        except Exception:
            sample_block = ""

    data_summary = "\n".join(
        [
            f"行数: {row_count}",
            f"场景: {schema.get('scenario_label') or schema.get('scenario')}",
            f"列名: {column_names}",
            f"时间列: {schema.get('detected_time_column')}",
            "## 字段质量",
            _profile_brief(schema),
            "## 图表与结论线索",
            _analysis_brief(analysis),
            "## 数值列描述统计",
            stats_block or "无",
        ]
    )
    if sample_block:
        data_summary += f"\n## 原始行样本（已显式授权）\n{sample_block}"

    fallback = _default_insight(context, data_summary)
    prompt_template = """你是一位顶级咨询顾问风格的数据分析师。请基于数据摘要生成一份短咨询式分析，适配任何行业与业务。

要求：
1. 中文输出，正文总量控制在 700-900 字以内，绝不超过 1000 字。
2. 只基于给定数据摘要推断，不能编造行业事实。
3. 先给结论，再给驱动，再给风险与动作。
4. 用业务中性表达，避免空泛口号。
5. 若数据不足，请明确写入 risks，而不是强行下结论。

输出 JSON（不要 markdown 代码块）：
{{
  "style": "consulting",
  "executiveSummary": ["一句话结论1", "一句话结论2", "一句话结论3"],
  "keyFindings": ["关键发现1", "关键发现2", "关键发现3"],
  "driverAnalysis": ["驱动分析1", "驱动分析2"],
  "risks": ["风险1", "风险2"],
  "opportunities": ["机会1", "机会2"],
  "actionPlan": ["动作1", "动作2", "动作3"],
  "chartTakeaways": ["图表要点1", "图表要点2"],
  "conclusions": ["关键结论1", "关键结论2"],
  "anomalies": ["风险提示1"],
  "suggestions": ["行动建议1", "行动建议2"]
}}

## 数据摘要
{data_summary}

## 用户问题
{query}
"""
    user_prompt = prompt_template.format(data_summary=data_summary, query=query or "通用经营分析")

    if llm_call:
        try:
            content = llm_call("", user_prompt)
            start = content.find("{")
            if start >= 0:
                depth, end = 0, -1
                for i in range(start, len(content)):
                    if content[i] == "{":
                        depth += 1
                    elif content[i] == "}":
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                if end > start:
                    insight = json.loads(content[start:end])
                    context["insight"] = _normalize_llm_insight(insight, fallback)
                    return context
        except Exception:
            pass

    context["insight"] = fallback
    return context
