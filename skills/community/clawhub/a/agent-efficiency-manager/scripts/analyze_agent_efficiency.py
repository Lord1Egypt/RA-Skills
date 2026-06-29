#!/usr/bin/env python3
"""
Agent 效率分析脚本
扫描 openclaw.json 中所有 Agent 配置，计算效率指标
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

def estimate_skill_tokens(skill_name):
    """预估单个 skill 的 token 消耗（基于 SKILL.md 长度）"""
    # 基础预估：每个 skill 的 SKILL.md 约 500-1000 tokens
    base_tokens = 500
    
    # 特殊 skill 调整
    high_token_skills = ["qclaw-skill-creator", "online-search", "tencent-docs", "xbrowser"]
    if skill_name in high_token_skills:
        base_tokens = 1000
    
    return base_tokens

def calculate_efficiency_score(agent_config):
    """计算 Agent 效率评分（0-100）"""
    skills = agent_config.get("skills", [])
    skill_count = len(skills)
    
    # 基础分：技能数量越少越好（满分 50）
    if skill_count <= 10:
        base_score = 50
    elif skill_count <= 20:
        base_score = 30
    else:
        base_score = 10
    
    # 冗余扣分：检测重复/无关技能
    redundancy_penalty = 0
    
    # 检查重复
    if len(skills) != len(set(skills)):
        redundancy_penalty += 20
    
    # 检查 another_them / another-them 重复
    if "another_them" in skills and "another-them" in skills:
        redundancy_penalty += 15
    
    # 检查 qclaw-migration（一次性工具）
    if "qclaw-migration" in skills:
        redundancy_penalty += 10
    
    # 最终评分
    score = max(0, base_score - redundancy_penalty)
    return score

def analyze_agent_efficiency(config_path, output_path):
    """分析所有 Agent 的效率"""
    # 读取配置
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    agents = config.get("agents", {}).get("list", [])
    
    results = []
    for agent in agents:
        agent_id = agent.get("id", "unknown")
        agent_name = agent.get("name", agent_id)
        skills = agent.get("skills", [])
        
        # 计算指标
        skill_count = len(skills)
        estimated_tokens = sum(estimate_skill_tokens(s) for s in skills)
        efficiency_score = calculate_efficiency_score(agent)
        
        # 识别冗余
        redundancies = []
        if len(skills) != len(set(skills)):
            redundancies.append("存在重复技能")
        if "another_them" in skills and "another-them" in skills:
            redundancies.append("another_them / another-them 重复")
        if "qclaw-migration" in skills:
            redundancies.append("qclaw-migration 应按需启用")
        
        # 生成优化建议
        recommendations = []
        if skill_count > 20:
            recommendations.append(f"技能数量过多（{skill_count}个），建议精简到 15 个以内")
        if "another_them" in skills and "another-them" in skills:
            recommendations.append("移除重复的 another_them / another-them")
        if "qclaw-migration" in skills:
            recommendations.append("qclaw-migration 改为按需启用")
        
        # 记录结果
        result = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "skill_count": skill_count,
            "estimated_tokens": estimated_tokens,
            "efficiency_score": efficiency_score,
            "redundancies": redundancies,
            "recommendations": recommendations,
            "skills": skills
        }
        results.append(result)
    
    # 按效率评分排序
    results.sort(key=lambda x: x["efficiency_score"])
    
    # 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_agents": len(results),
            "total_skills_referenced": sum(r["skill_count"] for r in results),
            "average_efficiency_score": sum(r["efficiency_score"] for r in results) / len(results) if results else 0
        },
        "agents": results
    }
    
    # 输出
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print(f"✅ 效率分析完成！")
    print(f"   - Agent 总数：{report['summary']['total_agents']}")
    print(f"   - 技能引用总数：{report['summary']['total_skills_referenced']}")
    print(f"   - 平均效率评分：{report['summary']['average_efficiency_score']:.1f}/100")
    print(f"\n📊 报告已保存到：{output_path}")
    
    # 打印低分 Agent
    low_score_agents = [r for r in results if r["efficiency_score"] < 50]
    if low_score_agents:
        print(f"\n⚠️  低效 Agent（评分 < 50）：")
        for agent in low_score_agents:
            print(f"   - {agent['agent_name']}（{agent['agent_id']}）：评分 {agent['efficiency_score']}/100")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent 效率分析")
    parser.add_argument("--config", default="~/.qclaw/openclaw.json", help="openclaw.json 路径")
    parser.add_argument("--output", default="efficiency_report.json", help="输出报告路径")
    args = parser.parse_args()
    
    config_path = Path(args.config).expanduser()
    output_path = Path(args.output).expanduser()
    
    analyze_agent_efficiency(config_path, output_path)
