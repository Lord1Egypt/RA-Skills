"""
TomorrowPlanner — 明日计划生成器
基于今日复盘和技能状态，生成明日工作计划
"""

import random
from typing import Dict, List


class TomorrowPlanner:
    """明日计划生成器"""
    
    def __init__(self, work_analysis: Dict, skill_scores: Dict):
        """
        初始化计划器
        work_analysis: WorkAnalyzer.analyze() 的结果
        skill_scores: SkillScorer.score_all_skills() 的结果
        """
        self.work_analysis = work_analysis
        self.skill_scores = skill_scores
    
    def generate_plan(self) -> Dict:
        """生成完整明日计划"""
        plan = {
            'date': '',  # 将在生成时填充
            'continued_tasks': [],    # 继续完成的任务
            'new_tasks': [],          # 新任务
            'skill_development': [],  # 技能开发计划
            'priority_order': [],      # 优先级顺序
            'reasoning': '',          # 计划逻辑说明
        }
        
        # 1. 处理未完成任务
        for task in self.work_analysis.get('incomplete_tasks', [])[:3]:
            plan['continued_tasks'].append({
                'task': task['content'],
                'reason': f"承接昨日：{task.get('possible_reason', '未完成')}",
                'priority': 'high'
            })
        
        # 2. 分析技能状态，决定是否需要技能开发
        skill_plan = self._analyze_skill_needs()
        plan['skill_development'] = skill_plan
        
        # 3. 生成新任务建议
        plan['new_tasks'] = self._generate_new_tasks()
        
        # 4. 确定优先级顺序
        plan['priority_order'] = self._determine_priority(plan)
        
        # 5. 生成计划说明
        plan['reasoning'] = self._generate_reasoning(plan)
        
        return plan
    
    def _analyze_skill_needs(self) -> List[Dict]:
        """分析技能需求，决定是否需要开发/学习新技能"""
        skill_plan = []
        
        # 找出低活跃或休眠的技能
        low_skills = [
            (name, data) for name, data in self.skill_scores.items()
            if data.get('tier') in ['💤', '🗄️', '⚰️']
        ]
        
        # 找出高度活跃的技能
        high_skills = [
            (name, data) for name, data in self.skill_scores.items()
            if data.get('tier') == '🔥'
        ]
        
        # 如果有低活跃技能，建议复习
        if low_skills:
            for skill_name, data in low_skills[:2]:
                skill_plan.append({
                    'type': 'review',
                    'skill': skill_name,
                    'reason': f"该技能已{data.get('days_since_last_call', 0)}天未用，需要复习巩固",
                    'priority': 'medium'
                })
        
        # 如果高度活跃技能太少，考虑新技能开发
        if len(high_skills) < 3 and self.work_analysis.get('incomplete_tasks'):
            skill_plan.append({
                'type': 'explore',
                'skill': '相关领域探索',
                'reason': "当前技能活跃度偏低，建议探索新领域",
                'priority': 'low'
            })
        
        return skill_plan
    
    def _generate_new_tasks(self) -> List[Dict]:
        """生成新任务建议"""
        new_tasks = []
        
        # 基于今日洞察生成新任务
        for insight in self.work_analysis.get('insights', [])[:2]:
            new_tasks.append({
                'task': f"实践洞察：{insight['content'][:50]}",
                'source': 'insight',
                'priority': 'medium'
            })
        
        # 如果有新决策，添加执行任务
        for decision in self.work_analysis.get('decisions', [])[:1]:
            new_tasks.append({
                'task': f"执行决策：{decision['content'][:50]}",
                'source': 'decision',
                'priority': 'high'
            })
        
        return new_tasks
    
    def _determine_priority(self, plan: Dict) -> List[str]:
        """确定任务优先级顺序"""
        priority_order = []
        
        # 高优先级：继续完成的任务
        for task in plan['continued_tasks']:
            if task['priority'] == 'high':
                priority_order.append(f"[高] {task['task'][:40]}")
        
        # 高优先级：新任务中的决策执行
        for task in plan['new_tasks']:
            if task.get('priority') == 'high':
                priority_order.append(f"[高] {task['task'][:40]}")
        
        # 中优先级：其他继续任务
        for task in plan['continued_tasks']:
            if task['priority'] != 'high':
                priority_order.append(f"[中] {task['task'][:40]}")
        
        # 中优先级：洞察实践
        for task in plan['new_tasks']:
            if task.get('priority') == 'medium':
                priority_order.append(f"[中] {task['task'][:40]}")
        
        # 技能开发
        for skill_item in plan['skill_development']:
            priority_order.append(f"[技能] {skill_item['type']}: {skill_item['skill']}")
        
        return priority_order
    
    def _generate_reasoning(self, plan: Dict) -> str:
        """生成计划逻辑说明"""
        parts = []
        
        incomplete = len(plan['continued_tasks'])
        if incomplete > 0:
            parts.append(f"今日有{incomplete}项未完成任务，需要延续执行。")
        
        new_count = len(plan['new_tasks'])
        if new_count > 0:
            parts.append(f"基于今日工作，新增{new_count}项任务。")
        
        skill_count = len(plan['skill_development'])
        if skill_count > 0:
            parts.append(f"根据技能用进废退分析，建议{skill_count}项技能相关活动。")
        
        if not parts:
            parts.append("今日工作正常完成，明日维持常规节奏。")
        
        return ' '.join(parts)
    
    def format_as_markdown(self, plan: Dict) -> str:
        """格式化为 Markdown 格式的计划"""
        from datetime import datetime, timedelta
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        lines = [
            f"# 📋 明日计划 — {tomorrow}",
            "",
            f"**计划逻辑：** {plan['reasoning']}",
            "",
        ]
        
        # 未完成任务
        if plan['continued_tasks']:
            lines.append("## 🔄 继续任务（承接今日）")
            for task in plan['continued_tasks']:
                lines.append(f"- [ ] {task['task']}")
                lines.append(f"  - 原因：{task['reason']}")
            lines.append("")
        
        # 新任务
        if plan['new_tasks']:
            lines.append("## ✨ 新增任务")
            for task in plan['new_tasks']:
                lines.append(f"- [ ] {task['task']}")
                lines.append(f"  - 来源：{task.get('source', '计划')}")
            lines.append("")
        
        # 技能开发
        if plan['skill_development']:
            lines.append("## 🛠️ 技能开发")
            for item in plan['skill_development']:
                lines.append(f"- **{item['type']}**: {item['skill']}")
                lines.append(f"  - {item['reason']}")
            lines.append("")
        
        # 优先级顺序
        if plan['priority_order']:
            lines.append("## 📊 执行顺序")
            for i, item in enumerate(plan['priority_order'][:8], 1):
                lines.append(f"{i}. {item}")
            lines.append("")
        
        return '\n'.join(lines)
