#!/usr/bin/env python3
"""
Phase 2.1 - 目标分解器 (Goal Decomposer)

将高层战略目标分解为可执行的战术目标和任务：

输入: {"goal": "提升XX降糖药在抖音渠道的品牌声量", "context": {...}}
输出: {
  strategic_goal: {...},
  tactical_goals: [...],
  tasks: [...],
  kpi_tree: {...},
  suggestions: [...]
}

三层分解:
  战略目标 (Strategy)  →  战术目标 (Tactic)  →  执行任务 (Task)

目标来源:
  - content_campaigns 表（当前活跃活动）
  - content_metrics 表（历史表现）
  - pharmacy_inventory + drug_products（产品上下文）
  - competitive_analysis（竞品上下文）
"""

import sys
import json
import uuid
import math
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 目标模板库
# ─────────────────────────────────────────

GOAL_TEMPLATES = {
    "brand_awareness": {
        "name": "品牌声量提升",
        "strategic_kpis": ["曝光量", "搜索指数", "话题讨论量", "粉丝增长"],
        "typical_tactics": [
            {"name": "KOL种草", "channel": "抖音/小红书", "kpis": ["互动率", "CPE"]},
            {"name": "信息流广告", "channel": "抖音/微信", "kpis": ["CPM", "曝光量"]},
            {"name": "话题营销", "channel": "微博/抖音", "kpis": ["话题阅读量", "参与人数"]},
        ],
    },
    "conversion": {
        "name": "转化提升",
        "strategic_kpis": ["转化率", "ROI", "GMV", "新患者数"],
        "typical_tactics": [
            {"name": "效果广告投放", "channel": "搜索/信息流", "kpis": ["CVR", "CPA", "ROAS"]},
            {"name": "KOL带货", "channel": "抖音/小红书", "kpis": ["GMV", "客单价"]},
            {"name": "患者教育活动", "channel": "微信/线下", "kpis": ["报名率", "到场率"]},
        ],
    },
    "doctor_outreach": {
        "name": "医生覆盖扩展",
        "strategic_kpis": ["拜访覆盖数", "KOL数量", "学术会议参与"],
        "typical_tactics": [
            {"name": "KOL合作", "channel": "线上会议", "kpis": ["合作KOL等级", "内容产出量"]},
            {"name": "学术推广", "channel": "线下拜访/会议", "kpis": ["拜访覆盖", "反馈率"]},
        ],
    },
    "compliance_audit": {
        "name": "内容合规率提升",
        "strategic_kpis": ["合规通过率", "平均审核时长", "违规率"],
        "typical_tactics": [
            {"name": "AI预审", "channel": "系统", "kpis": ["拦截率", "误报率"]},
            {"name": "人工抽检", "channel": "审核流程", "kpis": ["抽检覆盖率", "发现率"]},
        ],
    },
}


# ─────────────────────────────────────────
# 数据查询
# ─────────────────────────────────────────

def get_campaign_context(conn) -> dict:
    """从数据库获取当前活动上下文"""
    campaigns = conn.execute("""
        SELECT campaign_id, name, platform, status,
               start_date, end_date, budget
        FROM content_campaigns
        WHERE status = 'active'
        ORDER BY start_date DESC
    """).fetchall()

    campaign_list = [dict(r) for r in campaigns]

    # 获取各活动表现
    campaign_metrics = {}
    for c in campaign_list:
        cid = c["campaign_id"]
        rows = conn.execute("""
            SELECT SUM(impressions) as total_impr, SUM(clicks) as total_clicks,
                   SUM(conversions) as total_conv, AVG(ctr) as avg_ctr,
                   AVG(CAST(conversions AS FLOAT) / NULLIF(impressions, 0)) as avg_cvr, SUM(spend) as total_spend
            FROM content_metrics
            WHERE campaign_id = ?
        """, (cid,)).fetchone()
        campaign_metrics[cid] = dict(rows) if rows else {}

    return {
        "active_campaigns": campaign_list,
        "campaign_metrics": campaign_metrics,
    }


