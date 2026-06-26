# 调解进度看板
# 度量衡商事调解智库 - 案件进度可视化与统计分析

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

# ============================================================
# 数据结构
# ============================================================

@dataclass
class MediationPhase:
    """调解阶段"""
    phase_id: str
    name: str
    description: str
    duration_days: int      # 标准周期（天）
    status: str              # pending/in_progress/completed
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    tasks: List[str] = field(default_factory=list)


@dataclass
class CaseProgress:
    """案件进度"""
    case_id: str
    current_phase: str
    progress_percent: float  # 0-100
    completed_milestones: List[str]
    upcoming_milestones: List[str]
    risks: List[str]         # 当前风险
    last_update: str


@dataclass
class DashboardStats:
    """看板统计"""
    total_active: int        # 进行中案件
    completed_this_month: int # 本月完成
    avg_duration: float      # 平均周期
    success_rate: float      # 成功率


# ============================================================
# 预定义调解阶段
# ============================================================

DEFAULT_PHASES = [
    MediationPhase(
        phase_id="P1",
        name="受理与评估",
        description="受理调解申请，争议类型识别，可调解性评估",
        duration_days=5,
        status="pending",
        tasks=["审核申请材料", "识别争议类型", "评估可调解性", "确定调解员"]
    ),
    MediationPhase(
        phase_id="P2",
        name="准备阶段",
        description="案卷材料收集，争议焦点梳理，当事方访谈",
        duration_days=10,
        status="pending",
        tasks=["收集案件材料", "梳理争议焦点", "访谈当事方", "制定调解方案"]
    ),
    MediationPhase(
        phase_id="P3",
        name="调解会议",
        description="联席会议、背靠背会议、方案磋商",
        duration_days=5,
        status="pending",
        tasks=["召开联席会议", "利益探讨论证", "调解方案磋商", "协议条款谈判"]
    ),
    MediationPhase(
        phase_id="P4",
        name="协议达成",
        description="调解协议起草、双方确认、签署",
        duration_days=3,
        status="pending",
        tasks=["起草调解协议", "双方审查确认", "协议签署", "司法确认申请(如需)"]
    ),
    MediationPhase(
        phase_id="P5",
        name="执行跟踪",
        description="履行监督，争议复发处理",
        duration_days=0,  # 持续进行
        status="pending",
        tasks=["履行监督", "回访跟进", "争议复发处理"]
    ),
]


# ============================================================
# 进度计算引擎
# ============================================================

class ProgressCalculator:
    """进度计算引擎"""
    
    @staticmethod
    def calculate_by_phase(current_phase: str, phases: List[MediationPhase]) -> float:
        """按阶段计算进度"""
        phase_order = ["P1", "P2", "P3", "P4", "P5"]
        
        if current_phase not in phase_order:
            return 0
        
        current_idx = phase_order.index(current_phase)
        completed_weight = current_idx * 20
        
        # 当前阶段进度（简化：假设已完成50%）
        current_weight = 10
        
        return min(completed_weight + current_weight, 100)
    
    @staticmethod
    def calculate_by_time(start_date: str, current_phase: str, phases: List[MediationPhase]) -> float:
        """按时间计算进度"""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            now = datetime.now()
            days_elapsed = (now - start).days
            
            # 标准周期
            standard_days = sum(p.duration_days for p in phases if p.duration_days > 0)
            
            progress = min(days_elapsed / standard_days * 100, 100)
            return round(progress, 1)
        except:
            return 0
    
    @staticmethod
    def calculate_by_milestones(completed: List[str], total_milestones: List[str]) -> float:
        """按里程碑计算进度"""
        if not total_milestones:
            return 0
        
        return round(len(completed) / len(total_milestones) * 100, 1)


# ============================================================
# 调解看板
# ============================================================

