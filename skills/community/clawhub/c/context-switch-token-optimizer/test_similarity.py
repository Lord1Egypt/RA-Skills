#!/usr/bin/env python3
"""
测试相关度计算和上下文切换效果
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from context_manager import ContextManager, TopicSummary

def test_similarity_calculation():
    """测试相关度计算"""
    print("=" * 80)
    print("测试相关度计算")
    print("=" * 80)
    
    manager = ContextManager()
    
    # 从状态文件中读取历史主题
    state_file = Path("memory/context_switch_state.json")
    if state_file.exists():
        with open(state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        topic_history = []
        for topic_data in state_data.get('topic_history', []):
            topic_history.append(TopicSummary(
                topic=topic_data['topic'],
                keywords=topic_data['keywords'],
                timestamp=datetime.fromisoformat(topic_data['timestamp']),
                tokens_used=topic_data['tokens_used'],
                content_snippet=topic_data['content_snippet'],
                is_compressed=topic_data.get('is_compressed', False)
            ))
        
        print(f"\n历史主题数量: {len(topic_history)}")
        print("\n相关度计算列表:")
        print("-" * 80)
        
        # 计算相邻主题之间的相似度
        for i in range(len(topic_history) - 1):
            topic1 = topic_history[i]
            topic2 = topic_history[i + 1]
            
            similarity = manager.calculate_topic_similarity(topic1, topic2)
            action = manager.get_context_action(topic2)
            
            print(f"\n[{i+1} -> {i+2}]")
            print(f"  主题1: {topic1.topic}")
            print(f"  关键词1: {topic1.keywords}")
            print(f"  主题2: {topic2.topic}")
            print(f"  关键词2: {topic2.keywords}")
            print(f"  相似度: {similarity:.4f}")
            print(f"  动作: {action}")
            print(f"  时间差: {(topic2.timestamp - topic1.timestamp).total_seconds():.2f}秒")
            
            # 显示相似度阈值
            sim_threshold = manager.config['context_switch']['similarity_threshold']
            continuity_threshold = manager.config['context_switch'].get('continuity_threshold', 0.35)
            print(f"  阈值: continuous>={sim_threshold}, drift_compress=[{continuity_threshold}, {sim_threshold}), switch<{continuity_threshold}")
        
        # 检查压缩状态
        print("\n" + "=" * 80)
        print("压缩状态检查")
        print("=" * 80)
        compressed_count = sum(1 for t in topic_history if t.is_compressed)
        print(f"已压缩主题数: {compressed_count}/{len(topic_history)}")
        
        if compressed_count > 0:
            print("\n已压缩的主题:")
            for i, topic in enumerate(topic_history):
                if topic.is_compressed:
                    print(f"  [{i+1}] {topic.topic}: {topic.content_snippet}")
        else:
            print("\n暂无压缩的主题")
    else:
        print("状态文件不存在")

def test_context_switch():
    """测试上下文切换效果"""
    print("\n" + "=" * 80)
    print("测试上下文切换效果")
    print("=" * 80)
    
    manager = ContextManager()
    
    # 测试几个新的对话内容
    test_conversations = [
        "检查context-switch-token-optimizer技能是否生效",
        "查看相关度计算列表",
        "检查上下文切换和压缩效果",
        "记忆管理技能的设计和实现",
        "今天天气很好，我们去公园吧"
    ]
    
    print("\n处理新对话内容:")
    print("-" * 80)
    
    for i, content in enumerate(test_conversations, 1):
        print(f"\n[{i}] 输入: {content}")
        result = manager.manage_context(content)
        
        print(f"  动作: {result.get('action', 'unknown')}")
        print(f"  主题: {result.get('topic') or result.get('new_topic', 'unknown')}")
        print(f"  关键词: {result.get('keywords', [])}")
        
        if 'continuity_score' in result:
            print(f"  连续性分数: {result['continuity_score']:.4f}")
        
        if 'compressed_count' in result:
            print(f"  压缩数量: {result['compressed_count']}")
        
        if 'previous_topic' in result:
            print(f"  前一个主题: {result['previous_topic']}")
    
    # 显示最终状态
    print("\n" + "=" * 80)
    print("最终状态")
    print("=" * 80)
    print(f"当前主题: {manager.state.current_topic}")
    print(f"主题历史数: {len(manager.state.topic_history)}")
    print(f"切换次数: {manager.state.switch_count}")
    print(f"总Token: {manager.state.total_tokens}")

if __name__ == "__main__":
    test_similarity_calculation()
    test_context_switch()