def get_product_context(conn, product_id: str = None) -> dict:
    """获取产品上下文"""
    if product_id:
        products = conn.execute("""
            SELECT * FROM drug_products WHERE product_id = ?
        """, (product_id,)).fetchall()
    else:
        products = conn.execute("SELECT * FROM drug_products LIMIT 10").fetchall()

    return [dict(r) for r in products]


def get_channel_performance(conn, channel: str = None) -> dict:
    """获取渠道表现数据（通过campaign关联platform）"""
    sql = """
        SELECT
            c.platform as channel,
            COUNT(*) as content_count,
            SUM(m.impressions) as total_impr,
            SUM(m.clicks) as total_clicks,
            SUM(m.conversions) as total_conv,
            AVG(m.ctr) as avg_ctr,
            AVG(CAST(m.conversions AS FLOAT) / NULLIF(m.impressions, 0)) as avg_cvr,
            SUM(m.spend) as total_spend
        FROM content_metrics m
        JOIN content_campaigns c ON m.campaign_id = c.campaign_id
    """
    if channel:
        sql += " WHERE c.platform = ? GROUP BY c.platform"
        rows = conn.execute(sql, (channel,)).fetchall()
    else:
        sql += " GROUP BY c.platform"
        rows = conn.execute(sql).fetchall()

    result = {}
    for r in rows:
        d = dict(r)
        spend = d.get("total_spend") or 0
        conv = d.get("total_conv") or 0
        d["roas"] = round(conv * 50 / spend, 2) if spend > 0 else 0  # 假设客单价50元
        result[d["channel"]] = d
    return result


# ─────────────────────────────────────────
# 目标分解核心算法
# ─────────────────────────────────────────

def classify_goal(goal_text: str) -> str:
    """根据目标文本分类到目标模板"""
    goal_lower = goal_text.lower()

    awareness_keywords   = ["声量", "曝光", "知名度", "品牌", "认知", "影响"]
    conversion_keywords  = ["转化", "销售", "增长", "获客", "患者", "购买", "处方"]
    doctor_keywords      = ["医生", "KOL", "学术", "推广", "拜访", "覆盖"]
    compliance_keywords  = ["合规", "审核", "违规", "安全", "审查"]

    for kw in awareness_keywords:
        if kw in goal_lower:
            return "brand_awareness"
    for kw in conversion_keywords:
        if kw in goal_lower:
            return "conversion"
    for kw in doctor_keywords:
        if kw in goal_lower:
            return "doctor_outreach"
    for kw in compliance_keywords:
        if kw in goal_lower:
            return "compliance_audit"

    return "conversion"  # default


def decompose_goal(
    goal: str,
    context: dict = None,
    product_id: str = None,
    target_period_days: int = 30,
    target_growth_pct: float = 20,
) -> dict:
    """
    目标分解主函数
    将高层目标分解为战略→战术→任务三层
    """
    conn = get_conn()
    
    try:
        # 1. 获取上下文
        campaign_ctx = get_campaign_context(conn)
        channel_perf = get_channel_performance(conn)
        product_ctx  = get_product_context(conn, product_id)

        # 2. 分类目标
        goal_type = classify_goal(goal)
        template  = GOAL_TEMPLATES.get(goal_type, GOAL_TEMPLATES["conversion"])

        # 3. 生成战略目标
        strategic = _build_strategic_goal(
            goal, goal_type, template, campaign_ctx,
            channel_perf, target_growth_pct, target_period_days, conn
        )

        # 4. 生成战术目标
        tactics = _build_tactical_goals(
            strategic, goal_type, template, campaign_ctx, channel_perf, conn
        )

        # 5. 生成执行任务
        tasks = _build_execution_tasks(
            strategic, tactics, goal_type, campaign_ctx, product_ctx, conn
        )

        # 6. KPI 树
        kpi_tree = _build_kpi_tree(strategic, tactics, tasks)

        # 7. 建议
        suggestions = _generate_suggestions(strategic, tactics, tasks, channel_perf)

        return {
            "goal_type": goal_type,
            "goal_name": template["name"],
            "strategic_goal": strategic,
            "tactical_goals": tactics,
            "tasks": tasks,
            "kpi_tree": kpi_tree,
            "context": {
                "active_campaigns": len(campaign_ctx["active_campaigns"]),
                "channels": list(channel_perf.keys()),
                "products": len(product_ctx),
            },
            "suggestions": suggestions,
        }

    finally:
        close_conn(conn)


