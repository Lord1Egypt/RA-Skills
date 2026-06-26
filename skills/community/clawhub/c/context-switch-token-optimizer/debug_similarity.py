#!/usr/bin/env python3
"""
调试相似度计算问题
"""

import sys
import json
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from context_manager import ContextManager, TopicSummary

# 加载配置
config_file = current_dir / "config.json"
manager = ContextManager(str(config_file))

print("配置加载成功")
print(f"相似度阈值: {manager.config['context_switch']['similarity_threshold']}")
print(f"连续性阈值: {manager.config['context_switch'].get('continuity_threshold', 0.35)}")
print(f"Token优化启用: {manager.config['token_optimization'].get('enabled', True)}")

# 测试特定案例
print("\n测试相似度计算:")
topic1 = TopicSummary(
    topic="查看相关度计算列表相关",
    keywords=["查看相关度计算列表"],
    timestamp=datetime.now(),
    tokens_used=12,
    content_snippet="查看相关度计算列表",
    is_compressed=False
)

topic2 = TopicSummary(
    topic="上下文管理相关",
    keywords=["检查上下文切换和压缩效果"],
    timestamp=datetime.now(),
    tokens_used=16,
    content_snippet="检查上下文切换和压缩效果",
    is_compressed=False
)

similarity = manager.calculate_topic_similarity(topic1, topic2)
action = manager.get_context_action(topic2)

print(f"主题1: {topic1.topic}")
print(f"主题2: {topic2.topic}")
print(f"相似度: {similarity:.4f}")
print(f"动作: {action}")

# 判断应该的动作
sim_threshold = manager.config['context_switch']['similarity_threshold']
continuity_threshold = manager.config['context_switch'].get('continuity_threshold', 0.35)

if similarity >= sim_threshold:
    expected_action = "continuous"
elif similarity < continuity_threshold:
    expected_action = "switch"
else:
    expected_action = "drift_compress"

print(f"应该的动作: {expected_action}")

if action != expected_action:
    print(f"\n⚠️  问题：动作不匹配！")
    print(f"  相似度: {similarity:.4f}")
    print(f"  阈值范围: continuous>={sim_threshold}, drift_compress=[{continuity_threshold}, {sim_threshold}), switch<{continuity_threshold}")
    print(f"  实际动作: {action}")
    print(f"  期望动作: {expected_action}")