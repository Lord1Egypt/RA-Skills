# -*- coding: utf-8 -*-
"""
Feedback Collector - 自动收集用户反馈

从各渠道收集 Cognitive Flexibility Skill 的用户反馈
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self, feedback_dir: str = None):
        if feedback_dir is None:
            feedback_dir = os.path.join(os.path.dirname(__file__))
        
        self.feedback_dir = feedback_dir
        self.tracker_file = os.path.join(feedback_dir, 'FEEDBACK-TRACKER.md')
        self.feedback_log = os.path.join(feedback_dir, 'feedback-log.jsonl')
        
        # 确保目录存在
        os.makedirs(feedback_dir, exist_ok=True)
        
        # 加载反馈计数
        self.stats = self._load_stats()
    
    def _load_stats(self) -> dict:
        """加载统计数据"""
        stats_file = os.path.join(self.feedback_dir, 'feedback-stats.json')
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "total_feedback": 0,
            "by_type": {
                "bug": 0,
                "feature": 0,
                "experience": 0,
                "performance": 0
            },
            "by_status": {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
                "closed": 0
            },
            "avg_response_time_hours": 0.0,
            "avg_resolution_time_hours": 0.0,
            "user_satisfaction": 0.0,
            "last_updated": None
        }
    
    def add_feedback(self, feedback: dict):
        """
        添加反馈
        
        Args:
            feedback: 反馈字典，包含以下字段：
                - id: 反馈 ID (如 FB-001)
                - date: 日期 (ISO 格式)
                - user: 用户名
                - type: 类型 (bug/feature/experience/performance)
                - description: 描述
                - severity: 严重性 (P0/P1/P2/P3)
                - status: 状态 (open/in_progress/resolved/closed)
                - source: 来源 (clawhub/github/discord/email)
        """
        # 写入日志
        with open(self.feedback_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
        
        # 更新统计
        self._update_stats(feedback)
        
        # 更新追踪文件
        self._update_tracker(feedback)
        
        print(f"[Feedback] 已收集反馈：{feedback['id']} - {feedback['type']}")
    
    def _update_stats(self, feedback: dict):
        """更新统计数据"""
        self.stats["total_feedback"] += 1
        
        # 按类型统计
        fb_type = feedback.get("type", "other")
        if fb_type in self.stats["by_type"]:
            self.stats["by_type"][fb_type] += 1
        
        # 按状态统计
        status = feedback.get("status", "open")
        if status in self.stats["by_status"]:
            self.stats["by_status"][status] += 1
        
        self.stats["last_updated"] = datetime.now().isoformat()
        
        # 保存统计
        self._save_stats()
    
    def _save_stats(self):
        """保存统计数据"""
        stats_file = os.path.join(self.feedback_dir, 'feedback-stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def _update_tracker(self, feedback: dict):
        """更新追踪文件（简化实现）"""
        # 实际实现应该解析并更新 FEEDBACK-TRACKER.md
        # 这里只记录日志
        pass
    
    def get_stats(self) -> dict:
        """获取统计数据"""
        return self.stats.copy()
    
    def get_feedback_log(self, limit: int = 10) -> list:
        """获取最近的反馈日志"""
        logs = []
        
        if os.path.exists(self.feedback_log):
            with open(self.feedback_log, 'r', encoding='utf-8') as f:
                for line in f:
                    logs.append(json.loads(line))
        
        return logs[-limit:]
    
    def generate_report(self, days: int = 7) -> str:
        """
        生成反馈报告
        
        Args:
            days: 统计最近 N 天
        
        Returns:
            报告文本
        """
        stats = self.get_stats()
        
        report = []
        report.append("=" * 60)
        report.append("Cognitive Flexibility Skill 用户反馈报告")
        report.append("=" * 60)
        report.append("")
        report.append(f"总反馈数量：{stats['total_feedback']}")
        report.append(f"最后更新：{stats.get('last_updated', '无')}")
        report.append("")
        report.append("反馈类型分布:")
        for fb_type, count in stats["by_type"].items():
            report.append(f"  {fb_type}: {count}")
        report.append("")
        report.append("反馈状态分布:")
        for status, count in stats["by_status"].items():
            report.append(f"  {status}: {count}")
        report.append("")
        
        if stats.get("avg_response_time_hours", 0) > 0:
            report.append(f"平均响应时间：{stats['avg_response_time_hours']:.1f}小时")
        
        if stats.get("user_satisfaction", 0) > 0:
            report.append(f"用户满意度：{stats['user_satisfaction']:.1f}/5.0")
        
        report.append("")
        report.append("=" * 60)
        
        # 最近反馈
        recent = self.get_feedback_log(limit=5)
        if recent:
            report.append("")
            report.append("最近反馈:")
            for fb in recent:
                report.append(f"  [{fb['id']}] {fb['type']}: {fb.get('description', 'N/A')[:50]}...")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_feedback(self, output_file: str = None) -> str:
        """导出反馈"""
        if output_file is None:
            output_file = os.path.join(self.feedback_dir, 'feedback-export.json')
        
        logs = self.get_feedback_log(limit=1000)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return output_file


# 使用示例
if __name__ == "__main__":
    collector = FeedbackCollector()
    
    # 生成报告
    report = collector.generate_report(days=7)
    print(report)
    
    # 导出反馈
    export_file = collector.export_feedback()
    print(f"\n反馈已导出到：{export_file}")
