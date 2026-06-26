"""
Usage Monitor - 使用监控模块

追踪 Cognitive Flexibility Skill 的使用情况和效果。
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path


class UsageMonitor:
    """使用监控器"""
    
    def __init__(self, log_dir: str = None):
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, 'usage-log.jsonl')
        self.stats_file = os.path.join(log_dir, 'usage-stats.json')
        
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 加载统计数据
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """加载统计数据"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "total_uses": 0,
            "mode_distribution": {
                "OOA": 0,
                "OODA": 0,
                "OOCA": 0,
                "OOHA": 0
            },
            "success_count": 0,
            "failure_count": 0,
            "avg_confidence": 0.0,
            "total_tasks": 0,
            "first_use": None,
            "last_use": None,
            "tasks_by_type": {},
            "mode_effectiveness": {
                "OOA": {"count": 0, "avg_score": 0.0},
                "OODA": {"count": 0, "avg_score": 0.0},
                "OOCA": {"count": 0, "avg_score": 0.0},
                "OOHA": {"count": 0, "avg_score": 0.0}
            }
        }
    
    def log_usage(self, task: str, mode: str, result: Dict, context: Dict = None):
        """
        记录使用日志
        
        Args:
            task: 任务描述
            mode: 使用的认知模式
            result: 执行结果
            context: 上下文信息
        """
        timestamp = datetime.now().isoformat()
        
        # 创建日志条目
        log_entry = {
            "timestamp": timestamp,
            "task": task,
            "task_hash": hash(task),  # 用于去重
            "mode": mode,
            "confidence": result.get("confidence", 0.0),
            "assessment_score": result.get("assessment", {}).get("overall_score", 0.0),
            "success": result.get("assessment", {}).get("overall_score", 0.0) >= 0.7,
            "needs_improvement": result.get("assessment", {}).get("needs_improvement", False),
            "mode_switched": result.get("mode_switched", False),
            "previous_mode": result.get("previous_mode", None),
            "context": context or {}
        }
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # 更新统计数据
        self._update_stats(log_entry)
        
        print(f"[Monitor] 已记录使用：模式={mode}, 置信度={log_entry['confidence']:.2f}, 评分={log_entry['assessment_score']:.2f}")
    
    def _update_stats(self, log_entry: Dict):
        """更新统计数据"""
        # 总使用次数
        self.stats["total_uses"] += 1
        
        # 模式分布
        mode = log_entry["mode"]
        if mode in self.stats["mode_distribution"]:
            self.stats["mode_distribution"][mode] += 1
        
        # 成功/失败计数
        if log_entry["success"]:
            self.stats["success_count"] += 1
        else:
            self.stats["failure_count"] += 1
        
        # 平均置信度（移动平均）
        old_avg = self.stats["avg_confidence"]
        n = self.stats["total_uses"]
        self.stats["avg_confidence"] = old_avg + (log_entry["confidence"] - old_avg) / n
        
        # 模式效果统计
        if mode in self.stats["mode_effectiveness"]:
            mode_stats = self.stats["mode_effectiveness"][mode]
            mode_stats["count"] += 1
            old_mode_avg = mode_stats["avg_score"]
            mode_stats["avg_score"] = old_mode_avg + (log_entry["assessment_score"] - old_mode_avg) / mode_stats["count"]
        
        # 任务类型统计
        task_type = self._categorize_task(log_entry["task"])
        if task_type not in self.stats["tasks_by_type"]:
            self.stats["tasks_by_type"][task_type] = 0
        self.stats["tasks_by_type"][task_type] += 1
        
        # 首次/最后使用时间
        if self.stats["first_use"] is None:
            self.stats["first_use"] = log_entry["timestamp"]
        self.stats["last_use"] = log_entry["timestamp"]
        
        # 保存统计数据
        self._save_stats()
    
    def _categorize_task(self, task: str) -> str:
        """任务分类"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ["分析", "analysis", "评估", "evaluate"]):
            return "analysis"
        elif any(kw in task_lower for kw in ["设计", "design", "创意", "creative"]):
            return "creative"
        elif any(kw in task_lower for kw in ["为什么", "why", "探索", "explore", "研究", "research"]):
            return "research"
        elif any(kw in task_lower for kw in ["简单", "simple", "快速", "quick"]):
            return "simple"
        else:
            return "other"
    
    def _save_stats(self):
        """保存统计数据"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def get_stats(self, days: int = None) -> Dict:
        """
        获取统计数据
        
        Args:
            days: 仅统计最近 N 天，None 表示全部
        
        Returns:
            统计数据字典
        """
        if days is None:
            return self.stats.copy()
        
        # 过滤最近 N 天的日志
        cutoff = datetime.now() - timedelta(days=days)
        filtered_logs = []
        
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    log = json.loads(line)
                    log_time = datetime.fromisoformat(log["timestamp"])
                    if log_time >= cutoff:
                        filtered_logs.append(log)
        
        # 重新计算统计数据
        return self._calculate_stats_from_logs(filtered_logs)
    
    def _calculate_stats_from_logs(self, logs: List[Dict]) -> Dict:
        """从日志列表计算统计数据"""
        if not logs:
            return {"message": "无数据", "count": 0}
        
        stats = {
            "count": len(logs),
            "mode_distribution": {},
            "success_rate": 0.0,
            "avg_confidence": 0.0,
            "avg_score": 0.0,
            "mode_effectiveness": {}
        }
        
        success_count = 0
        total_confidence = 0.0
        total_score = 0.0
        
        for log in logs:
            # 模式分布
            mode = log["mode"]
            stats["mode_distribution"][mode] = stats["mode_distribution"].get(mode, 0) + 1
            
            # 成功率
            if log["success"]:
                success_count += 1
            
            # 平均置信度
            total_confidence += log.get("confidence", 0.0)
            total_score += log.get("assessment_score", 0.0)
        
        stats["success_rate"] = success_count / len(logs) * 100
        stats["avg_confidence"] = total_confidence / len(logs)
        stats["avg_score"] = total_score / len(logs)
        
        return stats
    
    def get_mode_comparison(self) -> Dict:
        """获取模式效果对比"""
        return self.stats["mode_effectiveness"].copy()
    
    def get_best_mode_for_task_type(self, task_type: str) -> str:
        """获取某类任务的最佳模式"""
        # 简化实现：返回使用次数最多的模式
        mode_dist = self.stats["mode_distribution"]
        if not mode_dist:
            return "OODA"  # 默认
        
        return max(mode_dist, key=mode_dist.get)
    
    def generate_report(self, days: int = 7) -> str:
        """
        生成使用报告
        
        Args:
            days: 统计最近 N 天
        
        Returns:
            报告文本
        """
        stats = self.get_stats(days)
        
        if "message" in stats:
            return f"最近{days}天无使用记录"
        
        report = []
        report.append("=" * 60)
        report.append(f"Cognitive Flexibility Skill 使用报告（最近{days}天）")
        report.append("=" * 60)
        report.append("")
        report.append(f"总使用次数：{stats['count']}")
        report.append(f"成功率：{stats['success_rate']:.1f}%")
        report.append(f"平均置信度：{stats['avg_confidence']:.2f}")
        report.append(f"平均评分：{stats['avg_score']:.2f}")
        report.append("")
        report.append("模式分布:")
        for mode, count in stats["mode_distribution"].items():
            percentage = count / stats["count"] * 100
            report.append(f"  {mode}: {count}次 ({percentage:.1f}%)")
        report.append("")
        report.append("模式效果对比:")
        mode_comp = self.get_mode_comparison()
        for mode, data in mode_comp.items():
            if data["count"] > 0:
                report.append(f"  {mode}: 使用{data['count']}次，平均评分{data['avg_score']:.2f}")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_logs(self, output_file: str = None) -> str:
        """导出日志"""
        if output_file is None:
            output_file = os.path.join(self.log_dir, 'usage-export.json')
        
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    logs.append(json.loads(line))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return output_file


# 使用示例
if __name__ == "__main__":
    monitor = UsageMonitor()
    
    # 生成报告
    report = monitor.generate_report(days=7)
    print(report)
    
    # 导出日志
    export_file = monitor.export_logs()
    print(f"\n日志已导出到：{export_file}")
