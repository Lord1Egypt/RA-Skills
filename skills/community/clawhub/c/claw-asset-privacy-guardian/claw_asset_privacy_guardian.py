#!/usr/bin/env python3
"""
Claw Asset & Privacy Guardian - 资产与隐私守护者
保护数字资产和隐私信息，不暴露主人的敏感信息
"""

import os
import re
import json
import yaml
import hashlib
import logging
import warnings
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import time
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 禁用一些警告
warnings.filterwarnings('ignore')

class RiskLevel(Enum):
    """风险评估等级"""
    CRITICAL = "critical"      # 严重风险
    HIGH = "high"              # 高风险  
    MEDIUM = "medium"          # 中等风险
    LOW = "low"                # 低风险
    INFO = "info"              # 信息性

class ProtectionCategory(Enum):
    """保护类别"""
    SENSITIVE_INFO = "sensitive_info"       # 敏感信息
    ACCOUNT_SECURITY = "account_security"   # 账号安全
    PRIVACY_SETTINGS = "privacy_settings"   # 隐私设置
    ASSET_SECURITY = "asset_security"       # 资产安全
    DATA_LEAK = "data_leak"                 # 数据泄露
    CONFIGURATION = "configuration"         # 配置问题

@dataclass
class PrivacyFinding:
    """隐私和安全发现"""
    id: str                           # 唯一标识（匿名化）
    category: ProtectionCategory      # 问题类别
    risk_level: RiskLevel             # 风险等级
    issue_type: str                   # 问题类型（通用描述）
    description: str                  # 问题描述（匿名化）
    location: str                     # 位置（匿名化处理）
    recommendation: str               # 修复建议
    detector_name: str                # 检测器名称
    
    # 隐私保护字段
    anonymized: bool = True           # 是否已匿名化
    sensitive_info_exposed: bool = False  # 是否暴露敏感信息
    auto_fixable: bool = False        # 是否可自动修复
    
    # 时间戳
    detected_at: float = field(default_factory=time.time)

@dataclass
class PrivacyReport:
    """隐私保护报告"""
    scan_id: str                      # 扫描ID（匿名）
    total_files: int                  # 总文件数
    scanned_files: int                # 已扫描文件数
    findings: List[PrivacyFinding] = field(default_factory=list)  # 所有发现
    scan_duration: float = 0.0        # 扫描耗时（秒）
    
    # 隐私保护统计
    sensitive_files_found: int = 0    # 发现敏感信息的文件数
    anonymized_findings: int = 0      # 已匿名化的发现数
    
    # 风险统计
    def risk_statistics(self) -> Dict[str, int]:
        """计算风险统计"""
        stats = {level.value: 0 for level in RiskLevel}
        for finding in self.findings:
            stats[finding.risk_level.value] += 1
        return stats
    
    def has_critical_or_high(self) -> bool:
        """是否有严重或高风险"""
        for finding in self.findings:
            if finding.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                return True
        return False
    
    def to_anonymous_dict(self) -> Dict[str, Any]:
        """转换为匿名化字典（不暴露敏感信息）"""
        result = {
            "scan_id": self.scan_id,
            "total_files": self.total_files,
            "scanned_files": self.scanned_files,
            "findings_count": len(self.findings),
            "sensitive_files_found": self.sensitive_files_found,
            "anonymized_findings": self.anonymized_findings,
            "scan_duration": self.scan_duration,
            "risk_statistics": self.risk_statistics(),
            "has_critical_or_high": self.has_critical_or_high(),
            "findings": []
        }
        
        # 匿名化每个发现
        for finding in self.findings:
            anonymous_finding = {
                "id": finding.id,
                "category": finding.category.value,
                "risk_level": finding.risk_level.value,
                "issue_type": finding.issue_type,
                "description": finding.description,
                "location": self._anonymize_location(finding.location),
                "recommendation": finding.recommendation,
                "detector_name": finding.detector_name,
                "anonymized": finding.anonymized,
                "sensitive_info_exposed": finding.sensitive_info_exposed,
                "auto_fixable": finding.auto_fixable
            }
            result["findings"].append(anonymous_finding)
        
        return result
    
    def to_anonymous_json(self) -> str:
        """转换为匿名化JSON"""
        return json.dumps(self.to_anonymous_dict(), indent=2, ensure_ascii=False)
    
    def _anonymize_location(self, location: str) -> str:
        """匿名化位置信息"""
        # 移除用户名等敏感信息
        location = location.replace(os.path.expanduser("~"), "~")
        
        # 通用化路径
        common_patterns = {
            r'/home/[^/]+/': '~/',
            r'/Users/[^/]+/': '~/',
            r'C:\\Users\\[^\\]+\\': '~\\',
        }
        
        for pattern, replacement in common_patterns.items():
            location = re.sub(pattern, replacement, location)
        
        return location

