#!/usr/bin/env python3
"""
Daily Learning Summary - 每日学习总结汇报

集成了 InStreet、ClawHub、技能使用、错误修复的学习总结生成器
"""

import json
import os
from datetime import datetime, date
from pathlib import Path

# 自动定位 workspace 根目录（从技能目录向上查找）
def find_workspace():
    """从当前脚本位置向上查找 workspace 根目录（包含 memory/ 目录的父级）"""
    current = Path(__file__).resolve()
    # 技能目录结构: workspace/skills/daily-learning-summary/scripts/
    # workspace 是 memory/ 和 skills/ 的父目录
    for parent in [current.parents[3], current.parents[2].parent, current.parents[4]]:
        if (parent / "memory").exists():
            return parent
    # 回退到环境变量或当前工作目录
    return Path(os.getenv("OPENCLAW_WORKSPACE", os.getcwd()))

WORKSPACE = find_workspace()
MEMORY_DIR = WORKSPACE / "memory"
LEARNING_DIR = MEMORY_DIR / "learning"
HEARTBEAT_STATE = MEMORY_DIR / "heartbeat-state.json"
INSTREET_LOG = MEMORY_DIR / "instreet_activity.log"
CLAWHUB_LOG = MEMORY_DIR / "clawhub_discoveries.md"

def read_log_file(path, default=""):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return default

def read_heartbeat_state():
    try:
        with open(HEARTBEAT_STATE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def get_today_learning_summary():
    """收集今日学习数据"""
    today = date.today().isoformat()
    summary = {
        "date": today,
        "instreet": {
            "browsed_posts": 0,
            "comments": 0,
            "likes": 0,
            "learned_points": [],
            "new_follows": []
        },
        "clawhub": {
            "searched": 0,
            "discoveries": [],
            "cost": 0,
            "earned": 0,
            "pending_evals": []
        },
        "skills_usage": {},
        "lessons": [],
        "todos_today": []
    }

    # 读取 InStreet 日志
    instreet_content = read_log_file(INSTREET_LOG)
    if instreet_content:
        lines = [l for l in instreet_content.split('\n') if l.strip()]
        summary["instreet"]["browsed_posts"] = len(lines) // 3
        summary["instreet"]["comments"] = sum(1 for l in lines if "comment" in l.lower() or "评论" in l)
        summary["instreet"]["learned_points"].append("查看社区动态，了解最新Agent趋势")

    # 读取虾评发现日志
    clawhub_content = read_log_file(CLAWHUB_LOG)
    if clawhub_content:
        discoveries = []
        for line in clawhub_content.split('\n'):
            if line.strip().startswith('|') and '⭐' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    skill_name = parts[1].strip()
                    rating = parts[2].strip()
                    discoveries.append(f"{skill_name} ({rating})")
        summary["clawhub"]["discoveries"] = discoveries[:5]

    # 从心跳状态读取统计
    state = read_heartbeat_state()
    stats = state.get("stats", {})
    summary["instreet"]["comments"] = stats.get("instreet_interactions_today", summary["instreet"]["comments"])
    summary["clawhub"]["earned"] = stats.get("clawhub_虾米_earned_today", 0)

    return summary

def generate_report(summary):
    """生成Markdown格式报告"""
    lines = [
        f"## 📚 每日学习总结 - {summary['date']}\n",
        "### InStreet 学习",
        f"- 浏览帖子: {summary['instreet']['browsed_posts']} 个",
        f"- 发表评论: {summary['instreet']['comments']} 条",
        f"- 学到要点: {len(summary['instreet']['learned_points'])} 条",
    ]
    if summary["instreet"]["learned_points"]:
        lines.extend([f"  - {pt}" for pt in summary["instreet"]["learned_points"]])
    else:
        lines.append("  - 暂无记录")

    lines.extend([
        "",
        "### 虾评Skill探索",
        f"- 搜索新技能: {summary['clawhub']['searched']} 个",
        f"- 高价值发现: {len(summary['clawhub']['discoveries'])} 个",
    ])
    if summary["clawhub"]["discoveries"]:
        lines.extend([f"  - {d}" for d in summary["clawhub"]["discoveries"]])
    else:
        lines.append("  - 暂无记录")
    lines.extend([
        f"- 虾米变动: +{summary['clawhub']['earned']} (收入) / -{summary['clawhub']['cost']} (支出)",
        "",
        "### 技能效能评估",
        "- 最有效技能: 待记录",
        "- 需要优化: 待记录",
        "",
        "### 待办跟进",
        "- [ ] 评估高价值技能",
        "- [ ] 安装并测试新技能",
        "",
        "### 明日计划",
        "- [具体学习任务...]",
        ""
    ])
    return "\n".join(lines)

def main():
    summary = get_today_learning_summary()
    report = generate_report(summary)

    # 确保目录存在
    LEARNING_DIR.mkdir(parents=True, exist_ok=True)

    # 写入学习日志
    log_file = LEARNING_DIR / f"{summary['date']}.md"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 学习总结已生成: {log_file}")
    print(f"📊 统计: InStreet评论={summary['instreet']['comments']}, 虾米={summary['clawhub']['earned']}")

if __name__ == "__main__":
    main()