def _build_strategic_goal(
    goal, goal_type, template, campaign_ctx, channel_perf,
    target_growth_pct, target_period_days, conn
) -> dict:
    """构建战略目标"""

    # 基于历史数据计算基准
    total_impr = sum(
        m.get("total_impr") or 0
        for m in campaign_ctx["campaign_metrics"].values()
    )
    total_conv = sum(
        m.get("total_conv") or 0
        for m in campaign_ctx["campaign_metrics"].values()
    )

    # 计算目标值
    target_impr  = int(total_impr * (1 + target_growth_pct / 100))
    target_conv  = int(total_conv * (1 + target_growth_pct / 100))

    # 基准ROI
    total_spend = sum(
        m.get("total_spend") or 1
        for m in campaign_ctx["campaign_metrics"].values()
    )
    baseline_roas = round(total_conv * 50 / total_spend, 2) if total_spend > 0 else 0

    goal_id = f"STR-{uuid.uuid4().hex[:8].upper()}"

    return {
        "goal_id": goal_id,
        "goal_text": goal,
        "goal_type": goal_type,
        "period_days": target_period_days,
        "baseline": {
            "total_impressions": total_impr,
            "total_conversions": total_conv,
            "baseline_roas": baseline_roas,
            "active_campaigns": len(campaign_ctx["active_campaigns"]),
        },
        "target": {
            "impressions": target_impr,
            "conversions": target_conv,
            "growth_pct": target_growth_pct,
            "roas_improvement": target_growth_pct * 0.5,  # 简化假设
        },
        "kpis": template["strategic_kpis"],
        "success_criteria": _build_success_criteria(
            goal_type, total_impr, total_conv, target_growth_pct
        ),
    }


def _build_success_criteria(
    goal_type: str, total_impr: int, total_conv: int, growth_pct: float
) -> list[str]:
    criteria = []
    if goal_type in ("brand_awareness", "conversion"):
        criteria.append(f"曝光量较基准提升 {growth_pct}% 以上")
        criteria.append(f"转化量较基准提升 {growth_pct}% 以上")
    if goal_type == "conversion":
        criteria.append("ROI 达到基准的 1.2 倍以上")
    if goal_type == "doctor_outreach":
        criteria.append("KOL 合作数量提升 30%")
    if goal_type == "compliance_audit":
        criteria.append("合规通过率达到 95% 以上")
    return criteria


def _build_tactical_goals(
    strategic, goal_type, template, campaign_ctx, channel_perf, conn
) -> list[dict]:
    """构建战术目标"""
    tactics = []
    template_tactics = template.get("typical_tactics", [])

    # 分配渠道
    channels = list(channel_perf.keys()) if channel_perf else ["抖音", "微信", "小红书"]

    for i, tc in enumerate(template_tactics):
        tactic_id = f"TAC-{strategic['goal_id']}-{i+1}"
        channel   = tc.get("channel", "全渠道").split("/")[0]

        # 从channel_perf获取基准
        ch_data = channel_perf.get(channel, {})
        baseline_impr = ch_data.get("total_impr") or 10000
        baseline_ctr  = ch_data.get("avg_ctr") or 0.02
        baseline_cvr  = ch_data.get("avg_cvr") or 0.01

        tactics.append({
            "tactic_id": tactic_id,
            "strategic_goal_id": strategic["goal_id"],
            "name": tc["name"],
            "channel": tc["channel"],
            "priority": "P0" if i == 0 else "P1" if i == 1 else "P2",
            "kpis": tc["kpis"],
            "baseline": {
                "impressions": baseline_impr,
                "ctr": round(baseline_ctr * 100, 2),
                "cvr": round(baseline_cvr * 100, 2),
            },
            "target": {
                "impressions": int(baseline_impr * (1 + strategic["target"]["growth_pct"] / 100)),
                "ctr": round(baseline_ctr * 100 * 1.15, 2),   # CTR 提升 15%
                "cvr": round(baseline_cvr * 100 * 1.20, 2),    # CVR 提升 20%
            },
            "weight": round(1.0 / len(template_tactics), 2),  # 平均分配权重
            "status": "planned",
        })

    return tactics


