#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广告账户管理 Skill 测试脚本
测试核心功能模块
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ad_manager import AdAccountManager, Platform, AccountType


def test_ad_manager():
    """测试账户管理器"""
    print("=" * 50)
    print("测试 AdAccountManager")
    print("=" * 50)
    
    # 初始化管理器
    manager = AdAccountManager()
    print("[OK] 管理器初始化成功")
    
    # 测试获取登录URL
    print("\n--- 测试获取登录URL ---")
    gdt_ad_url = manager.get_platform_login_url(Platform.GUANGDIANTONG, AccountType.ADVERTISER)
    print(f"广点通广告主URL: {gdt_ad_url}")
    
    gdt_agency_url = manager.get_platform_login_url(Platform.GUANGDIANTONG, AccountType.AGENCY)
    print(f"广点通服务商URL: {gdt_agency_url}")
    
    juliang_url = manager.get_platform_login_url(Platform.JULIANG)
    print(f"巨量引擎URL: {juliang_url}")
    
    # 测试列出账户
    print("\n--- 测试列出账户 ---")
    accounts = manager.list_accounts()
    print(f"当前账户数量: {len(accounts)}")
    
    # 测试账户总览
    print("\n--- 测试账户总览 ---")
    overview = manager.get_accounts_overview()
    print(f"总览数据: {overview}")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


def test_imports():
    """测试模块导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)
    
    try:
        import ad_manager
        print("[OK] ad_manager 导入成功")
    except Exception as e:
        print(f"[FAIL] ad_manager 导入失败: {e}")
        return False
    
    try:
        import browser_helper
        print("[OK] browser_helper 导入成功")
    except Exception as e:
        print(f"[FAIL] browser_helper 导入失败: {e}")
        return False
    
    print("\n[OK] 所有模块导入成功！")
    return True


if __name__ == "__main__":
    print("\n广告账户管理 Skill 测试\n")
    
    # 先测试导入
    if test_imports():
        # 再测试管理器
        test_ad_manager()
        
        print("\n提示: 运行 'python main.py' 可以启动交互式界面")
        print("提示: 在OpenClaw中说'管理广告账户'可以触发Skill")
