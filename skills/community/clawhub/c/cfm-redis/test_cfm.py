#!/usr/bin/env python3
"""
CFM 双向通信测试
测试 Hermès ↔ CHANEL 跨框架通信
"""

import sys
import time
import json
from cfm_messenger import CFMMessenger

def test_basic_send_receive():
    """测试基本发送和接收"""
    print("🧪 测试1: 基本发送和接收")
    print("-" * 40)
    
    # 接收方准备
    received_messages = []
    
    def on_receive(msg):
        received_messages.append(msg)
        print(f"  📨 收到消息: {msg['content']}")
    
    # 创建两个通信器
    hermes = CFMMessenger("hermes")
    chanel = CFMMessenger("chanel")
    
    # 注册
    hermes.register()
    chanel.register()
    print("  ✅ 双方注册成功")
    
    # CHANEL开始监听
    chanel.on_message(on_receive)
    chanel.start_listening()
    print("  ✅ CHANEL开始监听")
    
    # 等待一下让订阅生效
    time.sleep(0.5)
    
    # Hermès发送消息
    msg_id = hermes.send("chanel", "测试！Hermès呼叫CHANEL，收到请回答！")
    print(f"  ✅ Hermès发送消息 (ID: {msg_id})")
    
    # 等待接收
    time.sleep(1)
    
    # 检查结果
    if received_messages:
        print(f"  ✅ 测试通过！收到 {len(received_messages)} 条消息")
    else:
        print("  ❌ 测试失败！未收到消息")
    
    # 清理
    hermes.unregister()
    chanel.stop_listening()
    chanel.unregister()
    
    return len(received_messages) > 0

def test_bidirectional():
    """测试双向通信"""
    print("\n🧪 测试2: 双向通信")
    print("-" * 40)
    
    hermes_received = []
    chanel_received = []
    
    def hermes_on_msg(msg):
        hermes_received.append(msg)
        print(f"  📨 Hermès收到: {msg['content']}")
    
    def chanel_on_msg(msg):
        chanel_received.append(msg)
        print(f"  📨 CHANEL收到: {msg['content']}")
    
    # 创建通信器
    hermes = CFMMessenger("hermes")
    chanel = CFMMessenger("chanel")
    
    # 注册并开始监听
    hermes.register()
    chanel.register()
    
    hermes.on_message(hermes_on_msg)
    chanel.on_message(chanel_on_msg)
    
    hermes.start_listening()
    chanel.start_listening()
    
    time.sleep(0.5)
    
    # 双向发送
    print("  📤 Hermès → CHANEL: 你好！")
    hermes.send("chanel", "你好！")
    
    time.sleep(0.5)
    
    print("  📤 CHANEL → Hermès: 收到！")
    chanel.send("hermes", "收到！")
    
    time.sleep(1)
    
    # 检查结果
    success = len(chanel_received) > 0 and len(hermes_received) > 0
    
    if success:
        print(f"  ✅ 测试通过！")
        print(f"     Hermès收到: {len(hermes_received)} 条")
        print(f"     CHANEL收到: {len(chanel_received)} 条")
    else:
        print("  ❌ 测试失败！")
    
    # 清理
    hermes.stop_listening()
    chanel.stop_listening()
    hermes.unregister()
    chanel.unregister()
    
    return success

def test_message_persistence():
    """测试消息持久化"""
    print("\n🧪 测试3: 消息持久化")
    print("-" * 40)
    
    # 创建通信器
    hermes = CFMMessenger("hermes")
    chanel = CFMMessenger("chanel")
    
    # 注册
    hermes.register()
    chanel.register()
    
    # 发送一些消息
    hermes.send("chanel", "持久化测试消息1")
    hermes.send("chanel", "持久化测试消息2")
    chanel.send("hermes", "回复消息1")
    
    time.sleep(0.5)
    
    # 获取消息历史
    hermes_messages = hermes.get_messages(limit=10)
    chanel_messages = chanel.get_messages(limit=10)
    
    print(f"  📚 Hermès消息历史: {len(hermes_messages)} 条")
    print(f"  📚 CHANEL消息历史: {len(chanel_messages)} 条")
    
    # 清理
    hermes.unregister()
    chanel.unregister()
    
    success = len(hermes_messages) > 0 and len(chanel_messages) > 0
    
    if success:
        print("  ✅ 测试通过！消息已持久化")
    else:
        print("  ❌ 测试失败！")
    
    return success

def test_discover_agents():
    """测试发现agents"""
    print("\n🧪 测试4: 发现agents")
    print("-" * 40)
    
    # 创建多个通信器
    hermes = CFMMessenger("hermes")
    chanel = CFMMessenger("chanel")
    test = CFMMessenger("test-agent")
    
    # 注册
    hermes.register()
    chanel.register()
    test.register()
    
    # 发现
    agents = hermes.discover_agents()
    
    print(f"  🔍 发现 {len(agents)} 个agents:")
    for agent in agents:
        print(f"     - {agent.get('id', 'unknown')}: {agent.get('status', 'unknown')}")
    
    # 清理
    hermes.unregister()
    chanel.unregister()
    test.unregister()
    
    success = len(agents) >= 2
    
    if success:
        print("  ✅ 测试通过！")
    else:
        print("  ❌ 测试失败！")
    
    return success

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 CFM 双向通信测试")
    print("=" * 50)
    
    tests = [
        test_basic_send_receive,
        test_bidirectional,
        test_message_persistence,
        test_discover_agents
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i}. {test.__name__}: {status}")
    
    all_passed = all(results)
    print(f"\n🎯 总体结果: {'✅ 全部通过' if all_passed else '❌ 有失败项'}")
    
    sys.exit(0 if all_passed else 1)
