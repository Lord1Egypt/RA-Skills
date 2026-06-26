#!/usr/bin/env python3
"""
AI Humanizer CN - 中文 AI 文本优化器 v1.1.0
功能：将 AI 生成的文本优化为更自然的人类写作风格
更新：性能优化 + 新增风格模板
"""

import re
import random
from typing import List, Dict

VERSION = "1.1.0"

class AIHumanizer:
    """中文 AI 文本优化器"""
    
    def __init__(self):
        # 风格模板 v1.1.0 新增
        self.styles = {
            'casual': {
                'connectors': ['然后', '接着', '还有', '另外', '对了'],
                'particles': ['啊', '呢', '吧', '嘛', '哦'],
                'fillers': ['说实话', '讲真的', '怎么说呢', '简单来说'],
            },
            'formal': {
                'connectors': ['此外', '同时', '综上所述', '由此可见', '值得注意的是'],
                'particles': ['的', '了', '是', '为'],
                'fillers': ['具体而言', '换言之', '总的来说', '从某种意义上说'],
            },
            'academic': {
                'connectors': ['因此', '然而', '基于此', '综上所述', '进一步'],
                'particles': ['之', '其', '该', '此'],
                'fillers': ['研究表明', '数据显示', '根据分析', '可以认为'],
            }
        }
        
        # AI 常见表达替换表（性能优化：使用 dict 而非多次 if）
        self.ai_patterns = {
            '首先，': '简单来说，',
            '其次，': '另外，',
            '最后，': '总的来说，',
            '总之，': '所以说，',
            '综上所述，': '总的来说，',
            '值得注意的是，': '要说的是，',
            '需要指出的是，': '得提一下，',
        }
    
    def humanize(self, text: str, style: str = 'casual', intensity: float = 0.5) -> str:
        """
        优化 AI 文本为人类风格
        
        Args:
            text: AI 生成的文本
            style: 风格 (casual/formal/academic)
            intensity: 优化强度 (0.0-1.0)
        
        Returns:
            优化后的文本
        """
        if not text:
            return ""
        
        # 1. 替换 AI 常见表达
        result = self._replace_ai_patterns(text)
        
        # 2. 添加风格化连接词
        style_config = self.styles.get(style, self.styles['casual'])
        result = self._add_connectors(result, style_config, intensity)
        
        # 3. 调整句式（v1.1.0 新增）
        result = self._vary_sentence_structure(result, intensity)
        
        # 4. 添加语气词（v1.1.0 优化）
        result = self._add_particles(result, style_config, intensity)
        
        return result
    
    def _replace_ai_patterns(self, text: str) -> str:
        """替换 AI 常见表达"""
        for ai_expr, human_expr in self.ai_patterns.items():
            text = text.replace(ai_expr, human_expr)
        return text
    
    def _add_connectors(self, text: str, style_config: Dict, intensity: float) -> str:
        """添加连接词"""
        sentences = re.split(r'([。！？])', text)
        result = []
        
        for i, sentence in enumerate(sentences):
            if sentence and len(sentence) > 10 and random.random() < intensity * 0.3:
                connector = random.choice(style_config['connectors'])
                # v1.1.0 优化：避免重复
                if i == 0 or connector not in result[-1] if result else True:
                    result.append(f"{connector}{sentence}")
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return ''.join(result)
    
    def _vary_sentence_structure(self, text: str, intensity: float) -> str:
        """调整句式（v1.1.0 新增）"""
        # 将部分长句拆分为短句
        sentences = text.split('。')
        result = []
        
        for sentence in sentences:
            if len(sentence) > 50 and random.random() < intensity * 0.4:
                # 在逗号处拆分
                parts = sentence.split('，')
                if len(parts) > 2:
                    mid = len(parts) // 2
                    result.append('。'.join(['，'.join(parts[:mid]), '，'.join(parts[mid:])]))
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return '。'.join(result)
    
    def _add_particles(self, text: str, style_config: Dict, intensity: float) -> str:
        """添加语气词"""
        sentences = re.split(r'([。！？])', text)
        result = []
        
        for sentence in sentences:
            if sentence and sentence[-1] in '。！？' and random.random() < intensity * 0.2:
                particle = random.choice(style_config['particles'])
                result.append(f"{sentence[:-1]}{particle}{sentence[-1]}")
            else:
                result.append(sentence)
        
        return ''.join(result)
    
    def batch_humanize(self, texts: List[str], style: str = 'casual', 
                      intensity: float = 0.5) -> List[str]:
        """批量优化（v1.1.0 性能优化）"""
        return [self.humanize(text, style, intensity) for text in texts]


# 单例模式
_humanizer_instance = None

def get_humanizer() -> AIHumanizer:
    """获取单例实例"""
    global _humanizer_instance
    if _humanizer_instance is None:
        _humanizer_instance = AIHumanizer()
    return _humanizer_instance


def humanize_text(text: str, style: str = 'casual', intensity: float = 0.5) -> str:
    """快捷函数"""
    return get_humanizer().humanize(text, style, intensity)


if __name__ == '__main__':
    # 测试
    test_text = "首先，我们需要了解问题的本质。其次，分析各种可能的解决方案。最后，选择最优方案并实施。"
    
    print("原文本：")
    print(test_text)
    print("\n优化后 (casual)：")
    print(humanize_text(test_text, 'casual', 0.7))
    print("\n优化后 (formal)：")
    print(humanize_text(test_text, 'formal', 0.7))
