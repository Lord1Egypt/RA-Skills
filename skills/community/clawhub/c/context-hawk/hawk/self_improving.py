"""
self_improving.py — 自我反思学习模块

功能：
- 记录错误和纠正
- 分析错误模式
- 生成学习日志供下次参考
- 影响未来决策
"""

import os
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class LearningEntry:
    id: str
    timestamp: float
    error_type: str       # "recall_miss" | "extraction_empty" | "low_score" | "other"
    context: dict         # 错误上下文
    correction: str        # 纠正措施
    resolved: bool
    tags: list[str]


class SelfImproving:
    """
    自我反思学习
    - learn_from_error(): 记录错误
    - correct(): 标记已纠正
    - get_learnings(): 获取相关学习
    - get_stats(): 获取分析统计
    """

    LEARNING_PATH = "~/.hawk/learnings.json"
    PATTERNS_PATH = "~/.hawk/patterns.json"

    def __init__(self):
        self.learnings: list[LearningEntry] = []
        self.patterns: dict[str, int] = {}
        self._load()

    def _load(self):
        path_str = os.path.expanduser(self.LEARNING_PATH)
        if os.path.exists(path_str):
            with open(path_str) as f:
                data = json.load(f)
                self.learnings = [LearningEntry(**e) for e in data.get("learnings", [])]
                self.patterns = data.get("patterns", {})

        patterns_path = os.path.expanduser(self.PATTERNS_PATH)
        if os.path.exists(patterns_path):
            with open(patterns_path) as f:
                self.patterns = json.load(f)

    def _save(self):
        path_str = os.path.expanduser(self.LEARNING_PATH)
        os.makedirs(os.path.dirname(path_str), exist_ok=True)
        with open(path_str, 'w') as f:
            json.dump({
                "learnings": [asdict(l) for l in self.learnings],
                "patterns": self.patterns,
            }, f, indent=2, ensure_ascii=False)

    def learn_from_error(
        self,
        error_type: str,
        context: dict,
        correction: str = "",
        tags: list[str] = None
    ) -> str:
        """记录一个错误学习"""
        import hashlib
        id = hashlib.sha256(f"{error_type}{time.time()}".encode()).hexdigest()[:12]
        entry = LearningEntry(
            id=id,
            timestamp=time.time(),
            error_type=error_type,
            context=context,
            correction=correction,
            resolved=False,
            tags=tags or [],
        )
        self.learnings.append(entry)

        # 更新模式计数
        self.patterns[error_type] = self.patterns.get(error_type, 0) + 1
        self._save()
        return id

    def correct(self, id: str, correction: str):
        """标记错误已纠正并记录纠正方法"""
        for l in self.learnings:
            if l.id == id:
                l.resolved = True
                l.correction = correction
                break
        self._save()

    def get_learnings(self, error_type: str = None, limit: int = 10) -> list[LearningEntry]:
        """获取最近的学习记录"""
        learnings = self.learnings
        if error_type:
            learnings = [l for l in learnings if l.error_type == error_type]
        return sorted(learnings, key=lambda l: -l.timestamp)[:limit]

    def get_unresolved(self) -> list[LearningEntry]:
        return [l for l in self.learnings if not l.resolved]

    def get_stats(self) -> dict:
        """获取学习统计"""
        total = len(self.learnings)
        resolved = sum(1 for l in self.learnings if l.resolved)
        by_type = {}
        for l in self.learnings:
            by_type[l.error_type] = by_type.get(l.error_type, 0) + 1
        return {
            "total": total,
            "resolved": resolved,
            "unresolved": total - resolved,
            "resolution_rate": round(resolved / max(1, total), 3),
            "by_type": by_type,
            "patterns": self.patterns,
        }

    def suggest_improvement(self, context: dict) -> Optional[str]:
        """
        基于历史学习，给出改进建议
        如果有未解决的相关错误，返回建议
        """
        query = context.get("query", "")
        for l in self.learnings:
            if l.resolved:
                continue
            # 简单关键词匹配
            if any(kw in query.lower() for kw in l.context.get("keywords", [])):
                return f"[学习建议] {l.error_type}: {l.correction or '待解决'}"
        return None
