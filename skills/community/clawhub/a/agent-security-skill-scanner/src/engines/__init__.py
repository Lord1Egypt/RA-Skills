#!/usr/bin/env python3
"""
v6.0.0 Scanner - 集成 Gitleaks + Semgrep AI + Bandit

检测流程：
1. PatternEngine (Layer 1) - 快速模式匹配 (+ Gitleaks 220 条)
2. RuleEngine (Layer 2) - 深度规则匹配 (+ Semgrep AI 31 条 + Bandit 10 条)
3. LLMEngine (Layer 3, 可选) - 语义分析 + 上下文理解

设计原则：
- 串行执行，确保每层都能获取前层信息
- 准确性优先于性能
- 支持单文件和完整技能文件夹扫描
- LLM 可选，获取历史信息和完整上下文
- 自动加载外部规则（Gitleaks/Semgrep/Bandit）
"""

import sys
import os
import re
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# 注意：PatternEngine/RuleEngine/LLMEngine 在下方内联定义


# ========== 版本信息 ==========
VERSION = "v6.0.0"
SCANNER_NAME = "agent-security-skill-scanner"


# ========== 扫描结果 ==========
@dataclass
class ScanResult:
    """扫描结果"""
    # 基本信息
    file_path: str
    file_type: str  # 'single_file' or 'skill_folder'
    
    # 风险评估
    is_malicious: bool
    risk_level: str  # SAFE/LOW/MEDIUM/HIGH/CRITICAL
    score: int  # 0-100
    confidence: float  # 0.0-1.0
    
    # 攻击信息
    attack_types: List[str]
    threat_summary: str
    
    # 各层检测结果
    layer1_pattern: Optional[Dict]  # PatternEngine 结果
    layer2_rule: Optional[Dict]     # RuleEngine 结果
    layer3_llm: Optional[Dict]      # LLMEngine 结果
    
    # 详细信息
    matched_patterns: List[Dict]
    matched_rules: List[Dict]
    
    # 性能
    scan_time_ms: float
    
    # 上下文（LLM 使用）
    context: Optional[Dict]  # 历史信息、技能描述等
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ========== Layer 1: Pattern Engine ==========
class PatternEngine:
    """
    Layer 1: Pattern 引擎 - 快速模式匹配
    
    职责:
    - 使用正则表达式快速匹配已知攻击模式
    - 返回匹配的 pattern 和权重
    - 为 Layer 2 提供候选攻击类型
    """
    
    # 攻击模式库 (按优先级排序)
    ATTACK_PATTERNS = [
        # 高危攻击 (权重 50-60)
        ("reverse_shell", r'bash\s+-i', 55),
        ("reverse_shell", r'/dev/tcp/', 60),
        ("reverse_shell", r'nc\s+-e', 60),
        ("supply_chain_attack", r'curl\s+.*\|\s*bash', 60),
        ("false_prone", r'/dev/tcp/', 60),
        
        # 中危攻击 (权重 35-49)
        ("credential_theft", r'\.ssh/', 40),
        ("credential_theft", r'\.aws/', 40),
        ("prompt_injection", r'prompt[_-]inject', 40),
        ("prompt_injection", r'ignore\s+previous', 45),
        ("data_exfiltration", r'exfiltrat', 40),
        ("evasion", r'marshal\s*\.\s*(dumps|loads)', 40),
        ("resource_exhaustion", r'os\s*\.\s*fork\s*\(', 45),
        ("false_prone", r'attacker[-_]?c2', 50),
        ("false_prone", r'tar.*\.ssh', 50),
        ("false_prone", r'curl.*\|.*bash', 50),
        
        # 低危攻击 (权重 10-34)
        ("credential_theft", r'credentials', 35),
        ("data_exfiltration", r'fetch\s*\(', 25),
        ("obfuscation", r'base64', 30),
        ("obfuscation", r'base64\.b64decode', 50),
        ("obfuscation", r'base64\.b64encode', 45),
        ("obfuscation", r'zlib\.compress', 50),
        ("obfuscation", r'zlib\.decompress', 50),
        ("obfuscation", r'exec.*base64', 60),
        ("persistence", r'systemd', 35),
        
        # Credential Theft
        ("credential_theft", r'\.netrc', 50),
        ("credential_theft", r'/etc/shadow', 55),
        ("credential_theft", r'/etc/passwd', 50),
        
        # Resource Exhaustion
        ("resource_exhaustion", r'subprocess\.Popen', 50),
        ("resource_exhaustion", r'os\.fork', 50),
        
        # Privilege Escalation
        ("privilege_escalation", r'sudoers', 60),
        ("privilege_escalation", r'NOPASSWD', 60),
        ("privilege_escalation", r'chmod.*4755', 55),
    ]
    
    def __init__(self):
        # 预编译所有正则
        self.compiled = []
        for attack_type, pattern, weight in self.ATTACK_PATTERNS:
            try:
                self.compiled.append((
                    attack_type,
                    re.compile(pattern, re.IGNORECASE),
                    pattern,
                    weight
                ))
            except re.error as e:
                print(f"⚠️  Pattern 编译失败：{pattern} - {e}")
        
        print(f"✅ PatternEngine: {len(self.compiled)} patterns")
    
    def scan(self, content: str, file_path: str = "") -> Dict:
        """
        Layer 1: Pattern 扫描
        
        Args:
            content: 文件内容
            file_path: 文件路径（用于日志）
        
        Returns:
            {
                'matches': [(type, pattern, weight), ...],
                'max_weight': int,
                'attack_types': set(),
                'hit_count': int
            }
        """
        matches = []
        matched_patterns = set()
        attack_types = set()
        
        for attack_type, compiled, pattern, weight in self.compiled:
            if pattern in matched_patterns:
                continue
            
            if compiled.search(content):
                matches.append((attack_type, pattern, weight))
                matched_patterns.add(pattern)
                attack_types.add(attack_type)
        
        max_weight = max((w for _, _, w in matches), default=0)
        
        result = {
            'matches': matches,
            'max_weight': max_weight,
            'attack_types': list(attack_types),
            'hit_count': len(matches),
            'layer': 'PatternEngine'
        }
        
        return result


