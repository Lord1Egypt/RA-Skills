#!/usr/bin/env python3
"""
增强版事实提取器 - 支持分类、评级、重要事实识别
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple
from agent_mem.memory.config import CATEGORIES, RATING_RULES, IMPORTANT_FACT_SIGNALS

class EnhancedFactExtractor:
    def __init__(self):
        self.categories = CATEGORIES
        self.rating_rules = RATING_RULES
        self.important_signals = IMPORTANT_FACT_SIGNALS
        
    def classify_fact(self, text: str) -> str:
        """识别事实类别"""
        text_lower = text.lower()
        
        for category_id, category in self.categories.items():
            for keyword in category.get("keywords", []):
                if keyword.lower() in text_lower:
                    return category_id
        
        return "general"
    
    def rate_importance(self, text: str, category: str) -> int:
        """根据评级规则计算重要性分数"""
        max_score = 0
        
        # 按优先级检查各规则
        priority_order = [
            "system_structure_change",  # 10分
            "important_project",         # 8分  
            "repeated_question",         # 8分
            "verbal_important",           # 7分
            "preference",                # 7分
            "problem_solved",            # 6分
        ]
        
        for rule_key in priority_order:
            rule = self.rating_rules.get(rule_key, {})
            patterns = rule.get("patterns", [])
            
            for pattern in patterns:
                if re.search(pattern, text):
                    score = rule.get("score", 3)
                    max_score = max(max_score, score)
                    break  # 找到匹配就停止，避免被低分覆盖
        
        # 如果没有匹配，按类别基础分
        if max_score == 0:
            if category == "system_change":
                max_score = 8
            elif category == "preference":
                max_score = 6
            elif category == "insight":
                max_score = 5
            else:
                max_score = 3
                
        return max_score
    
    def is_important_fact(self, text: str) -> Tuple[bool, str]:
        """
        判断是否重要事实
        返回: (是否重要, 原因)
        """
        text_lower = text.lower()
        
        # 检查高频信号
        for signal in self.important_signals.get("high_frequency", []):
            if signal in text_lower:
                return True, f"高频信号: {signal}"
        
        # 检查系统变更
        for signal in self.important_signals.get("system_change", []):
            if signal in text_lower:
                return True, f"系统变更: {signal}"
        
        # 检查重点项目
        for signal in self.important_signals.get("important_project", []):
            if signal in text_lower:
                return True, f"重点项目: {signal}"
        
        # 检查偏好
        for signal in self.important_signals.get("preference", []):
            if signal in text_lower:
                return True, f"偏好信号: {signal}"
        
        # 检查决策
        for signal in self.important_signals.get("decision", []):
            if signal in text_lower:
                return True, f"决策信号: {signal}"
        
        return False, ""
    
    def extract_facts(self, content: str, source_file: str) -> List[Dict]:
        """从内容中提取所有事实"""
        facts = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) < 5:  # 跳过太短的行
                continue
                
            # 判断是否重要事实
            is_important, reason = self.is_important_fact(line)
            
            # 分类
            category = self.classify_fact(line)
            
            # 评级
            importance = self.rate_importance(line, category)
            
            # 提取实体
            entities = self.extract_entities_from_line(line)
            
            fact = {
                'text': line,
                'category': category,
                'importance': importance,
                'is_important': is_important,
                'important_reason': reason,
                'entities': entities,
                'source': source_file,
                'line': i + 1,
                'timestamp': datetime.now().isoformat()
            }
            facts.append(fact)
        
        return facts
    
    def extract_entities_from_line(self, line: str) -> List[str]:
        """从行中提取实体"""
        entities = []
        
        # 代码块中的内容
        code_matches = re.findall(r'`([^`]+)`', line)
        entities.extend(code_matches)
        
        # 加粗文本
        bold_matches = re.findall(r'\*\*([^*]+)\*\*', line)
        entities.extend(bold_matches)
        
        # Agent名称
        agent_matches = re.findall(r'[A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)*', line)
        entities.extend([a for a in agent_matches if '-' in a])
        
        return list(set(entities))

    def summarize_daily(self, facts: List[Dict], date: str) -> str:
        """生成每日摘要"""
        # 按重要性排序
        sorted_facts = sorted(facts, key=lambda x: -x['importance'])
        
        # 只取重要的
        important = [f for f in sorted_facts if f['is_important']][:10]
        
        if not important:
            return f"📅 {date} 记忆摘要\n\n无重要事项记录。"
        
        summary = f"""📅 {date} 记忆摘要

⭐ 重要事实 ({len(important)}条)：

"""
        for fact in important:
            cat_name = self.categories.get(fact['category'], {}).get('name', '📝 一般')
            summary += f"[{fact['importance']}/10] {cat_name}\n"
            summary += f"   {fact['text'][:100]}"
            if fact['important_reason']:
                summary += f" ({fact['important_reason']})"
            summary += "\n\n"
        
        return summary


if __name__ == '__main__':
    # 测试
    extractor = EnhancedFactExtractor()
    
    test_content = """
用户说喜欢用GLM模型
反复问关于Agent配置的问题
新增了code-architect Agent
公众号今天发文了
决定使用飞书知识库
系统升级了OpenClaw
这个问题之前已经解决过了
"""
    
    facts = extractor.extract_facts(test_content, "test.md")
    
    for f in facts:
        print(f"[{f['importance']}] [{f['category']}] {'⭐' if f['is_important'] else ''} {f['text'][:60]}")
        if f['important_reason']:
            print(f"    原因: {f['important_reason']}")
