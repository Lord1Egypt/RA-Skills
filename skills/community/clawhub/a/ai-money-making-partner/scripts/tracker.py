#!/usr/bin/env python3
"""
执行进度追踪器
功能：追踪用户副业执行进度，给出优化建议
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ExecutionTracker:
    """执行进度追踪器"""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.data_file = f"execution_data_{user_id}.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "user_id": self.user_id,
                "direction": None,
                "start_date": None,
                "tasks": [],
                "milestones": [],
                "problems": [],
                "adjustments": []
            }
    
    def _save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def start_project(self, direction: str):
        """开始一个项目"""
        self.data["direction"] = direction
        self.data["start_date"] = datetime.now().strftime("%Y-%m-%d")
        self._save_data()
        return f"项目已启动：{direction}"
    
    def log_task(self, day: int, task: str, status: str, note: str = ""):
        """
        记录任务执行
        
        Args:
            day: 第几天
            task: 任务描述
            status: 完成/未完成/遇到问题
            note: 备注
        """
        self.data["tasks"].append({
            "day": day,
            "task": task,
            "status": status,
            "note": note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save_data()
    
    def log_milestone(self, day: int, milestone: str, achieved: bool):
        """记录里程碑"""
        self.data["milestones"].append({
            "day": day,
            "milestone": milestone,
            "achieved": achieved,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save_data()
    
    def log_problem(self, day: int, problem: str, severity: str = "medium"):
        """记录问题"""
        self.data["problems"].append({
            "day": day,
            "problem": problem,
            "severity": severity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save_data()
    
    def get_progress(self) -> Dict:
        """获取进度"""
        direction = self.data.get("direction")
        start_date = self.data.get("start_date")
        
        if not start_date:
            return {"status": "未启动", "progress": 0}
        
        # 计算天数
        start = datetime.strptime(start_date, "%Y-%m-%d")
        days_passed = (datetime.now() - start).days + 1
        
        # 计算进度
        completed_tasks = sum(1 for t in self.data.get("tasks", []) if t["status"] == "完成")
        total_tasks = len(self.data.get("tasks", []))
        
        # 计算里程碑达成
        achieved_milestones = sum(1 for m in self.data.get("milestones", []) if m["achieved"])
        total_milestones = len(self.data.get("milestones", []))
        
        # 计算问题数
        problems_count = len(self.data.get("problems", []))
        
        progress_percent = 0
        if days_passed <= 14:
            progress_percent = min(completed_tasks / 10 * 100, 100)
        elif days_passed <= 45:
            progress_percent = min(30 + (completed_tasks - 10) / 20 * 70, 100)
        else:
            progress_percent = min(60 + (completed_tasks - 30) / 30 * 40, 100)
        
        return {
            "direction": direction,
            "days_passed": days_passed,
            "current_phase": self._get_phase(days_passed),
            "tasks": {
                "completed": completed_tasks,
                "total": total_tasks,
                "rate": f"{completed_tasks}/{total_tasks}" if total_tasks > 0 else "N/A"
            },
            "milestones": {
                "achieved": achieved_milestones,
                "total": total_milestones
            },
            "problems_count": problems_count,
            "progress_percent": int(progress_percent),
            "status": "正常" if progress_percent >= days_passed / 90 * 100 else "滞后"
        }
    
    def _get_phase(self, days: int) -> str:
        """获取当前阶段"""
        if days <= 14:
            return "冷启动期"
        elif days <= 45:
            return "成长期"
        else:
            return "稳定期"
    
    def analyze_and_suggest(self) -> Dict:
        """分析并给出建议"""
        progress = self.get_progress()
        problems = self.data.get("problems", [])
        
        suggestions = []
        
        # 基于阶段给出建议
        phase = progress.get("current_phase", "")
        
        if phase == "冷启动期":
            if progress.get("days_passed", 0) > 7 and progress.get("tasks", {}).get("completed", 0) < 3:
                suggestions.append({
                    "type": "warning",
                    "message": "启动较慢，建议加快执行速度",
                    "action": "每天至少完成1个核心任务"
                })
            
            # 检查是否有订单/变现
            tasks = self.data.get("tasks", [])
            monetized = any("订单" in t.get("task", "") or "变现" in t.get("task", "") for t in tasks)
            if progress.get("days_passed", 0) > 10 and not monetized:
                suggestions.append({
                    "type": "urgent",
                    "message": "还没验证变现？",
                    "action": "尽快出单或获取流量"
                })
        
        elif phase == "成长期":
            if progress.get("tasks", {}).get("rate", "0/0") == "0/0":
                suggestions.append({
                    "type": "warning",
                    "message": "需要加大输出了",
                    "action": "增加发布频率或内容数量"
                })
        
        # 基于问题给出建议
        recent_problems = problems[-3:] if problems else []
        for problem in recent_problems:
            if "流量" in problem.get("problem", ""):
                suggestions.append({
                    "type": "suggestion",
                    "message": "流量问题",
                    "action": "研究同行爆款，优化标题封面"
                })
            elif "转化" in problem.get("problem", ""):
                suggestions.append({
                    "type": "suggestion",
                    "message": "转化问题",
                    "action": "优化引导话术，调整产品"
                })
        
        # 如果没有问题，给出鼓励
        if not suggestions:
            suggestions.append({
                "type": "success",
                "message": "进展顺利！",
                "action": "继续保持当前节奏"
            })
        
        return {
            "progress": progress,
            "suggestions": suggestions,
            "next_milestone": self._get_next_milestone(progress.get("days_passed", 0))
        }
    
    def _get_next_milestone(self, days: int) -> Dict:
        """获取下一个里程碑"""
        milestones = {
            7: {"day": 7, "milestone": "完成基础准备"},
            14: {"day": 14, "milestone": "验证变现路径"},
            30: {"day": 30, "milestone": "收入稳定增长"},
            45: {"day": 45, "milestone": "建立稳定收入"},
            60: {"day": 60, "milestone": "开始规模化"},
            90: {"day": 90, "milestone": "达成目标收入"}
        }
        
        # 找下一个里程碑
        for day in sorted(milestones.keys()):
            if days < day:
                return milestones[day]
        
        return {"day": 90, "milestone": "达成目标"}


def create_tracker(user_id: str = "default") -> ExecutionTracker:
    """创建追踪器"""
    return ExecutionTracker(user_id)


if __name__ == "__main__":
    # 测试
    tracker = create_tracker("test_user")
    tracker.start_project("短视频带货")
    
    # 模拟记录
    tracker.log_task(1, "注册账号", "完成")
    tracker.log_task(2, "找对标账号", "完成")
    tracker.log_task(3, "拍摄视频", "遇到问题", "不会剪辑")
    
    # 获取进度
    progress = tracker.get_progress()
    print(json.dumps(progress, ensure_ascii=False, indent=2))
    
    # 获取分析和建议
    analysis = tracker.analyze_and_suggest()
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
