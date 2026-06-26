"""
DailyReporter — 每日汇报生成器
生成完整的每日工作汇报，包含六大模块
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class DailyReporter:
    """每日汇报生成器"""
    
    REPORT_TEMPLATE = """# 📊 每日汇报 — {date}

> 生成时间: {timestamp}
> 汇报类型: {report_type}

---

## 📝 今日总结

### 工作完成情况
{work_summary}

### 完成的任务 ({completed_count}项)
{completed_tasks}

### 未完成的任务 ({incomplete_count}项)
{incomplete_tasks}

### 阻碍因素
{blockers}

---

## 📋 明日计划

### 继续任务
{continued_tasks}

### 新增任务
{new_tasks}

### 技能开发计划
{skill_plan}

### 执行优先级
{priority_order}

---

## 🛠️ 技能开发

### 新开发的技能
{new_skills}

### 技能改进
{skill_improvements}

### 开发理由
{development_reasoning}

---

## 📈 技能评分（用进废退）

### 技能活跃度排行
{skill_ranking}

### 技能状态分布
{skill_distribution}

### 需关注的技能
{skills_to_watch}

### 用进废退记录
{decay_records}

---

## 🎯 精进点

### 今日学到的新东西
{learnings}

### 需要改进的地方
{improvements}

### 明日行动项
{tomorrow_actions}

---

## 💭 个人感想

{personal_thoughts}

---

