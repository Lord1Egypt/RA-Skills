#!/usr/bin/env python3
"""
基于 Agent 配置和可用技能列表，生成优化建议
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

def match_agent_role(agent_config, available_skills):
    """根据 Agent 角色匹配推荐技能"""
    agent_name = agent_config.get("name", "").lower()
    agent_id = agent_config.get("id", "").lower()
    current_skills = set(agent_config.get("skills", []))
    
    # 角色关键词映射
    role_keywords = {
        "stock": ["stock", "finance", "trading", "market", "analysis"],
        "writer": ["write", "doc", "report", "content"],
        "realestate": ["realestate", "property", "house", "home"],
        "enterprise": ["enterprise", "service", "customer"],
        "investment": ["investment", "park", "business"],
        "contract": ["contract", "legal", "review"],
        "finance": ["finance", "forecast", "budget"],
        "training": ["training", "education", "course"]
    }
    
    # 识别 Agent 角色
    matched_roles = []
    for role, keywords in role_keywords.items():
        if any(kw in agent_name or kw in agent_id for kw in keywords):
            matched_roles.append(role)
    
    # 如果没有匹配，使用通用推荐
    if not matched_roles:
        matched_roles = ["general"]
    
    # 过滤可用技能
    recommendations = []
    for skill in available_skills:
        skill_name = skill["name"]
        skill_desc = skill.get("description", "").lower()
        
        # 排除已安装
        if skill_name in current_skills:
            continue
        
        # 按角色匹配
        matched = False
        for role in matched_roles:
            if role == "general":
                matched = True
                break
            if any(kw in skill_desc for kw in role_keywords.get(role, [])):
                matched = True
                break
        
        if matched:
            recommendations.append({
                "skill_name": skill_name,
                "description": skill["description"],
                "rating": skill.get("rating", 0),
                "downloads": skill.get("downloads", 0),
                "reason": f"匹配角色：{', '.join(matched_roles)}"
            })
    
    # 按评分排序
    recommendations.sort(key=lambda x: x["rating"], reverse=True)
    return recommendations[:5]  # 最多推荐 5 个

def generate_recommendations(config_path, skills_path, output_path):
    """生成优化建议"""
    # 读取配置
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 读取可用技能
    with open(skills_path, "r", encoding="utf-8") as f:
        available_skills = json.load(f)
    
    agents = config.get("agents", {}).get("list", [])
    
    results = []
    for agent in agents:
        agent_id = agent.get("id", "unknown")
        agent_name = agent.get("name", agent_id)
        
        # 生成推荐
        recommendations = match_agent_role(agent, available_skills)
        
        # 生成移除建议
        current_skills = agent.get("skills", [])
        remove_suggestions = []
        
        # 检查重复
        if len(current_skills) != len(set(current_skills)):
            remove_suggestions.append({
                "skill": "（重复技能）",
                "reason": "存在重复技能，建议去重"
            })
        
        # 检查 another_them / another-them
        if "another_them" in current_skills and "another-them" in current_skills:
            remove_suggestions.append({
                "skill": "another_them / another-them",
                "reason": "重复技能，建议只保留一个"
            })
        
        # 检查 qclaw-migration
        if "qclaw-migration" in current_skills:
            remove_suggestions.append({
                "skill": "qclaw-migration",
                "reason": "一次性工具，建议按需启用"
            })
        
        # 记录结果
        result = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "add_recommendations": recommendations,
            "remove_suggestions": remove_suggestions,
            "summary": f"建议添加 {len(recommendations)} 个技能，移除 {len(remove_suggestions)} 个"
        }
        results.append(result)
    
    # 保存结果
    report = {
        "timestamp": datetime.now().isoformat(),
        "recommendations": results
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print(f"✅ 优化建议已生成：{output_path}")
    print(f"\n📊 推荐汇总：")
    for r in results:
        print(f"   - {r['agent_name']}：{r['summary']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成优化建议")
    parser.add_argument("--config", default="~/.qclaw/openclaw.json", help="openclaw.json 路径")
    parser.add_argument("--available", default="available_skills.json", help="可用技能列表")
    parser.add_argument("--output", default="recommendations.json", help="输出路径")
    args = parser.parse_args()
    
    from datetime import datetime
    
    config_path = Path(args.config).expanduser()
    skills_path = Path(args.available).expanduser()
    output_path = Path(args.output).expanduser()
    
    generate_recommendations(config_path, skills_path, output_path)
