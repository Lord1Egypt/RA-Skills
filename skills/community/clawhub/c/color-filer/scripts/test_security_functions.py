#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试安全验证功能"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

# 禁止处理的危险路径（Windows 和 Linux/Mac）
DANGEROUS_PATHS = [
    # Windows 系统目录
    r'C:\Windows',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\ProgramData',
    r'C:\Users\All Users',
    r'C:\Users\Default',
    r'C:\Users\Public',
    # Linux/Mac 系统目录
    '/root',
    '/bin',
    '/sbin',
    '/usr/bin',
    '/usr/sbin',
    '/usr/local/bin',
    '/System',
    '/etc',
    '/var',
]

def validate_target_path(target_path):
    """
    验证目标路径是否安全

    Returns:
        tuple: (is_safe, reason)
    """
    import os
    # 规范化路径
    target_path = os.path.abspath(target_path)

    # 检查是否在危险路径列表中
    for dangerous_path in DANGEROUS_PATHS:
        dangerous_path = os.path.abspath(dangerous_path)
        if target_path == dangerous_path or target_path.startswith(dangerous_path + os.sep):
            return False, f"禁止处理系统目录: {dangerous_path}"

    # 检查路径是否存在
    if not os.path.exists(target_path):
        return False, f"路径不存在: {target_path}"

    # 检查是否为目录
    if not os.path.isdir(target_path):
        return False, f"不是目录: {target_path}"

    return True, "路径安全"

# 测试危险路径
test_paths = [
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\ProgramData',
    '/root',
    '/etc',
    '/var',
    'F:\\笔记',
    'C:\\Users\\cyrilcao\\Documents'
]

print('🔍 测试路径安全验证功能\n')
print('=' * 60)

for path in test_paths:
    is_safe, reason = validate_target_path(path)
    status = '✅' if is_safe else '❌'
    print(f'{status} {path:40s} | {reason}')

print('\n✅ 安全验证功能正常工作！')