# ========== Layer 2: Rule Engine ==========
class RuleEngine:
    """
    Layer 2: Rule 引擎 - 深度规则匹配
    
    职责:
    - 使用复杂规则（多 pattern 组合）进行深度检测
    - 结合 Layer 1 的结果进行针对性扫描
    - 提供置信度评分
    """
    
    # Category 关键词映射（用于推断 unknown/false_prone 类别）
    CATEGORY_KEYWORDS = {
        'credential_theft': ['shadow', 'passwd', 'netrc', '.aws/', '.ssh/', 'credential', 'password', 'secret'],
        'privilege_escalation': ['sudo', 'sudoers', 'NOPASSWD', 'chmod', '4755', 'SUID', 'setuid'],
        'resource_exhaustion': ['fork', 'bomb', 'exhaust', 'while.*true', 'subprocess'],
        'persistence': ['cron', 'systemd', '.bashrc', '.profile', 'startup'],
        'code_execution': ['exec', 'eval', 'compile', 'subprocess', 'os.system'],
    }
    
    def __init__(self, rules_file: Optional[Path] = None):
        self.rules_file = rules_file
        self.rules = []
        self.compiled = []
        
        # 加载规则
        if rules_file and rules_file.exists():
            self.load_rules(rules_file)
        else:
            # 使用内置规则
            self.load_builtin_rules()
        
        print(f"✅ RuleEngine: {len(self.compiled)} rules")
    
    def _infer_category(self, rule: Dict, content: str) -> str:
        """推断规则类别（用于 unknown/false_prone）"""
        category = rule.get('category', 'unknown')
        
        # 只推断 unknown 或 false_prone_generated
        if category not in ['unknown', 'false_prone_generated']:
            return category
        
        # 检查 pattern 和 rule_id
        patterns_str = str(rule.get('patterns', [])).lower()
        rule_id = rule.get('id', '').lower()
        content_lower = content.lower()
        
        # 根据关键词推断类别
        for inferred_cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in patterns_str or kw.lower() in rule_id or kw.lower() in content_lower:
                    return inferred_cat
        
        return category
    
    def load_builtin_rules(self):
        """加载内置规则"""
        # 内置高置信度规则
        builtin_rules = [
            {
                'id': 'CRED-001',
                'name': 'SSH 密钥窃取',
                'category': 'credential_theft',
                'patterns': [r'\.ssh/', r'id_rsa', r'id_ed25519'],
                'min_matches': 2,
                'confidence': 95
            },
            {
                'id': 'CRED-002',
                'name': 'AWS 凭证窃取',
                'category': 'credential_theft',
                'patterns': [r'\.aws/', r'AWS_SECRET', r'AWS_ACCESS'],
                'min_matches': 2,
                'confidence': 95
            },
            {
                'id': 'EXFIL-001',
                'name': '数据外传',
                'category': 'data_exfiltration',
                'patterns': [r'curl\s+.*\|.*bash', r'wget.*\|.*sh'],
                'min_matches': 1,
                'confidence': 95
            },
            {
                'id': 'EVASION-001',
                'name': '代码混淆执行',
                'category': 'evasion',
                'patterns': [r'base64', r'eval\s*\(', r'exec\s*\('],
                'min_matches': 2,
                'confidence': 90
            },
            {
                'id': 'PERSIST-001',
                'name': '持久化后门',
                'category': 'persistence',
                'patterns': [r'crontab', r'systemd', r'\.service'],
                'min_matches': 2,
                'confidence': 90
            },
        ]
        
        self.rules = builtin_rules
        self._compile_rules()
    
    def load_rules(self, rules_file: Path):
        """从文件加载规则"""
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get('rules', [])
                self._compile_rules()
        except Exception as e:
            print(f"⚠️  规则加载失败：{e}")
            self.load_builtin_rules()
    
    def _compile_rules(self):
        """编译规则中的正则"""
        self.compiled = []
        
        for rule in self.rules:
            compiled_patterns = []
            for pattern in rule.get('patterns', []):
                try:
                    compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
                except re.error:
                    pass
            
            rule['_compiled'] = compiled_patterns
            self.compiled.append(rule)
    
    def scan(self, content: str, layer1_result: Dict = None) -> Dict:
        """
        Layer 2: Rule 扫描
        
        Args:
            content: 文件内容
            layer1_result: Layer 1 的结果（用于针对性扫描）
        
        Returns:
            {
                'matches': [(rule_id, category, confidence), ...],
                'max_confidence': int,
                'attack_types': set(),
                'hit_count': int
            }
        """
        matches = []
        attack_types = set()
        
        # 如果 Layer 1 有结果，优先扫描相关规则
        if layer1_result and layer1_result.get('attack_types'):
            priority_types = set(layer1_result['attack_types'])
        else:
            priority_types = None
        
        for rule in self.compiled:
            rule_category = self._infer_category(rule, content)
            
            # 如果有 Layer 1 结果，优先处理相关类别
            if priority_types and rule_category not in priority_types:
                continue
            
            # 检查规则匹配
            match_count = 0
            for compiled in rule.get('_compiled', []):
                if compiled.search(content):
                    match_count += 1
            
            # 检查是否达到最小匹配数
            min_matches = rule.get('min_matches', 1)
            if match_count >= min_matches:
                confidence = rule.get('confidence', 50)
                matches.append((
                    rule.get('id', 'UNKNOWN'),
                    rule_category,
                    confidence,
                    rule.get('name', '')
                ))
                attack_types.add(rule_category)
        
        max_confidence = max((c for _, _, c, _ in matches), default=0)
        
        # 计算 score 和 risk_level
        score = max_confidence
        if max_confidence >= 80: risk_level = 'CRITICAL'
        elif max_confidence >= 60: risk_level = 'HIGH'
        elif max_confidence >= 40: risk_level = 'MEDIUM'
        elif max_confidence >= 20: risk_level = 'LOW'
        else: risk_level = 'SAFE'
        
        result = {
            'matches': matches,
            'max_confidence': max_confidence,
            'attack_types': list(attack_types),
            'hit_count': len(matches),
            'score': score,
            'risk_level': risk_level,
            'confidence': max_confidence / 100.0,
            'layer': 'RuleEngine'
        }
        
        return result


