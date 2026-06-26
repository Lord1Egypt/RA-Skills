#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AK 配置测试 - 验证 AK 是否正确配置
"""

import sys
import os

# 添加项目根目录到 Python 路径
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _project_root)

from scripts.capabilities.configure.service import check_existing_config


def main():
    """测试 AK 配置"""
    print("=" * 60)
    print("AK 配置测试")
    print("=" * 60)
    print()
    
    is_configured, ak_info = check_existing_config()
    
    if is_configured:
        print("✅ AK 已配置")
        print(f"   AK ID: {ak_info[:8]}..." if ak_info and len(ak_info) > 8 else "")
    else:
        print("❌ AK 未配置")
        print()
        print("配置方式：")
        print("   python3 scripts/capabilities/configure/cmd.py YOUR_AK")
        print()
        print("获取 AK：")
        print("   打开 https://clawhub.1688.com 点击右上角钥匙🔑图标")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
