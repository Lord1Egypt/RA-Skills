"""
Risk Tier Classifier for Security Scanner v6.2.0

统一风险等级标准，并提供用户可理解的解释和操作建议。
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum, IntEnum


class RiskLevel(IntEnum):
    """标准化风险等级 (IntEnum 支持数值比较)"""
    SAFE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    
    def __str__(self):
        return self.name


# 风险等级描述和用户建议
RISK_TIER_INFO = {
    RiskLevel.CRITICAL: {
        "icon": "🔴",
        "title": "严重威胁",
        "description": "包含明确的恶意行为，如远程代码执行、数据外发、后门程序等",
        "user_action": "立即停止使用，确认来源，必要时隔离系统",
        "auto_action": "建议阻断",
        "examples": [
            "curl unknown_url | bash",
            "反向Shell连接",
            "凭据外发到外部服务器",
            "持久化后门"
        ]
    },
    RiskLevel.HIGH: {
        "icon": "🟠",
        "title": "高风险",
        "description": "存在潜在恶意模式或可疑行为，需要进一步核实",
        "user_action": "确认代码来源和用途，谨慎使用",
        "auto_action": "建议人工复核",
        "examples": [
            "subprocess 执行未知命令",
            "写入系统目录",
            "访问敏感文件"
        ]
    },
    RiskLevel.MEDIUM: {
        "icon": "🟡",
        "title": "中风险",
        "description": "存在一定风险，但可能是正常的工具行为",
        "user_action": "检查上下文，确认是否符合预期",
        "auto_action": "记录日志",
        "examples": [
            "执行系统命令",
            "网络请求",
            "文件读写"
        ]
    },
    RiskLevel.LOW: {
        "icon": "🟢",
        "title": "低风险",
        "description": "基本安全，但包含可能需要关注的模式",
        "user_action": "例行检查即可",
        "auto_action": "仅记录",
        "examples": [
            "白名单工具调用",
            "常见开发操作"
        ]
    },
    RiskLevel.SAFE: {
        "icon": "✅",
        "title": "安全",
        "description": "未检测到明显风险",
        "user_action": "无需操作",
        "auto_action": "通过",
        "examples": []
    }
}


@dataclass
class RiskTierResult:
    """风险分级结果"""
    level: RiskLevel
    score: int  # 0-100
    tier_info: Dict
    matched_categories: List[str]
    findings_summary: str
    user_guidance: str


class RiskTierClassifier:
    """
    风险分级分类器 - 将检测结果转换为用户可理解的风险等级
    
    判定逻辑:
    1. 分析所有 findings 的风险类型组合
    2. 确定最高风险等级
    3. 生成用户可理解的风险描述
    4. 提供操作建议
    """
    
    # 攻击类别 → 风险等级映射
    CATEGORY_RISK_MAP = {
        # 最高风险 - 明确恶意
        'reverse_shell': RiskLevel.CRITICAL,
        'c2_communication': RiskLevel.CRITICAL,
        'data_exfiltration': RiskLevel.CRITICAL,
        'credential_theft': RiskLevel.CRITICAL,
        'supply_chain_attack': RiskLevel.CRITICAL,
        'backdoor': RiskLevel.CRITICAL,
        'trojan': RiskLevel.CRITICAL,
        
        # 高风险 - 潜在恶意
        'remote_code_execution': RiskLevel.HIGH,
        'arbitrary_execution': RiskLevel.HIGH,
        'command_injection': RiskLevel.HIGH,
        'privilege_escalation': RiskLevel.HIGH,
        'persistence': RiskLevel.HIGH,
        'model_poisoning': RiskLevel.HIGH,
        'prompt_injection': RiskLevel.HIGH,
        'tool_poisoning': RiskLevel.HIGH,
        
        # 中风险 - 可疑行为
        'network_request': RiskLevel.MEDIUM,
        'file_write': RiskLevel.MEDIUM,
        'subprocess': RiskLevel.MEDIUM,
        'credential_access': RiskLevel.MEDIUM,
        'obfuscation': RiskLevel.MEDIUM,
        'memory_pollution': RiskLevel.MEDIUM,
        
        # 低风险 - 正常行为但需注意
        'resource_usage': RiskLevel.LOW,
        'benign_pattern': RiskLevel.LOW,
        'safe_call': RiskLevel.LOW,
    }
    
    def __init__(self):
        self._build_tier_lookup()
    
    def _build_tier_lookup(self):
        """构建分类查找表"""
        self._category_to_risk = {}
        for cat, level in self.CATEGORY_RISK_MAP.items():
            self._category_to_risk[cat.lower()] = level
    
    def normalize_risk_level(self, level: str) -> RiskLevel:
        """
        标准化风险等级字符串
        
        支持格式: "CRITICAL", "critical", "HIGH", "high", "MEDIUM", "medium", "LOW", "low"
        """
        if not level:
            return RiskLevel.SAFE
        
        upper = level.upper().strip()
        
        try:
            return RiskLevel(upper)
        except ValueError:
            # 处理非标准格式
            mapping = {
                'CRIT': RiskLevel.CRITICAL,
                'ERROR': RiskLevel.CRITICAL,
                'HI': RiskLevel.HIGH,
                'MED': RiskLevel.MEDIUM,
                'WARN': RiskLevel.MEDIUM,
                'LO': RiskLevel.LOW,
            }
            for key, val in mapping.items():
                if upper.startswith(key):
                    return val
            return RiskLevel.MEDIUM  # 默认中风险
    
    def classify_findings(self, findings: List[Dict], 
                         curl_findings: List[Dict] = None,
                         composite_findings: List[Dict] = None) -> RiskTierResult:
        """
        根据所有 findings 分类风险等级
        
        Args:
            findings: 规则匹配结果
            curl_findings: curl 风险分级结果
            composite_findings: 组合检测结果
        """
        all_categories = set()
        max_level = RiskLevel.SAFE
        max_score = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        
        # 分析原始 findings
        for f in findings:
            cat = f.get('category', 'unknown').lower()
            sev = f.get('severity', 'MEDIUM')
            score = f.get('score', f.get('confidence', 50))
            
            level = self.normalize_risk_level(sev)
            all_categories.add(cat)
            
            if level == RiskLevel.CRITICAL:
                critical_count += 1
            elif level == RiskLevel.HIGH:
                high_count += 1
            elif level == RiskLevel.MEDIUM:
                medium_count += 1
            
            # 更新最高风险 (使用 enum 直接比较)
            if level > max_level:
                max_level = level
                max_score = score
            elif level == max_level and score > max_score:
                max_score = score
        
        # 分析 curl findings
        if curl_findings:
            for cf in curl_findings:
                sev = cf.get('severity', 'MEDIUM')
                score = cf.get('score', 50)
                level = self.normalize_risk_level(sev)
                all_categories.add('network_curl')
                
                if level == RiskLevel.CRITICAL:
                    critical_count += 1
                elif level == RiskLevel.HIGH:
                    high_count += 1
                    
                if level > max_level:
                    max_level = level
                    max_score = score
        
        # 分析 composite findings
        if composite_findings:
            for cf in composite_findings:
                sev = cf.get('severity', 'MEDIUM')
                score = cf.get('score', 50)
                cat = cf.get('category', 'unknown').lower()
                level = self.normalize_risk_level(sev)
                
                all_categories.add(cat)
                
                if level == RiskLevel.CRITICAL:
                    critical_count += 1
                elif level == RiskLevel.HIGH:
                    high_count += 1
                    
                if level > max_level:
                    max_level = level
                    max_score = score
        
        # 生成摘要
        summary_parts = []
        if critical_count > 0:
            summary_parts.append(f"{critical_count} 个严重威胁")
        if high_count > 0:
            summary_parts.append(f"{high_count} 个高风险")
        if medium_count > 0:
            summary_parts.append(f"{medium_count} 个中风险")
        
        findings_summary = "，".join(summary_parts) if summary_parts else "无明显风险"
        
        # 生成用户指导
        tier_info = RISK_TIER_INFO.get(max_level, RISK_TIER_INFO[RiskLevel.SAFE])
        user_guidance = self._generate_guidance(max_level, all_categories, 
                                                critical_count, high_count)
        
        return RiskTierResult(
            level=max_level,
            score=min(max_score, 100),
            tier_info=tier_info,
            matched_categories=list(all_categories),
            findings_summary=findings_summary,
            user_guidance=user_guidance
        )
    
    def _generate_guidance(self, level: RiskLevel, categories: set,
                           critical_count: int, high_count: int) -> str:
        """生成用户指导建议"""
        if level == RiskLevel.CRITICAL:
            if 'reverse_shell' in categories or 'c2_communication' in categories:
                return "⚠️ 检测到反向Shell或C2通信！建议立即隔离并检查系统。"
            elif 'data_exfiltration' in categories:
                return "⚠️ 检测到数据外发行为！建议检查是否有敏感数据泄露。"
            elif 'supply_chain_attack' in categories:
                return "⚠️ 检测到可疑供应链攻击模式！建议暂停使用并核实来源。"
            else:
                return "🔴 检测到严重威胁！建议立即停止使用此技能。"
        
        elif level == RiskLevel.HIGH:
            if 'command_injection' in categories or 'arbitrary_execution' in categories:
                return "🟠 检测到命令执行风险！建议核实所有外部输入的来源。"
            elif 'persistence' in categories:
                return "🟠 检测到持久化尝试！建议检查是否有多余的启动项。"
            else:
                return "🟠 存在高风险行为，请确认代码来源可信。"
        
        elif level == RiskLevel.MEDIUM:
            if 'network_request' in categories:
                return "🟡 存在网络请求行为，请确认目标地址可信。"
            elif 'file_write' in categories:
                return "🟡 存在文件写入操作，请确认写入位置和内容。"
            else:
                return "🟡 存在可疑行为，建议查看详情并确认用途。"
        
        elif level == RiskLevel.LOW:
            return "🟢 基本安全，例行检查即可。"
        
        return "✅ 未检测到明显风险。"
    
    def generate_risk_report(self, scan_result: Dict) -> Dict:
        """
        为扫描结果生成增强的风险报告
        
        返回包含用户友好信息的报告结构
        """
        findings = scan_result.get('composite_findings', [])
        curl_findings = scan_result.get('curl_findings', [])
        
        tier_result = self.classify_findings(
            findings=findings,
            curl_findings=curl_findings,
            composite_findings=findings
        )
        
        # 构建增强报告
        report = {
            'file': scan_result.get('file', ''),
            'filename': scan_result.get('file', '').split('/')[-1],
            
            # 标准化风险等级 (使用 name 获取字符串)
            'risk_level': tier_result.level.name,
            'risk_icon': tier_result.tier_info['icon'],
            'risk_title': tier_result.tier_info['title'],
            'risk_description': tier_result.tier_info['description'],
            
            # 分数和统计
            'risk_score': tier_result.score,
            'findings_count': scan_result.get('findings_count', 0),
            'findings_summary': tier_result.findings_summary,
            
            # 匹配类别
            'matched_categories': tier_result.matched_categories,
            
            # 用户指导
            'user_action': tier_result.tier_info['user_action'],
            'user_guidance': tier_result.user_guidance,
            'auto_action': tier_result.tier_info['auto_action'],
            
            # 原始数据 (保留)
            'original_risk_level': scan_result.get('risk_level'),
            'matched_rules': scan_result.get('matched_rules', [])[:10],
            'curl_findings': curl_findings,
            'composite_findings': findings[:10],
        }
        
        return report


# 全局实例
_risk_tier_classifier = None

def get_risk_tier_classifier() -> RiskTierClassifier:
    """获取全局风险分级分类器"""
    global _risk_tier_classifier
    if _risk_tier_classifier is None:
        _risk_tier_classifier = RiskTierClassifier()
    return _risk_tier_classifier