class MediationDashboard:
    """
    调解进度看板
    
    功能：
    1. 案件进度追踪
    2. 阶段状态可视化
    3. 风险预警
    4. 统计报表
    5. 甘特图生成
    """
    
    def __init__(self, case_manager=None):
        self.phases = DEFAULT_PHASES.copy()
        self.case_manager = case_manager  # 可选：关联案件管理器
    
    # ========== 进度查询 ==========
    
    def get_case_progress(self, case_id: str) -> Optional[CaseProgress]:
        """获取案件进度"""
        if not self.case_manager:
            return None
        
        case = self.case_manager.get_case(case_id)
        if not case:
            return None
        
        # 确定当前阶段
        current_phase = self._infer_phase(case.status)
        
        # 计算进度
        progress = ProgressCalculator.calculate_by_phase(current_phase, self.phases)
        
        # 里程碑
        completed = self._get_completed_milestones(case)
        upcoming = self._get_upcoming_milestones(current_phase)
        
        # 风险识别
        risks = self._identify_risks(case, current_phase)
        
        return CaseProgress(
            case_id=case_id,
            current_phase=current_phase,
            progress_percent=progress,
            completed_milestones=completed,
            upcoming_milestones=upcoming,
            risks=risks,
            last_update=case.updated_date
        )
    
    def _infer_phase(self, status: str) -> str:
        """根据案件状态推断阶段"""
        mapping = {
            "待受理": "P1",
            "已受理": "P1",
            "准备中": "P2",
            "调解中": "P3",
            "达成协议": "P4",
            "已结案": "P5",
            "调解失败": "P5"
        }
        return mapping.get(status, "P1")
    
    def _get_completed_milestones(self, case) -> List[str]:
        """获取已完成的里程碑"""
        completed = []
        
        # 基于事件推断
        for event in case.events:
            if "受理" in event.event_type:
                completed.append("案件受理")
            if "调解" in event.event_type and event.result:
                completed.append("首次调解")
            if "协议" in event.event_type:
                completed.append("调解协议签署")
        
        return completed
    
    def _get_upcoming_milestones(self, current_phase: str) -> List[str]:
        """获取待完成的里程碑"""
        phase_milestones = {
            "P1": ["争议焦点梳理", "调解员确定"],
            "P2": ["材料收集完成", "调解方案制定"],
            "P3": ["调解会议召开", "协议条款确定"],
            "P4": ["协议签署", "司法确认"],
            "P5": ["履行监督", "结案归档"]
        }
        return phase_milestones.get(current_phase, [])
    
    def _identify_risks(self, case, current_phase: str) -> List[str]:
        """识别当前风险"""
        risks = []
        now = datetime.now()
        
        # 时间风险
        if case.deadline:
            try:
                deadline = datetime.strptime(case.deadline, "%Y-%m-%d")
                days_left = (deadline - now).days
                if days_left < 7:
                    risks.append(f"⚠️ 临近截止日期（{days_left}天）")
            except:
                pass
        
        # 争议焦点风险
        unresolved = [dp for dp in case.dispute_points if dp.status != "已解决"]
        if len(unresolved) > 3:
            risks.append(f"⚠️ 存在{len(unresolved)}个未解决争议焦点")
        
        # 金额风险
        if case.disputed_amount > 10000000:
            risks.append("⚠️ 争议金额较大，建议多方论证")
        
        # 阶段风险
        if current_phase == "P3" and len(case.events) < 2:
            risks.append("⚠️ 调解会议进展缓慢")
        
        return risks
    
    # ========== 看板展示 ==========
    
    def render_progress_bar(self, progress: float, width: int = 20) -> str:
        """渲染进度条"""
        filled = int(width * progress / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {progress:.1f}%"
    
    def display_case_dashboard(self, case_id: str) -> str:
        """展示案件看板"""
        progress = self.get_case_progress(case_id)
        if not progress:
            return "未找到案件信息"
        
        lines = [
            f"# 📊 案件进度看板",
            f"",
            f"**案件ID**: {progress.case_id}",
            f"**最后更新**: {progress.last_update}",
            "",
            "---",
            "",
            f"## 当前阶段",
            "",
            f"阶段名称：{self._get_phase_name(progress.current_phase)}",
            f"进度：{self.render_progress_bar(progress.progress_percent)}",
            "",
            "---",
            "",
            "## ✅ 已完成",
        ]
        
        for m in progress.completed_milestones:
            lines.append(f"- {m}")
        
        lines.extend([
            "",
            "## ⏳ 待完成",
        ])
        
        for m in progress.upcoming_milestones:
            lines.append(f"- {m}")
        
        if progress.risks:
            lines.extend([
                "",
                "## ⚠️ 风险预警",
            ])
            for r in progress.risks:
                lines.append(f"- {r}")
        
        return "\n".join(lines)
    
    def _get_phase_name(self, phase_id: str) -> str:
        """获取阶段名称"""
        for p in self.phases:
            if p.phase_id == phase_id:
                return p.name
        return "未知阶段"
    
    # ========== 统计报表 ==========
    
    def get_dashboard_stats(self) -> DashboardStats:
        """获取看板统计"""
        if not self.case_manager:
            return DashboardStats(0, 0, 0, 0)
        
        cases = self.case_manager.list_cases()
        
        # 进行中
        active = [c for c in cases if c.status not in ["已结案", "调解失败"]]
        
        # 本月完成
        now = datetime.now()
        this_month = now.strftime("%Y-%m")
        completed = [c for c in cases 
                   if c.status == "已结案" 
                   and c.updated_date.startswith(this_month)]
        
        # 平均周期
        durations = []
        for c in cases:
            if c.status == "已结案":
                try:
                    start = datetime.strptime(c.created_date, "%Y-%m-%d")
                    end = datetime.strptime(c.updated_date, "%Y-%m-%d")
                    durations.append((end - start).days)
                except:
                    pass
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 成功率
        closed = [c for c in cases if c.status in ["已结案", "调解失败"]]
        success = [c for c in closed if c.status == "已结案"]
        success_rate = len(success) / len(closed) * 100 if closed else 0
        
        return DashboardStats(
            total_active=len(active),
            completed_this_month=len(completed),
            avg_duration=round(avg_duration, 1),
            success_rate=round(success_rate, 1)
        )
    
    def render_gantt_chart(self, case_id: str) -> str:
        """渲染甘特图"""
        progress = self.get_case_progress(case_id)
        if not progress:
            return "未找到案件"
        
        lines = [
            "# 📅 调解甘特图",
            "",
            "| 阶段 | 进度 | 状态 |",
            "|------|------|------|"
        ]
        
        for p in self.phases:
            if p.phase_id == progress.current_phase:
                status = "🔄 进行中"
                bar = self.render_progress_bar(progress.progress_percent, 10)
            elif self._phase_completed(p.phase_id, progress.current_phase):
                status = "✅ 已完成"
                bar = "100%"
            else:
                status = "⏳ 待开始"
                bar = "0%"
            
            lines.append(f"| {p.name} | {bar} | {status} |")
        
        return "\n".join(lines)
    
    def _phase_completed(self, phase_id: str, current: str) -> bool:
        order = ["P1", "P2", "P3", "P4", "P5"]
        try:
            return order.index(phase_id) < order.index(current)
        except:
            return False
    
    # ========== 批量看板 ==========
    
    def list_all_progress(self) -> List[Dict]:
        """列出所有案件进度"""
        if not self.case_manager:
            return []
        
        results = []
        for case in self.case_manager.list_cases():
            progress = self.get_case_progress(case.case_id)
            if progress:
                results.append({
                    "case_id": case.case_id,
                    "case_name": case.case_name,
                    "progress": progress.progress_percent,
                    "phase": progress.current_phase,
                    "risks": len(progress.risks),
                    "status": case.status
                })
        
        # 按进度排序
        results.sort(key=lambda x: x["progress"])
        return results


# ============================================================
# 便捷函数
# ============================================================

def show_dashboard(case_id: str, case_manager=None) -> str:
    """快速显示案件看板"""
    dashboard = MediationDashboard(case_manager)
    return dashboard.display_case_dashboard(case_id)


def show_gantt(case_id: str, case_manager=None) -> str:
    """快速显示甘特图"""
    dashboard = MediationDashboard(case_manager)
    return dashboard.render_gantt_chart(case_id)


def get_stats(case_manager=None) -> Dict:
    """快速获取统计"""
    dashboard = MediationDashboard(case_manager)
    stats = dashboard.get_dashboard_stats()
    return {
        "进行中": stats.total_active,
        "本月完成": stats.completed_this_month,
        "平均周期": f"{stats.avg_duration}天",
        "成功率": f"{stats.success_rate}%"
    }


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    # 导入案例管理器
    try:
        from case_manager import CaseManager
        
        # 初始化
        case_manager = CaseManager()
        dashboard = MediationDashboard(case_manager)
        
        # 示例1：查看所有案件进度
        print("=== 所有案件进度 ===")
        all_progress = dashboard.list_all_progress()
        for p in all_progress[:5]:
            print(f"{p['case_id']}: {p['progress']}% - {p['phase']}")
        
        # 示例2：获取统计
        print("\n=== 看板统计 ===")
        stats = get_stats(case_manager)
        for k, v in stats.items():
            print(f"{k}: {v}")
            
    except Exception as e:
        print("提示：需先创建案件数据才能展示看板")
        print(f"错误: {e}")
        
        # 演示看板功能
        dashboard = MediationDashboard()
        print("\n=== 看板功能演示 ===")
        print("已创建以下模块：")
        print("- 案件进度追踪")
        print("- 阶段状态可视化")
        print("- 风险预警")
        print("- 统计报表")
        print("- 甘特图渲染")