def _build_execution_tasks(
    strategic, tactics, goal_type, campaign_ctx, product_ctx, conn
) -> list[dict]:
    """构建执行任务"""
    tasks = []
    task_templates = _get_task_templates(goal_type)

    for i, task_tmpl in enumerate(task_templates):
        task_id = f"TSK-{strategic['goal_id']}-{i+1}"
        tactic_id = tactics[i % len(tactics)]["tactic_id"] if tactics else None

        tasks.append({
            "task_id": task_id,
            "tactic_id": tactic_id,
            "name": task_tmpl["name"],
            "description": task_tmpl["description"],
            "priority": task_tmpl.get("priority", "P1"),
            "estimated_hours": task_tmpl.get("hours", 4),
            "tool": task_tmpl.get("tool"),
            "owner": task_tmpl.get("owner", "AI"),
            "status": "pending",
            "success_metric": task_tmpl.get("success_metric", ""),
        })

    return tasks


def _get_task_templates(goal_type: str) -> list[dict]:
    """获取目标类型对应的任务模板"""
    templates = {
        "brand_awareness": [
            {"name": "KOL 筛选与建联", "description": "从数据库筛选 S/A 级 KOL，发送合作邀约", "priority": "P0", "hours": 6, "tool": "ask", "success_metric": "邀约回复率 > 30%"},
            {"name": "内容策略制定", "description": "制定本期内容主题、关键词、投放节奏", "priority": "P0", "hours": 4, "tool": "content", "success_metric": "策略文档完成"},
            {"name": "信息流广告创建", "description": "创建抖音/微信信息流广告组，设置预算和定向", "priority": "P1", "hours": 3, "tool": "ad_optimization", "success_metric": "CPM < ¥15"},
            {"name": "话题活动上线", "description": "策划并发布抖音话题挑战赛", "priority": "P1", "hours": 5, "tool": "content", "success_metric": "话题阅读量 > 500万"},
            {"name": "数据复盘（周）", "description": "每周汇总各渠道曝光数据，生成周报", "priority": "P2", "hours": 2, "tool": "smart_analytics", "success_metric": "周报完成"},
        ],
        "conversion": [
            {"name": "效果广告优化", "description": "调整竞价策略，优化落地页，提升 CVR", "priority": "P0", "hours": 4, "tool": "ad_optimization", "success_metric": "CVR 提升 20%"},
            {"name": "KOL 带货排期", "description": "安排 KOL 直播/短视频带货档期", "priority": "P0", "hours": 3, "tool": "ask", "success_metric": "GMV 达成率 > 100%"},
            {"name": "患者社群激活", "description": "在微信患者群推送活动，提升进店率", "priority": "P1", "hours": 3, "tool": "patient", "success_metric": "社群转化率 > 3%"},
            {"name": "活动转化追踪", "description": "配置转化追踪代码，关联 CRM 数据", "priority": "P1", "hours": 4, "tool": "attribution", "success_metric": "归因准确率 > 90%"},
            {"name": "周 ROI 复盘", "description": "分析各渠道 ROAS，提出优化建议", "priority": "P2", "hours": 2, "tool": "smart_analytics", "success_metric": "报告完成"},
        ],
        "doctor_outreach": [
            {"name": "KOL 分级盘点", "description": "更新 KOL 分级档案，识别潜力 KOL", "priority": "P0", "hours": 4, "tool": "ask", "success_metric": "分级准确率 > 90%"},
            {"name": "拜访计划制定", "description": "根据分级结果制定月度拜访计划", "priority": "P0", "hours": 3, "tool": "ask", "success_metric": "覆盖率达到 80%"},
            {"name": "学术会议筹备", "description": "组织科室会或线上学术会议", "priority": "P1", "hours": 6, "tool": "content", "success_metric": "参会医生 > 30人"},
            {"name": "KOL 合作内容审核", "description": "审核 KOL 合作内容，确保合规", "priority": "P1", "hours": 2, "tool": "compliance", "success_metric": "合规通过率 100%"},
            {"name": "月度效果评估", "description": "评估本月 KOL 合作效果，更新档案", "priority": "P2", "hours": 2, "tool": "attribution", "success_metric": "评估报告完成"},
        ],
        "compliance_audit": [
            {"name": "历史内容全量扫描", "description": "对现有内容库进行合规扫描", "priority": "P0", "hours": 8, "tool": "compliance_audit", "success_metric": "覆盖率 100%"},
            {"name": "高风险内容整改", "description": "识别并整改高风险内容（severity > 60）", "priority": "P0", "hours": 6, "tool": "compliance_audit", "success_metric": "高风险清零"},
            {"name": "合规 SOP 更新", "description": "更新内容合规审核标准操作流程", "priority": "P1", "hours": 4, "tool": "ask", "success_metric": "SOP 文档完成"},
            {"name": "审核人员培训", "description": "对运营人员进行合规审核培训", "priority": "P2", "hours": 3, "tool": "ask", "success_metric": "培训覆盖率 100%"},
        ],
    }
    return templates.get(goal_type, templates["conversion"])


