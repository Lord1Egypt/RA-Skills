"""
Cost Tracker - 成本追踪

记录每次编排的 token 消耗和成本。
支持按任务、模型、时间维度统计。
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


# 模型价格表（美元 / 1K tokens）
MODEL_PRICING = {
    # lixiang 内部模型
    "glm": {"input": 0.001, "output": 0.001},
    "kimi": {"input": 0.01, "output": 0.01},
    "lixiang-glm-5/kivy-glm-5": {"input": 0.001, "output": 0.001},
    "lixiang-kimi-2-5/kivy-kimi-k2_5": {"input": 0.01, "output": 0.01},
    # 其他模型（备用）
    "gemini": {"input": 0.01, "output": 0.02},
    "sonnet": {"input": 0.03, "output": 0.15},
    "opus": {"input": 0.15, "output": 0.75},
}


@dataclass
class CostRecord:
    """成本记录"""
    # 基本信息
    task: str                              # 任务描述
    session_id: str = ""                   # 会话ID
    timestamp: str = ""                    # 时间戳
    
    # 模型消耗
    model: str = ""                        # 模型名称
    input_tokens: int = 0                  # 输入 tokens
    output_tokens: int = 0                 # 输出 tokens
    total_tokens: int = 0                  # 总 tokens
    
    # 成本
    input_cost: float = 0.0                # 输入成本（美元）
    output_cost: float = 0.0               # 输出成本（美元）
    total_cost: float = 0.0                # 总成本（美元）
    
    # 元数据
    duration: float = 0.0                  # 执行时间（秒）
    success: bool = True                   # 是否成功
    agent_label: str = ""                  # Agent 标签
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if self.total_tokens == 0:
            self.total_tokens = self.input_tokens + self.output_tokens
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CostRecord":
        return cls(**data)


class CostTracker:
    """
    成本追踪器
    
    记录和统计编排成本
    
    Example:
        >>> tracker = CostTracker()
        >>> tracker.record(model="glm", input_tokens=1000, output_tokens=500)
        >>> stats = tracker.get_stats()
    """
    
    def __init__(
        self,
        track_path: str = "/workspace/projects/claw-orchestra/costs.json",
        max_records: int = 10000,
    ):
        self.track_path = track_path
        self.max_records = max_records
        self.records: List[CostRecord] = []
        self._load()
    
    def _load(self):
        """从文件加载记录"""
        if os.path.exists(self.track_path):
            try:
                with open(self.track_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [
                        CostRecord.from_dict(r) 
                        for r in data.get('records', [])
                    ]
            except Exception as e:
                print(f"[CostTracker] 加载失败: {e}")
                self.records = []
    
    def _save(self):
        """保存记录到文件"""
        os.makedirs(os.path.dirname(self.track_path), exist_ok=True)
        with open(self.track_path, 'w', encoding='utf-8') as f:
            json.dump({
                'records': [r.to_dict() for r in self.records],
                'updated_at': datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
    
    def record(
        self,
        task: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        duration: float = 0.0,
        success: bool = True,
        agent_label: str = "",
        session_id: str = "",
    ) -> CostRecord:
        """
        记录一次成本
        
        Args:
            task: 任务描述
            model: 模型名称
            input_tokens: 输入 tokens
            output_tokens: 输出 tokens
            duration: 执行时间
            success: 是否成功
            agent_label: Agent 标签
            session_id: 会话ID
            
        Returns:
            CostRecord: 成本记录
        """
        # 获取价格
        pricing = MODEL_PRICING.get(model, {"input": 0.01, "output": 0.01})
        
        # 计算成本
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        # 创建记录
        record = CostRecord(
            task=task,
            session_id=session_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            duration=duration,
            success=success,
            agent_label=agent_label,
        )
        
        # 添加到列表
        self.records.append(record)
        
        # 限制数量
        if len(self.records) > self.max_records:
            self.records = self.records[-self.max_records:]
        
        # 保存
        self._save()
        
        return record
    
    def get_stats(
        self,
        by: str = "total",  # total | model | day | task
        days: int = 7,
    ) -> Dict[str, Any]:
        """
        获取统计信息
        
        Args:
            by: 统计维度
            days: 统计天数
            
        Returns:
            统计结果
        """
        # 过滤时间范围
        cutoff = datetime.now() - timedelta(days=days)
        recent_records = [
            r for r in self.records 
            if datetime.fromisoformat(r.timestamp) >= cutoff
        ]
        
        if by == "total":
            return self._stats_total(recent_records)
        elif by == "model":
            return self._stats_by_model(recent_records)
        elif by == "day":
            return self._stats_by_day(recent_records)
        elif by == "task":
            return self._stats_by_task(recent_records)
        else:
            return self._stats_total(recent_records)
    
    def _stats_total(self, records: List[CostRecord]) -> Dict[str, Any]:
        """总体统计"""
        if not records:
            return {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "avg_cost_per_request": 0.0,
            }
        
        total_tokens = sum(r.total_tokens for r in records)
        total_cost = sum(r.total_cost for r in records)
        
        return {
            "total_requests": len(records),
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "avg_cost_per_request": total_cost / len(records),
            "success_rate": sum(1 for r in records if r.success) / len(records),
        }
    
    def _stats_by_model(self, records: List[CostRecord]) -> Dict[str, Any]:
        """按模型统计"""
        by_model = defaultdict(lambda: {"tokens": 0, "cost": 0.0, "count": 0})
        
        for r in records:
            by_model[r.model]["tokens"] += r.total_tokens
            by_model[r.model]["cost"] += r.total_cost
            by_model[r.model]["count"] += 1
        
        return dict(by_model)
    
    def _stats_by_day(self, records: List[CostRecord]) -> Dict[str, Any]:
        """按天统计"""
        by_day = defaultdict(lambda: {"tokens": 0, "cost": 0.0, "count": 0})
        
        for r in records:
            day = r.timestamp[:10]  # YYYY-MM-DD
            by_day[day]["tokens"] += r.total_tokens
            by_day[day]["cost"] += r.total_cost
            by_day[day]["count"] += 1
        
        return dict(by_day)
    
    def _stats_by_task(self, records: List[CostRecord]) -> Dict[str, Any]:
        """按任务统计"""
        by_task = defaultdict(lambda: {"tokens": 0, "cost": 0.0, "count": 0})
        
        for r in records:
            # 任务名称截断
            task_key = r.task[:30] + "..." if len(r.task) > 30 else r.task
            by_task[task_key]["tokens"] += r.total_tokens
            by_task[task_key]["cost"] += r.total_cost
            by_task[task_key]["count"] += 1
        
        return dict(by_task)
    
    def format_cost(self, record: CostRecord) -> str:
        """格式化成本显示"""
        return (
            f"💰 成本: ${record.total_cost:.4f} "
            f"({record.input_tokens} in / {record.output_tokens} out tokens)"
        )
    
    def format_stats(self, stats: Dict[str, Any]) -> str:
        """格式化统计显示"""
        lines = ["📊 成本统计"]
        lines.append(f"  总请求: {stats.get('total_requests', 0)}")
        lines.append(f"  总 tokens: {stats.get('total_tokens', 0):,}")
        lines.append(f"  总成本: ${stats.get('total_cost', 0):.4f}")
        lines.append(f"  平均成本: ${stats.get('avg_cost_per_request', 0):.4f}/请求")
        
        if 'success_rate' in stats:
            lines.append(f"  成功率: {stats['success_rate']*100:.1f}%")
        
        return "\n".join(lines)


# === 全局实例 ===

_cost_tracker: Optional[CostTracker] = None

def get_cost_tracker() -> CostTracker:
    """获取全局成本追踪器"""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker


def track_cost(
    task: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    duration: float = 0.0,
    success: bool = True,
    agent_label: str = "",
) -> CostRecord:
    """记录一次成本（便捷函数）"""
    tracker = get_cost_tracker()
    return tracker.record(
        task=task,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        duration=duration,
        success=success,
        agent_label=agent_label,
    )


# 导出
__all__ = [
    "CostRecord",
    "CostTracker",
    "MODEL_PRICING",
    "get_cost_tracker",
    "track_cost",
]