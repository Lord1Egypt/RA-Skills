"""
Experience Store - 经验库

记录成功的编排策略，下次遇到类似任务可以复用。
让 ClawOrchestra 越用越聪明。
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class OrchestrationExperience:
    """一次编排经验"""
    # 任务信息
    task: str                              # 原始任务
    task_type: str                         # 任务类型 (research/code/analysis/writing)
    
    # 分解策略
    subtasks: List[Dict[str, Any]]         # 子任务列表
    strategy: str                          # parallel/sequential/hybrid
    
    # 执行结果
    success: bool                          # 是否成功
    total_duration: float                  # 总耗时（秒）
    total_tokens: int                      # 总 token 消耗
    
    # 效果评分
    efficiency_score: float = 0.0          # 效率评分 (0-1)
    cost_score: float = 0.0                # 成本评分 (0-1，越低越好)
    
    # 元数据
    timestamp: str = ""                    # 时间戳
    session_id: str = ""                   # 会话ID
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrchestrationExperience":
        return cls(**data)


class ExperienceStore:
    """
    经验库
    
    存储和检索编排经验，支持相似任务检索
    
    Example:
        >>> store = ExperienceStore()
        >>> store.save(experience)
        >>> similar = store.find_similar("调研 LangChain")
    """
    
    def __init__(
        self,
        store_path: str = "/workspace/projects/claw-orchestra/experiences.json",
        max_experiences: int = 1000,
    ):
        self.store_path = store_path
        self.max_experiences = max_experiences
        self.experiences: List[OrchestrationExperience] = []
        self._load()
    
    def _load(self):
        """从文件加载经验"""
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.experiences = [
                        OrchestrationExperience.from_dict(e) 
                        for e in data.get('experiences', [])
                    ]
            except Exception as e:
                print(f"[ExperienceStore] 加载失败: {e}")
                self.experiences = []
    
    def _save(self):
        """保存经验到文件"""
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        with open(self.store_path, 'w', encoding='utf-8') as f:
            json.dump({
                'experiences': [e.to_dict() for e in self.experiences],
                'updated_at': datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
    
    def save(self, experience: OrchestrationExperience):
        """保存经验"""
        # 计算评分
        experience.efficiency_score = self._calculate_efficiency(experience)
        experience.cost_score = self._calculate_cost(experience)
        
        # 添加到列表
        self.experiences.append(experience)
        
        # 限制数量
        if len(self.experiences) > self.max_experiences:
            self.experiences = self.experiences[-self.max_experiences:]
        
        # 保存
        self._save()
        
        print(f"[ExperienceStore] 保存经验: {experience.task[:30]}... (效率={experience.efficiency_score:.2f}, 成本={experience.cost_score:.2f})")
    
    def find_similar(
        self,
        task: str,
        limit: int = 3,
        min_similarity: float = 0.3,
    ) -> List[OrchestrationExperience]:
        """
        查找相似任务的经验
        
        Args:
            task: 当前任务
            limit: 返回数量
            min_similarity: 最小相似度阈值
            
        Returns:
            相似的经验列表
        """
        # 简单的关键词匹配
        task_keywords = set(task.lower().split())
        
        scored = []
        for exp in self.experiences:
            if not exp.success:
                continue
            
            exp_keywords = set(exp.task.lower().split())
            
            # Jaccard 相似度
            intersection = len(task_keywords & exp_keywords)
            union = len(task_keywords | exp_keywords)
            similarity = intersection / union if union > 0 else 0
            
            if similarity >= min_similarity:
                scored.append((similarity, exp))
        
        # 按相似度排序
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return [exp for _, exp in scored[:limit]]
    
    def get_best_practice(self, task_type: str) -> Optional[OrchestrationExperience]:
        """获取某类型任务的最佳实践"""
        candidates = [
            e for e in self.experiences 
            if e.task_type == task_type and e.success
        ]
        
        if not candidates:
            return None
        
        # 按效率评分排序
        candidates.sort(key=lambda x: x.efficiency_score, reverse=True)
        return candidates[0]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.experiences:
            return {
                "total": 0,
                "success_rate": 0,
                "avg_duration": 0,
                "avg_tokens": 0,
            }
        
        success_count = sum(1 for e in self.experiences if e.success)
        
        return {
            "total": len(self.experiences),
            "success_rate": success_count / len(self.experiences),
            "avg_duration": sum(e.total_duration for e in self.experiences) / len(self.experiences),
            "avg_tokens": sum(e.total_tokens for e in self.experiences) / len(self.experiences),
            "by_type": self._count_by_type(),
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """按任务类型统计"""
        counts = {}
        for e in self.experiences:
            counts[e.task_type] = counts.get(e.task_type, 0) + 1
        return counts
    
    def _calculate_efficiency(self, exp: OrchestrationExperience) -> float:
        """计算效率评分"""
        # 基于成功率和耗时
        if not exp.success:
            return 0.0
        
        # 耗时越短越好（假设 30s 是基准）
        duration_score = max(0, 1 - exp.total_duration / 60)
        
        # 子任务数量合理（假设 2-5 个是最佳）
        subtask_count = len(exp.subtasks)
        subtask_score = 1.0 if 2 <= subtask_count <= 5 else 0.5
        
        return (duration_score + subtask_score) / 2
    
    def _calculate_cost(self, exp: OrchestrationExperience) -> float:
        """计算成本评分（越低越好）"""
        # 基于 token 消耗
        # 假设 50k token 是基准
        return min(1.0, exp.total_tokens / 50000)


# === 便捷函数 ===

_experience_store: Optional[ExperienceStore] = None

def get_experience_store() -> ExperienceStore:
    """获取全局经验库实例"""
    global _experience_store
    if _experience_store is None:
        _experience_store = ExperienceStore()
    return _experience_store


def record_experience(
    task: str,
    task_type: str,
    subtasks: List[Dict[str, Any]],
    success: bool,
    duration: float,
    tokens: int,
) -> OrchestrationExperience:
    """记录一次编排经验"""
    exp = OrchestrationExperience(
        task=task,
        task_type=task_type,
        subtasks=subtasks,
        strategy="parallel" if len(subtasks) > 1 else "single",
        success=success,
        total_duration=duration,
        total_tokens=tokens,
    )
    
    store = get_experience_store()
    store.save(exp)
    
    return exp


def find_similar_experiences(task: str, limit: int = 3) -> List[OrchestrationExperience]:
    """查找相似任务的经验"""
    store = get_experience_store()
    return store.find_similar(task, limit)


# 导出
__all__ = [
    "OrchestrationExperience",
    "ExperienceStore",
    "get_experience_store",
    "record_experience",
    "find_similar_experiences",
]