def _build_kpi_tree(strategic, tactics, tasks) -> dict:
    """构建 KPI 树（战略 KPI 向下分解）"""

    def kpi_node(label, value, children=None):
        node = {"label": label, "value": value}
        if children:
            node["children"] = children
        return node

    tactic_nodes = [
        kpi_node(
            t["name"],
            {"channel": t["channel"], "target": t["target"]},
            [
                kpi_node(kpi, t["target"].get(kpi.lower().replace(" ", "_")))
                for kpi in t["kpis"]
            ]
        )
        for t in tactics
    ]

    return kpi_node(
        strategic["goal_text"],
        {"target": strategic["target"], "period": strategic["period_days"]},
        tactic_nodes
    )


def _generate_suggestions(strategic, tactics, tasks, channel_perf) -> list[str]:
    suggestions = []

    # 找出表现最好的渠道
    if channel_perf:
        best_ch = max(channel_perf.items(), key=lambda x: x[1].get("roas", 0))
        suggestions.append(f"渠道 {best_ch[0]} ROAS 最高 ({best_ch[1].get('roas', 0)})，建议增加投入")

    # 战术优先级建议
    if tactics:
        suggestions.append(f"最高优先级战术: {tactics[0]['name']}（{tactics[0]['channel']}）")

    # 任务建议
    critical_tasks = [t for t in tasks if t.get("priority") == "P0"]
    if critical_tasks:
        suggestions.append(f"P0 任务 {len(critical_tasks)} 个，建议优先完成:")
        for t in critical_tasks:
            suggestions.append(f"  - {t['name']}（预计{t['estimated_hours']}h）")

    # 风险提示
    if strategic["target"]["growth_pct"] > 30:
        suggestions.append("⚠️ 目标增长超过 30%，建议分阶段实施，避免资源挤兑")

    return suggestions


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "decompose")

    if action == "decompose":
        result = decompose_goal(
            goal=args.get("goal", "提升品牌声量和转化"),
            context=args.get("context"),
            product_id=args.get("product_id"),
            target_period_days=args.get("period_days", 30),
            target_growth_pct=args.get("growth_pct", 20),
        )
    elif action == "templates":
        result = {"goal_templates": GOAL_TEMPLATES}
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
