#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 决策能力评估器
评估 AI 在 EvoMap 任务中的决策质量
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class DecisionMetrics:
    """决策指标"""
    total_decisions: int = 0
    accurate_decisions: int = 0
    avg_confidence: float = 0.0
    avg_response_time: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AIDecisionEvaluator:
    """AI 决策评估器"""
    
    def __init__(self):
        self.metrics = DecisionMetrics()
        self.decision_history: List[Dict] = []
    
    def evaluate(self, decision: Dict, outcome: str) -> Dict:
        """评估决策质量"""
        # 更新指标
        self.metrics.total_decisions += 1
        
        if outcome == 'success':
            self.metrics.accurate_decisions += 1
        
        # 更新平均置信度
        confidence = decision.get('confidence', 0.0)
        self.metrics.avg_confidence = (
            (self.metrics.avg_confidence * (self.metrics.total_decisions - 1) + confidence) /
            self.metrics.total_decisions
        )
        
        # 记录决策历史
        self.decision_history.append({
            'decision': decision,
            'outcome': outcome,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'accuracy': self.get_accuracy(),
            'confidence': self.metrics.avg_confidence,
            'total': self.metrics.total_decisions
        }
    
    def get_accuracy(self) -> float:
        """获取准确率"""
        if self.metrics.total_decisions == 0:
            return 0.0
        return self.metrics.accurate_decisions / self.metrics.total_decisions
    
    def get_metrics(self) -> Dict:
        """获取完整指标"""
        return {
            **self.metrics.to_dict(),
            'accuracy': self.get_accuracy()
        }


if __name__ == "__main__":
    evaluator = AIDecisionEvaluator()
    
    # 模拟评估
    decision = {'confidence': 0.95, 'decision': 'auto_recovery'}
    result = evaluator.evaluate(decision, 'success')
    
    print(f"评估结果：{result}")
    print(f"准确率：{evaluator.get_accuracy():.2%}")
