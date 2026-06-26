#!/usr/bin/env python3
"""
Claw Ethics Checker - Core Module
伦理合规检查器核心模块
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import re

class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "low"      # 低风险
    MEDIUM = "medium" # 中风险
    HIGH = "high"    # 高风险

@dataclass
class EthicsCheckResult:
    """伦理检查结果"""
    risk_level: RiskLevel          # 风险等级
    is_compliant: bool             # 是否合规
    needs_human_review: bool       # 是否需要人工审核
    recommendations: List[str]     # 建议列表
    warnings: List[str]            # 警告列表
    legal_issues: List[str]        # 法律问题列表
    ethical_concerns: List[str]    # 伦理问题列表
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'risk_level': self.risk_level.value,
            'is_compliant': self.is_compliant,
            'needs_human_review': self.needs_human_review,
            'recommendations': self.recommendations,
            'warnings': self.warnings,
            'legal_issues': self.legal_issues,
            'ethical_concerns': self.ethical_concerns
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

class EthicsChecker:
    """伦理合规检查器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化伦理检查器
        
        Args:
            config: 配置字典，可包含：
                - risk_threshold: 风险阈值 (low/medium/high)
                - require_human_review: 是否要求人工审核
                - log_decisions: 是否记录决策
        """
        self.config = config or {}
        self.risk_threshold = self.config.get('risk_threshold', 'medium')
        self.require_human_review = self.config.get('require_human_review', True)
        self.log_decisions = self.config.get('log_decisions', True)
        
        # 加载规则数据库
        self.load_rules()
        
        # 决策日志
        self.decision_log: List[Dict[str, Any]] = []
    
    def load_rules(self):
        """加载伦理规则数据库"""
        # 这里可以连接外部数据库或加载本地规则文件
        # 目前使用内置规则
        self.rules = {
            'privacy': {
                'keywords': ['personal data', 'private information', 'user data', '敏感信息', '个人数据', '隐私'],
                'rules': [
                    '不收集个人身份信息',
                    '不存储敏感数据', 
                    '遵守GDPR/CCPA等隐私法规',
                    '数据匿名化处理',
                    '获取用户明确同意'
                ]
            },
            'security': {
                'keywords': ['hack', 'bypass', 'exploit', 'attack', '入侵', '绕过', '破解', '漏洞'],
                'rules': [
                    '不进行未授权访问',
                    '不绕过安全措施',
                    '不进行DDoS攻击',
                    '不利用安全漏洞',
                    '遵守计算机安全法'
                ]
            },
            'legal': {
                'keywords': ['competitor', 'scrape', 'monitor', '竞争对手', '爬取', '监控'],
                'rules': [
                    '遵守当地法律法规',
                    '尊重知识产权',
                    '不参与非法活动',
                    '遵守反不正当竞争法',
                    '遵守数据保护法'
                ]
            },
            'ethical': {
                'keywords': ['harm', 'damage', 'deceive', '欺骗', '损害', '伤害'],
                'rules': [
                    '不损害他人利益',
                    '保持透明度',
                    '公平竞争',
                    '不欺骗用户',
                    '承担社会责任'
                ]
            }
        }
    
    def analyze_task(self, task_description: str, task_details: Dict[str, Any]) -> EthicsCheckResult:
        """
        分析任务伦理合规性
        
        Args:
            task_description: 任务描述
            task_details: 任务详细信息
            
        Returns:
            EthicsCheckResult: 检查结果
        """
        # 初始化结果
        recommendations: List[str] = []
        warnings: List[str] = []
        legal_issues: List[str] = []
        ethical_concerns: List[str] = []
        
        # 合并文本用于检查
        combined_text = f"{task_description} {json.dumps(task_details, ensure_ascii=False)}".lower()
        
        # 检查各个维度
        privacy_violation = self._check_privacy_violation(combined_text)
        security_violation = self._check_security_violation(combined_text)
        legal_checks = self._check_legal_compliance(combined_text, task_details)
        ethical_checks = self._check_ethical_concerns(combined_text)
        
        # 收集问题
        if privacy_violation:
            warnings.append('可能涉及隐私侵犯')
            ethical_concerns.append('隐私保护问题')
            recommendations.append('进行数据匿名化处理')
            recommendations.append('获取用户明确同意')
        
        if security_violation:
            warnings.append('可能涉及安全违规')
            legal_issues.append('可能违反计算机安全法')
            recommendations.append('使用合法授权的方法')
            recommendations.append('避免安全绕过行为')
        
        legal_issues.extend(legal_checks)
        ethical_concerns.extend(ethical_checks)
        
        # 根据问题数量生成额外建议
        if legal_checks:
            recommendations.append('咨询法律专家')
            recommendations.append('审查相关法律法规')
        
        if ethical_checks:
            recommendations.append('进行伦理影响评估')
            recommendations.append('考虑替代方案')
        
        # 确定风险等级
        risk_level = self._determine_risk_level(
            len(warnings), 
            len(legal_issues), 
            len(ethical_concerns)
        )
        
        # 生成总体建议
        if risk_level == RiskLevel.HIGH:
            recommendations.insert(0, '建议拒绝此任务')
            recommendations.insert(1, '必须进行人工审核')
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.insert(0, '建议修改任务方案')
            recommendations.insert(1, '建议进行人工审核')
        else:
            recommendations.insert(0, '任务基本合规')
            if self.require_human_review:
                recommendations.insert(1, '建议简单审核')
        
        # 是否需要人工审核
        needs_human_review = (
            risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH] or 
            self.require_human_review
        )
        
        # 创建结果
        result = EthicsCheckResult(
            risk_level=risk_level,
            is_compliant=(risk_level == RiskLevel.LOW),
            needs_human_review=needs_human_review,
            recommendations=list(set(recommendations)),  # 去重
            warnings=list(set(warnings)),
            legal_issues=list(set(legal_issues)),
            ethical_concerns=list(set(ethical_concerns))
        )
        
        # 记录决策
        if self.log_decisions:
            self._log_decision(task_description, task_details, result)
        
        return result
    
    def _check_privacy_violation(self, text: str) -> bool:
        """检查隐私侵犯"""
        privacy_keywords = self.rules['privacy']['keywords']
        for keyword in privacy_keywords:
            if keyword.lower() in text:
                return True
        return False
    
    def _check_security_violation(self, text: str) -> bool:
        """检查安全违规"""
        security_keywords = self.rules['security']['keywords']
        for keyword in security_keywords:
            if keyword.lower() in text:
                return True
        return False
    
    def _check_legal_compliance(self, text: str, task_details: Dict[str, Any]) -> List[str]:
        """检查法律合规性"""
        issues = []
        
        # 检查竞争对手相关
        if any(word in text for word in ['competitor', '竞争对手']):
            if 'scrape' in text or '爬取' in text:
                issues.append('可能违反反不正当竞争法')
                issues.append('需要审查数据获取方式')
        
        # 检查监控相关
        if 'monitor' in text or '监控' in text:
            if 'user' in text or '用户' in text:
                issues.append('需要用户明确同意')
                issues.append('可能涉及隐私法规')
        
        # 检查数据来源
        data_source = task_details.get('data_source', '').lower()
        if 'unauthorized' in data_source or '未授权' in data_source:
            issues.append('数据来源未授权')
            issues.append('可能违反数据保护法')
        
        return issues
    
    def _check_ethical_concerns(self, text: str) -> List[str]:
        """检查伦理问题"""
        concerns = []
        
        # 检查损害相关
        if any(word in text for word in ['harm', 'damage', '损害', '伤害']):
            concerns.append('可能损害他人利益')
        
        # 检查欺骗相关
        if any(word in text for word in ['deceive', 'cheat', '欺骗', '作弊']):
            concerns.append('涉及欺骗行为')
            concerns.append('违反诚信原则')
        
        # 检查公平性
        if 'unfair' in text or '不公平' in text:
            concerns.append('可能涉及不公平竞争')
        
        return concerns
    
    def _determine_risk_level(self, warnings: int, legal_issues: int, ethical_concerns: int) -> RiskLevel:
        """确定风险等级"""
        total_issues = warnings + legal_issues + ethical_concerns
        
        # 高风险条件
        if legal_issues > 0 or total_issues >= 3:
            return RiskLevel.HIGH
        
        # 中风险条件
        elif total_issues >= 1:
            return RiskLevel.MEDIUM
        
        # 低风险
        else:
            return RiskLevel.LOW
    
    def _log_decision(self, task_description: str, task_details: Dict[str, Any], result: EthicsCheckResult):
        """记录决策"""
        log_entry = {
            'task_description': task_description,
            'task_details': task_details,
            'result': result.to_dict(),
            'timestamp': self._get_timestamp()
        }
        self.decision_log.append(log_entry)
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_decision_log(self) -> List[Dict[str, Any]]:
        """获取决策日志"""
        return self.decision_log
    
    def clear_decision_log(self):
        """清空决策日志"""
        self.decision_log.clear()
    
    def export_decision_log(self, filepath: str):
        """导出决策日志到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.decision_log, f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    # 创建检查器
    checker = EthicsChecker()
    
    # 测试用例
    test_task = {
        'description': '分析用户行为数据以改进产品',
        'client': '科技公司',
        'methods': ['data_analysis', 'machine_learning'],
        'data_source': '用户同意收集的数据'
    }
    
    result = checker.analyze_task('用户行为分析', test_task)
    
    print("🧪 Claw Ethics Checker 示例")
    print("=" * 50)
    print(f"任务: {test_task['description']}")
    print(f"风险等级: {result.risk_level.value}")
    print(f"是否合规: {result.is_compliant}")
    print(f"需要人工审核: {result.needs_human_review}")
    print(f"建议: {', '.join(result.recommendations)}")
    
    if result.warnings:
        print(f"警告: {', '.join(result.warnings)}")
    
    if result.legal_issues:
        print(f"法律问题: {', '.join(result.legal_issues)}")
    
    if result.ethical_concerns:
        print(f"伦理问题: {', '.join(result.ethical_concerns)}")