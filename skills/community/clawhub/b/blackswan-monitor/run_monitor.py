#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股黑天鹅监控脚本 - 包装器
确保正确执行并发送邮件
"""

import subprocess
import sys
import os

# 设置环境
os.chdir('/root/.openclaw/workspace/blackswan-monitor')

# 使用超时执行主脚本
print("=" * 70)
print("启动A股黑天鹅监控脚本 (带超时保护)")
print("=" * 70)

try:
    result = subprocess.run(
        ['python3', 'scripts/blackswan_monitor.py'],
        timeout=180,  # 3分钟超时
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"\n❌ 脚本执行失败，退出码: {result.returncode}")
        sys.exit(1)
    else:
        print("\n✅ 脚本执行成功")
        sys.exit(0)
        
except subprocess.TimeoutExpired:
    print("\n❌ 脚本执行超时 (超过3分钟)")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ 执行出错: {e}")
    sys.exit(1)
