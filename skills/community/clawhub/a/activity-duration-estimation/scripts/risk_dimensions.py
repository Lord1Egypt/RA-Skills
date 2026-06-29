"""
风险维度库 — 按项目上下文自动匹配分析维度 + 生成LLM提示

用法：
    from risk_dimensions import select_dimensions, build_dimension_prompt
    
    # 1. 选维度
    dims = select_dimensions(context)
    
    # 2. 生成维度简报（给LLM的结构指引，不是硬编码内容）
    prompt = build_dimension_prompt(dims, cpm_result, mc_results, phases)
    
    # 3. LLM根据简报写具体的风险分析
    state.risk_analysis = llm_generate(prompt)
"""

import re


# ═══════════════════════════════════════════════════
# 维度定义（只含选择条件和结构指引，不含硬编码内容）
# ═══════════════════════════════════════════════════

DIMENSIONS = {
    "D1": {
        "id": "D1",
        "name": "技术风险",
        "icon": "🛠️",
        "condition": lambda ctx: ctx.get("tech_novelty", "medium") in ("high", "medium")
                                  or "ai" in ctx.get("domain", "").lower(),
        "guide": "技术选型、实现复杂度、集成难度、性能扩展性、安全合规",
    },
    "D2": {
        "id": "D2",
        "name": "供应商/外部依赖风险",
        "icon": "🔗",
        "condition": lambda ctx: ctx.get("domain", "") in ("ai-enterprise", "saas", "platform")
                                  or ctx.get("integration_count", 0) > 2,
        "guide": "第三方API依赖、开源组件、供应商锁定、生态兼容性",
    },
    "D3": {
        "id": "D3",
        "name": "相关方风险",
        "icon": "👥",
        "condition": lambda ctx: ctx.get("scale", "medium") in ("large", "enterprise")
                                  or ctx.get("integration_count", 0) > 3,
        "guide": "用户接受度、管理层支持、跨部门协作、变革阻力",
    },
    "D4": {
        "id": "D4",
        "name": "进度风险",
        "icon": "📅",
        "condition": lambda ctx: True,  # 总是启用
        "guide": "关键路径集中度、并行分支汇合、估算偏差、资源争用",
    },
    "D5": {
        "id": "D5",
        "name": "商务风险",
        "icon": "💰",
        "condition": lambda ctx: ctx.get("is_commercial", False)
                                  or "roi" in str(ctx.get("phases", "")).lower(),
        "guide": "ROI不确定性、市场时机、预算超支、商业可持续性",
    },
    "D6": {
        "id": "D6",
        "name": "资源风险",
        "icon": "👤",
        "condition": lambda ctx: "ai" in ctx.get("domain", "").lower()
                                  or ctx.get("tech_novelty", "medium") == "high",
        "guide": "关键人才获取、团队技能匹配、人员流失风险、培训成本",
    },
    "D7": {
        "id": "D7",
        "name": "路径实现风险",
        "icon": "🔄",
        "condition": lambda ctx: ctx.get("integration_count", 0) > 2
                                  or ctx.get("critical_path_len", 0) > 10,
        "guide": "架构演进、技术债务、回溯兼容、集成测试复杂度",
    },
}


def select_dimensions(context: dict) -> list[dict]:
    """根据项目上下文选择匹配的风险维度"""
    active = []
    for dim_id, dim in DIMENSIONS.items():
        try:
            if dim["condition"](context):
                active.append(dim)
        except Exception:
            pass
    return active


def build_dimension_prompt(
    active_dims: list[dict],
    cpm_result=None,
    mc_results=None,
    phases: list[dict] = None
) -> str:
    """
    为LLM生成维度简报（结构指引，非硬编码内容）。
    LLM根据此简报 + 自身经验 + 项目数据 生成具体风险分析。
    """
    lines = []
    lines.append("# 风险分析框架\n")
    lines.append("请根据以下选中的风险维度，结合项目实际数据生成风险分析。")
    lines.append("不要写泛泛的套话——每一条都要有具体的项目背景。\n")

    # 关键数据
    lines.append("## 项目关键数据")
    lines.append(f"- CPM总工期: {cpm_result.project_duration:.0f}天" if cpm_result else "")
    if cpm_result and cpm_result.critical_ids:
        cp_names = [phases[t-1]["name"] for t in sorted(cpm_result.critical_ids) if t <= len(phases)]
        lines.append(f"- 关键路径 ({len(cp_names)}个任务): {' → '.join(cp_names[:5])}{'...' if len(cp_names) > 5 else ''}")
    if mc_results:
        q = mc_results.get("pert", {}).get("quantiles", {})
        if q:
            p50, p90 = q.get("p50",0), q.get("p90",0)
            lines.append(f"- P50={p50:.0f}天, P90={p90:.0f}天, 跨度={p90-p50:.0f}天")

    lines.append("")
    lines.append(f"## 选中维度 ({len(active_dims)}个)")
    lines.append("")
    for dim in active_dims:
        lines.append(f"### {dim.get('icon','')} {dim['name']}")
        lines.append(f"分析要点: {dim.get('guide', '')}")
        lines.append("针对此项目实际情况写1-3条具体风险，包括：")
        lines.append("- 风险描述（基于实际项目任务和数据）")
        lines.append("- 严重程度（高/中/低，结合数据判断）")
        lines.append("- 具体缓解措施（针对此项目，非通用套话）")
        lines.append("")

    lines.append("## 输出格式")
    lines.append("请输出完整的HTML片段（不含<html>/<head>/<body>标签），")
    lines.append("每条风险用卡片样式展示。\n")
    lines.append("## 要求")
    lines.append("- 不写泛泛的通用建议")
    lines.append("- 每条风险都关联到具体项目数据或任务")
    lines.append("- 如果项目数据支持量化判断，给出量化结论")

    return "\n".join(lines)


def build_minimal_fallback(active_dims: list[dict]) -> str:
    """
    极简fallback（仅当LLM未提供风险分析时使用）。
    只显示维度标题和说明，不留空，不让用户看到空白块。
    """
    lines = ['<div class="card"><h2>项目风险维度概览</h2>']
    lines.append('<p>以下风险维度根据项目特征自动匹配。详细分析由项目管理顾问生成。</p>')
    for dim in active_dims:
        lines.append(f'<div style="margin:8px 0;padding:8px;border-left:3px solid #3498db;background:#f8f9fa">')
        lines.append(f'<strong>{dim.get("icon","")} {dim["name"]}</strong>')
        lines.append(f'<p style="color:#666;font-size:0.9em;margin:4px 0 0 0">{dim.get("guide","")}</p>')
        lines.append('</div>')
    lines.append('</div>')
    return "\n".join(lines)