*本汇报由梦境技能自动生成*
"""


    def __init__(self, date_str: Optional[str] = None):
        self.date_str = date_str or datetime.now().strftime('%Y-%m-%d')
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.report_type = "晚间汇报"  # 早晚汇报用同一个类
    
    def generate(self,
                 work_analysis: Dict,
                 tomorrow_plan: Dict,
                 skill_scores: Dict,
                 skill_development: Dict,
                 decay_report: Dict,
                 learnings: List[str],
                 personal_thoughts: str = "") -> str:
        """
        生成完整汇报
        """
        # 格式化各部分内容
        work_summary = self._format_work_summary(work_analysis)
        completed_tasks = self._format_task_list(work_analysis.get('completed_tasks', []))
        incomplete_tasks = self._format_task_list(work_analysis.get('incomplete_tasks', []))
        blockers = self._format_blockers(work_analysis.get('blockers', []))
        
        continued_tasks = self._format_continued(tomorrow_plan.get('continued_tasks', []))
        new_tasks = self._format_new_tasks(tomorrow_plan.get('new_tasks', []))
        skill_plan = self._format_skill_plan(tomorrow_plan.get('skill_development', []))
        priority_order = self._format_priority(tomorrow_plan.get('priority_order', []))
        
        new_skills = self._format_new_skills(skill_development.get('created', []))
        skill_improvements = self._format_improvements(skill_development.get('improved', []))
        development_reasoning = skill_development.get('reasoning', '根据工作需求自动判断')
        
        skill_ranking = self._format_skill_ranking(skill_scores)
        skill_distribution = self._format_distribution(skill_scores)
        skills_to_watch = self._format_watch(skill_scores, decay_report)
        decay_records = self._format_decay_records(decay_report)
        
        learnings_text = self._format_learnings(learnings)
        improvements = self._format_improvements_list(work_analysis.get('corrections', []))
        tomorrow_actions = self._format_tomorrow_actions(tomorrow_plan)
        
        personal = personal_thoughts or "今日工作充实，继续保持节奏。"
        
        return self.REPORT_TEMPLATE.format(
            date=self.date_str,
            timestamp=self.timestamp,
            report_type=self.report_type,
            work_summary=work_summary,
            completed_count=len(work_analysis.get('completed_tasks', [])),
            completed_tasks=completed_tasks or "_（无）_",
            incomplete_count=len(work_analysis.get('incomplete_tasks', [])),
            incomplete_tasks=incomplete_tasks or "_（无）_",
            blockers=blockers or "_（无）_",
            continued_tasks=continued_tasks or "_（无）_",
            new_tasks=new_tasks or "_（无）_",
            skill_plan=skill_plan or "_（无）_",
            priority_order=priority_order or "_（无）_",
            new_skills=new_skills or "_（无新技能）_",
            skill_improvements=skill_improvements or "_（无改进）_",
            development_reasoning=development_reasoning,
            skill_ranking=skill_ranking,
            skill_distribution=skill_distribution,
            skills_to_watch=skills_to_watch or "_（无）_",
            decay_records=decay_records or "_（无状态变化）_",
            learnings=learnings_text,
            improvements=improvements or "_（无明显改进空间）_",
            tomorrow_actions=tomorrow_actions or "_（保持常规节奏）_",
            personal_thoughts=personal,
        )
    
    def _format_work_summary(self, analysis: Dict) -> str:
        """格式化工作摘要"""
        total = analysis.get('total_entries', 0)
        completed = len(analysis.get('completed_tasks', []))
        incomplete = len(analysis.get('incomplete_tasks', []))
        
        if total == 0:
            return "今日对话活动正常，无明确任务记录。"
        
        rate = completed / (completed + incomplete) * 100 if (completed + incomplete) > 0 else 0
        return f"今日共{total}条对话记录，识别{total}个任务项，完成率约{rate:.0f}%。"
    
    def _format_task_list(self, tasks: List[Dict]) -> str:
        """格式化任务列表"""
        if not tasks:
            return ""
        lines = []
        for i, task in enumerate(tasks[:10], 1):
            content = task.get('content', '')[:60]
            lines.append(f"{i}. {content}")
        return "\n".join(lines)
    
    def _format_blockers(self, blockers: List[str]) -> str:
        """格式化阻碍因素"""
        if not blockers:
            return ""
        return "\n".join([f"- {b}" for b in blockers[:3]])
    
    def _format_continued(self, tasks: List[Dict]) -> str:
        """格式化继续任务"""
        if not tasks:
            return ""
        lines = []
        for task in tasks[:5]:
            lines.append(f"- [ ] {task.get('task', '')[:60]}")
        return "\n".join(lines)
    
    def _format_new_tasks(self, tasks: List[Dict]) -> str:
        """格式化新任务"""
        if not tasks:
            return ""
        lines = []
        for task in tasks[:5]:
            lines.append(f"- [ ] {task.get('task', '')[:60]}")
        return "\n".join(lines)
    
    def _format_skill_plan(self, plan: List[Dict]) -> str:
        """格式化技能计划"""
        if not plan:
            return ""
        lines = []
        for item in plan:
            t = item.get('type', '')
            s = item.get('skill', '')
            r = item.get('reason', '')[:30]
            lines.append(f"- **{t}**: {s} — {r}")
        return "\n".join(lines)
    
    def _format_priority(self, priorities: List[str]) -> str:
        """格式化优先级"""
        if not priorities:
            return ""
        lines = []
        for i, p in enumerate(priorities[:8], 1):
            lines.append(f"{i}. {p}")
        return "\n".join(lines)
    
    def _format_new_skills(self, skills: List[Dict]) -> str:
        """格式化新技能"""
        if not skills:
            return ""
        lines = []
        for s in skills:
            name = s.get('name', '')
            desc = s.get('description', '')[:40]
            lines.append(f"- **{name}**: {desc}")
        return "\n".join(lines)
    
    def _format_improvements(self, improvements: List[Dict]) -> str:
        """格式化技能改进"""
        if not improvements:
            return ""
        lines = []
        for imp in improvements:
            name = imp.get('skill', '')
            desc = imp.get('change', '')
            lines.append(f"- **{name}**: {desc}")
        return "\n".join(lines)
    
    def _format_skill_ranking(self, scores: Dict) -> str:
        """格式化技能排行"""
        if not scores:
            return "_（暂无数据）_"
        
        # 取前10
        sorted_skills = sorted(
            scores.items(),
            key=lambda x: x[1].get('score', 0),
            reverse=True
        )[:10]
        
        lines = []
        for i, (name, data) in enumerate(sorted_skills, 1):
            tier = data.get('tier', '')
            score = data.get('score', 0)
            calls = data.get('calls', 0)
            lines.append(f"{i}. {tier} {name}: {score}分 ({calls}次调用)")
        
        return "\n".join(lines)
    
    def _format_distribution(self, scores: Dict) -> str:
        """格式化技能分布"""
        if not scores:
            return "_（暂无数据）_"
        
        tiers = {"🔥": 0, "📈": 0, "💤": 0, "🗄️": 0, "⚰️": 0}
        for data in scores.values():
            tier = data.get('tier', '⚰️')
            if tier in tiers:
                tiers[tier] += 1
        
        lines = []
        for tier, count in tiers.items():
            if count > 0:
                lines.append(f"{tier}: {count}个技能")
        
        return "\n".join(lines) if lines else "_（暂无数据）_"
    
    def _format_watch(self, scores: Dict, decay: Dict) -> str:
        """格式化需关注技能"""
        if not scores:
            return ""
        
        warnings = []
        for name, data in scores.items():
            days = data.get('days_since_last_call')
            if days and days >= 30:
                warnings.append(f"- {name}: {days}天未用")
        
        if not warnings:
            return "_（无技能需要关注）_"
        
        return "\n".join(warnings[:5])
    
    def _format_decay_records(self, decay: Dict) -> str:
        """格式化用进废退记录"""
        changes = decay.get('changes', [])
        if not changes:
            return "_（无状态变化）_"
        
        lines = []
        for c in changes[:5]:
            old = c.get('old_status', '')
            new = c.get('new_status', '')
            skill = c.get('skill', '')
            lines.append(f"- {skill}: {old} -> {new}")
        
        return "\n".join(lines)
    
    def _format_learnings(self, learnings: List[str]) -> str:
        """格式化今日学到"""
        if not learnings:
            return "_（无新学习）_"
        return "\n".join([f"- {l}" for l in learnings[:5]])
    
    def _format_improvements_list(self, corrections: List[Dict]) -> str:
        """格式化改进点"""
        if not corrections:
            return "_（无需改进）_"
        
        lines = []
        for c in corrections[:3]:
            content = c.get('content', '')[:60]
            lines.append(f"- {content}")
        
        return "\n".join(lines)
    
    def _format_tomorrow_actions(self, plan: Dict) -> str:
        """格式化明日行动"""
        actions = plan.get('priority_order', [])[:5]
        if not actions:
            return "_（保持常规节奏）_"
        return "\n".join([f"- {a}" for a in actions])
    
    def generate_morning_report(self) -> str:
        """生成早间简报"""
        self.report_type = "早间简报"
        return f"""# 🌅 早间简报 — {self.date_str}

> 生成时间: {self.timestamp}

今日是新的开始，请查看昨日完整汇报了解详情。

*完整汇报请查看晚间报告。*
"""
    
    def generate_evening_report(self,
                                work_analysis: Dict,
                                tomorrow_plan: Dict,
                                skill_scores: Dict,
                                skill_development: Dict,
                                decay_report: Dict,
                                learnings: List[str],
                                personal_thoughts: str = "") -> str:
        """生成晚间完整汇报"""
        self.report_type = "晚间完整汇报"
        return self.generate(
            work_analysis=work_analysis,
            tomorrow_plan=tomorrow_plan,
            skill_scores=skill_scores,
            skill_development=skill_development,
            decay_report=decay_report,
            learnings=learnings,
            personal_thoughts=personal_thoughts,
        )