class Anonymizer:
    """匿名化处理器"""
    
    @staticmethod
    def anonymize_text(text: str, context: str = "") -> str:
        """匿名化文本中的敏感信息"""
        if not text:
            return text
        
        # 移除电子邮件
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
        
        # 移除电话号码
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_REDACTED]', text)
        
        # 移除身份证/社保号等
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', text)
        
        # 移除加密货币地址（部分）
        text = re.sub(r'\b(0x)?[A-Fa-f0-9]{40,}\b', '[CRYPTO_ADDRESS_REDACTED]', text)
        
        # 移除API密钥模式
        text = re.sub(r'\b(sk|pk)_[a-zA-Z0-9_\-]{20,}\b', '[API_KEY_REDACTED]', text)
        
        # 移除JWT令牌
        text = re.sub(r'\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b', '[JWT_TOKEN_REDACTED]', text)
        
        return text
    
    @staticmethod
    def anonymize_finding_description(description: str, original_text: str = "") -> str:
        """匿名化问题描述"""
        # 通用问题描述模板
        templates = {
            "api_key": "检测到API密钥硬编码",
            "private_key": "检测到私钥文件或内容",
            "password": "检测到密码硬编码",
            "email": "检测到电子邮件地址",
            "phone": "检测到电话号码",
            "crypto_wallet": "检测到加密货币钱包地址",
            "jwt_token": "检测到JWT令牌",
            "database_url": "检测到数据库连接字符串",
            "aws_key": "检测到AWS凭证",
        }
        
        # 尝试匹配已知模式
        for key, template in templates.items():
            if key in description.lower():
                return template
        
        # 通用匿名化
        return "检测到敏感信息泄露"

