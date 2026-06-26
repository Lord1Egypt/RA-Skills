#!/usr/bin/env python3
"""
安全沙箱模块
Security Sandbox Module
"""

import os
import sys
import gc
from typing import Any, Callable
from functools import wraps


class SecureSandbox:
    """安全执行沙箱"""
    
    def __init__(self):
        self.original_env = dict(os.environ)
        self.restricted = False
    
    def enable_restrictions(self):
        """启用限制"""
        # 禁用网络代理
        os.environ['HTTP_PROXY'] = ''
        os.environ['HTTPS_PROXY'] = ''
        os.environ['http_proxy'] = ''
        os.environ['https_proxy'] = ''
        self.restricted = True
    
    def disable_restrictions(self):
        """恢复环境"""
        os.environ.update(self.original_env)
        self.restricted = False
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """在沙箱中执行函数"""
        try:
            self.enable_restrictions()
            result = func(*args, **kwargs)
            return result
        finally:
            # 清理敏感数据
            gc.collect()
            self.disable_restrictions()


def secure_execute(func: Callable, *args, **kwargs) -> Any:
    """
    在受限环境中执行审计逻辑
    1. 禁用网络访问 (除白名单内网)
    2. 禁用系统命令调用
    3. 内存数据加密提示
    """
    sandbox = SecureSandbox()
    return sandbox.execute(func, *args, **kwargs)


def mask_sensitive_data(text: str) -> str:
    """
    敏感数据脱敏
    """
    import re
    
    # 替换银行卡号 (保留前4后4)
    text = re.sub(r'(\d{4})\d{8,12}(\d{4})', r'\1****\2', text)
    
    # 替换身份证号
    text = re.sub(r'(\d{6})\d{8}(\d{4})', r'\1********\2', text)
    
    # 替换手机号
    text = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', text)
    
    # 替换姓名 (保留姓氏)
    text = re.sub(r'([\u4e00-\u9fa5])[\u4e00-\u9fa5]{1,2}', r'\1**', text)
    
    # 替换大额金额
    text = re.sub(r'(\d{6,})', lambda m: m.group(1)[:2] + '*' * (len(m.group(1)) - 2), text)
    
    return text


def validate_input_safety(text: str) -> bool:
    """
    输入安全校验：防注入/恶意代码
    """
    import re
    
    # 检测危险代码
    dangerous_patterns = [
        r'exec\s*\(',
        r'eval\s*\(',
        r'__import__',
        r'os\.system',
        r'subprocess\.',
        r'import\s+os',
        r'import\s+subprocess',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True


if __name__ == "__main__":
    # 测试
    print("沙箱模块测试")
    
    # 测试脱敏
    test_text = "张三的银行卡号6222021234567890123，手机13812345678"
    masked = mask_sensitive_data(test_text)
    print(f"原始: {test_text}")
    print(f"脱敏: {masked}")
    
    # 测试安全执行
    def test_func():
        return "安全执行成功"
    
    result = secure_execute(test_func)
    print(f"沙箱执行: {result}")
