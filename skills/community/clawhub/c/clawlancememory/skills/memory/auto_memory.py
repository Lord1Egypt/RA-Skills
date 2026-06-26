#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动记忆抽取器
从对话中识别并自动保存重要信息到 LanceDB
"""

import re
import json
from typing import List, Dict, Optional


class AutoMemoryExtractor:
    """自动记忆抽取器"""
    
    def __init__(self, memory_integration):
        """
        初始化抽取器
        
        Args:
            memory_integration: OpenClawMemoryIntegration 实例
        """
        self.memory = memory_integration
        
        # 记忆触发模式（正则表达式）
        self.patterns = {
            "preference": [
                r"我喜欢 (.+)",
                r"我偏好 (.+)",
                r"记住我喜欢 (.+)",
                r"别忘了我喜欢 (.+)",
                r"我习惯 (.+)",
                r"我通常 (.+)",
                r"偏好 (.+)"
            ],
            "fact": [
                r"我是 (.+)",
                r"我负责 (.+)",
                r"我在 (.+) 工作",
                r"我在 (.+) 上班",
                r"记住我是 (.+)",
                r"我擅长 (.+)",
                r"我的工作是 (.+)",
                r"负责 (.+)"
            ],
            "task": [
                r"我需要 (.+)",
                r"我计划 (.+)",
                r"别忘了 (.+)",
                r"提醒我 (.+)",
                r"记得 (.+)",
                r"我要 (.+)",
                r"明天要 (.+)",
                r"下周要 (.+)",
                r"要 (.+)"
            ]
        }
        
        # 忽略词（避免误触发）
        self.ignore_words = [
            "了", "的", "是", "在", "和", "与", "或",
            "吗", "呢", "吧", "啊", "哦", "嗯"
        ]
    
    def extract_from_message(self, message: str) -> List[Dict]:
        """
        从单条消息中提取记忆（简单字符串匹配，兼容 Python 3.6）
        
        Args:
            message: 用户消息
            
        Returns:
            提取的记忆列表
        """
        extracted = []
        
        # 简单关键词匹配（避免 Python 3.6 re 模块中文问题）
        keywords = {
            "preference": ["我喜欢", "我偏好", "我习惯"],
            "fact": ["我负责", "我是", "我擅长", "我在"],
            "task": ["别忘了", "我需要", "提醒我", "记得", "明天要"]
        }
        
        for mem_type, keys in keywords.items():
            for key in keys:
                if key in message:
                    # 提取关键词后面的内容
                    idx = message.index(key)
                    content = message[idx + len(key):].strip()
                    
                    # 过滤太短的内容
                    if len(content) < 2:
                        continue
                    
                    # 过滤句号结尾
                    content = content.rstrip('。！？.!')
                    
                    # 检查是否已存在相似记忆
                    similar = self._check_similar(content, mem_type)
                    if not similar:
                        extracted.append({
                            "content": content,
                            "type": mem_type,
                            "source": message
                        })
                    break  # 每个类型只匹配一次
        
        return extracted
    
    def _check_similar(self, content: str, mem_type: str, threshold: float = 0.8) -> bool:
        """
        检查是否存在相似记忆
        
        Args:
            content: 新内容
            mem_type: 记忆类型
            threshold: 相似度阈值
            
        Returns:
            True 如果存在相似记忆
        """
        # 检索相关记忆
        results = self.memory.search_memory(content, k=5)
        
        for r in results:
            if r["type"] == mem_type:
                # 简单相似度检查（可以升级为向量相似度）
                existing = r["content"]
                similarity = self._text_similarity(content, existing)
                if similarity > threshold:
                    print(f"⚠️ 发现相似记忆：'{content}' ≈ '{existing}' (相似度：{similarity:.2f})")
                    return True
        
        return False
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（简单版本）
        
        Args:
            text1: 文本 1
            text2: 文本 2
            
        Returns:
            相似度 0-1
        """
        # 转为集合
        set1 = set(text1)
        set2 = set(text2)
        
        # Jaccard 相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def save_memories(self, extracted: List[Dict], **kwargs) -> List[str]:
        """
        保存提取的记忆
        
        Args:
            extracted: 提取的记忆列表
            **kwargs: 其他参数（importance, expires_hours 等）
            
        Returns:
            保存的记忆 ID 列表
        """
        saved_ids = []
        
        for mem in extracted:
            memory_id = self.memory.add_memory(
                content=mem["content"],
                type=mem["type"],
                **kwargs
            )
            saved_ids.append(memory_id)
            print(f"✅ 自动保存记忆：[{mem['type']}] {mem['content']}")
        
        return saved_ids
    
    def process_conversation(self, conversation: List[Dict]) -> List[str]:
        """
        处理整个对话，提取并保存记忆
        
        Args:
            conversation: 对话列表
                [{"role": "user", "content": "..."}, ...]
            
        Returns:
            保存的记忆 ID 列表
        """
        all_saved = []
        
        for msg in conversation:
            if msg.get("role") == "user":
                extracted = self.extract_from_message(msg["content"])
                if extracted:
                    saved = self.save_memories(extracted)
                    all_saved.extend(saved)
        
        return all_saved


# 测试
if __name__ == "__main__":
    import sys
    import os
    
    # 添加路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from openclaw_integration import OpenClawMemoryIntegration
    
    print("="*60)
    print("自动记忆抽取器测试")
    print("="*60)
    
    # 初始化
    mem = OpenClawMemoryIntegration(user_id="ou_9c8820c5e5c8af48776988bf363ee0ae")
    extractor = AutoMemoryExtractor(mem)
    
    # 测试消息
    test_messages = [
        "我喜欢早上开会",
        "我负责 POC 项目",
        "别忘了每周四提交周报",
        "我需要买咖啡",
        "我擅长 Python 开发",
        "明天要出差"
    ]
    
    print("\n测试消息处理:")
    for msg in test_messages:
        print(f"\n消息：{msg}")
        extracted = extractor.extract_from_message(msg)
        if extracted:
            for e in extracted:
                print(f"  → 提取：[{e['type']}] {e['content']}")
        else:
            print(f"  → 无记忆提取")
    
    # 测试保存
    print("\n" + "="*60)
    print("测试保存记忆:")
    test_msg = "我喜欢简洁的代码风格"
    print(f"消息：{test_msg}")
    extracted = extractor.extract_from_message(test_msg)
    if extracted:
        extractor.save_memories(extracted)
    
    # 测试对话处理
    print("\n" + "="*60)
    print("测试对话处理:")
    conversation = [
        {"role": "user", "content": "我负责 POC 项目"},
        {"role": "assistant", "content": "好的，我记住了"},
        {"role": "user", "content": "每周四要提交 OKR 周报"},
        {"role": "assistant", "content": "明白了"},
        {"role": "user", "content": "我喜欢简洁的汇报风格"}
    ]
    
    saved_ids = extractor.process_conversation(conversation)
    print(f"\n共保存 {len(saved_ids)} 条记忆")
    
    print("\n✅ 自动记忆抽取器测试完成！")
