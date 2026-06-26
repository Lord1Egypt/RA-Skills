#!/usr/bin/env python3
"""
Token优化器 - 负责Token使用监控和优化
"""

import json
import re
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from context_manager import ContextManager, TopicSummary

@dataclass
class TokenUsage:
    """Token使用记录"""
    timestamp: datetime
    tokens_used: int
    context_action: str
    topic: str
    memory_loaded: bool

class TokenOptimizer:
    """Token优化器（与 ContextManager 共用同一份 load_skill_config 结果）"""
    
    def __init__(
        self,
        config_file: Optional[str] = None,
        context_manager: Optional[ContextManager] = None,
    ):
        if context_manager is not None:
            self.context_manager = context_manager
            self.config = context_manager.config
        else:
            self.context_manager = ContextManager(config_file)
            self.config = self.context_manager.config
        self.usage_log = []
        self.optimization_log = []
    
    def monitor_token_usage(self, current_tokens: int) -> Dict:
        """监控Token使用情况"""
        token_limit = self.config['token_optimization']['token_limit']
        compression_threshold = self.config['token_optimization']['compression_threshold']
        
        usage_percentage = (current_tokens / token_limit) * 100
        
        monitoring_result = {
            'current_tokens': current_tokens,
            'token_limit': token_limit,
            'usage_percentage': usage_percentage,
            'compression_threshold': compression_threshold,
            'remaining_tokens': token_limit - current_tokens,
            'status': self._get_usage_status(usage_percentage),
            'context_state': self.context_manager.state.current_topic,
            'switch_count': self.context_manager.state.switch_count,
            'last_optimization': self._get_last_optimization_time()
        }
        
        # 记录使用情况
        self._record_token_usage(current_tokens, monitoring_result['status'])
        
        # 检查是否需要优化（TOKEN_OPTIMIZER_ENABLED=false 时跳过）
        enabled = self.config.get("token_optimization", {}).get("enabled", True)
        if enabled and usage_percentage > 70:
            optimization_action = self.trigger_optimization(monitoring_result)
            monitoring_result["optimization_triggered"] = optimization_action
        
        return monitoring_result
    
    def _get_usage_status(self, usage_percentage: float) -> str:
        """获取使用状态"""
        if usage_percentage < 50:
            return "healthy"
        elif usage_percentage < 70:
            return "warning"
        elif usage_percentage < 90:
            return "critical"
        else:
            return "emergency"
    
    def _record_token_usage(self, tokens: int, status: str):
        """记录Token使用情况"""
        usage_record = TokenUsage(
            timestamp=datetime.now(),
            tokens_used=tokens,
            context_action=self.context_manager.state.current_topic or "unknown",
            topic=self.context_manager.state.current_topic or "unknown",
            memory_loaded=bool(self.context_manager.state.memory_context)
        )
        
        self.usage_log.append(usage_record)
        
        # 限制历史记录大小
        max_history = self.config['token_optimization']['max_history_size']
        if len(self.usage_log) > max_history:
            self.usage_log = self.usage_log[-max_history:]
    
    def _get_last_optimization_time(self) -> Optional[datetime]:
        """获取最后优化时间"""
        if not self.optimization_log:
            return None
        
        last_optimization = self.optimization_log[-1]
        return datetime.fromisoformat(last_optimization['timestamp'])
    
    def trigger_optimization(self, current_status: Dict) -> Dict:
        """触发优化"""
        optimization_action = self._determine_optimization_action(current_status)
        
        # 执行优化
        if optimization_action['action'] == 'compress_context':
            result = self._compress_context()
        elif optimization_action['action'] == 'cleanup_memory':
            result = self._cleanup_memory()
        elif optimization_action['action'] == 'reset_context':
            result = self._reset_context()
        else:
            result = {'action': 'no_action', 'reason': '无需优化'}
        
        tokens_after = self._estimate_current_tokens()
        tokens_savings = max(0, current_status['current_tokens'] - int(tokens_after))

        # 记录优化
        optimization_record = {
            'timestamp': datetime.now().isoformat(),
            'trigger_reason': current_status['status'],
            'action_taken': optimization_action['action'],
            'result': result,
            'tokens_before': current_status['current_tokens'],
            'tokens_after': tokens_after,
            'tokens_savings': tokens_savings
        }
        
        self.optimization_log.append(optimization_record)
        
        return optimization_record
    
    def _determine_optimization_action(self, current_status: Dict) -> Dict:
        """确定优化动作"""
        usage_percentage = current_status['usage_percentage']
        
        if usage_percentage > 90:
            return {
                'action': 'reset_context',
                'priority': 'high',
                'reason': f'使用率过高 ({usage_percentage:.1f}%)，需要完全重置上下文'
            }
        elif usage_percentage > 75:
            return {
                'action': 'compress_context',
                'priority': 'medium',
                'reason': f'使用率较高 ({usage_percentage:.1f}%)，需要压缩上下文'
            }
        elif usage_percentage > 65:
            return {
                'action': 'cleanup_memory',
                'priority': 'low',
                'reason': f'使用率中等 ({usage_percentage:.1f}%)，可以清理部分记忆'
            }
        else:
            return {
                'action': 'no_action',
                'priority': 'low',
                'reason': '使用率在正常范围内，无需优化'
            }
    
    def _compress_context(self) -> Dict:
        """压缩上下文"""
        original_history = len(self.context_manager.state.topic_history)
        
        # 保留最近的5个主题历史
        max_history = min(5, self.context_manager.config['context_switch']['max_topic_history'])
        self.context_manager.state.topic_history = self.context_manager.state.topic_history[-max_history:]
        
        # 清理详细记忆，只保留摘要
        if self.context_manager.state.memory_context:
            memory_context = self.context_manager.state.memory_context
            if 'core_content' in memory_context:
                # 只保留核心内容的前50%
                original_length = len(memory_context['core_content'])
                memory_context['core_content'] = memory_context['core_content'][:original_length//2]
        
        # 更新切换时间
        self.context_manager.state.last_switch_time = datetime.now()
        
        # 保存状态
        self.context_manager.save_context_state()
        
        return {
            'action': 'compress_context',
            'original_history_size': original_history,
            'compressed_history_size': len(self.context_manager.state.topic_history),
            'memory_compressed': bool(self.context_manager.state.memory_context),
            'token_savings': self._estimate_token_savings()
        }
    
    def _cleanup_memory(self) -> Dict:
        """清理记忆"""
        cleaned_count = 0
        
        if self.context_manager.state.memory_context:
            # 清理超过24小时的记忆
            current_time = datetime.now()
            memory_age = current_time - datetime.fromisoformat(self.context_manager.state.memory_context['loaded_at'])
            
            if memory_age.total_seconds() > 86400:  # 24小时
                self.context_manager.state.memory_context = None
                cleaned_count += 1
        
        # 清理超过1周的使用记录
        original_usage_count = len(self.usage_log)
        self.usage_log = [
            usage for usage in self.usage_log 
            if (datetime.now() - usage.timestamp).total_seconds() < 604800  # 7天
        ]
        usage_records_cleaned = original_usage_count - len(self.usage_log)
        
        # 保存状态
        self.context_manager.save_context_state()
        
        return {
            'action': 'cleanup_memory',
            'memories_cleaned': cleaned_count,
            'usage_records_cleaned': usage_records_cleaned,
            'token_savings': self._estimate_token_savings()
        }
    
    def _reset_context(self) -> Dict:
        """重置上下文"""
        original_state = {
            'topic': self.context_manager.state.current_topic,
            'history_size': len(self.context_manager.state.topic_history),
            'memory_loaded': bool(self.context_manager.state.memory_context),
            'switch_count': self.context_manager.state.switch_count
        }
        
        # 重置上下文状态
        self.context_manager.state = self.context_manager._load_context_state()
        
        return {
            'action': 'reset_context',
            'original_state': original_state,
            'memory_cleared': True,
            'context_cleared': True,
            'token_savings': self._estimate_token_savings()
        }
    
    def _estimate_current_tokens(self) -> int:
        """估算当前Token使用"""
        # 基础Token使用
        base_tokens = 1000
        
        # 主题历史Token
        history_tokens = sum(topic.tokens_used for topic in self.context_manager.state.topic_history)
        
        # 记忆上下文Token
        memory_tokens = 0
        if self.context_manager.state.memory_context:
            memory_content = self.context_manager.state.memory_context.get('core_content', '')
            memory_tokens = len(memory_content) // 0.75  # 中文字符估算
        
        return base_tokens + history_tokens + memory_tokens
    
    def _estimate_token_savings(self) -> int:
        """估算节省的Token"""
        return int(self._estimate_current_tokens() * 0.3)  # 估算节省30%
    
    def generate_optimization_report(self) -> Dict:
        """生成优化报告"""
        if not self.optimization_log:
            return {'message': '暂无优化记录'}
        
        # 统计优化情况
        total_optimizations = len(self.optimization_log)
        compression_count = sum(1 for log in self.optimization_log if log['action_taken'] == 'compress_context')
        cleanup_count = sum(1 for log in self.optimization_log if log['action_taken'] == 'cleanup_memory')
        reset_count = sum(1 for log in self.optimization_log if log['action_taken'] == 'reset_context')
        
        # 计算总节省（兼容旧记录可能无 tokens_savings）
        total_savings = sum(log.get('tokens_savings', 0) for log in self.optimization_log)
        
        # 最近优化
        recent_optimization = self.optimization_log[-1] if self.optimization_log else None
        
        return {
            'report_generated': datetime.now().isoformat(),
            'total_optimizations': total_optimizations,
            'optimization_breakdown': {
                'compressions': compression_count,
                'cleanups': cleanup_count,
                'resets': reset_count
            },
            'total_tokens_saved': total_savings,
            'average_tokens_per_optimization': total_savings / total_optimizations if total_optimizations > 0 else 0,
            'recent_optimization': recent_optimization,
            'current_context': self.context_manager.state.current_topic,
            'current_token_usage': self._estimate_current_tokens()
        }
    
    def get_optimization_suggestions(self) -> List[Dict]:
        """获取优化建议"""
        suggestions = []
        
        current_tokens = self._estimate_current_tokens()
        usage_percentage = (current_tokens / self.config['token_optimization']['token_limit']) * 100
        
        # 1. 基于使用率的建议
        if usage_percentage > 80:
            suggestions.append({
                'priority': 'high',
                'type': 'usage',
                'suggestion': 'Token使用率过高，建议立即优化上下文',
                'action': 'trigger_compression'
            })
        
        # 2. 基于主题历史的建议
        if len(self.context_manager.state.topic_history) > 10:
            suggestions.append({
                'priority': 'medium',
                'type': 'history',
                'suggestion': '主题历史过多，可以清理较旧的记录',
                'action': 'cleanup_history'
            })
        
        # 3. 基于记忆的建议
        if self.context_manager.state.memory_context:
            memory_age = datetime.now() - datetime.fromisoformat(self.context_manager.state.memory_context['loaded_at'])
            if memory_age.total_seconds() > 86400:  # 24小时
                suggestions.append({
                    'priority': 'low',
                    'type': 'memory',
                    'suggestion': '记忆上下文较旧，可以更新或清理',
                    'action': 'refresh_memory'
                })
        
        # 4. 基于切换频率的建议
        if self.context_manager.state.switch_count > 20:
            suggestions.append({
                'priority': 'medium',
                'type': 'switching',
                'suggestion': '主题切换过于频繁，可能导致上下文不稳定',
                'action': 'stabilize_context'
            })
        
        return suggestions

def main():
    """测试Token优化器"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Token优化器测试工具')
    parser.add_argument('--monitor', action='store_true', help='监控Token使用')
    parser.add_argument('--trigger-optimization', action='store_true', help='触发优化')
    parser.add_argument('--report', action='store_true', help='生成优化报告')
    parser.add_argument('--suggestions', action='store_true', help='获取优化建议')
    parser.add_argument('--test-usage', type=int, help='测试Token使用量')
    
    args = parser.parse_args()
    
    optimizer = TokenOptimizer()
    
    if args.test_usage:
        # 测试特定Token使用量
        result = optimizer.monitor_token_usage(args.test_usage)
        print(f"Token使用测试 ({args.test_usage} tokens):")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.monitor:
        # 监控当前Token使用
        current_tokens = optimizer._estimate_current_tokens()
        result = optimizer.monitor_token_usage(current_tokens)
        print("=== Token监控结果 ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.trigger_optimization:
        # 触发优化
        current_tokens = optimizer._estimate_current_tokens()
        current_status = {
            'current_tokens': current_tokens,
            'usage_percentage': (current_tokens / optimizer.config['token_optimization']['token_limit']) * 100,
            'status': optimizer._get_usage_status((current_tokens / optimizer.config['token_optimization']['token_limit']) * 100)
        }
        
        optimization_result = optimizer.trigger_optimization(current_status)
        print("=== 优化结果 ===")
        print(json.dumps(optimization_result, indent=2, ensure_ascii=False))
    
    if args.report:
        # 生成优化报告
        report = optimizer.generate_optimization_report()
        print("=== 优化报告 ===")
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    if args.suggestions:
        # 获取优化建议
        suggestions = optimizer.get_optimization_suggestions()
        print("=== 优化建议 ===")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. [{suggestion['priority'].upper()}] {suggestion['suggestion']}")
            print(f"   类型: {suggestion['type']}")
            print(f"   建议: {suggestion['action']}")
            print()

if __name__ == "__main__":
    main()