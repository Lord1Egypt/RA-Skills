"""
Quality Scoring Package

对标 QClaw 5维评分 + 90分达标机制

Architecture:
    QualityReviewer   ← Orchestrator 调用入口
    ├── QualityScorer   → 5维度评分
    │   ├── completeness   (完整性)
    │   ├── accuracy      (准确性)
    │   ├── relevance     (相关性)
    │   ├── timeliness    (时效性)
    │   └── usability     (可用性)
    └── QualityGate      → 90分达标判断 + 改进建议
         └── RetryLoop    → 不达标自动重试（最多3次）
"""

from .models import (
    QualityDimension,
    QualityScore,
    QualityReport,
    AgentResult,
    TaskContext,
    RetryStrategy,
)
from .scorer import QualityScorer
from .gate import QualityGate
from .reviewer import QualityReviewer, ReviewResult
from .retry_loop import QualityRetryLoop

__all__ = [
    "QualityDimension",
    "QualityScore",
    "QualityReport",
    "AgentResult",
    "TaskContext",
    "RetryStrategy",
    "QualityScorer",
    "QualityGate",
    "QualityReviewer",
    "ReviewResult",
    "QualityRetryLoop",
]
