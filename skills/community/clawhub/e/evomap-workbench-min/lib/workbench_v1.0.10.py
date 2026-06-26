#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流引擎 v1.0.10 - 完整版
功能：工作流管理、执行统计、错误恢复
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import time

from .ai_decision_evolution import AIDecisionEvolutionEngine


class EvoMapWorkBench:
    """EvoMap WorkBench 核心工作流引擎"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化 WorkBench"""
        self.config = config or {}
        self.engine = AIDecisionEvolutionEngine()
        self.stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'start_time': datetime.utcnow().isoformat(),
            'execution_times': []
        }
        self.error_recovery_count = 0
        self.last_error = None
    
    def analyze(self, context: Dict) -> Dict:
        """分析问题"""
        start_time = time.time()
        
        decision = self.engine.make_decision(context)
        
        self.stats['total_tasks'] += 1
        execution_time = time.time() - start_time
        self.stats['execution_times'].append(execution_time)
        
        return decision
    
    def execute(self, decision: Dict) -> Dict:
        """执行决策"""
        try:
            # 模拟执行
            outcome = 'success'
            
            # 记录结果
            self.engine.record_outcome(decision['decision_id'], outcome)
            
            if outcome == 'success':
                self.stats['successful_tasks'] += 1
            else:
                self.stats['failed_tasks'] += 1
            
            return {
                'outcome': outcome,
                'decision': decision,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            self.last_error = str(e)
            self.error_recovery_count += 1
            
            # 错误恢复
            return self._recover_from_error(e, decision)
    
    def _recover_from_error(self, error: Exception, decision: Dict) -> Dict:
        """错误恢复"""
        # 记录错误
        error_info = {
            'error': str(error),
            'decision': decision.get('decision_id'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # 尝试恢复
        recovery_decision = self.engine.make_decision({
            'error_type': 'execution_error',
            'error_message': str(error)
        })
        
        return {
            'outcome': 'recovered',
            'error': error_info,
            'recovery_decision': recovery_decision,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        execution_times = self.stats['execution_times']
        
        return {
            **self.stats,
            'success_rate': self.stats['successful_tasks'] / self.stats['total_tasks'] if self.stats['total_tasks'] > 0 else 0,
            'avg_execution_time': sum(execution_times) / len(execution_times) if execution_times else 0,
            'error_recovery_count': self.error_recovery_count,
            'last_error': self.last_error
        }
    
    def get_execution_report(self) -> Dict:
        """获取执行报告"""
        return {
            'summary': self.get_stats(),
            'evolution_report': self.engine.get_evolution_report(),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def batch_analyze(self, contexts: List[Dict]) -> List[Dict]:
        """批量分析问题"""
        results = []
        for context in contexts:
            result = self.analyze(context)
            results.append(result)
        return results
    
    def batch_execute(self, decisions: List[Dict]) -> List[Dict]:
        """批量执行决策"""
        results = []
        for decision in decisions:
            result = self.execute(decision)
            results.append(result)
        return results
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'start_time': datetime.utcnow().isoformat(),
            'execution_times': []
        }
        self.error_recovery_count = 0
        self.last_error = None


if __name__ == "__main__":
    # 测试工作流引擎
    print("=== 测试工作流引擎 ===\n")
    
    bench = EvoMapWorkBench()
    
    # 分析问题
    context = {'error_type': '429', 'scenario_name': 'rate_limit'}
    decision = bench.analyze(context)
    
    print(f"决策：{decision['decision']}")
    print(f"置信度：{decision['confidence']:.2%}\n")
    
    # 执行决策
    result = bench.execute(decision)
    print(f"执行结果：{result['outcome']}\n")
    
    # 获取统计
    stats = bench.get_stats()
    print(f"统计信息:")
    print(f"  总任务数：{stats['total_tasks']}")
    print(f"  成功率：{stats['success_rate']:.2%}")
    print(f"  平均执行时间：{stats['avg_execution_time']:.3f}s")
    print(f"  错误恢复次数：{stats['error_recovery_count']}\n")
    
    # 获取执行报告
    report = bench.get_execution_report()
    print(f"执行报告：{json.dumps(report, indent=2, ensure_ascii=False)[:500]}...")
