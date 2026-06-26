#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AK 配置测试 - 设置 AK
"""

import sys
import os

# 添加项目根目录到 Python 路径
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _project_root)

from scripts.capabilities.configure.service import configure_via_gateway


def main():
    """设置 AK"""
    print("=" * 60)
    print("AK 配置")
    print("=" * 60)
    print()
    print("获取 AK：打开 https://clawhub.1688.com 点击右上角钥匙🔑图标")
    print()
    
    ak = input("请输入 AK: ").strip()
    
    if not ak:
        print("\n❌ AK 不能为空")
        return
    
    print(f"\n正在配置 AK: {ak[:8]}...")
    print()
    
    success = configure_via_gateway(ak)
    
    if success:
        print("✅ AK 配置成功")
    else:
        print("❌ AK 配置失败")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
