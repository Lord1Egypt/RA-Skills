#!/usr/bin/env python3
"""
🔧 配置文件识别器

自动识别 JSON/YAML 配置文件，分离统计
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


class ConfigFileDetector:
    """配置文件检测器"""
    
    # 配置文件扩展名
    CONFIG_EXTENSIONS = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'}
    
    # 可执行代码特征
    CODE_PATTERNS = [
        r'function\s+\w+\s*\(',  # 函数定义
        r'def\s+\w+\s*\(',       # Python 函数
        r'class\s+\w+',          # 类定义
        r'import\s+\w+',         # 导入语句
        r'require\s*\(',         # Node.js require
        r'from\s+\w+\s+import',  # Python from import
        r'Invoke-Expression',    # PowerShell IEX
        r'Invoke-Command',       # PowerShell 远程
        r'eval\s*\(',            # eval 执行
        r'exec\s*\(',            # exec 执行
        r'subprocess\.',         # 子进程
        r'os\.system',           # 系统调用
        r'\.DownloadString',     # 下载执行
        r'IEX\s*\(',             # PowerShell IEX
    ]
    
    # 恶意配置特征
    MALICIOUS_CONFIG_PATTERNS = [
        r'attacker',
        r'malicious',
        r'exploit',
        r'payload',
        r'backdoor',
        r'reverse.*shell',
        r'c2.*server',
        r'exfil',
        r'steal.*credential',
    ]
    
    # 白名单模式 - 这些文件名/模式是安全的 Agent 配置文件
    SAFE_CONFIG_PATTERNS = [
        # Agent 核心配置
        r'agent-manifest\.json$',
        r'agent_skills\.json$',
        r'agent_roles\.yaml$',
        r'agent_prompts\.yaml$',
        r'agent[-_]?coordination\.json$',
        r'ai-agent\.json$',
        r'.*_schema_.*\.(json|yaml)$',
        r'tool_contract\.json$',
        r'executor.*\.json$',
        r'eval[s]?\.(json|yaml)$',
        r'sample-eval\.json$',
        
        # 工作流和节点配置
        r'workflows/.*\.json$',
        r'.*-handler\.json$',
        r'.*-flow\.json$',
        r'.*-node\.json$',
        r'.*\.flow\.json$',
        
        # 配置目录
        r'config/.*\.yaml$',
        r'config/.*\.json$',
        r'examples/.*\.json$',
        
        # 安全/监控配置 (通常是误报)
        r'agentguard\.yaml$',
        r'.*guard\.yaml$',
        r'.*monitor.*\.yaml$',
        r'.*security.*\.yaml$',
        
        # 检测规则/模式库 (误报高发)
        r'.*injection.*\.json$',
        r'.*patterns.*\.json$',
        r'.*-patterns\.json$',
        r'.*_patterns\.json$',
        r'.*commander.*\.json$',
        r'.*tokenizer.*\.json$',
        
        # 数据样本文件 (误报)
        r'sample-data.*\.json$',
        r'.*-data\.json$',
        r'.*_data\.json$',
        r'.*commands.*\.json$',
        r'dangerous-commands\.json$',
        
        # exfil/payload 相关 (通常在排除列表或变量名中)
        r'exfil.*\.(json|yaml)$',
        r'.*exfil\.(json|yaml)$',
    ]
    
    def is_config_file(self, file_path: str, content: str) -> bool:
        """
        判断是否为配置文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
        
        Returns:
            True=配置文件，False=代码文件
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        
        # 检查扩展名
        if ext not in self.CONFIG_EXTENSIONS:
            return False
        
        # 检查是否包含可执行代码
        for pattern in self.CODE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return False  # 包含代码，不是纯配置文件
        
        return True  # 纯配置文件
    
    def is_safe_config(self, file_path: str, content: str) -> bool:
        """
        检查配置文件是否在白名单中（安全的 Agent 配置文件）
        
        Args:
            file_path: 文件路径
            content: 文件内容
        
        Returns:
            True=安全配置，False=需要检查
        """
        for pattern in self.SAFE_CONFIG_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False
    
    def has_malicious_config(self, file_path: str, content: str) -> bool:
        """
        检查配置文件是否包含恶意配置
        
        策略：
        - 白名单内的配置文件：完全信任（Agent 配置等）
        - 黑名单文件名：直接标记为恶意
        - 其他配置文件：检查内容中的恶意特征
        
        Args:
            file_path: 文件路径
            content: 文件内容
        
        Returns:
            True=恶意配置，False=正常配置
        """
        # 1. 白名单内的配置文件完全信任
        if self.is_safe_config(file_path, content):
            return False
        
        # 2. 黑名单文件名直接标记为恶意
        BLACKLIST_FILENAMES = [
            r'malicious.*\.(json|yaml)$',
            r'backdoor.*\.(json|yaml)$',
            r'C2[_-]?server.*\.(json|yaml)$',
            r'attacker.*\.(json|yaml)$',
        ]
        
        for pattern in BLACKLIST_FILENAMES:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        
        # 3. 其他配置文件检查内容中的恶意特征
        # 使用更精确的恶意特征（避免误报）
        MALICIOUS_INDICATORS = [
            # 明确的恶意命令执行
            r'curl.*\|.*bash',
            r'curl.*\|.*sh',
            r'wget.*\|.*bash',
            r'wget.*\|.*sh',
            r'curl.*&&.*bash',
            r'wget.*&&.*python',
            
            # 明确的凭据窃取
            r'steal.*credential',
            r'exfil.*data',
            r'exfiltrat.*data',
            
            # 明确的后门/C2
            r'reverse.*shell',
            r'c2.*server',
            r'backdoor.*install',
            
            # 明确的攻击者域名
            r'attacker\.com',
            r'evil\.com',
            r'malicious-site',
        ]
        
        for pattern in MALICIOUS_INDICATORS:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        # 默认安全
        return False
    
    def classify_file(self, file_path: str, content: str) -> Tuple[str, str]:
        """
        分类文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
        
        Returns:
            (文件类型，风险等级)
            文件类型：config/code
            风险等级：safe/suspicious/malicious
        """
        # YAML/JSON 文件如果是攻击样本，应该进入正常扫描流程
        # 只有纯配置（不含代码）才走配置检测
        
        # 检查是否包含代码特征
        code_indicators = [
            'system_prompt', 'user_input', 'attack_config', 'payload',
            'injection', 'malicious', 'bypass', 'ignore', 'disregard',
            'exec(', 'eval(', 'import ', 'def ', 'function ', 'class ',
            # remote_load 特征
            'curl', 'wget', 'bash', 'python', 'sh', 'script',
            'http', 'https', 'pipe',
            # resource_exhaustion 特征 - 这些应该进入扫描流程
            'fork_bomb', 'memory_attack', 'allocation_storm', 'cpu_hog',
            'memory_hog', 'spawn_rate', 'max_processes'
        ]
        
        content_lower = content.lower()
        has_code = any(ind in content_lower for ind in code_indicators)
        
        if has_code:
            # 包含代码特征，进入正常扫描流程
            return ('code', 'unknown')
        
        # 纯配置文件才走配置检测
        if self.is_config_file(file_path, content):
            if self.has_malicious_config(file_path, content):
                return ('config', 'malicious')
            else:
                return ('config', 'safe')
        else:
            return ('code', 'unknown')


# 测试
if __name__ == '__main__':
    detector = ConfigFileDetector()
    
    # 测试用例
    test_cases = [
        ('test.json', '{"name": "test"}', 'config', 'safe'),
        ('test.yaml', 'name: test', 'config', 'safe'),
        ('test.ps1', 'IEX (New-Object Net.WebClient)', 'code', 'unknown'),
        ('evil.json', '{"c2_server": "attacker.com"}', 'config', 'malicious'),
    ]
    
    print("=== 配置文件识别器测试 ===")
    for file_path, content, expected_type, expected_risk in test_cases:
        file_type, risk = detector.classify_file(file_path, content)
        status = "✅" if (file_type == expected_type and risk == expected_risk) else "❌"
        print(f"{status} {file_path}: {file_type}/{risk} (期望：{expected_type}/{expected_risk})")
    
    print("\n✅ 配置文件识别器测试完成")