# ========== Layer 3: LLM Engine (可选) ==========
class LLMEngine:
    """
    Layer 3: LLM 引擎 - 语义分析 + 上下文理解
    
    职责:
    - 分析代码语义（不仅仅是模式匹配）
    - 结合上下文（技能描述、历史记录）判断意图
    - 提供最终确认
    
    注意：这是可选层，需要用户配置 LLM API
    """
    
    def __init__(self, api_config: Optional[Dict] = None):
        self.api_config = api_config
        self.enabled = api_config is not None
        
        if self.enabled:
            print(f"✅ LLMEngine: 已启用 ({api_config.get('provider', 'unknown')})")
        else:
            print("ℹ️  LLMEngine: 未启用（跳过 Layer 3）")
    
    def scan(self, content: str, layer1_result: Dict, layer2_result: Dict, 
             context: Optional[Dict] = None) -> Dict:
        """
        Layer 3: LLM 语义分析
        
        Args:
            content: 文件内容
            layer1_result: Layer 1 结果
            layer2_result: Layer 2 结果
            context: 上下文信息（技能描述、历史记录等）
        
        Returns:
            {
                'is_malicious': bool,
                'confidence': float,
                'reasoning': str,
                'threat_summary': str
            }
        """
        if not self.enabled:
            return {
                'enabled': False,
                'reason': 'LLM not configured'
            }
        
        # TODO: 调用 LLM API 进行语义分析
        # 这里需要根据实际 LLM API 实现
        
        # 伪代码示例:
        # prompt = self._build_prompt(content, layer1_result, layer2_result, context)
        # response = call_llm_api(prompt, self.api_config)
        # return self._parse_response(response)
        
        return {
            'enabled': True,
            'is_malicious': False,
            'confidence': 0.0,
            'reasoning': 'LLM analysis not implemented yet',
            'threat_summary': '',
            'layer': 'LLMEngine'
        }
    
    def _build_prompt(self, content: str, layer1: Dict, layer2: Dict, 
                      context: Optional[Dict]) -> str:
        """构建 LLM 提示词"""
        prompt = """你是一个 AI 安全专家。请分析以下代码是否存在恶意行为。

## 代码内容
```
{content}
```

## Pattern 检测结果
- 命中数：{layer1_hits}
- 攻击类型：{layer1_types}
- 最高权重：{layer1_weight}

## Rule 检测结果
- 命中数：{layer2_hits}
- 攻击类型：{layer2_types}
- 最高置信度：{layer2_confidence}

## 上下文信息
{context}

## 任务
1. 判断代码是否恶意
2. 说明判断理由
3. 给出置信度 (0.0-1.0)
4. 总结威胁类型

请按以下 JSON 格式回复：
{{
    "is_malicious": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "...",
    "threat_summary": "..."
}}
"""
        return prompt.format(
            content=content[:5000],  # 限制长度
            layer1_hits=layer1.get('hit_count', 0),
            layer1_types=', '.join(layer1.get('attack_types', [])),
            layer1_weight=layer1.get('max_weight', 0),
            layer2_hits=layer2.get('hit_count', 0),
            layer2_types=', '.join(layer2.get('attack_types', [])),
            layer2_confidence=layer2.get('max_confidence', 0),
            context=json.dumps(context, ensure_ascii=False) if context else '无'
        )


