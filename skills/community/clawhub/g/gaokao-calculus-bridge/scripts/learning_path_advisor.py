#!/usr/bin/env python3
"""
自适应学习路径推荐器
基于诊断评估生成个性化学习方案
"""

import argparse
import json
import re
from datetime import datetime
from typing import Dict, List

class LearningPathAdvisor:
    """学习路径顾问"""

    # 能力维度定义
    ABILITY_DIMENSIONS = {
        "情境理解": {
            "description": "从长文本中提取数学信息的能力",
            "test_items": ["长题干解析", "图表理解", "跨学科术语"],
            "resources": ["《科学美国人》中文", "果壳网", "学术论文摘要"]
        },
        "数学建模": {
            "description": "将现实问题转化为数学模型的能力",
            "test_items": ["开放问题建模", "假设简化", "模型验证"],
            "resources": ["数学建模竞赛题", "真实数据集", "案例研究"]
        },
        "计算求解": {
            "description": "数学运算与算法实现能力",
            "test_items": ["符号计算", "数值方法", "编程实现"],
            "resources": ["Python/Matlab教程", "Wolfram Alpha", "数值分析教材"]
        },
        "跨学科应用": {
            "description": "将数学工具应用于其他领域的能力",
            "test_items": ["物理建模", "经济分析", "生物统计"],
            "resources": ["跨学科教材", "领域综述论文", "MOOC课程"]
        }
    }

    def __init__(self, assessment: Dict = None, goal: str = "bridge", duration: str = "12周"):
        self.assessment = assessment or {}
        self.goal = goal
        self.duration = self._parse_duration(duration)

    def _parse_duration(self, duration_str: str) -> int:
        """解析时长字符串"""
        match = re.search(r'(\d+)', duration_str)
        return int(match.group(1)) if match else 12

    def generate_path(self) -> Dict:
        """生成学习路径"""
        diagnosis = self._diagnose()
        milestones = self._define_milestones()
        weekly_plan = self._generate_weekly_plan(diagnosis, milestones)

        return {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "target_duration": f"{self.duration}周",
                "learning_goal": self.goal,
                "difficulty_level": diagnosis.get("overall_level", "中等")
            },
            "diagnosis": diagnosis,
            "milestones": milestones,
            "weekly_plan": weekly_plan[:4],  # 只显示前4周
            "full_plan_weeks": self.duration
        }

    def _diagnose(self) -> Dict:
        """诊断当前水平"""
        if not self.assessment:
            return {
                "overall_level": "中等",
                "dimensions": {
                    dim: {"score": 60, "gap": "需系统提升"} 
                    for dim in self.ABILITY_DIMENSIONS.keys()
                }
            }

        dimensions = {}
        for dim, score in self.assessment.items():
            if dim in self.ABILITY_DIMENSIONS:
                level = "优秀" if score >= 85 else "良好" if score >= 70 else "中等"
                dimensions[dim] = {"score": score, "level": level}

        avg_score = sum(d["score"] for d in dimensions.values()) / len(dimensions)
        return {
            "overall_level": "优秀" if avg_score >= 85 else "良好" if avg_score >= 70 else "中等",
            "dimensions": dimensions
        }

    def _define_milestones(self) -> List[Dict]:
        """定义里程碑"""
        if self.goal == "bridge":
            return [
                {"week": 3, "name": "高中知识巩固", "deliverable": "高考真题90+分"},
                {"week": 6, "name": "大学基础建立", "deliverable": "核心定理证明"},
                {"week": 9, "name": "应用能力提升", "deliverable": "建模项目1个"},
                {"week": 12, "name": "综合素养形成", "deliverable": "跨学科研究报告"}
            ]
        return []

    def _generate_weekly_plan(self, diagnosis: Dict, milestones: List[Dict]) -> List[Dict]:
        """生成周计划"""
        weekly_plan = []
        phase_duration = self.duration // 3

        for week in range(1, self.duration + 1):
            if week <= phase_duration:
                phase, focus = "基础阶段", "概念理解与基本计算"
            elif week <= 2 * phase_duration:
                phase, focus = "提升阶段", "综合应用与建模训练"
            else:
                phase, focus = "冲刺阶段", "真题实战与查漏补缺"

            milestone = next((m for m in milestones if m["week"] == week), None)

            weekly_plan.append({
                "week": week,
                "phase": phase,
                "focus": focus,
                "milestone": milestone,
                "estimated_hours": 15 if week <= 4 else 20
            })

        return weekly_plan

def format_plan(plan: Dict) -> str:
    """格式化为可读文本"""
    md = f"""# 个性化学习路径方案

## 基本信息
- **目标**：{plan['meta']['learning_goal']}
- **时长**：{plan['meta']['target_duration']}
- **难度**：{plan['meta']['difficulty_level']}

## 诊断分析
**整体水平**：{plan['diagnosis']['overall_level']}

"""
    for dim, info in plan['diagnosis'].get('dimensions', {}).items():
        md += f"- **{dim}**：{info['score']}分（{info['level']}）\n"

    md += "\n## 里程碑规划\n"
    for ms in plan['milestones']:
        md += f"- **第{ms['week']}周**：{ms['name']} → {ms['deliverable']}\n"

    md += "\n## 周计划详情\n"
    for week in plan['weekly_plan']:
        md += f"**第{week['week']}周** [{week['phase']}] - {week['focus']} ({week['estimated_hours']}h)\n"
        if week['milestone']:
            md += f"  🎯 里程碑：{week['milestone']['name']}\n"

    return md

def main():
    parser = argparse.ArgumentParser(description='自适应学习路径推荐')
    parser.add_argument('--assessment', type=str, default='{}')
    parser.add_argument('--goal', default='bridge')
    parser.add_argument('--duration', default='12周')
    parser.add_argument('--output-format', choices=['markdown', 'json'], default='markdown')

    args = parser.parse_args()

    assessment = json.loads(args.assessment) if args.assessment else None
    advisor = LearningPathAdvisor(assessment, args.goal, args.duration)
    plan = advisor.generate_path()

    if args.output_format == 'json':
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(format_plan(plan))

if __name__ == "__main__":
    main()
