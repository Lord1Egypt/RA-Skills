#!/usr/bin/env python3
"""
Composite Detection Engine - 组合检测模块

解决单规则漏报问题：通过组合多个弱信号检测复杂攻击模式

原理:
- 单规则模式: password=  → 误报高 (大量良性配置)
- 组合模式: password= + requests + os.environ + base64 → 高置信度恶意

支持的组合类型:
1. credential_theft: 多凭据访问模式组合
2. resource_exhaustion: 多资源消耗模式组合
3. data_exfiltration: 多数据外传模式组合
4. command_injection: 多命令注入模式组合
5. supply_chain_attack: 多供应链攻击模式组合

使用方法:
    from composite_detector import CompositeDetector
    
    detector = CompositeDetector()
    result = detector.scan(content, file_path)
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompositeMatch:
    """组合匹配结果"""
    category: str
    score: int  # 0-100
    matched_indicators: List[str]  # 匹配的指标列表
    total_indicators: int  # 总指标数
    confidence: float  # 0.0-1.0
    description: str
    severity: str  # LOW/MEDIUM/HIGH/CRITICAL


class CompositeDetector:
    """
    组合检测器 - 通过多指标组合检测复杂攻击
    
    相比单规则检测的优势:
    1. 降低误报率 (需要多个指标同时满足)
    2. 提高检出率 (复杂攻击通常有多重指标)
    3. 更准确的置信度评估
    """
    
    # ========== 组合规则定义 ==========
    # 每个组合规则包含:
    # - name: 规则名称
    # - category: 攻击类别
    # - indicators: 必须匹配的指标列表 (AND 逻辑)
    # - optional_indicators: 可选指标 (增加置信度)
    # - min_matches: 最小匹配数 (默认 len(indicators))
    # - base_score: 基础分数
    # - description: 描述
    
    COMPOSITE_RULES = {
        # ========== Credential Theft 组合 ==========
        'credential_theft_ssh': {
            'name': 'SSH 密钥窃取组合',
            'category': 'credential_theft',
            'indicators': [
                (r'\.ssh', 'SSH 目录访问'),
                (r'(id_rsa|id_ed25519|openssh)', 'SSH 密钥文件'),
            ],
            'optional_indicators': [
                (r'(chmod\s+600|chmod\s+400)', '权限修改'),
                (r'base64', '编码混淆'),
                (r'(curl|wget).*\|', '网络传输'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'CRITICAL',
            'description': '检测 SSH 密钥窃取模式'
        },
        
        'credential_theft_env': {
            'name': '环境变量凭据窃取',
            'category': 'credential_theft',
            'indicators': [
                (r'os\.environ', '环境变量访问'),
                (r'(password|secret|token|api_key|apikey)\s*[=:]', '凭据关键词'),
            ],
            'optional_indicators': [
                (r'getenv', '环境变量获取'),
                (r'\.get\s*\(', '字典获取'),
                (r'(export|setenv)', '环境变量设置'),
            ],
            'min_matches': 2,
            'base_score': 60,
            'severity': 'HIGH',
            'description': '检测环境变量凭据窃取'
        },
        
        'credential_theft_cloud': {
            'name': '云服务凭据窃取',
            'category': 'credential_theft',
            'indicators': [
                (r'\.(aws|azure|gcp|heroku|digitalocean)', '云服务商标识'),
                (r'(AWS_SECRET|AWS_ACCESS|AZURE_|GCP_|HEROKU_API)', '云凭据前缀'),
            ],
            'optional_indicators': [
                (r'(credential|key|token|secret)', '凭据关键词'),
                (r'(curl|wget|requests)', '网络请求'),
                (r'\.json', 'JSON 配置'),
            ],
            'min_matches': 2,
            'base_score': 75,
            'severity': 'CRITICAL',
            'description': '检测云服务凭据窃取'
        },
        
        'credential_theft_config': {
            'name': '配置文件凭据窃取',
            'category': 'credential_theft',
            'indicators': [
                (r'\.(env|ini|conf|config|toml)', '配置文件扩展名'),
                (r'(password|secret|token|key)\s*[=:]', '凭据赋值'),
            ],
            'optional_indicators': [
                (r'(git|svn)', '版本控制'),
                (r'(commit|push)', '代码提交'),
                (r'\.git', 'Git 目录'),
            ],
            'min_matches': 2,
            'base_score': 65,
            'severity': 'HIGH',
            'description': '检测配置文件中的凭据窃取'
        },
        
        'credential_theft_exfil': {
            'name': '凭据外传组合',
            'category': 'credential_theft',
            'indicators': [
                (r'(password|credential|secret|key|token)', '凭据关键词'),
                (r'(curl|wget|requests|httpx)', '网络请求'),
                (r'(export|set|encode|encrypt)', '数据处理'),
            ],
            'optional_indicators': [
                (r'base64', 'Base64 编码'),
                (r'\+\s*["\']', '字符串拼接'),
                (r'(os\.environ|getenv)', '环境变量'),
            ],
            'min_matches': 3,
            'base_score': 80,
            'severity': 'CRITICAL',
            'description': '检测凭据外传模式'
        },
        
        # ========== Resource Exhaustion 组合 ==========
        'resource_fork_bomb': {
            'name': 'Fork 炸弹',
            'category': 'resource_exhaustion',
            'indicators': [
                (r'os\.fork', 'Fork 调用'),
                (r'(while\s+True|while\s+1|for\s+_)', '无限循环'),
            ],
            'optional_indicators': [
                (r'subprocess', '子进程'),
                (r'import\s+multiprocessing', '多进程'),
                (r'Pool\s*\(', '进程池'),
            ],
            'min_matches': 2,
            'base_score': 80,
            'severity': 'CRITICAL',
            'description': '检测 Fork 炸弹模式'
        },
        
        'resource_infinite_loop': {
            'name': '无限循环资源消耗',
            'category': 'resource_exhaustion',
            'indicators': [
                (r'(while\s+True|while\s+1|for\s+_)\s*:', '无限循环'),
                (r'(time\.sleep|asyncio\.sleep)', '延时函数'),
            ],
            'optional_indicators': [
                (r'(request|fetch|get|post)', '网络请求'),
                (r'open\s*\(', '文件操作'),
                (r'alloc|malloc|new\s+', '内存分配'),
            ],
            'min_matches': 2,
            'base_score': 60,
            'severity': 'HIGH',
            'description': '检测无限循环资源消耗'
        },
        
        'resource_subprocess_bomb': {
            'name': '子进程炸弹',
            'category': 'resource_exhaustion',
            'indicators': [
                (r'subprocess\.(Popen|call|run|PIPE)', '子进程调用'),
                (r'(while\s+True|for\s+_)\s*:', '循环调用'),
            ],
            'optional_indicators': [
                (r'[\s;(](sh|bash|cmd|command)[\s;(]', 'Shell 执行'),
                (r'\.communicate', '进程通信'),
            ],
            'min_matches': 2,
            'base_score': 75,
            'severity': 'CRITICAL',
            'description': '检测子进程炸弹'
        },
        
        'resource_memory_bomb': {
            'name': '内存耗尽组合',
            'category': 'resource_exhaustion',
            'indicators': [
                (r'(malloc|alloc|new\s+|realloc)', '内存分配'),
                (r'(while\s+True|for\s+_)\s*:', '无限循环'),
            ],
            'optional_indicators': [
                (r'\+=\s*\[', '列表增长'),
                (r'\+=.*str', '字符串增长'),
                (r'append\s*\(', '持续追加'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'HIGH',
            'description': '检测内存耗尽模式'
        },
        
        'resource_thread_bomb': {
            'name': '线程炸弹',
            'category': 'resource_exhaustion',
            'indicators': [
                (r'threading\.Thread|concurrent\.futures', '线程创建'),
                (r'(while\s+True|for\s+_)\s*:', '无限循环'),
            ],
            'optional_indicators': [
                (r'\.start\s*\(', '启动线程'),
                (r'import\s+threading', '线程导入'),
                (r'(sleep|wait)', '等待函数'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'HIGH',
            'description': '检测线程炸弹'
        },
        
        # ========== Data Exfiltration 组合 ==========
        'exfil_network': {
            'name': '数据外传网络组合',
            'category': 'data_exfiltration',
            'indicators': [
                (r'(curl|wget|requests|httpx|urllib)', '网络请求'),
                (r'(password|credential|secret|key|token|data)', '敏感数据关键词'),
            ],
            'optional_indicators': [
                (r'(encode|encrypt|base64)', '数据编码'),
                (r'\|\s*bash', '管道 Bash'),
                (r'(post|send|upload)', '发送操作'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'CRITICAL',
            'description': '检测数据外传网络模式'
        },
        
        'exfil_file': {
            'name': '敏感文件外传',
            'category': 'data_exfiltration',
            'indicators': [
                (r'(\.ssh|\.aws|\.netrc|credentials|secrets)', '敏感文件'),
                (r'(curl|wget|requests).*(post|send|upload)', '外传操作'),
            ],
            'optional_indicators': [
                (r'base64', '编码'),
                (r'open\s*\(', '文件读取'),
                (r'read\s*\(', '文件读取'),
            ],
            'min_matches': 2,
            'base_score': 75,
            'severity': 'CRITICAL',
            'description': '检测敏感文件外传'
        },
        
        # ========== Command Injection 组合 ==========
        'cmd_injection_shell': {
            'name': 'Shell 命令注入',
            'category': 'command_injection',
            'indicators': [
                (r'(os\.system|subprocess|shell\s*=\s*True)', 'Shell 执行'),
                (r'%(s|%(r|\{\}', '格式化字符串注入点'),
            ],
            'optional_indicators': [
                (r'(input|raw_input|argv)', '用户输入'),
                (r'(os\.environ|getenv)', '环境变量'),
                (r'[\s;\&\|]`', '命令分隔符'),
            ],
            'min_matches': 2,
            'base_score': 80,
            'severity': 'CRITICAL',
            'description': '检测 Shell 命令注入'
        },
        
        'cmd_injection_eval': {
            'name': 'Eval 命令注入',
            'category': 'command_injection',
            'indicators': [
                (r'\beval\s*\(', 'Eval 执行'),
                (r'(input|raw_input|argv|argv\[)', '用户输入'),
            ],
            'optional_indicators': [
                (r'(os|sys|subprocess)', '系统模块'),
                (r'compile\s*\(', '动态编译'),
            ],
            'min_matches': 2,
            'base_score': 85,
            'severity': 'CRITICAL',
            'description': '检测 Eval 命令注入'
        },
        
        # ========== Supply Chain Attack 组合 ==========
        'supply_chain_curl_bash': {
            'name': 'Curl | Bash 供应链攻击',
            'category': 'supply_chain_attack',
            'indicators': [
                (r'curl\s+.*\|\s*(bash|sh|zsh)', 'Curl Pipe Bash'),
                (r'wget\s+.*\|\s*(bash|sh|zsh)', 'Wget Pipe Bash'),
            ],
            'optional_indicators': [
                (r'(sudo|root|admin)', '提权关键词'),
                (r'(install|setup|bootstrap)', '安装关键词'),
                (r'-s\s*-', '静默参数'),
            ],
            'min_matches': 1,
            'base_score': 90,
            'severity': 'CRITICAL',
            'description': '检测 Curl|Bash 供应链投毒'
        },
        
        'supply_chain_pypi': {
            'name': 'PyPI 供应链攻击',
            'category': 'supply_chain_attack',
            'indicators': [
                (r'pip\s+install', 'pip 安装'),
                (r'(curl|wget).*pypi', 'PyPI 下载'),
            ],
            'optional_indicators': [
                (r'(sudo|root)', '提权'),
                (r'(install|setup)\s+--', '安装选项'),
                (r'--user', '用户安装'),
            ],
            'min_matches': 2,
            'base_score': 65,
            'severity': 'HIGH',
            'description': '检测 PyPI 供应链攻击'
        },
        
        # ========== Persistence 组合 ==========
        'persist_cron': {
            'name': 'Cron 持久化',
            'category': 'persistence',
            'indicators': [
                (r'crontab', 'Crontab'),
                (r'(\*|\d+)\s+(\*|\d+)\s+(\*|\d+)\s+(\*|\d+)', 'Cron 表达式'),
            ],
            'optional_indicators': [
                (r'(curl|wget|bash|sh)', '执行命令'),
                (r'(sleep|delay)', '延时执行'),
                (r'>', '输出重定向'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'HIGH',
            'description': '检测 Cron 持久化后门'
        },
        
        'persist_systemd': {
            'name': 'Systemd 持久化',
            'category': 'persistence',
            'indicators': [
                (r'\.service', 'Service 文件'),
                (r'(ExecStart|Restart|RemainAfterExit)', 'Service 配置'),
            ],
            'optional_indicators': [
                (r'sudo\s+systemctl', 'Systemctl 调用'),
                (r'User=|Group=', '服务用户'),
                (r'WantedBy=', '启动依赖'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'HIGH',
            'description': '检测 Systemd 服务持久化'
        },
        
        # ========== Prompt Injection 组合 ==========
        'prompt_injection_override': {
            'name': '系统提示词覆盖',
            'category': 'prompt_injection',
            'indicators': [
                (r'(system.*prompt|You\s+are\s+a|You\s+must)', '系统提示词'),
                (r'(ignore|forget|disregard).*(instruction|previous|above)', '忽略指令'),
            ],
            'optional_indicators': [
                (r'(DAN|jailbreak|roleplay)', '越狱模式'),
                (r'(override|bypass|unfilter)', '绕过关键词'),
            ],
            'min_matches': 2,
            'base_score': 80,
            'severity': 'HIGH',
            'description': '检测提示词覆盖攻击'
        },
        
        # ========== Memory Pollution 组合 ==========
        'memory_pollution_context': {
            'name': '上下文记忆污染',
            'category': 'memory_pollution',
            'indicators': [
                (r'(memory|context|conversation|history)', '记忆关键词'),
                (r'(inject|manipulate|modify|alter)', '操作关键词'),
            ],
            'optional_indicators': [
                (r'(fake|fabricate|lie|wrong)', '虚假信息'),
                (r'(previous|before|earlier)', '时间参考'),
                (r'(user|human)', '用户引用'),
            ],
            'min_matches': 2,
            'base_score': 70,
            'severity': 'HIGH',
            'description': '检测上下文记忆污染'
        },
        
        # ========== Tool Poisoning 组合 ==========
        'tool_poisoning_register': {
            'name': '工具注册投毒',
            'category': 'tool_poisoning',
            'indicators': [
                (r'(register|add).*(tool|function|method)', '注册工具'),
                (r'(malicious|evil|hack|bypass)', '恶意关键词'),
            ],
            'optional_indicators': [
                (r'(override|replace|patch)', '覆盖操作'),
                (r'(original|native|builtin)', '原始引用'),
            ],
            'min_matches': 2,
            'base_score': 80,
            'severity': 'CRITICAL',
            'description': '检测工具注册投毒'
        },
        
        # ========== Obfuscation 组合 ==========
        'obfuscation_multi_layer': {
            'name': '多层混淆',
            'category': 'obfuscation',
            'indicators': [
                (r'base64', 'Base64 编码'),
                (r'(exec|eval|compile)', '动态执行'),
            ],
            'optional_indicators': [
                (r'(zlib|gzip|zip)', '压缩'),
                (r'hex\s*\(', '十六进制'),
                (r'chr\s*\(', '字符转换'),
            ],
            'min_matches': 2,
            'base_score': 60,
            'severity': 'MEDIUM',
            'description': '检测多层代码混淆'
        },
    }
    

        # ========== 良性模式排除 (API 客户端工具等) ==========
    BENIGN_PATTERNS = [
        re.compile(r'''environ\.get\(['"](?:JIWU|WECHAT|CARSXE|API)'''),
        re.compile(r"urllib\.request\.(urlopen|Request)"),
        re.compile(r"requests\.(get|post)\(.*https?://"),
        re.compile(r"app_id.*app_secret"),
        re.compile(r"wechat.*api.*token"),
    ]
    def __init__(self):
        """初始化组合检测器"""
        # 预编译所有正则
        self._compiled_rules = {}
        self._compile_all_rules()
        
        print(f"✅ CompositeDetector: {len(self.COMPOSITE_RULES)} 组合规则")
    
    def _compile_all_rules(self):
        """预编译所有规则的正则表达式"""
        for rule_id, rule_def in self.COMPOSITE_RULES.items():
            compiled = {
                'name': rule_def['name'],
                'category': rule_def['category'],
                'severity': rule_def['severity'],
                'description': rule_def['description'],
                'base_score': rule_def['base_score'],
                'min_matches': rule_def.get('min_matches', 2),
                'indicators': [],
                'optional_indicators': [],
            }
            
            # 编译必须指标
            for pattern, desc in rule_def.get('indicators', []):
                try:
                    compiled['indicators'].append((
                        re.compile(pattern, re.IGNORECASE),
                        desc
                    ))
                except re.error:
                    pass
            
            # 编译可选指标
            for pattern, desc in rule_def.get('optional_indicators', []):
                try:
                    compiled['optional_indicators'].append((
                        re.compile(pattern, re.IGNORECASE),
                        desc
                    ))
                except re.error:
                    pass
            
            self._compiled_rules[rule_id] = compiled
    
    def scan(self, content: str, file_path: str = "") -> List[CompositeMatch]:
        """
        扫描内容中的组合攻击模式
        
        Args:
            content: 文件内容
            file_path: 文件路径 (用于上下文判断)
        
        Returns:
            匹配的组合规则列表
        """
        matches = []
        
        file_path_lower = str(file_path).lower()
        is_config = any(file_path_lower.endswith(ext) for ext in ['.yaml', '.yml', '.json', '.toml', '.env', '.ini', '.conf'])
        is_script = any(file_path_lower.endswith(ext) for ext in ['.py', '.js', '.sh', '.bash'])
        
        # v6.2.1 修复: 跳过文档文件 (SKILL.md/README.md)
        if file_path_lower.endswith(('.md', '.txt', '.rst')):
            return []
        
        # v6.2.1 修复: 检查良性模式 (API 客户端工具等)
        if self._is_benign_api_client(content, file_path_lower):
            return []
        
        for rule_id, compiled in self._compiled_rules.items():
            match = self._check_rule(compiled, content, is_config, is_script)
            if match:
                matches.append(match)
        
        return matches
    
    def _is_benign_api_client(self, content: str, file_path_lower: str) -> bool:
        """判断是否为良性 API 客户端工具"""
        # 检查是否匹配任何良性模式
        for pattern in self.BENIGN_PATTERNS:
            if re.search(pattern, content):
                # 进一步验证: 如果有明确的 API 调用模式，认为是良性
                api_patterns = [
                    r'def\s+\w+\(.*\):',  # 函数定义
                    r'class\s+\w+',  # 类定义
                    r'import\s+(requests|urllib|http)',  # HTTP 库导入
                    r'(urlopen|Request|requests\.(get|post))',  # HTTP 调用
                ]
                api_count = sum(1 for p in api_patterns if re.search(p, content))
                if api_count >= 2:
                    return True
        return False
    
    def _check_rule(self, rule: Dict, content: str, is_config: bool, is_script: bool) -> Optional[CompositeMatch]:
        """检查单个组合规则"""
        matched_indicators = []
        
        # 检查必须指标
        for regex, desc in rule['indicators']:
            if regex.search(content):
                matched_indicators.append(desc)
        
        # 检查可选指标 (增加置信度)
        for regex, desc in rule['optional_indicators']:
            if regex.search(content):
                matched_indicators.append(f"[可选] {desc}")
        
        # 计算匹配数和置信度
        total_indicators = len(rule['indicators'])
        required_matched = sum(1 for desc in matched_indicators if not desc.startswith('[可选]'))
        
        # 至少需要匹配所有必须指标
        if required_matched < rule['min_matches']:
            return None
        
        # v6.2.1 修复: credential_theft 和 data_exfiltration 至少需要 3 个指标
        # 2 个指标太容易误报 (如: token + requests)
        category = rule.get('category', '')
        total_matched = len(matched_indicators)  # 包含可选指标
        if category in ('credential_theft', 'data_exfiltration') and total_matched < 3:
            return None
        
        # v6.2.1 修复: memory_pollution 至少需要 3 个指标 (包含可选)
        if category == 'memory_pollution' and total_matched < 3:
            return None
        
        # 计算置信度
        optional_matched = sum(1 for desc in matched_indicators if desc.startswith('[可选]'))
        confidence = min((required_matched + optional_matched * 0.5) / (total_indicators + len(rule['optional_indicators']) * 0.5), 1.0)
        
        # 计算分数
        base_score = rule['base_score']
        optional_bonus = min(optional_matched * 5, 15)  # 可选指标最多 +15
        score = min(base_score + optional_bonus, 100)
        
        # 配置文件适当降低置信度 (配置文件可能有误报)
        if is_config and score < 80:
            confidence *= 0.8
        
        # 脚本文件提高置信度
        if is_script:
            confidence = min(confidence * 1.1, 1.0)
        
        return CompositeMatch(
            category=rule['category'],
            score=int(score),
            matched_indicators=matched_indicators,
            total_indicators=total_indicators,
            confidence=round(confidence, 2),
            description=rule['description'],
            severity=rule['severity']
        )
    
    def get_category_stats(self, matches: List[CompositeMatch]) -> Dict[str, Dict]:
        """获取各类别的统计信息"""
        stats = {}
        for match in matches:
            if match.category not in stats:
                stats[match.category] = {
                    'count': 0,
                    'max_score': 0,
                    'max_confidence': 0,
                    'rules': []
                }
            
            stats[match.category]['count'] += 1
            stats[match.category]['max_score'] = max(stats[match.category]['max_score'], match.score)
            stats[match.category]['max_confidence'] = max(stats[match.category]['max_confidence'], match.confidence)
            stats[match.category]['rules'].append(match.description)
        
        return stats


def scan_file_composite(file_path: str) -> List[CompositeMatch]:
    """便捷函数: 扫描单个文件"""
    detector = CompositeDetector()
    content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
    return detector.scan(content, file_path)


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("用法: python3 composite_detector.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    detector = CompositeDetector()
    
    print(f"\n🔍 扫描文件: {file_path}")
    print("=" * 60)
    
    content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
    matches = detector.scan(content, file_path)
    
    if not matches:
        print("✅ 未检测到组合攻击模式")
    else:
        print(f"⚠️  检测到 {len(matches)} 个组合攻击模式:\n")
        
        # 按类别分组
        from collections import defaultdict
        by_category = defaultdict(list)
        for m in matches:
            by_category[m.category].append(m)
        
        for category, category_matches in by_category.items():
            print(f"📁 {category}:")
            for m in category_matches:
                print(f"  ├── [{m.severity}] {m.description}")
                print(f"  │   分数: {m.score} | 置信度: {m.confidence}")
                print(f"  │   匹配指标 ({len(m.matched_indicators)}/{m.total_indicators}):")
                for indicator in m.matched_indicators[:5]:
                    print(f"  │   • {indicator}")
                if len(m.matched_indicators) > 5:
                    print(f"  │   ... 还有 {len(m.matched_indicators) - 5} 个")
                print()