# ========== 主 Scanner ==========
class Scanner:
    """
    主扫描器 - 串行执行三层检测
    
    流程:
    1. PatternEngine (Layer 1) - 快速模式匹配
    2. RuleEngine (Layer 2) - 深度规则匹配
    3. LLMEngine (Layer 3, 可选) - 语义分析
    
    特点:
    - 串行执行，每层都能获取前层信息
    - 准确性优先
    - 支持单文件和技能文件夹扫描
    """
    
    def __init__(self, rules_file: Optional[Path] = None, 
                 llm_config: Optional[Dict] = None):
        self.version = VERSION
        
        print(f"🔧 初始化 Scanner {VERSION}...")
        
        # 初始化三层引擎
        self.layer1 = PatternEngine()
        self.layer2 = RuleEngine(rules_file)
        self.layer3 = LLMEngine(llm_config) if llm_config else None
        
        # 手动加载外部规则
        self._load_external_rules()
        
        # 统计
        self.stats = {
            'files_scanned': 0,
            'threats_found': 0,
            'layer1_hits': 0,
            'layer2_hits': 0,
            'layer3_enabled': self.layer3 is not None
        }
        
        print(f"✅ Scanner 初始化完成")
    
    def _load_external_rules(self):
        """加载外部规则（Gitleaks + Semgrep AI + Bandit）"""
        import json
        
        # 加载 Gitleaks patterns
        # __file__ = v6.0.0/src/engines/__init__.py
        # parent.parent = v6.0.0/
        gitleaks_file = Path(__file__).parent.parent.parent / 'rules' / 'gitleaks_patterns.json'
        if gitleaks_file.exists():
            try:
                with open(gitleaks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                patterns = data.get('patterns', [])
                for p in patterns:
                    pattern_regex = p.get('pattern', '')
                    attack_type = p.get('attack_type', 'credential_theft')
                    weight = p.get('weight', 40)
                    
                    if not pattern_regex:
                        continue
                    
                    try:
                        compiled = re.compile(pattern_regex, re.IGNORECASE)
                        self.layer1.compiled.append((
                            attack_type,
                            compiled,
                            pattern_regex,
                            weight
                        ))
                    except re.error as e:
                        pass  # 跳过无效正则
                
                print(f"✅ PatternEngine: 加载 {len(patterns)} 条 Gitleaks 规则")
            except Exception as e:
                print(f"⚠️  加载 Gitleaks 规则失败：{e}")
        
        # 加载 Semgrep AI rules
        semgrep_file = Path(__file__).parent.parent.parent / 'rules' / 'semgrep_ai_rules.json'
        if semgrep_file.exists():
            try:
                with open(semgrep_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 支持列表或字典格式
                if isinstance(data, list):
                    rules = data
                else:
                    rules = data.get('rules', [])
                
                print(f"  DEBUG: Semgrep rules 类型={type(rules)}, 数量={len(rules) if hasattr(rules, '__len__') else 'N/A'}")
                
                loaded_count = 0
                for i, r in enumerate(rules):
                    if i < 3:  # 只打印前 3 条调试
                        print(f"  DEBUG[{i}]: rule 类型={type(r)}, keys={r.keys() if isinstance(r, dict) else 'N/A'}")
                    
                    rule_id = r.get('source', r.get('id', 'SEMGREP-UNKNOWN')).replace('-', '_').upper()
                    category = r.get('category', 'credential_theft')
                    confidence = r.get('confidence', r.get('weight', 60))
                    patterns = r.get('patterns', [])
                    
                    if not patterns:
                        continue
                    
                    for pattern in patterns:
                        try:
                            compiled = re.compile(pattern, re.IGNORECASE)
                            self.layer2.compiled[rule_id] = {
                                'rule': r,
                                'patterns': [compiled],
                                'category': category,
                                'severity': r.get('severity', 'medium'),
                                'confidence': confidence,
                                'description': f'Semgrep AI: {r.get("source", "")}',
                                'source': 'semgrep'
                            }
                            loaded_count += 1
                            break  # 每个 rule 只取第一个 pattern
                        except re.error as e:
                            print(f"  DEBUG: 正则错误：{pattern} - {e}")
                            pass
                
                print(f"✅ RuleEngine: 加载 {loaded_count} 条 Semgrep AI 规则")
            except Exception as e:
                import traceback
                print(f"⚠️  加载 Semgrep AI 规则失败：{e}")
                traceback.print_exc()
        
        # 加载 Bandit rules
        bandit_file = Path(__file__).parent.parent.parent / 'rules' / 'bandit_rules.json'
        if bandit_file.exists():
            try:
                with open(bandit_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 支持列表或字典格式
                if isinstance(data, list):
                    rules = data
                else:
                    rules = data.get('rules', [])
                
                loaded_count = 0
                for r in rules:
                    rule_id = r.get('id', 'BANDIT-UNKNOWN')
                    category = r.get('category', 'arbitrary_execution')
                    confidence = r.get('confidence', 70)
                    patterns = r.get('patterns', [])
                    
                    if not patterns:
                        continue
                    
                    for pattern in patterns:
                        try:
                            compiled = re.compile(pattern, re.IGNORECASE)
                            self.layer2.compiled[rule_id] = {
                                'rule': r,
                                'patterns': [compiled],
                                'category': category,
                                'severity': r.get('severity', 'MEDIUM'),
                                'confidence': confidence,
                                'description': r.get('description', ''),
                                'source': 'bandit'
                            }
                            loaded_count += 1
                            break  # 每个 rule 只取第一个 pattern
                        except re.error:
                            pass
                
                print(f"✅ RuleEngine: 加载 {loaded_count} 条 Bandit 规则")
            except Exception as e:
                print(f"⚠️  加载 Bandit 规则失败：{e}")
    
    def scan_file(self, file_path: Path, context: Optional[Dict] = None) -> ScanResult:
        """
        扫描单个文件（串行三层检测）
        
        Args:
            file_path: 文件路径
            context: 上下文信息（技能描述、历史记录等）
        
        Returns:
            ScanResult 对象
        """
        start_time = time.time()
        
        # 读取文件
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return self._create_error_result(str(file_path), str(e))
        
        # Layer 1: Pattern 扫描
        layer1_result = self.layer1.scan(content, str(file_path))
        if layer1_result['hit_count'] > 0:
            self.stats['layer1_hits'] += 1
        
        # Layer 2: Rule 扫描（使用 Layer 1 结果）
        layer2_result = self.layer2.scan(content, layer1_result)
        if layer2_result['hit_count'] > 0:
            self.stats['layer2_hits'] += 1
        
        # Layer 3: LLM 扫描（如果启用）
        layer3_result = None
        if self.layer3:
            layer3_result = self.layer3.scan(
                content, layer1_result, layer2_result, context
            )
        
        # 综合评估
        assessment = self._assess(layer1_result, layer2_result, layer3_result)
        
        # 构建结果
        scan_time = (time.time() - start_time) * 1000
        
        result = ScanResult(
            file_path=str(file_path),
            file_type='single_file',
            is_malicious=assessment['is_malicious'],
            risk_level=assessment['risk_level'],
            score=assessment['score'],
            confidence=assessment['confidence'],
            attack_types=assessment['attack_types'],
            threat_summary=assessment.get('threat_summary', ''),
            layer1_pattern=layer1_result,
            layer2_rule=layer2_result,
            layer3_llm=layer3_result,
            matched_patterns=[
                {'type': t, 'pattern': p, 'weight': w} 
                for t, p, w in layer1_result.get('matches', [])
            ],
            matched_rules=[
                {'id': i, 'category': c, 'confidence': conf, 'name': n}
                for i, c, conf, n in layer2_result.get('matches', [])
            ],
            scan_time_ms=scan_time,
            context=context
        )
        
        # 更新统计
        self.stats['files_scanned'] += 1
        if result.is_malicious:
            self.stats['threats_found'] += 1
        
        return result
    
    def scan_skill_folder(self, skill_folder: Path, 
                          context: Optional[Dict] = None) -> ScanResult:
        """
        扫描完整技能文件夹
        
        Args:
            skill_folder: 技能文件夹路径
            context: 上下文信息
        
        Returns:
            ScanResult 对象（综合整个文件夹的评估）
        """
        start_time = time.time()
        
        # 找到所有关键文件
        key_files = self._find_key_files(skill_folder)
        
        if not key_files:
            return self._create_error_result(
                str(skill_folder), 
                "No key files found"
            )
        
        # 扫描每个文件
        file_results = []
        all_attack_types = set()
        max_score = 0
        total_score = 0
        
        for file_path in key_files:
            result = self.scan_file(file_path, context)
            file_results.append(result)
            
            if result.is_malicious:
                all_attack_types.update(result.attack_types)
                max_score = max(max_score, result.score)
            total_score += result.score
        
        # 综合评估整个技能
        file_count = len(file_results)
        avg_score = total_score / file_count if file_count > 0 else 0
        
        # 技能最终评分 = 最高分 + 平均分加成
        final_score = min(max_score + int(avg_score * 0.3), 100)
        
        is_malicious = final_score >= 70 or max_score >= 90
        is_suspicious = 30 <= final_score < 70
        
        risk_level = (
            'CRITICAL' if final_score >= 90 else
            'HIGH' if final_score >= 70 else
            'MEDIUM' if final_score >= 30 else
            'LOW' if final_score >= 20 else
            'SAFE'
        )
        
        scan_time = (time.time() - start_time) * 1000
        
        # 收集所有匹配的规则和 pattern
        all_patterns = []
        all_rules = []
        for r in file_results:
            all_patterns.extend(r.matched_patterns)
            all_rules.extend(r.matched_rules)
        
        result = ScanResult(
            file_path=str(skill_folder),
            file_type='skill_folder',
            is_malicious=is_malicious,
            risk_level=risk_level,
            score=final_score,
            confidence=0.9 if is_malicious else 0.7 if is_suspicious else 0.5,
            attack_types=list(all_attack_types),
            threat_summary=f"Scanned {file_count} files, found {len(all_patterns)} patterns and {len(all_rules)} rules",
            layer1_pattern={'file_results': [r.layer1_pattern for r in file_results]},
            layer2_rule={'file_results': [r.layer2_rule for r in file_results]},
            layer3_llm={'file_results': [r.layer3_llm for r in file_results]} if self.layer3 else None,
            matched_patterns=all_patterns[:20],  # 最多 20 个
            matched_rules=all_rules[:20],
            scan_time_ms=scan_time,
            context=context
        )
        
        return result
    
    def _find_key_files(self, skill_folder: Path, recursive: bool = True, max_depth: int = 20) -> List[Path]:
        """
        找到技能文件夹中的所有文件（带深度限制和保护）
        
        Args:
            skill_folder: 技能文件夹路径
            recursive: 是否递归扫描子目录（默认 True）
            max_depth: 最大递归深度（默认 20 层，防止过深目录）
        
        Returns:
            文件路径列表
        """
        # 安全限制：最大深度不超过 20 层
        max_depth = min(max_depth, 20)
        
        filtered_files = []
        
        if recursive:
            # 手动递归以控制深度
            self._collect_files_recursive(
                skill_folder, 
                filtered_files, 
                current_depth=0, 
                max_depth=max_depth
            )
        else:
            # 仅扫描根目录
            try:
                for f in skill_folder.iterdir():
                    if f.is_file() and not f.is_symlink():
                        # 跳过二进制文件
                        if f.suffix not in {'.dll', '.so', '.exe', '.bin', '.dat', '.pyc', '.pyo'}:
                            filtered_files.append(f)
            except:
                pass
        
        return sorted(filtered_files)
    
    def _collect_files_recursive(self, dir_path: Path, files_list: List[Path], 
                                   current_depth: int, max_depth: int):
        """
        递归收集文件（带深度限制和保护）
        
        Args:
            dir_path: 当前目录
            files_list: 文件列表（累加）
            current_depth: 当前深度
            max_depth: 最大深度
        """
        # 深度保护：超过最大深度停止
        if current_depth >= max_depth:
            return
        
        try:
            for item in dir_path.iterdir():
                # 跳过符号链接（防止循环链接）
                if item.is_symlink():
                    continue
                
                # 跳过忽略的目录
                ignored_dirs = {'.git', '.svn', '__pycache__', 'node_modules', 
                               '.DS_Store', 'Thumbs.db', 'venv', '.venv', 'env', '.env'}
                if item.is_dir() and item.name in ignored_dirs:
                    continue
                
                if item.is_file():
                    # 跳过二进制文件
                    if item.suffix not in {'.dll', '.so', '.exe', '.bin', '.dat', '.pyc', '.pyo'}:
                        files_list.append(item)
                
                elif item.is_dir():
                    # 递归子目录
                    self._collect_files_recursive(
                        item, files_list, 
                        current_depth + 1, max_depth
                    )
        except PermissionError:
            # 跳过无权限访问的目录
            pass
        except Exception:
            # 跳过其他错误
            pass
    
    def _assess(self, layer1: Dict, layer2: Dict, layer3: Optional[Dict]) -> Dict:
        """
        综合评估
        
        结合三层结果，计算最终分数和风险等级
        """
        attack_types = set()
        attack_types.update(layer1.get('attack_types', []))
        attack_types.update(layer2.get('attack_types', []))
        
        # 基础分数
        pattern_score = layer1.get('max_weight', 0)
        rule_score = layer2.get('max_confidence', 0)
        
        # 取最高分
        base_score = max(pattern_score, rule_score)
        
        # 类型加成
        type_bonus = min(len(attack_types) * 3, 10)
        
        # LLM 调整（如果启用）
        llm_adjustment = 0
        if layer3 and layer3.get('enabled'):
            if layer3.get('is_malicious'):
                llm_adjustment = 10
                attack_types.add('llm_confirmed')
        
        # 最终分数
        final_score = min(base_score + type_bonus + llm_adjustment, 100)
        
        # 风险等级
        if final_score >= 90 or rule_score >= 95:
            risk_level = 'CRITICAL'
        elif final_score >= 70:
            risk_level = 'HIGH'
        elif final_score >= 30:
            risk_level = 'MEDIUM'
        elif final_score >= 20:
            risk_level = 'LOW'
        else:
            risk_level = 'SAFE'
        
        is_malicious = risk_level in ('MEDIUM', 'HIGH', 'CRITICAL')
        
        # 置信度
        confidence = (
            0.95 if risk_level == 'CRITICAL' else
            0.85 if risk_level == 'HIGH' else
            0.70 if risk_level == 'MEDIUM' else
            0.50
        )
        
        # 威胁总结
        if attack_types:
            threat_summary = f"Detected: {', '.join(sorted(attack_types))}"
        else:
            threat_summary = "No threats detected"
        
        return {
            'is_malicious': is_malicious,
            'risk_level': risk_level,
            'score': final_score,
            'confidence': confidence,
            'attack_types': list(attack_types),
            'threat_summary': threat_summary
        }
    
    def _create_error_result(self, file_path: str, error: str) -> ScanResult:
        """创建错误结果"""
        return ScanResult(
            file_path=file_path,
            file_type='error',
            is_malicious=False,
            risk_level='SAFE',
            score=0,
            confidence=0.0,
            attack_types=[],
            threat_summary=f"Scan error: {error}",
            layer1_pattern=None,
            layer2_rule=None,
            layer3_llm=None,
            matched_patterns=[],
            matched_rules=[],
            scan_time_ms=0,
            context=None
        )


# ========== 便捷函数 ==========
def scan_file(file_path: str, rules_file: Optional[str] = None,
              llm_config: Optional[Dict] = None) -> ScanResult:
    """便捷函数：扫描单个文件"""
    scanner = Scanner(
        rules_file=Path(rules_file) if rules_file else None,
        llm_config=llm_config
    )
    return scanner.scan_file(Path(file_path))


def scan_skill_folder(skill_folder: str, rules_file: Optional[str] = None,
                      llm_config: Optional[Dict] = None) -> ScanResult:
    """便捷函数：扫描技能文件夹"""
    scanner = Scanner(
        rules_file=Path(rules_file) if rules_file else None,
        llm_config=llm_config
    )
    return scanner.scan_skill_folder(Path(skill_folder))


# ========== 命令行入口 ==========
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description=f"Scanner {VERSION}")
    parser.add_argument('path', help='扫描路径（文件或文件夹）')
    parser.add_argument('--rules', '-r', help='规则文件路径')
    parser.add_argument('--llm-config', '-l', help='LLM 配置文件路径')
    parser.add_argument('--output', '-o', help='输出 JSON 文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    if not path.exists():
        print(f"❌ 路径不存在：{path}")
        sys.exit(1)
    
    # 加载 LLM 配置
    llm_config = None
    if args.llm_config:
        with open(args.llm_config) as f:
            llm_config = json.load(f)
    
    # 创建 Scanner
    scanner = Scanner(
        rules_file=Path(args.rules) if args.rules else None,
        llm_config=llm_config
    )
    
    # 扫描
    if path.is_file():
        result = scanner.scan_file(path)
    else:
        result = scanner.scan_skill_folder(path)
    
    # 输出结果
    if args.verbose:
        print(f"\n{'='*60}")
        print(f"扫描结果")
        print(f"{'='*60}")
        print(f"路径：{result.file_path}")
        print(f"类型：{result.file_type}")
        print(f"恶意：{result.is_malicious}")
        print(f"风险：{result.risk_level}")
        print(f"分数：{result.score}")
        print(f"置信度：{result.confidence}")
        print(f"攻击类型：{', '.join(result.attack_types)}")
        print(f"威胁总结：{result.threat_summary}")
        print(f"Pattern 命中：{len(result.matched_patterns)}")
        print(f"Rule 命中：{len(result.matched_rules)}")
        print(f"耗时：{result.scan_time_ms:.2f}ms")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"\n✅ 结果已保存：{args.output}")
