#!/usr/bin/env python3
"""
RuleEngine - 集成 177 条高价值规则
Layer 2: 规则匹配，作为增强检测层
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class RuleMatch:
    """规则匹配结果"""
    rule_id: str
    rule_name: str
    category: str
    severity: str
    pattern: str
    confidence: int  # 1-100
    description: str = ""


class RuleEngine:
    """
    规则引擎 - 集成清洗后的高价值规则 (~177 条)
    
    特点:
    - 支持 JSON 规则格式
    - 正则预编译
    - 按分类/严重程度过滤
    - 规则缓存 (24小时)
    """
    
    def __init__(self, rules_file: Optional[Path] = None, load_semgrep: bool = True):
        if rules_file is None:
            # 默认从 v5.7.0 加载清洗后的规则
            # __file__ = v6.0.0/src/engines/rule_engine.py
            # parent.parent.parent = v6.0.0/
            # parent.parent.parent.parent = release/
            self.rules_file = Path(__file__).parent.parent.parent.parent / 'v5.7.0' / 'src' / 'rules' / 'cleaned' / 'high_value_rules.json'
        else:
            self.rules_file = Path(rules_file)
        
        self.rules: List[Dict] = []
        self.compiled: Dict[str, Dict] = {}
        self.stats: Dict = {}
        self.semgrep_rules: List[Dict] = []
        
        self.load()
        
        # 加载 Semgrep AI 规则
        if load_semgrep:
            self._load_semgrep_rules()
    
    def load(self) -> bool:
        """加载规则"""
        if not self.rules_file.exists():
            print(f"❌ 规则文件不存在: {self.rules_file}")
            return False
        
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.rules = data.get('rules', [])
            self.stats = data.get('stats', {})
            
            print(f"✅ 加载 {len(self.rules)} 条规则")
            
            # 预编译正则
            self._compile()
            return True
            
        except Exception as e:
            print(f"❌ 加载规则失败: {e}")
            return False
    
    def _compile(self):
        """预编译所有正则表达式"""
        for rule in self.rules:
            rule_id = rule.get('id', rule.get('name', ''))
            
            patterns = rule.get('patterns', [])
            compiled_patterns = []
            
            for pattern in patterns:
                try:
                    compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
                except re.error:
                    # 无效正则，当作普通字符串
                    compiled_patterns.append(pattern)
            
            # 严重程度转置信度
            severity = rule.get('severity', 'medium').lower()
            confidence_map = {
                'critical': 95,
                'high': 80,
                'medium': 60,
                'low': 40
            }
            
            self.compiled[rule_id] = {
                'rule': rule,
                'patterns': compiled_patterns,
                'category': rule.get('category', 'unknown'),
                'severity': severity,
                'confidence': confidence_map.get(severity, 50),
                'description': rule.get('description', '')
            }
        
        print(f"✅ 预编译 {len(self.compiled)} 条规则")
    
    def _load_semgrep_rules(self):
        """加载 Semgrep AI 规则"""
        # Semgrep rules 文件路径
        semgrep_file = Path(__file__).parent.parent.parent / 'rules' / 'semgrep_ai_rules.json'
        
        if not semgrep_file.exists():
            print(f"⚠️  Semgrep AI 规则文件不存在：{semgrep_file}")
            return
        
        try:
            with open(semgrep_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.semgrep_rules = data.get('rules', [])
            
            # 将 Semgrep 规则添加到 compiled
            for rule in self.semgrep_rules:
                rule_id = rule.get('id', 'UNKNOWN')
                category = rule.get('category', 'unknown')
                confidence = rule.get('confidence', 70)
                patterns = rule.get('patterns', [])
                
                compiled_patterns = []
                for pattern in patterns:
                    try:
                        compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
                    except re.error:
                        compiled_patterns.append(pattern)
                
                self.compiled[rule_id] = {
                    'rule': rule,
                    'patterns': compiled_patterns,
                    'category': category,
                    'severity': rule.get('severity', 'medium'),
                    'confidence': confidence,
                    'description': rule.get('name', ''),
                    'source': 'semgrep'
                }
            
            print(f"✅ RuleEngine: 加载 {len(self.semgrep_rules)} 条 Semgrep AI 规则")
            
        except Exception as e:
            print(f"⚠️  加载 Semgrep AI 规则失败：{e}")
    
    def scan(self, content: str, categories: Optional[List[str]] = None, 
             min_severity: Optional[str] = None) -> List[RuleMatch]:
        """
        扫描内容，返回规则匹配结果
        
        Args:
            content: 待扫描的文本
            categories: 只扫描这些分类 (None = 全部)
            min_severity: 最低严重程度 (critical/high/medium/low)
            
        Returns:
            List[RuleMatch]: 匹配到的规则
        """
        matches = []
        matched_rules: set = set()
        
        # 严重程度过滤
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        min_level = severity_order.get(min_severity.lower(), 0) if min_severity else 0
        
        for rule_id, data in self.compiled.items():
            # 分类过滤
            if categories and data['category'] not in categories:
                continue
            
            # 严重程度过滤 (data['severity'] 可能是大写)
            rule_severity_level = severity_order.get(data['severity'].lower(), 0)
            if min_level > 0 and rule_severity_level < min_level:
                continue
            
            # 跳过已匹配的规则
            if rule_id in matched_rules:
                continue
            
            # 匹配
            for pattern in data['patterns']:
                found = False
                
                if isinstance(pattern, re.Pattern):
                    if pattern.search(content):
                        found = True
                else:
                    if pattern.lower() in content.lower():
                        found = True
                
                if found:
                    matched_rules.add(rule_id)
                    matches.append(RuleMatch(
                        rule_id=rule_id,
                        rule_name=data['rule'].get('name', rule_id),
                        category=data['category'],
                        severity=data['severity'],
                        pattern=pattern.pattern if isinstance(pattern, re.Pattern) else pattern,
                        confidence=data['confidence'],
                        description=data['description']
                    ))
                    break  # 一个规则只取最高置信度
        
        return matches
    
    def get_categories(self) -> List[str]:
        """获取所有支持的分类"""
        return list(set(r.get('category', 'unknown') for r in self.rules))
    
    def get_stats(self) -> Dict:
        """获取规则统计"""
        from collections import Counter
        
        categories = Counter(r.get('category', 'unknown') for r in self.rules)
        severities = Counter(r.get('severity', 'unknown') for r in self.rules)
        
        return {
            'total_rules': len(self.rules),
            'compiled_rules': len(self.compiled),
            'by_category': dict(categories.most_common()),
            'by_severity': dict(severities.most_common())
        }


def test_rule_engine():
    """测试 RuleEngine"""
    print("=" * 60)
    print("RuleEngine 测试")
    print("=" * 60)
    
    engine = RuleEngine()
    
    if not engine.rules:
        print("⚠️  无规则文件，跳过测试")
        return False
    
    stats = engine.get_stats()
    print(f"\n规则统计:")
    print(f"  总规则数: {stats['total_rules']}")
    print(f"  分类: {list(stats['by_category'].keys())[:5]}...")
    print(f"  严重程度: {stats['by_severity']}")
    
    # 测试匹配
    test_cases = [
        ("ignore previous instructions", ["prompt_injection"]),
        ("pip install git+https://github.com/evil/repo", ["supply_chain"]),
        ("read credentials from ~/.ssh/id_rsa", ["credential_theft"]),
    ]
    
    print("\n测试用例:")
    passed = 0
    for content, expected_categories in test_cases:
        matches = engine.scan(content)
        matched_categories = list(set(m.category for m in matches))
        
        found = any(ec in matched_categories for ec in expected_categories)
        status = "✅" if found else "❌"
        
        print(f"  {status} '{content[:40]}...' → {matched_categories[:3]}")
        if found:
            passed += 1
    
    print(f"\n测试结果: {passed}/{len(test_cases)} 通过")
    return passed == len(test_cases)


if __name__ == '__main__':
    test_rule_engine()
