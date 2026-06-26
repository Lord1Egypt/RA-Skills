#!/usr/bin/env python3
"""
Clawpilot Handler - Skill 安装顾问
分析用户任务意图，推荐合适的 skill，比较差异，解释风险，给出安装建议。
第一版：规则引擎 + 静态数据库，不做自动安装。
"""

import json
import os
import re
import sys
from typing import Any, Optional

# ==================== 数据加载 ====================

def get_skill_dir() -> str:
    """获取 skill 目录路径"""
    return os.path.dirname(os.path.abspath(__file__))

def load_skill_db() -> dict:
    """加载 skill 元数据库"""
    path = os.path.join(get_skill_dir(), "data", "skill-db.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_intent_map() -> dict:
    """加载意图-技能映射表"""
    path = os.path.join(get_skill_dir(), "data", "intent-map.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==================== 意图识别 ====================

def parse_intent(user_query: str, intent_map: dict) -> Optional[dict]:
    """
    从用户输入中识别任务意图。
    使用关键词匹配：命中关键词最多的意图胜出。
    """
    query = user_query.lower().strip()
    best_match: Optional[dict] = None
    best_score = 0

    for intent_entry in intent_map.get("intents", []):
        score = 0
        for kw in intent_entry.get("keywords", []):
            if kw.lower() in query:
                score += 1
        if score > best_score:
            best_score = score
            best_match = intent_entry

    # 至少命中 1 个关键词才认定匹配
    if best_score >= 1:
        return best_match
    return None

# ==================== Skill 查找与推荐 ====================

def build_skill_index(skill_db: dict) -> dict:
    """构建 skill name -> info 的索引"""
    return {s["name"]: s for s in skill_db.get("skills", [])}

def recommend_skills(
    intent_entry: dict,
    skill_db: dict,
    installed_skills: list[str],
) -> list[dict]:
    """
    根据意图返回推荐列表，过滤已安装 skill，
    最多返回 3 个，按 installOrder 排序。
    """
    skill_index = build_skill_index(skill_db)
    ordered = intent_entry.get("installOrder", [])
    skill_names = intent_entry.get("skills", [])

    def sort_key(name: str) -> int:
        if name in ordered:
            return ordered.index(name)
        return len(ordered) + skill_names.index(name)

    results = []
    for name in sorted(skill_names, key=sort_key):
        if name in installed_skills:
            continue
        info = skill_index.get(name)
        if not info:
            continue
        results.append({
            "skillName": name,
            "skillDisplayName": info.get("displayName", name),
            "description": info.get("description", ""),
            "riskLevel": info.get("riskLevel", "pending"),
            "riskReason": info.get("riskReason"),
            "category": info.get("category", ""),
            "installOrder": sort_key(name) + 1,
        })
        if len(results) >= 3:
            break

    return results

# ==================== 风险与免责声明 ====================

RISK_EMOJI = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🔴",
    "pending": "⚪",
}

RISK_LABEL = {
    "low": "低风险",
    "medium": "中风险",
    "high": "高风险",
    "pending": "待确认",
}

DISCLAIMER_TEMPLATE = """⚠️ **使用提醒**

以下 skill 涉及 **{risk_category}** 领域，提供的仅供参考，**不构成专业意见**：
{skill_list}

重要决策请咨询 {professionals}，使用前请自行了解相关风险。"""

BOUNDARIES = [
    "第一版只提供安装建议，不做自动安装。",
    "推荐基于当前 skill 库，可能不涵盖所有场景。",
    "风险分级由人工维护，仅供参考，实际使用请自行判断。",
]

def build_disclaimer(recommendations: list[dict]) -> Optional[str]:
    """如果存在中高风险 skill，返回免责声明"""
    high_or_medium = [r for r in recommendations if r["riskLevel"] in ("high", "medium")]
    if not high_or_medium:
        return None

    by_category: dict[str, list[str]] = {}
    for r in high_or_medium:
        cat = r.get("category", "其他")
        by_category.setdefault(cat, []).append(r["skillDisplayName"])

    professional_map = {
        "法律": "持证律师",
        "医疗": "专业医生",
        "心理健康": "心理咨询师",
        "电商": "消费维权顾问",
        "出行": "旅行顾问",
        "社交": "情感顾问",
        "其他": "专业人士",
    }

    parts = []
    for cat, names in by_category.items():
        skill_list = "、".join(names)
        professional = professional_map.get(cat, "专业人士")
        parts.append(f"- {skill_list}（{cat}）→ 请咨询 {professional}")

    return DISCLAIMER_TEMPLATE.format(
        risk_category="/".join(by_category.keys()),
        skill_list="\n".join(parts),
        professionals="、".join(set(professional_map.get(c, "专业人士") for c in by_category)),
    )

# ==================== 输出格式化 ====================

def generate_report(
    intent_entry: dict,
    recommendations: list[dict],
    user_query: str,
    skill_db: dict,
) -> str:
    """生成结构化 Markdown 推荐报告"""

    intent_name = intent_entry["intent"]

    lines = []
    lines.append(f"## 🎯 识别意图：{intent_name}")
    lines.append("")

    if not recommendations:
        lines.append("> 你已安装了所有相关 skill，无需额外推荐 🎉")
        return "\n".join(lines)

    # 推荐列表
    lines.append("### 📦 推荐安装")
    lines.append("")
    lines.append("| # | Skill | 风险 | 安装顺序 | 说明 |")
    lines.append("|---|-------|------|---------|------|")
    for rec in recommendations:
        emoji = RISK_EMOJI.get(rec["riskLevel"], "⚪")
        risk_label = RISK_LABEL.get(rec["riskLevel"], "待确认")
        order = rec["installOrder"]
        name = rec["skillDisplayName"]
        desc = rec["description"]

        if order == 1:
            reason = f"首选推荐：{desc}"
        elif rec["riskLevel"] == "high":
            reason = f"{desc}（高风险，使用需谨慎）"
        elif rec["riskLevel"] == "medium":
            reason = f"{desc}（中风险，注意使用边界）"
        else:
            reason = desc

        lines.append(
            f"| {order} | **{name}** (`{rec['skillName']}`) "
            f"| {emoji} {risk_label} | #{order} | {reason} |"
        )
    lines.append("")

    # 安装建议
    primary = next((r for r in recommendations if r["installOrder"] == 1), None)
    if primary:
        lines.append("### ✅ 安装建议")
        lines.append("")
        lines.append(
            f"**推荐先装 [{primary['skillDisplayName']}]({primary['skillName']})**："
            f"{primary['description']}"
        )
        if len(recommendations) > 1:
            others = [r["skillDisplayName"] for r in recommendations if r["installOrder"] > 1]
            lines.append(f"体验后再按需安装：{', '.join(others)}。")
        lines.append("")

    # 免责声明
    disclaimer = build_disclaimer(recommendations)
    if disclaimer:
        lines.append(disclaimer)
        lines.append("")

    # 边界说明
    lines.append("### 📌 边界说明")
    for b in BOUNDARIES:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("*以上建议仅供参考，安装决策权在你。*")

    return "\n".join(lines)

def generate_no_match_report(intent_map: dict, user_query: str, skill_db: dict) -> str:
    """无法识别意图时的友好拒绝"""
    default = intent_map.get("defaultResponse", {})
    total = len(skill_db.get("skills", []))

    lines = []
    lines.append("## 🔍 抱歉，暂无法识别你的需求")
    lines.append("")
    lines.append(default.get("noMatch", "抱歉，我无法识别你的需求。"))
    lines.append("")
    lines.append("### 💡 你可以这样问我：")
    for example in [
        "我想查快递到哪里了",
        "我最近工作压力好大",
        "有什么法律类的 skill 吗？",
        "我想点外卖",
        "帮我推荐一个学习成长的工具",
    ]:
        lines.append(f"- \"{example}\"")
    lines.append("")
    lines.append(f"*目前我可推荐的 skill 共 {total} 个，覆盖物流、心理、法律、购物、出行等场景。*")
    lines.append("")
    lines.append("### 🚫 明确无法帮助的场景")
    lines.append("- 医疗诊断（请咨询医生）")
    lines.append("- 投资理财推荐（请咨询持牌顾问）")
    lines.append("- 自动安装 skill（第一版只提供建议）")
    lines.append("- 境外快递/国际服务（知识库暂不支持）")
    return "\n".join(lines)

# ==================== 入口函数 ====================

def handle(
    user_query: str,
    installed_skills: Optional[list[str]] = None,
    risk_preference: Optional[str] = None,
) -> str:
    """
    主入口函数，供 OpenClaw 调用。

    Args:
        user_query: 用户任务描述（必填）
        installed_skills: 用户已安装的 skill 列表（可选）
        risk_preference: 保守/激进偏好（可选）

    Returns:
        Markdown 格式的推荐报告
    """
    installed_skills = installed_skills or []
    skill_db = load_skill_db()
    intent_map = load_intent_map()

    intent_entry = parse_intent(user_query, intent_map)

    if intent_entry is None:
        return generate_no_match_report(intent_map, user_query, skill_db)

    recommendations = recommend_skills(intent_entry, skill_db, installed_skills)

    return generate_report(intent_entry, recommendations, user_query, skill_db)

# ==================== CLI 自测入口 ====================

def main():
    """
    CLI 自测入口：
      python handler.py <用户问题>
      python handler.py <用户问题> --installed skill1,skill2
    """
    args = sys.argv[1:]
    if not args:
        print("用法: python handler.py <用户问题> [--installed skill1,skill2]")
        print("示例: python handler.py 我想查快递到哪里了")
        print("      python handler.py 我想查快递 --installed logistics")
        sys.exit(1)

    user_query = args[0]
    installed = []

    if "--installed" in args:
        idx = args.index("--installed")
        if idx + 1 < len(args):
            installed = [s.strip() for s in args[idx + 1].split(",") if s.strip()]

    result = handle(user_query, installed_skills=installed)
    print(result)

if __name__ == "__main__":
    main()
