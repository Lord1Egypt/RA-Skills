"""
SkillReportGenerator — 技能开发专项报告
生成技能开发、技能评分、技能进退的详细报告
"""

from datetime import datetime
from typing import Dict, List, Optional


class SkillReportGenerator:
    """技能报告生成器"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    def generate_skill_development_report(self, development_result: Dict) -> str:
        """生成技能开发专项报告"""
        created = development_result.get('created', [])
        improved = development_result.get('improved', [])
        failed = development_result.get('failed', [])
        
        lines = [
            "## 🛠️ 技能开发报告",
            "",
            f"**生成时间**: {self.timestamp}",
            "",
        ]
        
        if created:
            lines.append(f"### ✨ 新开发技能 ({len(created)}个)")
            lines.append("")
            for skill in created:
                name = skill.get('name', '')
                desc = skill.get('description', '')[:60]
                quality = skill.get('quality_score', 0)
                lines.append(f"- **{name}**")
                lines.append(f"  - 描述: {desc}")
                lines.append(f"  - 质量评分: {quality}/100")
                lines.append("")
        
        if improved:
            lines.append(f"### 🔧 改进技能 ({len(improved)}个)")
            lines.append("")
            for skill in improved:
                name = skill.get('name', '')
                changes = skill.get('changes', [])
                lines.append(f"- **{name}**: {', '.join(changes)}")
            lines.append("")
        
        if failed:
            lines.append(f"### ❌ 开发失败 ({len(failed)}个)")
            lines.append("")
            for skill in failed:
                name = skill.get('name', '')
                reason = skill.get('reason', '')
                lines.append(f"- **{name}**: {reason}")
            lines.append("")
        
        if not created and not improved and not failed:
            lines.append("_今日无技能开发活动_")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_skill_score_report(self, scores: Dict) -> str:
        """生成技能评分专项报告"""
        if not scores:
            return "## 📈 技能评分报告\n\n_暂无评分数据_\n"
        
        lines = [
            "## 📈 技能评分报告",
            "",
            f"**生成时间**: {self.timestamp}",
            "",
        ]
        
        # 统计信息
        total = len(scores)
        tiers = {"🔥": [], "📈": [], "💤": [], "🗄️": [], "⚰️": []}
        for name, data in scores.items():
            tier = data.get('tier', '⚰️')
            if tier in tiers:
                tiers[tier].append(name)
        
        lines.append("### 技能状态分布")
        lines.append("")
        tier_descs = {
            "🔥": "高度活跃",
            "📈": "正常",
            "💤": "低活跃",
            "🗄️": "休眠",
            "⚰️": "已归档",
        }
        for tier, names in tiers.items():
            if names:
                desc = tier_descs.get(tier, '')
                lines.append(f"{tier} {desc}: {len(names)}个")
                lines.append(f"  {', '.join(names[:5])}")
                if len(names) > 5:
                    lines.append(f"  ...还有{len(names)-5}个")
                lines.append("")
        
        # 排行前10
        lines.append("### 🏆 活跃度排行 (Top 10)")
        lines.append("")
        sorted_skills = sorted(
            scores.items(),
            key=lambda x: x[1].get('score', 0),
            reverse=True
        )[:10]
        
        for i, (name, data) in enumerate(sorted_skills, 1):
            tier = data.get('tier', '')
            score = data.get('score', 0)
            calls = data.get('calls', 0)
            days = data.get('days_since_last_call', 0)
            lines.append(f"{i}. {tier} **{name}** — {score}分 ({calls}次调用, {days}天前)")
        
        lines.append("")
        return "\n".join(lines)
    
    def generate_decay_report(self, decay_report: Dict) -> str:
        """生成用进废退专项报告"""
        lines = [
            "## ⚡ 用进废退报告",
            "",
            f"**生成时间**: {self.timestamp}",
            "",
        ]
        
        # 统计
        total = decay_report.get('total', 0)
        by_status = decay_report.get('by_status', {})
        
        lines.append(f"### 当前状态")
        lines.append("")
        lines.append(f"- 总技能数: {total}")
        for status, count in by_status.items():
            lines.append(f"- {status}: {count}个")
        lines.append("")
        
        # 警告
        warnings = decay_report.get('warnings', [])
        if warnings:
            lines.append(f"### ⚠️ 需关注的技能 ({len(warnings)}个)")
            lines.append("")
            for w in warnings[:5]:
                lines.append(f"- {w['skill']}: {w['days_idle']}天未用")
            lines.append("")
        
        # 建议归档
        need_archive = decay_report.get('need_archive', [])
        if need_archive:
            lines.append(f"### 🗄️ 建议归档 ({len(need_archive)}个)")
            lines.append("")
            for a in need_archive[:5]:
                lines.append(f"- {a['skill']}: {a['days_idle']}天未用")
            lines.append("")
        
        if not warnings and not need_archive:
            lines.append("_用进废退状态正常，无特殊警告_")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_combined_report(self,
                                 work_analysis: Dict,
                                 tomorrow_plan: Dict,
                                 skill_scores: Dict,
                                 skill_development: Dict,
                                 decay_report: Dict,
                                 learnings: List[str]) -> str:
        """生成完整日报"""
        
        # 工作总结
        work_section = self._generate_work_section(work_analysis)
        
        # 明日计划
        plan_section = self._generate_plan_section(tomorrow_plan)
        
        # 技能评分
        score_section = self.generate_skill_score_report(skill_scores)
        
        # 用进废退
        decay_section = self.generate_decay_report(decay_report)
        
        # 技能开发
        dev_section = self.generate_skill_development_report(skill_development)
        
        # 精进点
        learning_section = self._generate_learning_section(learnings)
        
        return "\n\n".join([
            work_section,
            plan_section,
            score_section,
            decay_section,
            dev_section,
            learning_section,
        ])
    
    def _generate_work_section(self, analysis: Dict) -> str:
        """生成工作总结"""
        total = analysis.get('total_entries', 0)
        completed = len(analysis.get('completed_tasks', []))
        incomplete = len(analysis.get('incomplete_tasks', []))
        
        lines = [
            "## 📝 今日总结",
            "",
        ]
        
        if total == 0:
            lines.append("今日无工作记录。")
        else:
            rate = completed / (completed + incomplete) * 100 if (completed + incomplete) > 0 else 0
            lines.append(f"共{total}条记录，识别任务项完成率约{rate:.0f}%。")
            
            if analysis.get('completed_tasks'):
                lines.append("")
                lines.append("### ✅ 已完成")
                for task in analysis['completed_tasks'][:5]:
                    lines.append(f"- {task.get('content', '')[:60]}")
            
            if analysis.get('incomplete_tasks'):
                lines.append("")
                lines.append("### ⏳ 未完成")
                for task in analysis['incomplete_tasks'][:5]:
                    lines.append(f"- {task.get('content', '')[:60]}")
        
        return "\n".join(lines)
    
    def _generate_plan_section(self, plan: Dict) -> str:
        """生成计划部分"""
        lines = [
            "## 📋 明日计划",
            "",
        ]
        
        continued = plan.get('continued_tasks', [])
        if continued:
            lines.append("### 继续任务")
            for t in continued[:5]:
                lines.append(f"- [ ] {t.get('task', '')[:60]}")
            lines.append("")
        
        new_tasks = plan.get('new_tasks', [])
        if new_tasks:
            lines.append("### 新增任务")
            for t in new_tasks[:5]:
                lines.append(f"- [ ] {t.get('task', '')[:60]}")
            lines.append("")
        
        skill_plan = plan.get('skill_development', [])
        if skill_plan:
            lines.append("### 技能开发")
            for s in skill_plan:
                lines.append(f"- **{s.get('type')}**: {s.get('skill', '')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_learning_section(self, learnings: List[str]) -> str:
        """生成精进点部分"""
        lines = [
            "## 🎯 精进点",
            "",
        ]
        
        if learnings:
            for l in learnings[:5]:
                lines.append(f"- {l}")
        else:
            lines.append("_暂无新的精进点_")
        
        return "\n".join(lines)
