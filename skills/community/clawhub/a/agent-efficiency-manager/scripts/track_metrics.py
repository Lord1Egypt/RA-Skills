#!/usr/bin/env python3
"""
长期跟踪 Agent 效率指标，生成趋势分析
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def load_history(history_path):
    """加载历史指标数据"""
    if not history_path.exists():
        return []
    
    with open(history_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_trends(history):
    """计算趋势指标"""
    if len(history) < 2:
        return {
            "token_trend": "stable",
            "efficiency_trend": "stable",
            "skill_count_trend": "stable"
        }
    
    # 取最近 2 次数据
    latest = history[-1]
    previous = history[-2]
    
    # Token 消耗趋势
    latest_tokens = latest["summary"]["total_skills_referenced"]
    previous_tokens = previous["summary"]["total_skills_referenced"]
    token_change = (latest_tokens - previous_tokens) / previous_tokens * 100
    
    # 效率评分趋势
    latest_score = latest["summary"]["average_efficiency_score"]
    previous_score = previous["summary"]["average_efficiency_score"]
    score_change = latest_score - previous_score
    
    # 技能数量趋势
    latest_count = sum(len(a["skills"]) for a in latest["agents"])
    previous_count = sum(len(a["skills"]) for a in previous["agents"])
    count_change = (latest_count - previous_count) / previous_count * 100
    
    return {
        "token_trend": "increasing" if token_change > 5 else "decreasing" if token_change < -5 else "stable",
        "efficiency_trend": "improving" if score_change > 5 else "declining" if score_change < -5 else "stable",
        "skill_count_trend": "increasing" if count_change > 5 else "decreasing" if count_change < -5 else "stable",
        "token_change_percent": round(token_change, 2),
        "score_change": round(score_change, 2),
        "count_change_percent": round(count_change, 2)
    }

def generate_trend_report(history, trends):
    """生成趋势报告（Markdown 格式）"""
    if not history:
        return "# Agent 效率趋势报告\n\n暂无历史数据。\n"
    
    latest = history[-1]
    
    report = f"""# Agent 效率趋势报告

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 总体趋势

| 指标 | 当前值 | 趋势 |
|------|--------|------|
| 平均效率评分 | {latest['summary']['average_efficiency_score']:.1f}/100 | {trends['efficiency_trend']} ({trends.get('score_change', 0):+.1f}) |
| 总技能引用数 | {latest['summary']['total_skills_referenced']} | {trends['token_trend']} ({trends.get('token_change_percent', 0):+.1f}%) |
| Agent 数量 | {latest['summary']['total_agents']} | - |

## 改进建议

"""
    
    # 基于趋势给出建议
    if trends['efficiency_trend'] == "declining":
        report += "- ⚠️ 效率评分下降，建议重新评估技能配置\n"
    
    if trends['token_trend'] == "increasing":
        report += "- ⚠️ Token 消耗增加，建议精简技能列表\n"
    
    if trends['skill_count_trend'] == "increasing":
        report += "- ⚠️ 技能数量增加，检查是否有冗余配置\n"
    
    if trends['efficiency_trend'] == "improving":
        report += "- ✅ 效率持续提升，保持当前优化策略\n"
    
    # 低效 Agent 列表
    low_score_agents = [a for a in latest["agents"] if a["efficiency_score"] < 50]
    if low_score_agents:
        report += f"\n## 低效 Agent（评分 < 50）\n\n"
        for agent in low_score_agents:
            report += f"- **{agent['agent_name']}**（{agent['agent_id']}）：评分 {agent['efficiency_score']}/100\n"
    
    return report

def track_metrics(config_path, history_path, output_path):
    """跟踪指标并生成报告"""
    # 读取当前配置
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 加载历史
    history = load_history(history_path)
    
    # 分析当前效率（复用 analyze_agent_efficiency.py 的逻辑）
    agents = config.get("agents", {}).get("list", [])
    current_metrics = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_agents": len(agents),
            "total_skills_referenced": sum(len(a.get("skills", [])) for a in agents),
            "average_efficiency_score": 0  # TODO：需要计算
        },
        "agents": []
    }
    
    # TODO：完整实现需要从 analyze_agent_efficiency.py 导入逻辑
    # 这里简化为记录基本信息
    
    # 添加到历史
    history.append(current_metrics)
    
    # 只保留最近 90 天
    cutoff = datetime.now() - timedelta(days=90)
    history = [h for h in history if datetime.fromisoformat(h["timestamp"]) > cutoff]
    
    # 保存历史
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    # 计算趋势
    trends = calculate_trends(history)
    
    # 生成报告
    report = generate_trend_report(history, trends)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ 指标跟踪完成！")
    print(f"   - 历史记录已保存到：{history_path}")
    print(f"   - 趋势报告已生成：{output_path}")
    print(f"\n📊 趋势摘要：")
    print(f"   - 效率趋势：{trends['efficiency_trend']}")
    print(f"   - Token 趋势：{trends['token_trend']}")
    print(f"   - 技能数量趋势：{trends['skill_count_trend']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="跟踪 Agent 效率指标")
    parser.add_argument("--config", default="~/.qclaw/openclaw.json", help="openclaw.json 路径")
    parser.add_argument("--history", default="metrics_history.json", help="历史数据文件路径")
    parser.add_argument("--output", default="trend_report.md", help="输出报告路径")
    args = parser.parse_args()
    
    config_path = Path(args.config).expanduser()
    history_path = Path(args.history).expanduser()
    output_path = Path(args.output).expanduser()
    
    track_metrics(config_path, history_path, output_path)
