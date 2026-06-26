#!/usr/bin/env python3
"""
🛡️ 安全工具识别器 (v6.2.0)

识别技能是否为安全/运维工具，调整风险等级评估
核心逻辑：安全工具的"危险行为"可能是正常运维操作
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SecurityToolDetector:
    """安全工具检测器"""
    
    # ========== 工具类型分类 ==========
    
    TOOL_CATEGORIES = {
        # 安全监控类
        'security_monitor': {
            'keywords': ['security', 'monitor', 'scan', 'audit', 'guard', 'shield', 'defender'],
            'patterns': [
                r'security.*scan',
                r'monitor.*alert',
                r'audit.*log',
                r'defend.*attack',
            ],
            'risk_adjustment': -20,  # 风险降低 20%
            'description': '安全监控/审计工具'
        },
        
        # 网络管理类
        'network_admin': {
            'keywords': ['router', 'switch', 'firewall', 'vpn', 'network', 'ping', 'traceroute'],
            'patterns': [
                r'router.*manage',
                r'network.*admin',
                r'firewall.*rule',
                r'vpn.*connect',
            ],
            'risk_adjustment': -15,
            'description': '网络管理工具'
        },
        
        # 运维工具类
        'ops_tool': {
            'keywords': ['backup', 'deploy', 'drift', 'version', 'config', 'provision'],
            'patterns': [
                r'version.*drift',
                r'config.*manage',
                r'deploy.*script',
                r'backup.*restore',
            ],
            'risk_adjustment': -10,
            'description': '运维/配置管理工具'
        },
        
        # 渗透测试类
        'pentest_tool': {
            'keywords': ['pentest', 'exploit', 'nmap', 'metasploit', 'burp', 'owasp'],
            'patterns': [
                r'pentest.*tool',
                r'exploit.*detect',
                r'nmap.*scan',
                r'vulnerability.*assess',
            ],
            'risk_adjustment': -5,  # 渗透测试工具风险降低较少
            'description': '渗透测试/漏洞评估工具'
        },
        
        # 开发工具类
        'dev_tool': {
            'keywords': ['generator', 'scaffold', 'template', 'boilerplate', 'cli'],
            'patterns': [
                r'project.*generator',
                r'code.*scaffold',
                r'template.*engine',
                r'cli.*tool',
            ],
            'risk_adjustment': -10,
            'description': '开发/代码生成工具'
        },
    }
    
    # ========== 正常运维行为模式 ==========
    
    LEGITIMATE_OPS_PATTERNS = [
        # 版本查询
        (r'docker\s+--version', 'docker version check'),
        (r'nginx\s+-v', 'nginx version check'),
        (r'python3?\s+--version', 'python version check'),
        (r'node\s+-v', 'node version check'),
        (r'npm\s+list', 'npm package list'),
        
        # 系统检查
        (r'ss\s+-', 'socket status check'),
        (r'lsof\s+', 'open files check'),
        (r'ps\s+', 'process list'),
        (r'netstat\s+', 'network stats'),
        
        # 网络诊断
        (r'ping\s+-', 'ping diagnostic'),
        (r'traceroute\s+', 'traceroute'),
        (r'dig\s+', 'DNS query'),
        (r'nslookup\s+', 'DNS lookup'),
        
        # API 查询
        (r'api\.github\.com/repos', 'GitHub API'),
        (r'registry\.npmjs\.org', 'npm registry'),
        (r'pypi\.org/p/', 'PyPI API'),
        (r'hub\.docker\.com', 'Docker Hub'),
    ]
    
    # ========== 风险调整规则 ==========
    
    RISK_ADJUSTMENTS = {
        # 安全工具 + 正常运维行为 = 降低风险
        'security_tool + shell_exec': {
            'condition': 'tool_type in [security_monitor, pentest_tool] AND behavior in [shell_exec, subprocess]',
            'adjustment': -15,
            'reason': '安全工具执行 shell 命令可能是正常审计操作'
        },
        'network_admin + network_call': {
            'condition': 'tool_type == network_admin AND behavior == network_call',
            'adjustment': -20,
            'reason': '网络管理工具需要网络访问'
        },
        'ops_tool + config_read': {
            'condition': 'tool_type == ops_tool AND behavior == config_read',
            'adjustment': -10,
            'reason': '运维工具读取配置是正常操作'
        },
        'dev_tool + subprocess': {
            'condition': 'tool_type == dev_tool AND behavior == subprocess',
            'adjustment': -10,
            'reason': '代码生成工具可能需要 subprocess 执行构建命令'
        },
    }
    
    def __init__(self):
        self.compiled_patterns = {}
        self._compile_patterns()
    
    def _compile_patterns(self):
        """预编译正则表达式"""
        for category, info in self.TOOL_CATEGORIES.items():
            self.compiled_patterns[category] = [
                re.compile(p, re.IGNORECASE) for p in info['patterns']
            ]
    
    def detect_tool_type(self, skill_path: str, content: str = '') -> Dict:
        """
        检测技能工具类型
        
        Args:
            skill_path: 技能路径
            content: 文件内容 (可选)
            
        Returns:
            {
                'tool_type': str,
                'confidence': float,
                'category': str,
                'risk_adjustment': int,
                'reason': str
            }
        """
        # 从路径提取关键词
        path_lower = skill_path.lower()
        path_parts = path_lower.split('/')
        
        # 1. 路径关键词匹配
        path_scores = {}
        for category, info in self.TOOL_CATEGORIES.items():
            score = 0
            for keyword in info['keywords']:
                if keyword in path_lower:
                    score += 10
                # 检查是否在目录名中
                for part in path_parts:
                    if keyword in part:
                        score += 5
            if score > 0:
                path_scores[category] = score
        
        # 2. 内容模式匹配
        content_scores = {}
        if content:
            for category, patterns in self.compiled_patterns.items():
                score = 0
                for pattern in patterns:
                    if pattern.search(content):
                        score += 15
                if score > 0:
                    content_scores[category] = score
        
        # 3. 综合评分
        all_scores = {}
        for cat in set(list(path_scores.keys()) + list(content_scores.keys())):
            all_scores[cat] = path_scores.get(cat, 0) + content_scores.get(cat, 0)
        
        if not all_scores:
            return {
                'tool_type': 'unknown',
                'confidence': 0.0,
                'category': None,
                'risk_adjustment': 0,
                'reason': '无法识别工具类型'
            }
        
        # 选择最高分
        best_category = max(all_scores, key=all_scores.get)
        best_score = all_scores[best_category]
        confidence = min(best_score / 30.0, 1.0)  # 归一化到 0-1
        
        return {
            'tool_type': self.TOOL_CATEGORIES[best_category]['description'],
            'confidence': round(confidence, 2),
            'category': best_category,
            'risk_adjustment': self.TOOL_CATEGORIES[best_category]['risk_adjustment'],
            'reason': f'路径匹配得分{path_scores.get(best_category, 0)}, 内容匹配得分{content_scores.get(best_category, 0)}'
        }
    
    def check_legitimate_behavior(self, content: str) -> List[Dict]:
        """
        检查内容是否包含正常运维行为模式
        
        Args:
            content: 文件内容
            
        Returns:
            [{pattern, description, count}]
        """
        findings = []
        for pattern, desc in self.LEGITIMATE_OPS_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                findings.append({
                    'pattern': pattern,
                    'description': desc,
                    'count': len(matches)
                })
        return findings
    
    def adjust_risk_level(self, original_risk: str, tool_type: str, 
                         behaviors: List[str]) -> Dict:
        """
        根据工具类型和行为调整风险等级
        
        Args:
            original_risk: 原始风险等级 (CRITICAL/HIGH/MEDIUM/LOW/SAFE)
            tool_type: 工具类型
            behaviors: 检测到的行为列表
            
        Returns:
            {
                'original_risk': str,
                'adjusted_risk': str,
                'adjustment': int,
                'reason': str
            }
        """
        risk_scores = {
            'CRITICAL': 100,
            'HIGH': 75,
            'MEDIUM': 50,
            'LOW': 25,
            'SAFE': 0
        }
        
        original_score = risk_scores.get(original_risk, 50)
        adjustment = 0
        reasons = []
        
        # 根据工具类型调整
        for category, info in self.TOOL_CATEGORIES.items():
            if category in tool_type.lower() or info['description'] in tool_type:
                adjustment += info['risk_adjustment']
                reasons.append(f'{info["description"]} 风险调整 {info["risk_adjustment"]}')
        
        # 根据行为调整
        for behavior in behaviors:
            for rule_key, rule in self.RISK_ADJUSTMENTS.items():
                if behavior.lower() in rule_key.lower():
                    adjustment += rule['adjustment']
                    reasons.append(rule['reason'])
        
        # 计算调整后分数
        adjusted_score = max(0, min(100, original_score + adjustment))
        
        # 映射回风险等级
        if adjusted_score >= 80:
            adjusted_risk = 'CRITICAL'
        elif adjusted_score >= 60:
            adjusted_risk = 'HIGH'
        elif adjusted_score >= 40:
            adjusted_risk = 'MEDIUM'
        elif adjusted_score >= 20:
            adjusted_risk = 'LOW'
        else:
            adjusted_risk = 'SAFE'
        
        return {
            'original_risk': original_risk,
            'adjusted_risk': adjusted_risk,
            'adjustment': adjustment,
            'reason': '; '.join(reasons) if reasons else '无调整'
        }


# ========== 全局实例 ==========
security_tool_detector = SecurityToolDetector()
