#!/usr/bin/env python3
"""
Context Switch Token Optimizer - 主入口工具
集成上下文管理和Token优化的完整解决方案
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from context_manager import ContextManager
from token_optimizer import TokenOptimizer

class ContextSwitchTokenOptimizer:
    """上下文切换和Token优化器主类"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.context_manager = ContextManager(config_file)
        self.token_optimizer = TokenOptimizer(context_manager=self.context_manager)
        
    def process_conversation(self, conversation_content: str) -> Dict:
        """处理对话内容"""
        print(f"处理对话内容: {conversation_content[:50]}...")
        
        # 1. 管理上下文
        context_result = self.context_manager.manage_context(conversation_content)
        
        # 2. 监控Token使用
        current_tokens = self.token_optimizer._estimate_current_tokens()
        token_monitoring = self.token_optimizer.monitor_token_usage(current_tokens)
        
        # 3. 如果需要，触发优化
        optimization_result = None
        if token_monitoring.get('optimization_triggered'):
            optimization_result = token_monitoring['optimization_triggered']
        
        # 4. 合并结果
        result = {
            'timestamp': self.context_manager.state.topic_history[-1].timestamp.isoformat() if self.context_manager.state.topic_history else None,
            'context_management': context_result,
            'token_monitoring': token_monitoring,
            'optimization_triggered': optimization_result,
            'summary': self._generate_summary(context_result, token_monitoring)
        }
        
        return result
    
    def _generate_summary(self, context_result: Dict, token_monitoring: Dict) -> str:
        """生成处理摘要"""
        action = context_result.get('action', 'unknown')
        topic = context_result.get('topic') or context_result.get('new_topic', 'unknown')
        token_status = token_monitoring.get('status', 'unknown')
        
        if action == 'switch_context':
            return f"主题切换: {topic} (Token状态: {token_status})"
        elif action == 'drift_compress':
            compressed = context_result.get('compressed_count', 0)
            return f"渐变漂移(已压缩{compressed}轮): {topic} (Token状态: {token_status})"
        elif action == 'continuous_context':
            return f"保持连续: {topic} (Token状态: {token_status})"
        else:
            return f"处理完成: {topic} (Token状态: {token_status})"
    
    def generate_status_report(self) -> Dict:
        """生成状态报告"""
        # 1. 获取上下文状态
        context_state = {
            'current_topic': self.context_manager.state.current_topic,
            'topic_history_count': len(self.context_manager.state.topic_history),
            'switch_count': self.context_manager.state.switch_count,
            'memory_loaded': bool(self.context_manager.state.memory_context),
            'last_switch_time': self.context_manager.state.last_switch_time.isoformat() if self.context_manager.state.last_switch_time else None
        }
        
        # 2. 获取Token状态
        current_tokens = self.token_optimizer._estimate_current_tokens()
        token_status = self.token_optimizer.monitor_token_usage(current_tokens)
        
        # 3. 获取优化报告
        optimization_report = self.token_optimizer.generate_optimization_report()
        
        # 4. 获取优化建议
        suggestions = self.token_optimizer.get_optimization_suggestions()
        
        return {
            'report_generated': '2026-03-17T11:00:00',
            'context_state': context_state,
            'token_status': token_status,
            'optimization_report': optimization_report,
            'optimization_suggestions': suggestions,
            'health_score': self._calculate_health_score(token_status, suggestions)
        }
    
    def _calculate_health_score(self, token_status: Dict, suggestions: List[Dict]) -> int:
        """计算健康分数 (0-100)"""
        score = 100
        
        # 根据Token使用情况扣分
        usage_percentage = token_status.get('usage_percentage', 0)
        if usage_percentage > 90:
            score -= 40
        elif usage_percentage > 80:
            score -= 25
        elif usage_percentage > 70:
            score -= 15
        elif usage_percentage > 60:
            score -= 5
        
        # 根据优化建议扣分
        high_priority_suggestions = [s for s in suggestions if s['priority'] == 'high']
        medium_priority_suggestions = [s for s in suggestions if s['priority'] == 'medium']
        
        score -= len(high_priority_suggestions) * 10
        score -= len(medium_priority_suggestions) * 5
        
        return max(0, score)
    
    def reset_context(self) -> Dict:
        """重置上下文"""
        # 重置上下文管理器
        self.context_manager.state = self.context_manager._load_context_state()
        
        # 生成重置报告
        return {
            'action': 'reset_context',
            'timestamp': '2026-03-17T11:00:00',
            'context_cleared': True,
            'token_optimization_active': True,
            'message': '上下文已重置，可以开始新的对话主题'
        }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Context Switch Token Optimizer')
    parser.add_argument('--process', help='处理对话内容')
    parser.add_argument('--status', action='store_true', help='生成状态报告')
    parser.add_argument('--reset', action='store_true', help='重置上下文')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--test', action='store_true', help='运行测试')
    
    args = parser.parse_args()
    
    optimizer = ContextSwitchTokenOptimizer(args.config)
    
    if args.test:
        # 运行测试
        test_conversations = [
            "记忆管理技能的设计和实现",
            "今天天气很好，我们去公园吧",
            "飞书API权限问题处理",
            "Python编程技巧分享",
            "机器学习算法优化"
        ]
        
        print("=== Context Switch Token Optimizer 测试 ===")
        
        for i, conversation in enumerate(test_conversations, 1):
            print(f"\n测试 {i}: {conversation}")
            result = optimizer.process_conversation(conversation)
            
            print(f"处理摘要: {result['summary']}")
            print(f"Token状态: {result['token_monitoring']['status']}")
            print(f"操作类型: {result['context_management']['action']}")
            
            if result['optimization_triggered']:
                print(f"优化触发: {result['optimization_triggered']['action_taken']}")
        
        # 生成状态报告
        print("\n=== 最终状态报告 ===")
        final_report = optimizer.generate_status_report()
        print(f"健康分数: {final_report['health_score']}/100")
        print(f"当前主题: {final_report['context_state']['current_topic']}")
        print(f"切换次数: {final_report['context_state']['switch_count']}")
        print(f"Token使用: {final_report['token_status']['usage_percentage']:.1f}%")
        
        if final_report['optimization_suggestions']:
            print("\n优化建议:")
            for i, suggestion in enumerate(final_report['optimization_suggestions'], 1):
                print(f"{i}. [{suggestion['priority'].upper()}] {suggestion['suggestion']}")
        
        return
    
    if args.process:
        # 处理指定对话内容
        result = optimizer.process_conversation(args.process)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    if args.status:
        # 生成状态报告
        report = optimizer.generate_status_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    
    if args.reset:
        # 重置上下文
        result = optimizer.reset_context()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # 显示帮助
    parser.print_help()

if __name__ == "__main__":
    main()