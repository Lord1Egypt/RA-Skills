#!/usr/bin/env python3
"""
claw-security-suite
第三层：运行时实时防护
检测并阻止提示注入、命令注入、SSRF等攻击，自动净化输入
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

# 攻击模式匹配
# 注意：patterns 用于检测攻击，以下是常见攻击特征关键词
PROMPT_INJECTION_PATTERNS = [
    # 直接指令覆盖
    r'ignore.*previous.*instruct',
    r'ignore.*above.*instruct',
    r'forget.*previous.*instruct',
    r'disregard.*previous',
    # 提权/系统提示符
    r'system:|SYSTEM:|### System',
    r'\[SYSTEM\]|\<SYSTEM\>',
    # 注入后门
    r'from now on you will',
    r'you are now going to act as',
    r'you are now',
    r'your new instruct.* are',
    # 越狱
    r'DAN\|do anything now',
    r'reflectively\%20accessible',
    r'repeat the words above',
    # 敏感操作诱导
    r'execute the following commands',
    r'run the following code',
    r'ignore all safety guide',
    r'disregard safety proto',
]

COMMAND_INJECTION_PATTERNS = [
    r';.*rm',
    r'&&.*rm',
    r'\|\s*rm',
    r';.*curl',
    r'&&.*curl',
    r'\|\s*curl',
    r';.*wget',
    r'&&.*wget',
    r'\|\s*wget',
    r';.*python\s+-c',
    r'&&.*bash',
    r'\$\(.*\)',
    r'`.*`',
]

SSRF_PATTERNS = [
    r'http://169\.254\.169\.254',
    r'http://127\.0\.0\.1',
     r'http://localhost',
    r'http://10\.',
    r'http://172\.(1[6-9]|2[0-9]|3[0-1])\.',
    r'http://192\.168\.',
    r'file://',
    r'gopher://',
    r'dict://',
]

@dataclass
class CheckResult:
    is_malicious: bool
    attack_type: Optional[str]
    reason: str
    clean_input: str
    matched: List[str]

class RuntimeProtector:
    def __init__(self):
        self.pi_patterns = [re.compile(p, re.I) for p in PROMPT_INJECTION_PATTERNS]
        self.ci_patterns = [re.compile(p, re.I) for p in COMMAND_INJECTION_PATTERNS]
        self.ssrf_patterns = [re.compile(p) for p in SSRF_PATTERNS]
    
    def check_prompt_injection(self, text: str) -> Tuple[bool, Optional[str]]:
        """检查提示注入"""
        for pattern in self.pi_patterns:
            match = pattern.search(text)
            if match:
                return True, f"检测到提示注入模式: {match.group(0)}"
        return False, None
    
    def check_command_injection(self, text: str) -> Tuple[bool, Optional[str]]:
        """检查命令注入"""
        for pattern in self.ci_patterns:
            match = pattern.search(text)
            if match:
                return True, f"检测到命令注入模式: {match.group(0)}"
        return False, None
    
    def check_ssrf(self, text: str) -> Tuple[bool, Optional[str]]:
        """检查SSRF"""
        for pattern in self.ssrf_patterns:
            match = pattern.search(text)
            if match:
                return True, f"检测到SSRF内网访问尝试: {match.group(0)}"
        return False, None
    
    def check(self, text: str) -> CheckResult:
        """综合检查用户输入"""
        matched = []
        is_malicious = False
        attack_type = None
        reason = ""
        
        # 检查提示注入
        pi_match, pi_reason = self.check_prompt_injection(text)
        if pi_match:
            is_malicious = True
            attack_type = "prompt_injection"
            reason = pi_reason
            matched.append("prompt_injection")
        
        # 检查命令注入
        if not is_malicious:
            ci_match, ci_reason = self.check_command_injection(text)
            if ci_match:
                is_malicious = True
                attack_type = "command_injection"
                reason = ci_reason
                matched.append("command_injection")
        
        # 检查SSRF
        if not is_malicious:
            ssrf_match, ssrf_reason = self.check_ssrf(text)
            if ssrf_match:
                is_malicious = True
                attack_type = "ssrf"
                reason = ssrf_reason
                matched.append("ssrf")
        
        return CheckResult(
            is_malicious=is_malicious,
            attack_type=attack_type,
            reason=reason,
            clean_input=text,  # 如果需要净化，可以在这里处理
            matched=matched
        )
    
    def sanitize(self, text: str) -> str:
        """净化输入，移除可疑模式"""
        # 简单净化：移除换行后的命令注入
        sanitized = text
        for pattern in self.ci_patterns:
            sanitized = pattern.sub('[removed]', sanitized)
        return sanitized

def check_input(text: str) -> CheckResult:
    """对外接口：检查用户输入"""
    protector = RuntimeProtector()
    return protector.check(text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} \"<input_text>\"")
        print(f"Example: python {sys.argv[0]} \"ignore[space]previous[space]instructions\"")
        sys.exit(1)
    
    text = sys.argv[1]
    result = check_input(text)
    
    if result.is_malicious:
        print(f"❌ 检测到恶意输入: {result.attack_type}")
        print(f"  原因: {result.reason}")
        sys.exit(1)
    else:
        print("✅ 输入安全，未检测到攻击")