class BasePrivacyDetector:
    """隐私检测器基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
        self.anonymizer = Anonymizer()
        
    def detect(self, file_path: str, content: str) -> List[PrivacyFinding]:
        """检测文件内容，返回匿名化的隐私发现列表"""
        raise NotImplementedError("子类必须实现detect方法")
    
    def should_skip_file(self, file_path: str) -> bool:
        """是否跳过该文件"""
        skip_patterns = [
            r'node_modules/',
            r'\.git/',
            r'__pycache__/',
            r'\.pyc$',
            r'\.log$',
            r'\.tmp$',
            r'\.cache$',
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False
    
    def _create_finding(self, 
                       category: ProtectionCategory,
                       risk_level: RiskLevel,
                       issue_type: str,
                       description: str,
                       location: str,
                       recommendation: str,
                       original_evidence: str = "") -> PrivacyFinding:
        """创建匿名化的发现"""
        # 匿名化描述
        anonymized_description = self.anonymizer.anonymize_finding_description(description, original_evidence)
        
        # 检查是否可能暴露敏感信息
        sensitive_exposed = self._check_sensitive_exposure(original_evidence)
        
        # 生成匿名ID
        anonymous_id = f"priv_{hashlib.md5(f'{location}:{issue_type}'.encode()).hexdigest()[:8]}"
        
        return PrivacyFinding(
            id=anonymous_id,
            category=category,
            risk_level=risk_level,
            issue_type=issue_type,
            description=anonymized_description,
            location=location,
            recommendation=recommendation,
            detector_name=self.name,
            anonymized=True,
            sensitive_info_exposed=sensitive_exposed,
            auto_fixable=False
        )
    
    def _check_sensitive_exposure(self, evidence: str) -> bool:
        """检查证据是否包含敏感信息"""
        sensitive_patterns = [
            r'@[A-Za-z0-9._%+-]+\.[A-Z|a-z]{2,}',  # 电子邮件
            r'\d{3}[-.]?\d{3}[-.]?\d{4}',           # 电话号码
            r'\d{3}-\d{2}-\d{4}',                   # 社保号
            r'0x[A-Fa-f0-9]{40,}',                  # 加密货币地址
            r'sk_[a-zA-Z0-9_\-]{20,}',              # Stripe密钥
            r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',  # JWT
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, evidence, re.IGNORECASE):
                return True
        return False

class SensitiveInfoDetector(BasePrivacyDetector):
    """敏感信息检测器"""
    
    def __init__(self):
        super().__init__("sensitive_info_detector", "检测敏感信息泄露")
        
        # 敏感信息模式
        self.sensitive_patterns = [
            # API密钥和令牌
            (r'(api[_-]?key|apikey)[\s=:]+["\']?([a-zA-Z0-9_\-]{20,})["\']?', 
             ProtectionCategory.SENSITIVE_INFO, RiskLevel.CRITICAL,
             "API密钥硬编码", "移除硬编码的API密钥，使用环境变量或安全存储"),
            
            # 私钥和密码
            (r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
             ProtectionCategory.SENSITIVE_INFO, RiskLevel.CRITICAL,
             "私钥文件", "将私钥移出代码库，使用安全密钥管理"),
            
            # 密码
            (r'password[\s=:]+["\']?([^\s"\']{6,})["\']?',
             ProtectionCategory.SENSITIVE_INFO, RiskLevel.HIGH,
             "密码硬编码", "移除硬编码的密码，使用环境变量或密钥管理"),
            
            # 数据库连接
            (r'(mysql|postgresql|mongodb)://[^:]+:[^@]+@',
             ProtectionCategory.SENSITIVE_INFO, RiskLevel.CRITICAL,
             "数据库凭据", "移除数据库连接字符串中的凭据"),
            
            # AWS凭证
            (r'AWS_ACCESS_KEY_ID[\s=:]+["\']?([A-Z0-9]{20})["\']?',
             ProtectionCategory.SENSITIVE_INFO, RiskLevel.CRITICAL,
             "AWS凭证", "移除AWS凭证，使用IAM角色或环境变量"),
            
            # 加密货币钱包
            (r'\b(0x)?[A-Fa-f0-9]{40,}\b',
             ProtectionCategory.ASSET_SECURITY, RiskLevel.CRITICAL,
             "加密货币地址", "保护加密货币地址和私钥"),
            
            # 个人信息
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
             ProtectionCategory.PRIVACY_SETTINGS, RiskLevel.MEDIUM,
             "电子邮件地址", "避免在代码中暴露个人信息"),
        ]
    
    def detect(self, file_path: str, content: str) -> List[PrivacyFinding]:
        if self.should_skip_file(file_path):
            return []
        
        findings = []
        
        for pattern, category, risk_level, issue_type, recommendation in self.sensitive_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                evidence = match.group(0)
                if len(evidence) > 100:
                    evidence = evidence[:100] + "..."
                
                finding = self._create_finding(
                    category=category,
                    risk_level=risk_level,
                    issue_type=issue_type,
                    description=f"检测到{issue_type}",
                    location=file_path,
                    recommendation=recommendation,
                    original_evidence=evidence
                )
                findings.append(finding)
        
        return findings

class AccountSecurityDetector(BasePrivacyDetector):
    """账号安全检测器"""
    
    def __init__(self):
        super().__init__("account_security_detector", "检查账号安全配置")
    
    def detect(self, file_path: str, content: str) -> List[PrivacyFinding]:
        if self.should_skip_file(file_path):
            return []
        
        findings = []
        
        # 检查配置文件中的账号安全设置
        if file_path.endswith('.json') or file_path.endswith('.yaml') or file_path.endswith('.yml'):
            try:
                if file_path.endswith('.json'):
                    config = json.loads(content)
                else:
                    config = yaml.safe_load(content)
                
                if isinstance(config, dict):
                    findings.extend(self._check_config_security(config, file_path))
                    
            except (json.JSONDecodeError, yaml.YAMLError):
                pass
        
        # 检查环境文件
        if '.env' in file_path.lower():
            findings.extend(self._check_env_security(content, file_path))
        
        return findings
    
    def _check_config_security(self, config: Dict, file_path: str) -> List[PrivacyFinding]:
        """检查配置文件安全"""
        findings = []
        
        # 检查是否启用双因素认证
        if self._has_auth_config(config):
            mfa_enabled = config.get('mfa', config.get('two_factor', config.get('2fa', False)))
            if not mfa_enabled:
                finding = self._create_finding(
                    category=ProtectionCategory.ACCOUNT_SECURITY,
                    risk_level=RiskLevel.MEDIUM,
                    issue_type="双因素认证缺失",
                    description="账号配置未启用双因素认证",
                    location=file_path,
                    recommendation="启用双因素认证提高账号安全性"
                )
                findings.append(finding)
        
        # 检查会话超时设置
        if self._has_session_config(config):
            session_timeout = config.get('session_timeout', config.get('timeout', 0))
            if session_timeout > 86400:  # 超过24小时
                finding = self._create_finding(
                    category=ProtectionCategory.ACCOUNT_SECURITY,
                    risk_level=RiskLevel.MEDIUM,
                    issue_type="会话超时过长",
                    description="会话超时设置过长可能带来安全风险",
                    location=file_path,
                    recommendation="缩短会话超时时间，建议不超过4小时"
                )
                findings.append(finding)
        
        return findings
    
    def _check_env_security(self, content: str, file_path: str) -> List[PrivacyFinding]:
        """检查环境文件安全"""
        findings = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 检查密码强度要求
            if 'password' in line.lower() and 'policy' not in line.lower():
                if 'min_length' not in line.lower() and 'strength' not in line.lower():
                    finding = self._create_finding(
                        category=ProtectionCategory.ACCOUNT_SECURITY,
                        risk_level=RiskLevel.LOW,
                        issue_type="密码策略缺失",
                        description="未指定密码强度要求",
                        location=f"{file_path}:{line_num}",
                        recommendation="添加密码强度策略（最小长度、复杂度要求）"
                    )
                    findings.append(finding)
        
        return findings
    
    def _has_auth_config(self, config: Dict) -> bool:
        """检查是否有认证配置"""
        auth_keys = ['auth', 'authentication', 'login', 'user', 'password']
        return any(key in str(config).lower() for key in auth_keys)
    
    def _has_session_config(self, config: Dict) -> bool:
        """检查是否有会话配置"""
        session_keys = ['session', 'timeout', 'expire', 'cookie']
        return any(key in str(config).lower() for key in session_keys)

class AssetSecurityDetector(BasePrivacyDetector):
    """资产安全检测器"""
    
    def __init__(self):
        super().__init__("asset_security_detector", "检查资产安全")
    
    def detect(self, file_path: str, content: str) -> List[PrivacyFinding]:
        if self.should_skip_file(file_path):
            return []
        
        findings = []
        
        # 检查加密货币钱包相关文件
        if self._is_crypto_related(file_path, content):
            findings.extend(self._check_crypto_security(content, file_path))
        
        # 检查财务相关配置
        if self._is_financial_related(file_path, content):
            findings.extend(self._check_financial_security(content, file_path))
        
        return findings
    
    def _is_crypto_related(self, file_path: str, content: str) -> bool:
        """检查是否与加密货币相关"""
        crypto_keywords = [
            'bitcoin', 'ethereum', 'solana', 'wallet', 'crypto',
            'blockchain', 'defi', 'nft', 'token', 'coinbase'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in crypto_keywords)
    
    def _is_financial_related(self, file_path: str, content: str) -> bool:
        """检查是否与财务相关"""
        financial_keywords = [
            'stripe', 'paypal', 'payment', 'invoice', 'transaction',
            'bank', 'account', 'finance', 'money', 'currency'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in financial_keywords)
    
    def _check_crypto_security(self, content: str, file_path: str) -> List[PrivacyFinding]:
        """检查加密货币安全"""
        findings = []
        
        # 检查助记词模式
        mnemonic_pattern = r'\b([a-z]+\s){11,23}[a-z]+\b'
        if re.search(mnemonic_pattern, content, re.IGNORECASE):
            finding = self._create_finding(
                category=ProtectionCategory.ASSET_SECURITY,
                risk_level=RiskLevel.CRITICAL,
                issue_type="加密货币助记词暴露",
                description="检测到可能的加密货币助记词",
                location=file_path,
                recommendation="立即移除助记词，使用硬件钱包或安全存储"
            )
            findings.append(finding)
        
        # 检查私钥文件
        if 'PRIVATE KEY' in content and 'BEGIN' in content:
            finding = self._create_finding(
                category=ProtectionCategory.ASSET_SECURITY,
                risk_level=RiskLevel.CRITICAL,
                issue_type="加密货币私钥暴露",
                description="检测到加密货币私钥",
                location=file_path,
                recommendation="立即移除私钥，使用安全密钥管理"
            )
            findings.append(finding)
        
        return findings
    
    def _check_financial_security(self, content: str, file_path: str) -> List[PrivacyFinding]:
        """检查财务安全"""
        findings = []
        
        # 检查支付API密钥
        payment_patterns = [
            (r'sk_(live|test)_[a-zA-Z0-9_\-]{20,}', 'Stripe密钥'),
            (r'PAYPAL-[A-Z0-9]{16,}', 'PayPal密钥'),
            (r'AKIA[0-9A-Z]{16}', 'AWS支付相关'),
        ]
        
        for pattern, key_type in payment_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                finding = self._create_finding(
                    category=ProtectionCategory.ASSET_SECURITY,
                    risk_level=RiskLevel.CRITICAL,
                    issue_type=f"支付{key_type}暴露",
                    description=f"检测到支付{key_type}",
                    location=file_path,
                    recommendation="立即移除支付密钥，使用环境变量或密钥管理"
                )
                findings.append(finding)
        
        return findings

class PrivacyGuardian:
    """隐私守护者主类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.detectors = self._initialize_detectors()
        self.anonymizer = Anonymizer()
        
        # 支持的文件扩展名
        self.supported_extensions = [
            '.py', '.js', '.ts', '.json', '.yaml', '.yml', 
            '.md', '.txt', '.sh', '.bash', '.env', '.toml',
            '.sql', '.html', '.css'
        ]
    
    def _initialize_detectors(self) -> List[BasePrivacyDetector]:
        """初始化检测器"""
        return [
            SensitiveInfoDetector(),
            AccountSecurityDetector(),
            AssetSecurityDetector(),
        ]
    
    def scan_directory(self, directory: str) -> PrivacyReport:
        """扫描目录"""
        directory = os.path.abspath(directory)
        
        logger.info(f"开始隐私安全扫描: {directory}")
        
        # 收集所有文件
        all_files = self._collect_files(directory)
        logger.info(f"找到 {len(all_files)} 个文件")
        
        # 初始化报告
        report = PrivacyReport(
            scan_id=f"scan_{hashlib.md5(f'{directory}:{time.time()}'.encode()).hexdigest()[:12]}",
            total_files=len(all_files),
            scanned_files=0,
            findings=[],
            scan_duration=0.0
        )
        
        start_time = time.time()
        
        # 扫描每个文件
        scanned_count = 0
        sensitive_files = 0
        
        for file_path in all_files:
            if not self._should_scan_file(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 运行所有检测器
                file_findings = []
                for detector in self.detectors:
                    if detector.enabled:
                        findings = detector.detect(file_path, content)
                        file_findings.extend(findings)
                
                if file_findings:
                    report.findings.extend(file_findings)
                    sensitive_files += 1
                    logger.debug(f"文件 {os.path.basename(file_path)} 发现 {len(file_findings)} 个问题")
                
                scanned_count += 1
                
            except Exception as e:
                logger.warning(f"扫描文件失败 {file_path}: {e}")
        
        report.scanned_files = scanned_count
        report.sensitive_files_found = sensitive_files
        report.anonymized_findings = len(report.findings)  # 所有发现都已匿名化
        report.scan_duration = time.time() - start_time
        
        logger.info(f"扫描完成: 扫描了 {scanned_count} 个文件，发现 {len(report.findings)} 个问题")
        
        return report
    
    def _collect_files(self, directory: str) -> List[str]:
        """收集目录中的所有文件"""
        all_files = []
        for root, dirs, files in os.walk(directory):
            # 跳过一些目录
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
            
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        
        return all_files
    
    def _should_scan_file(self, file_path: str) -> bool:
        """判断是否应该扫描该文件"""
        # 检查扩展名
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.supported_extensions:
            return True
        
        # 检查特殊文件
        special_files = ['Dockerfile', 'docker-compose.yml', 'Makefile', '.env', '.env.example']
        if os.path.basename(file_path) in special_files:
            return True
        
        # 检查没有扩展名的文件
        if not ext:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline()
                    if first_line.startswith('#!') and ('python' in first_line or 'bash' in first_line or 'sh' in first_line):
                        return True
            except:
                pass
        
        return False
    
    def generate_report(self, report: PrivacyReport, format: str = "console") -> str:
        """生成报告"""
        if format == "json":
            return report.to_anonymous_json()
        elif format == "console":
            return self._generate_console_report(report)
        elif format == "markdown":
            return self._generate_markdown_report(report)
        else:
            raise ValueError(f"不支持的报告格式: {format}")
    
    def _generate_console_report(self, report: PrivacyReport) -> str:
        """生成控制台报告"""
        try:
            import colorama
            from colorama import Fore, Style
            colorama.init()
            has_color = True
        except ImportError:
            has_color = False
        
        report_lines = []
        
        if has_color:
            report_lines.append(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            report_lines.append(f"{Fore.GREEN}Claw Asset & Privacy Guardian 报告{Style.RESET_ALL}")
            report_lines.append(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        else:
            report_lines.append("=" * 60)
            report_lines.append("Claw Asset & Privacy Guardian 报告")
            report_lines.append("=" * 60)
        
        report_lines.append(f"扫描ID: {report.scan_id}")
        report_lines.append(f"扫描时间: {report.scan_duration:.2f}秒")
        report_lines.append(f"文件统计: {report.scanned_files}/{report.total_files} 个文件已扫描")
        report_lines.append(f"敏感文件: {report.sensitive_files_found} 个")
        report_lines.append(f"匿名发现: {report.anonymized_findings} 个")
        report_lines.append("")
        
        # 隐私保护声明
        if has_color:
            report_lines.append(f"{Fore.BLUE}🔒 隐私保护声明:{Style.RESET_ALL}")
        else:
            report_lines.append("🔒 隐私保护声明:")
        report_lines.append("  • 所有报告均已匿名化处理")
        report_lines.append("  • 不包含具体敏感信息")
        report_lines.append("  • 仅显示问题类型和建议")
        report_lines.append("")
        
        # 风险统计
        stats = report.risk_statistics()
        if has_color:
            report_lines.append(f"{Fore.YELLOW}📊 风险统计:{Style.RESET_ALL}")
        else:
            report_lines.append("📊 风险统计:")
        
        for level_name, count in stats.items():
            if has_color:
                color = {
                    'critical': Fore.RED,
                    'high': Fore.LIGHTRED_EX,
                    'medium': Fore.YELLOW,
                    'low': Fore.GREEN,
                    'info': Fore.BLUE
                }.get(level_name, Fore.WHITE)
                report_lines.append(f"  {color}{level_name.upper():<10}{Style.RESET_ALL}: {count}")
            else:
                report_lines.append(f"  {level_name.upper():<10}: {count}")
        
        report_lines.append("")
        
        if not report.findings:
            if has_color:
                report_lines.append(f"{Fore.GREEN}✅ 未发现隐私和安全问题！{Style.RESET_ALL}")
            else:
                report_lines.append("✅ 未发现隐私和安全问题！")
        else:
            # 按风险等级分组
            critical_high = [f for f in report.findings if f.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]]
            medium_low = [f for f in report.findings if f.risk_level in [RiskLevel.MEDIUM, RiskLevel.LOW]]
            
            if critical_high:
                if has_color:
                    report_lines.append(f"{Fore.RED}⚠️  严重/高风险问题 ({len(critical_high)}个):{Style.RESET_ALL}")
                else:
                    report_lines.append(f"⚠️  严重/高风险问题 ({len(critical_high)}个):")
                
                for finding in critical_high[:5]:  # 只显示前5个
                    if has_color:
                        risk_color = Fore.RED if finding.risk_level == RiskLevel.CRITICAL else Fore.LIGHTRED_EX
                        report_lines.append(f"  {risk_color}● [{finding.category.value}] {finding.issue_type}{Style.RESET_ALL}")
                    else:
                        report_lines.append(f"  ● [{finding.category.value}] {finding.issue_type}")
                    report_lines.append(f"     描述: {finding.description}")
                    report_lines.append(f"     位置: {report._anonymize_location(finding.location)}")
                    report_lines.append(f"     建议: {finding.recommendation}")
                    report_lines.append("")
            
            if medium_low:
                if has_color:
                    report_lines.append(f"{Fore.YELLOW}中等/低风险问题 ({len(medium_low)}个):{Style.RESET_ALL}")
                else:
                    report_lines.append(f"中等/低风险问题 ({len(medium_low)}个):")
                
                for finding in medium_low[:3]:
                    report_lines.append(f"  ● [{finding.category.value}] {finding.issue_type}")
                    report_lines.append(f"     描述: {finding.description}")
                    report_lines.append("")
        
        if has_color:
            report_lines.append(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        else:
            report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def _generate_markdown_report(self, report: PrivacyReport) -> str:
        """生成Markdown报告"""
        report_lines = []
        report_lines.append("# Claw Asset & Privacy Guardian 报告")
        report_lines.append("")
        report_lines.append(f"**扫描ID**: `{report.scan_id}`")
        report_lines.append(f"**扫描时间**: {report.scan_duration:.2f}秒")
        report_lines.append(f"**文件统计**: {report.scanned_files}/{report.total_files} 个文件已扫描")
        report_lines.append(f"**敏感文件**: {report.sensitive_files_found} 个")
        report_lines.append(f"**匿名发现**: {report.anonymized_findings} 个")
        report_lines.append("")
        
        # 隐私保护声明
        report_lines.append("## 🔒 隐私保护声明")
        report_lines.append("")
        report_lines.append("本报告已进行匿名化处理：")
        report_lines.append("- ✅ 不包含具体敏感信息")
        report_lines.append("- ✅ 仅显示问题类型和建议")
        report_lines.append("- ✅ 所有分析在本地完成")
        report_lines.append("")
        
        # 风险统计
        stats = report.risk_statistics()
        report_lines.append("## 📊 风险统计")
        report_lines.append("")
        report_lines.append("| 风险等级 | 数量 |")
        report_lines.append("|----------|------|")
        for level_name, count in stats.items():
            if count > 0:
                report_lines.append(f"| {level_name.upper()} | {count} |")
        report_lines.append("")
        
        if not report.findings:
            report_lines.append("## ✅ 扫描结果")
            report_lines.append("")
            report_lines.append("**未发现隐私和安全问题！**")
            report_lines.append("")
            report_lines.append("您的资产和隐私保护状况良好。")
        else:
            # 按风险等级分组
            critical_high = [f for f in report.findings if f.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]]
            medium_low = [f for f in report.findings if f.risk_level in [RiskLevel.MEDIUM, RiskLevel.LOW]]
            
            if critical_high:
                report_lines.append("## ⚠️ 严重/高风险问题")
                report_lines.append("")
                for i, finding in enumerate(critical_high, 1):
                    report_lines.append(f"### {i}. [{finding.category.value.upper()}] {finding.issue_type}")
                    report_lines.append("")
                    report_lines.append(f"**风险等级**: {finding.risk_level.value.upper()}")
                    report_lines.append("")
                    report_lines.append(f"**描述**: {finding.description}")
                    report_lines.append("")
                    report_lines.append(f"**位置**: `{report._anonymize_location(finding.location)}`")
                    report_lines.append("")
                    report_lines.append(f"**建议**: {finding.recommendation}")
                    report_lines.append("")
            
            if medium_low:
                report_lines.append("## 中等/低风险问题")
                report_lines.append("")
                for i, finding in enumerate(medium_low[:10], 1):
                    report_lines.append(f"{i}. **[{finding.category.value}] {finding.issue_type}**")
                    report_lines.append(f"   - 风险: {finding.risk_level.value}")
                    report_lines.append(f"   - 描述: {finding.description}")
                    report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("*报告生成工具: Claw Asset & Privacy Guardian v0.1.0*")
        report_lines.append("*隐私保护: 所有分析在本地完成，不发送任何数据到外部*")
        
        return "\n".join(report_lines)

# 命令行接口
def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claw Asset & Privacy Guardian - 资产与隐私守护者')
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('--format', choices=['console', 'json', 'markdown'], default='console',
                       help='报告格式 (default: console)')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 检查路径是否存在
    if not os.path.exists(args.directory):
        print(f"错误: 路径不存在: {args.directory}")
        sys.exit(1)
    
    # 运行扫描
    guardian = PrivacyGuardian()
    report = guardian.scan_directory(args.directory)
    
    # 生成报告
    report_content = guardian.generate_report(report, args.format)
    
    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"报告已保存到: {args.output}")
    else:
        print(report_content)
    
    # 退出码：如果有严重或高风险，返回非零
    if report.has_critical_or_high():
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()