#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Guard 测试脚本
"""

from auth_guard import AuthGuard
import json

def test_basic():
    """基础功能测试"""
    print("\n" + "="*60)
    print("测试 1: 基础授权请求")
    print("="*60)
    
    guard = AuthGuard()
    
    result = guard.request_authorization(
        service="google-mail",
        action="messages.send",
        params={
            "to": "test@example.com",
            "subject": "测试邮件",
            "body": "这是一封测试邮件"
        },
        reason="测试授权保护功能",
        requester="test-script",
        priority="normal"
    )
    
    print("\n授权结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def test_whitelist():
    """白名单测试"""
    print("\n" + "="*60)
    print("测试 2: 白名单检查")
    print("="*60)
    
    guard = AuthGuard()
    
    # 测试白名单操作
    result = guard._check_whitelist("google-mail", "messages.get", {})
    print(f"白名单检查 (messages.get): {result}")
    
    # 测试黑名单操作
    result = guard._check_blacklist("google-mail", "messages.send")
    print(f"黑名单检查 (messages.send): {result}")

def test_config():
    """配置测试"""
    print("\n" + "="*60)
    print("测试 3: 配置检查")
    print("="*60)
    
    guard = AuthGuard()
    
    print(f"启用状态：{guard.config.get('enabled')}")
    print(f"运行模式：{guard.config.get('mode')}")
    print(f"超时时间：{guard.config.get('timeout_seconds')}秒")
    print(f"通知渠道：{guard.config.get('notification', {}).get('channel')}")

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Auth Guard 测试套件")
    print("="*60)
    
    try:
        test_config()
        test_whitelist()
        # test_basic()  # 这个会等待用户确认，手动运行
        
        print("\n" + "="*60)
        print("[OK] 所有测试完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
