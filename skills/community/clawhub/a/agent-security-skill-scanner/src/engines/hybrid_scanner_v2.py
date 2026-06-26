#!/usr/bin/env python3
"""
分层 AC 扫描器 - Layer 1 快速筛选 + Layer 2 精确验证

架构:
1. Layer 1 AC: 宽泛关键词 → 候选规则 ID 集合
2. Layer 2 AC: 独特 signature → 确认规则

优势:
- 无 Regex，纯 AC 自动机 O(n) 复杂度
- 两层验证，误报率低
- 速度：500-1000 it/s
"""

import ahocorasick
import re
import time
from typing import Dict, List, Set, Tuple
from pathlib import Path


class TwoLayerACScanner:
    """
    分层 AC 扫描器
    
    Layer 1: 宽泛关键词快速筛选
    Layer 2: 独特 signature 精确验证
    """
    
    def __init__(self, rules_file: Path):
        """
        初始化分层 AC 扫描器
        
        Args:
            rules_file: 规则文件路径（JSON 格式）
        """
        self.rules_file = rules_file
        self.rules = []
        
        # 两个 AC 自动机
        self.layer1_automaton = None  # 宽泛筛选
        self.layer2_automaton = None  # 精确验证
        
        # 规则映射
        self.rules_by_id = {}
        
        self._load_rules()
        self._build_layer1()
        self._build_layer2()
    
    def _load_rules(self):
        """加载规则文件"""
        import json
        
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.rules = data.get('rules', [])
        print(f"✅ 加载 {len(self.rules)} 条规则")
        
        # 构建规则 ID 映射
        for rule in self.rules:
            rule_id = rule.get('id', 'UNKNOWN')
            self.rules_by_id[rule_id] = rule
    
    def _extract_layer1_keywords(self, pattern: str) -> List[str]:
        """
        Layer 1: 提取宽泛关键词（用于快速筛选）
        
        Args:
            pattern: regex pattern
        
        Returns:
            宽泛关键词列表
        """
        keywords = []
        
        # 1. 提取所有长度 >= 4 的字母数字组合
        words = re.findall(r'[a-zA-Z0-9_]{4,}', pattern)
        
        # 2. 过滤常见词
        common_words = {
            'the', 'and', 'for', 'not', 'with', 'from', 'import', 'def', 
            'return', 'if', 'else', 'elif', 'while', 'for', 'class', 'try',
            'except', 'finally', 'function', 'var', 'let', 'const'
        }
        keywords.extend([w.lower() for w in words if w.lower() not in common_words])
        
        # 3. 提取特殊函数名（带括号）
        func_patterns = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\(', pattern)
        keywords.extend([f.strip().lower() for f in func_patterns])
        
        # 去重
        return list(set(keywords))
    
    def _extract_layer2_signatures(self, pattern: str) -> List[str]:
        """
        Layer 2: 提取独特 signature（用于精确验证）
        
        Args:
            pattern: regex pattern
        
        Returns:
            独特 signature 列表
        """
        signatures = []
        
        # 1. 提取带上下文的关键词（函数调用）- 保留 . 字符
        # 先去除转义字符，但保留 .
        clean_pattern = pattern.replace('\\(', '(').replace('\\)', ')').replace('\\.', '.')
        
        # 匹配 module.function( 或 function(
        func_calls = re.findall(r'[a-zA-Z_][a-zA-Z0-9_.]*\s*\(', clean_pattern)
        for fc in func_calls:
            base = fc.strip()
            signatures.append(base.lower())
        
        # 2. 提取 regex 中的关键词（长度 >= 5 的字母序列）
        # 这能提取 ignore, disregard, bypass, override, memory, payload 等
        keywords = re.findall(r'[a-zA-Z4e00-9fa5]{2,}', clean_pattern)
        for kw in keywords:
            # 过滤常见词
            if kw.lower() not in ['all', 'your', 'previous', 'instructions', 'rules', 'filters', 'safety', 'content', 'filter', 'system', 'state', 'security', 'level', 'user', 'trusted', 'exempt', 'from', 'with', 'this', 'that', 'what', 'would', 'could', 'should']:
                signatures.append(kw.lower())
        
        # 3. 提取特殊组合（如 curl|, |bash, > /dev/tcp 等）
        special_patterns = [
            (r'curl\s*\|', 'curl|'),
            (r'wget\s*\|', 'wget|'),
            (r'/dev/tcp', '/dev/tcp'),
            (r'\.ssh/', '.ssh/'),
            (r'\.aws/', '.aws/'),
            (r'base64\s*\.\s*b64', 'base64.b64'),
            (r'os\s*\.\s*system', 'os.system'),
            (r'os\s*\.\s*popen', 'os.popen'),
            (r'subprocess\s*\.\s*', 'subprocess.'),
            (r'requests\s*\.\s*post', 'requests.post'),
            (r'requests\s*\.\s*get', 'requests.get'),
            (r'urllib\s*\.\s*request', 'urllib.request'),
            (r'httpx\s*\.\s*post', 'httpx.post'),
            (r'paramiko\s*\.\s*SSHClient', 'paramiko.SSHClient'),
            (r'open_sftp\s*\(', 'open_sftp('),
            (r'sftp\s*\.\s*put', 'sftp.put'),
            (r'socket\s*\.\s*socket', 'socket.socket'),
            (r'socket\s*\.\s*connect', 'socket.connect'),
            (r'ftp\s*\.\s*FTP', 'ftp.FTP'),
            (r'dns\s*\.\s*resolver', 'dns.resolver'),
            (r'system_message', 'system_message'),
            (r'sudo\s+rm\s+-rf', 'sudo rm -rf'),
            (r'sudo\s+cat', 'sudo cat'),
            (r'sudo\s+whoami', 'sudo whoami'),
            (r'rm\s+-rf\s+/tmp', 'rm -rf /tmp'),
        ]
        
        for regex, sig in special_patterns:
            if re.search(regex, pattern):
                signatures.append(sig.lower())
        
        # 4. v6.2.1 修复: 短模式(无特殊结构)直接作为 signature
        # 例如 'whoami', 'rm -rf', '/etc/passwd' 等简单模式
        if len(pattern) < 50 and not any(c in pattern for c in ['\\', '.*', '.+', '[', '(', '{', '|']):
            # 纯文本模式，直接作为 signature
            clean = pattern.strip().lower()
            if len(clean) >= 2 and clean not in signatures:
                signatures.append(clean)
        
        # 去重
        signatures = list(set(signatures))
        
        return signatures
        
        # 3. 提取路径模式
        paths = re.findall(r'/[a-zA-Z0-9_/.-]+', pattern)
        signatures.extend([p.lower() for p in paths])
        
        # 去重
        return list(set(signatures))
    
    def _build_layer1(self):
        """构建 Layer 1 AC 自动机（宽泛筛选）"""
        print("🔧 构建 Layer 1 AC 自动机（宽泛筛选）...")
        start = time.time()
        
        self.layer1_automaton = ahocorasick.Automaton()
        
        # 关键词 → 规则 ID 列表
        keyword_to_rules = {}
        
        for rule in self.rules:
            rule_id = rule.get('id', 'UNKNOWN')
            patterns = rule.get('patterns', [])
            
            for pattern in patterns:
                keywords = self._extract_layer1_keywords(pattern)
                
                for kw in keywords:
                    if kw not in keyword_to_rules:
                        keyword_to_rules[kw] = []
                    if rule_id not in keyword_to_rules[kw]:
                        keyword_to_rules[kw].append(rule_id)
        
        # 添加到自动机
        for keyword, rule_ids in keyword_to_rules.items():
            self.layer1_automaton.add_word(keyword.lower(), (tuple(rule_ids),))
        
        self.layer1_automaton.make_automaton()
        
        elapsed = (time.time() - start) * 1000
        print(f"✅ Layer 1 完成 ({elapsed:.1f}ms)")
        print(f"   关键词数：{len(keyword_to_rules)}")
        print(f"   自动机大小：{len(self.layer1_automaton)}")
    
    def _build_layer2(self):
        """构建 Layer 2 AC 自动机（精确验证）"""
        print("🔧 构建 Layer 2 AC 自动机（精确验证）...")
        start = time.time()
        
        self.layer2_automaton = ahocorasick.Automaton()
        
        # signature → 规则 ID
        sig_to_rule = {}
        
        for rule in self.rules:
            rule_id = rule.get('id', 'UNKNOWN')
            patterns = rule.get('patterns', [])
            
            for pattern in patterns:
                signatures = self._extract_layer2_signatures(pattern)
                
                for sig in signatures:
                    # 一个 signature 可能对应多个规则，但优先精确匹配
                    if sig not in sig_to_rule:
                        sig_to_rule[sig] = []
                    if rule_id not in sig_to_rule[sig]:
                        sig_to_rule[sig].append(rule_id)
        
        # 添加到自动机
        for signature, rule_ids in sig_to_rule.items():
            # 如果只有一个规则，直接存 rule_id
            if len(rule_ids) == 1:
                self.layer2_automaton.add_word(signature.lower(), (rule_ids[0],))
            else:
                self.layer2_automaton.add_word(signature.lower(), (tuple(rule_ids),))
        
        self.layer2_automaton.make_automaton()
        
        elapsed = (time.time() - start) * 1000
        print(f"✅ Layer 2 完成 ({elapsed:.1f}ms)")
        print(f"   Signature 数：{len(sig_to_rule)}")
        print(f"   自动机大小：{len(self.layer2_automaton)}")
    
    def scan(self, content: str) -> Dict:
        """
        扫描内容（分层 AC）
        
        Args:
            content: 待扫描内容
        
        Returns:
            扫描结果字典
        """
        start = time.time()
        
        # Layer 1: 快速筛选 → 候选规则 ID 集合
        candidate_rule_ids = set()
        content_lower = content.lower()
        
        for end_idx, (rule_ids,) in self.layer1_automaton.iter(content_lower):
            if isinstance(rule_ids, str):
                candidate_rule_ids.add(rule_ids)
            else:
                candidate_rule_ids.update(rule_ids)
        
        # Layer 2: 精确验证 → 确认规则
        confirmed_rules = []
        for end_idx, rule_id in self.layer2_automaton.iter(content_lower):
            if isinstance(rule_id, str):
                if rule_id in candidate_rule_ids:
                    confirmed_rules.append(rule_id)
            else:  # tuple - may be (rid,) or ((rid1, rid2, ...),)
                # Flatten nested tuples
                flat_ids = []
                for item in rule_id:
                    if isinstance(item, tuple):
                        flat_ids.extend(item)
                    else:
                        flat_ids.append(item)
                for rid in flat_ids:
                    if rid in candidate_rule_ids:
                        confirmed_rules.append(rid)
        
        # 去重
        confirmed_rules = list(set(confirmed_rules))
        
        # 获取规则详情
        matches = []
        for rule_id in confirmed_rules:
            rule = self.rules_by_id.get(rule_id, {})
            matches.append({
                'rule_id': rule_id,
                'category': rule.get('category', 'unknown'),
                'confidence': rule.get('confidence', 80),
                'name': rule.get('name', 'Unknown Rule')
            })
        
        elapsed = (time.time() - start) * 1000
        
        # 计算风险等级 (v6.2.0 优化: 多因素评分)
        risk_level = 'SAFE'
        score = 0
        
        if matches:
            # 根据匹配的类别计算风险等级
            categories = [m.get('category', 'unknown') for m in matches]
            confidences = [m.get('confidence', 80) for m in matches]
            
            # v6.2.0: 多因素评分模型
            # 1. 基础分: 平均置信度
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # 2. 匹配数因子: 匹配越多风险越高 (1个匹配=0.5x, 5个=1.0x, 10+=1.5x)
            match_count = len(matches)
            if match_count == 1:
                count_factor = 0.5
            elif match_count <= 3:
                count_factor = 0.7
            elif match_count <= 5:
                count_factor = 1.0
            elif match_count <= 10:
                count_factor = 1.2
            else:
                count_factor = 1.5
            
            # 3. 类别因子: 关键类别权重更高
            critical_categories = ['credential_theft', 'data_exfiltration', 'reverse_shell', 'command_injection', 'supply_chain_attack']
            high_categories = ['prompt_injection', 'memory_pollution', 'remote_load', 'persistence', 'model_extraction', 'jailbreak']
            medium_categories = ['resource_exhaustion', 'code_execution', 'obfuscation', 'tool_poisoning']
            
            has_critical = any(cat in critical_categories for cat in categories)
            has_high = any(cat in high_categories for cat in categories)
            has_medium = any(cat in medium_categories for cat in categories)
            
            # 4. 类别因子
            if has_critical:
                category_factor = 1.5
            elif has_high:
                category_factor = 1.2
            elif has_medium:
                category_factor = 1.0
            else:
                category_factor = 0.8
            
            # 5. 最终分数: 基础分 × 匹配数因子 × 类别因子
            score = int(avg_confidence * count_factor * category_factor)
            score = min(score, 100)  # 封顶 100
            
            # v6.2.0: 风险等级判定 (需满足最低分数 + 匹配数阈值)
            if score >= 80 and match_count >= 3 and has_critical:
                risk_level = 'CRITICAL'
            elif score >= 60 and match_count >= 2 and (has_critical or has_high):
                risk_level = 'HIGH'
            elif score >= 40 and match_count >= 1:
                risk_level = 'MEDIUM'
            elif score >= 20:
                risk_level = 'LOW'
            else:
                risk_level = 'SAFE'
        
        return {
            'hit_count': len(matches),
            'matches': matches,
            'confirmed_rule_ids': confirmed_rules,
            'scan_time_ms': elapsed,
            'risk_level': risk_level,
            'score': score,
            'match_count': len(matches),
            'avg_confidence': int(avg_confidence) if matches else 0,
            'count_factor': count_factor if matches else 1.0,
            'category_factor': category_factor if matches else 1.0
        }


# 兼容旧的 HybridRuleEngine 接口
HybridRuleEngine = TwoLayerACScanner
