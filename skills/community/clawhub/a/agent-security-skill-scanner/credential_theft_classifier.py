"""
Credential Theft Risk Classifier for Security Scanner v6.2.0

检测凭据窃取的完整攻击链：
1. 诱导获取凭据 (Inducement)
2. 混淆隐藏意图 (Obfuscation)  
3. 外发窃取凭据 (Exfiltration)

类似于 curl_risk_classifier 的思路，对凭据相关行为进行风险分级。
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import IntEnum


class CredentialRiskLevel(IntEnum):
    """凭据风险等级"""
    SAFE = 0
    LOW = 1      # 正常凭据访问
    MEDIUM = 2   # 可疑凭据行为
    HIGH = 3     # 组合可疑行为
    CRITICAL = 4  # 明确的凭据窃取攻击链


# 敏感路径/文件 (高风险)
SENSITIVE_PATHS = [
    # SSH 凭据
    r'\.ssh/id_rsa', r'\.ssh/id_ed25519', r'\.ssh/authorized_keys',
    r'\.ssh/known_hosts',
    # 云凭据
    r'\.aws/credentials', r'\.aws/config', r'aws_access_key', r'aws_secret',
    r'\.azure/', r'azure_credentials',
    r'\.gcloud/', r'google_credentials',
    # Git/Docker 凭据
    r'\.git-credentials', r'\.netrc', r'\.docker/config.json',
    # 配置文件中的凭据
    r'\.env', r'\.env\.\w+', r'config.*\.json', r'credentials\.json',
    r'apikey', r'api_key', r'secret', r'token',
    # OpenClaw/Agent 凭据
    r'\.openclaw/openclaw\.json', r'\.openclaw/.*\.json',
    r'workspace/TOOLS\.md', r'workspace/MEMORY\.md',
    # 钱包/加密
    r'wallet\.json', r'keystore', r'\.gnupg/', r'ssh-agent',
]

# 凭据窃取诱导模式
INDUCEMENT_PATTERNS = [
    # 伪装的授权请求
    (r'(?i)(verify|check|validate|scan).*(credential|token|auth|key)',
     '伪装验证获取凭据'),
    (r'(?i)(enter|input|provide).*(password|token|key|secret|credential)',
     '诱导用户输入凭据'),
    (r'(?i)(save|store|export).*(credential|token|key|secret)',
     '伪装存储凭据'),
    (r'(?i)(refresh|renew|update).*(token|credential)',
     '伪装刷新令牌'),
    # 钓鱼相关
    (r'(?i)(urgent|immediate|action.required|verify.account)',
     '钓鱼话术诱导'),
    (r'(?i)(click.*link|open.*attachment|login.*here)',
     '钓鱼链接诱导'),
    # 伪装的诊断/修复
    (r'(?i)(diagnostic|debug|fix|repair).*(credential|token|auth)',
     '伪装诊断获取凭据'),
    (r'(?i)(security.*scan|vulnerability.*check|audit)',
     '伪装安全扫描获取凭据'),
]

# 混淆模式
OBFUSCATION_PATTERNS = [
    # Base64 混淆
    (r'base64.*(-d|--decode|decode)', 'Base64 解码操作'),
    (r'echo.*\|.*base64', 'Base64 编码字符串'),
    (r'import.*base64|from.*base64', 'Python Base64 导入'),
    # Hex 混淆
    (r'\\x[0-9a-f]{2}', 'Hex 编码字符'),
    (r'\\\\x', '双重转义 Hex'),
    # 字符串拼接混淆
    (r'["\']\s*\+\s*["\']', '字符串拼接'),
    (r'\+\s*["\']', '字符串拼接变量'),
    # Shell 混淆
    (r'\$?\([^\)]+\)', '命令替换'),
    (r'`[^`]+`', '反引号命令执行'),
    (r'eval\s*\(', 'Eval 动态执行'),
    (r'exec\s*\(', 'Exec 动态执行'),
    # 编码转换
    (r'chr\(', '字符编码转换'),
    (r'ord\(', '字符转编码'),
    (r'format\(.*%', '字符串格式化混淆'),
]

# 外发模式
EXFILTRATION_PATTERNS = [
    # 网络外发
    (r'curl.*(-X\s*POST|--post|-d\s*@)', 'Curl POST 外发'),
    (r'wget.*(-O|--output)', 'Wget 下载外发'),
    (r'requests\.(post|put)', 'Python HTTP POST'),
    (r'httpx\.(post|put)', 'HTTPX HTTP POST'),
    (r'fetch\([^)]*(post|put)', 'JS Fetch POST'),
    (r'\.post\(', '通用 POST 请求'),
    # 邮件外发
    (r'smtplib|sendmail|mail\(', '邮件外发'),
    # DNS 外发
    (r'dig\s+@|nslookup', 'DNS 查询外发'),
    # 文件外发
    (r'tar\s+czf.*\|', '压缩打包外发'),
    (r'gzip.*\|.*curl', '压缩数据外发'),
    # 隐蔽外发
    (r'2>&1\s*\|', '隐藏输出管道'),
    (r'>\s*/dev/null', '静默执行'),
    (r'\.git/', 'Git 外发'),
    (r'git\s+push', 'Git Push 外发'),
]

# 凭据读取模式
CREDENTIAL_ACCESS_PATTERNS = [
    (r'open\([^)]*\(id_rsa|credential|secret|key\)', '读取私钥/凭据'),
    (r'cat\s+.*\.(json|env|yaml|yml|cfg|conf)', '读取配置文件'),
    (r'cat\s+.*\$HOME', '读取用户目录文件'),
    (r'getenv\(|os\.environ', '读取环境变量'),
    (r'keyring\.|keyring\.get_password', '读取系统密钥环'),
    (r'passlib|pysftp|paramiko', '凭据使用库'),
]


@dataclass
class CredentialRiskResult:
    """凭据风险检测结果"""
    level: CredentialRiskLevel
    pattern: str           # 匹配的检测模式
    reason: str           # 用户可理解的原因
    matched_content: str  # 匹配的代码片段
    confidence: int        # 置信度 0-100
    attack_chain: List[str]  # 检测到的攻击链步骤


class CredentialTheftClassifier:
    """
    凭据窃取风险分类器
    
    检测凭据窃取的完整攻击链，而不仅仅是单个关键词。
    类似 curl_risk_classifier 的分级思路：
    - LOW: 正常凭据访问（白名单工具、白名单路径）
    - MEDIUM: 可疑凭据行为（单独出现）
    - HIGH: 组合可疑行为（凭据访问+网络请求等）
    - CRITICAL: 明确的攻击链（诱导+混淆+外发）
    """
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """预编译正则表达式"""
        import re
        
        self._sensitive_paths = [re.compile(p, re.I) for p in SENSITIVE_PATHS]
        
        self._inducement_patterns = [(re.compile(p, re.I | re.DOTALL), msg) 
                                     for p, msg in INDUCEMENT_PATTERNS]
        self._obfuscation_patterns = [(re.compile(p, re.I | re.DOTALL), msg) 
                                      for p, msg in OBFUSCATION_PATTERNS]
        self._exfil_patterns = [(re.compile(p, re.I | re.DOTALL), msg) 
                                for p, msg in EXFILTRATION_PATTERNS]
        self._access_patterns = [(re.compile(p, re.I | re.DOTALL), msg) 
                                for p, msg in CREDENTIAL_ACCESS_PATTERNS]
    
    def classify_credential_behavior(self, content: str) -> List[CredentialRiskResult]:
        """
        分析内容中的凭据窃取风险
        
        Returns:
            按风险等级排序的检测结果列表 (最高风险在前)
        """
        results = []
        
        # 1. 检测凭据访问
        access_found = []
        for pattern, msg in self._access_patterns:
            match = pattern.search(content)
            if match:
                access_found.append({
                    'pattern': msg,
                    'matched': match.group()[:80]
                })
        
        # 2. 检测诱导模式
        inducement_found = []
        for pattern, msg in self._inducement_patterns:
            match = pattern.search(content)
            if match:
                inducement_found.append({
                    'pattern': msg,
                    'matched': match.group()[:80]
                })
        
        # 3. 检测混淆模式
        obfuscation_found = []
        for pattern, msg in self._obfuscation_patterns:
            match = pattern.search(content)
            if match:
                obfuscation_found.append({
                    'pattern': msg,
                    'matched': match.group()[:80]
                })
        
        # 4. 检测外发模式
        exfil_found = []
        for pattern, msg in self._exfil_patterns:
            match = pattern.search(content)
            if match:
                exfil_found.append({
                    'pattern': msg,
                    'matched': match.group()[:80]
                })
        
        # 5. 检测敏感路径访问
        sensitive_access = []
        for pattern in self._sensitive_paths:
            match = pattern.search(content)
            if match:
                sensitive_access.append({
                    'pattern': '敏感路径访问',
                    'matched': match.group()[:80]
                })
        
        # 6. 分析攻击链组合
        attack_chain = []
        if inducement_found:
            attack_chain.append('诱导获取凭据')
        if sensitive_access:
            attack_chain.append('访问敏感路径')
        if obfuscation_found:
            attack_chain.append('混淆隐藏意图')
        if exfil_found:
            attack_chain.append('外发数据')
        
        # 7. 风险分级判定
        critical_indicators = len(inducement_found) + len(sensitive_access) + len(exfil_found)
        obfuscation_count = len(obfuscation_found)
        
        if critical_indicators >= 3 and obfuscation_count >= 1:
            # CRITICAL: 诱导/窃取 + 混淆 + 外发 = 明确攻击链
            level = CredentialRiskLevel.CRITICAL
            reason = f"检测到凭据窃取攻击链: {' + '.join(attack_chain)}"
            confidence = 95
        elif critical_indicators >= 2 and obfuscation_count >= 1:
            # HIGH: 多种可疑行为 + 混淆
            level = CredentialRiskLevel.HIGH
            reason = f"检测到组合可疑行为: {' + '.join(attack_chain[:2])}"
            confidence = 80
        elif critical_indicators >= 2:
            # MEDIUM: 多种可疑行为
            level = CredentialRiskLevel.MEDIUM
            reason = f"存在可疑凭据行为: {attack_chain[0] if attack_chain else '凭据相关'}"
            confidence = 65
        elif len(sensitive_access) >= 1 or len(inducement_found) >= 1:
            # LOW: 单个可疑行为
            level = CredentialRiskLevel.LOW
            reason = f"检测到凭据相关操作: {attack_chain[0] if attack_chain else '凭据访问'}"
            confidence = 50
        else:
            # SAFE: 无明显风险
            level = CredentialRiskLevel.SAFE
            reason = "未检测到凭据窃取风险"
            confidence = 0
            attack_chain = []
        
        # 构建结果
        if attack_chain or level > CredentialRiskLevel.SAFE:
            results.append(CredentialRiskResult(
                level=level,
                pattern='ATTACK_CHAIN' if len(attack_chain) > 1 else 'SINGLE_BEHAVIOR',
                reason=reason,
                matched_content=', '.join([a for a in attack_chain]),
                confidence=confidence,
                attack_chain=attack_chain
            ))
        
        # 如果有具体的模式匹配，也添加到结果
        for item in inducement_found[:2]:
            results.append(CredentialRiskResult(
                level=CredentialRiskLevel.MEDIUM,
                pattern='INDUCEMENT',
                reason=item['pattern'],
                matched_content=item['matched'],
                confidence=75,
                attack_chain=['诱导获取凭据']
            ))
        
        for item in obfuscation_found[:3]:
            results.append(CredentialRiskResult(
                level=CredentialRiskLevel.MEDIUM,
                pattern='OBFUSCATION',
                reason=item['pattern'],
                matched_content=item['matched'],
                confidence=70,
                attack_chain=['混淆隐藏意图']
            ))
        
        for item in exfil_found[:3]:
            results.append(CredentialRiskResult(
                level=CredentialRiskLevel.HIGH,
                pattern='EXFILTRATION',
                reason=item['pattern'],
                matched_content=item['matched'],
                confidence=85,
                attack_chain=['外发数据']
            ))
        
        # 按风险等级排序
        results.sort(key=lambda x: -x.level.value)
        
        # 去重，保留最高风险
        seen = set()
        unique_results = []
        for r in results:
            if r.pattern not in seen:
                seen.add(r.pattern)
                unique_results.append(r)
        
        return unique_results[:5]  # 最多返回 5 个结果
    
    def is_whitelisted(self, content: str) -> bool:
        """检查是否是白名单行为"""
        import re
        
        # 白名单模式
        whitelist = [
            r'keyring\.get_password',  # 正常读取密钥环
            r'getpass\.getpass',         # 安全输入密码
            r'os\.getenv\(["\']\w+["\']',  # 读取环境变量（常见操作）
            r'password\s*=\s*input',    # 用户输入密码
            r'argparse\.add_argument\(["\']--password',  # 命令行参数
        ]
        
        for p in whitelist:
            if re.search(p, content, re.I):
                return True
        return False


# 全局实例 (延迟初始化)
_credential_classifier = None

def get_credential_classifier() -> CredentialTheftClassifier:
    """获取全局凭据分类器"""
    global _credential_classifier
    if _credential_classifier is None:
        _credential_classifier = CredentialTheftClassifier()
    return _credential_classifier


def generate_credential_report(content: str) -> dict:
    """生成凭据风险报告"""
    classifier = get_credential_classifier()
    
    if classifier.is_whitelisted(content):
        return {
            'has_credential_risk': False,
            'level': 'SAFE',
            'findings': [],
            'attack_chain': [],
            'summary': '白名单行为，无风险'
        }
    
    results = classifier.classify_credential_behavior(content)
    
    if not results:
        return {
            'has_credential_risk': False,
            'level': 'SAFE',
            'findings': [],
            'attack_chain': [],
            'summary': '未检测到凭据窃取风险'
        }
    
    # 最高风险
    highest = results[0]
    
    return {
        'has_credential_risk': True,
        'level': highest.level.name,
        'level_value': highest.level.value,
        'confidence': highest.confidence,
        'findings': [
            {
                'pattern': r.pattern,
                'reason': r.reason,
                'matched': r.matched_content[:100],
                'severity': r.level.name
            }
            for r in results
        ],
        'attack_chain': highest.attack_chain,
        'summary': highest.reason,
        'user_guidance': _generate_guidance(highest),
    }


def _generate_guidance(result: CredentialRiskResult) -> str:
    """生成用户指导"""
    if result.level == CredentialRiskLevel.CRITICAL:
        return "🔴 检测到凭据窃取攻击链！立即停止使用，检查是否有凭据泄露。"
    elif result.level == CredentialRiskLevel.HIGH:
        return "🟠 检测到可疑凭据行为组合，建议检查数据流向。"
    elif result.level == CredentialRiskLevel.MEDIUM:
        return "🟡 检测到凭据相关可疑操作，建议确认用途。"
    elif result.level == CredentialRiskLevel.LOW:
        return "🟢 检测到凭据访问操作，确认是否为正常用途。"
    return "✅ 未检测到凭据窃取风险。"
