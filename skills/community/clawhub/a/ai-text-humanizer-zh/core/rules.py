#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rule loading and merging for AI text detection and rewriting."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# 默认规则文件路径
DEFAULT_RULES_FILE = Path(__file__).parent.parent / "resources" / "zh_rules.json"


class RuleSet:
    """Container for all detection and rewriting rules."""
    
    def __init__(self, rules_data: Dict[str, Any]):
        self.data = rules_data
    
    @property
    def replacements(self) -> Dict[str, str]:
        """替换规则：短语 -> 替换文本"""
        return self.data.get("replacements", {})
    
    @property
    def sentence_patterns(self) -> List[Dict[str, str]]:
        """句子级改写模式列表"""
        return self.data.get("sentence_patterns", [])
    
    @property
    def ai_jargon(self) -> List[str]:
        """AI 高频词汇列表"""
        return self.data.get("ai_jargon", [])
    
    @property
    def puffery_phrases(self) -> List[str]:
        """夸大性短语"""
        return self.data.get("puffery_phrases", [])
    
    @property
    def marketing_speak(self) -> List[str]:
        """宣传性语言"""
        return self.data.get("marketing_speak", [])
    
    @property
    def vague_attributions(self) -> List[str]:
        """模糊归因"""
        return self.data.get("vague_attributions", [])
    
    @property
    def hedging_phrases(self) -> List[str]:
        """模棱两可表达"""
        return self.data.get("hedging_phrases", [])
    
    @property
    def chatbot_artifacts(self) -> List[str]:
        """聊天机器人痕迹"""
        return self.data.get("chatbot_artifacts", [])
    
    @property
    def citation_bugs(self) -> List[str]:
        """引用痕迹"""
        return self.data.get("citation_bugs", [])
    
    @property
    def knowledge_cutoff(self) -> List[str]:
        """知识截止表述"""
        return self.data.get("knowledge_cutoff", [])
    
    @property
    def markdown_artifacts(self) -> List[str]:
        """Markdown 痕迹"""
        return self.data.get("markdown_artifacts", [])
    
    @property
    def negative_parallelisms(self) -> List[str]:
        """否定平行结构"""
        return self.data.get("negative_parallelisms", [])
    
    @property
    def superficial_verbs(self) -> List[str]:
        """肤浅动词"""
        return self.data.get("superficial_verbs", [])
    
    @property
    def filler_phrases(self) -> List[str]:
        """填充短语"""
        return self.data.get("filler_phrases", [])
    
    @property
    def rule_of_three_patterns(self) -> List[str]:
        """三点式结构"""
        return self.data.get("rule_of_three_patterns", [])
    
    @property
    def list_markers(self) -> List[str]:
        """列表标记"""
        return self.data.get("list_markers", [])
    
    @property
    def punctuation(self) -> Dict[str, int]:
        """标点阈值配置"""
        return self.data.get("punctuation", {})
    
    @property
    def rhetorical_patterns(self) -> List[str]:
        """反问句模式"""
        return self.data.get("rhetorical_patterns", [])
    
    @property
    def sentence_starters(self) -> List[str]:
        """句首连接词"""
        return self.data.get("sentence_starters", [])


def load_rules(file_path: Union[str, Path] = None) -> RuleSet:
    """加载规则文件，返回 RuleSet 实例。"""
    path = Path(file_path) if file_path else DEFAULT_RULES_FILE
    if not path.exists():
        raise FileNotFoundError(f"Rules file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return RuleSet(data)


def merge_rules(base: RuleSet, user_rules: Dict[str, Any]) -> RuleSet:
    """合并用户自定义规则到基础规则集。"""
    merged = base.data.copy()
    for key, value in user_rules.items():
        if key in merged:
            if isinstance(merged[key], list) and isinstance(value, list):
                if value == []:
                    merged[key] = []
                else:
                    merged[key].extend(value)
            elif isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
        else:
            merged[key] = value
    return RuleSet(merged)


def load_rules_with_user(user_rules_path: Optional[Union[str, Path]] = None) -> RuleSet:
    """加载默认规则，并可选地合并用户提供的规则文件。"""
    base = load_rules()
    if user_rules_path:
        with open(user_rules_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
        return merge_rules(base, user_data)
    return base
