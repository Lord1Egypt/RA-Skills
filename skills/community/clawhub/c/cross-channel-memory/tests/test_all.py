#!/usr/bin/env python3
"""
跨渠道记忆同步 - 完整测试套件
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_init_mapping():
    """测试用户映射初始化"""
    print("\n=== 测试 init_mapping.py ===")
    
    # 创建临时测试用户
    import subprocess
    
    # 添加用户
    result = subprocess.run([
        sys.executable, 
        "init_mapping.py", 
        "add-user", 
        "--id", "test_user_001",
        "--name", "测试用户"
    ], capture_output=True, text=True)
    
    print(f"添加用户结果：{result.stdout}")
    if result.returncode != 0:
        print(f"错误：{result.stderr}")
    
    # 绑定 QQ 渠道
    result = subprocess.run([
        sys.executable,
        "init_mapping.py",
        "link",
        "--user", "test_user_001",
        "--channel", "qqbot",
        "--channel-id", "QQ_TEST_ID_001",
        "--account", "coder"
    ], capture_output=True, text=True)
    
    print(f"绑定 QQ 渠道结果：{result.stdout}")
    
    # 列出用户
    result = subprocess.run([
        sys.executable,
        "init_mapping.py",
        "list"
    ], capture_output=True, text=True)
    
    print(f"用户列表：{result.stdout}")

def test_lookup_user():
    """测试用户查找"""
    print("\n=== 测试 lookup_user.py ===")
    
    import subprocess
    
    # 查找用户
    result = subprocess.run([
        sys.executable,
        "lookup_user.py",
        "--channel", "qqbot",
        "--id", "QQ_TEST_ID_001",
        "--account", "coder"
    ], capture_output=True, text=True)
    
    print(f"查找用户结果：{result.stdout}")
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        assert data["found"] == True, "应该找到用户"
        assert data["userId"] == "test_user_001", "用户 ID 不匹配"
        print("✓ 用户查找成功")

def test_memory_sync():
    """测试记忆同步"""
    print("\n=== 测试 memory_sync.py ===")
    
    import subprocess
    
    # lookup 命令
    result = subprocess.run([
        sys.executable,
        "memory_sync.py",
        "lookup",
        "--channel", "qqbot",
        "--id", "QQ_TEST_ID_001",
        "--account", "coder"
    ], capture_output=True, text=True)
    
    print(f"查找记忆路径结果：{result.stdout}")
    
    # write 命令
    result = subprocess.run([
        sys.executable,
        "memory_sync.py",
        "write",
        "--channel", "qqbot",
        "--id", "QQ_TEST_ID_001",
        "--account", "coder",
        "--type", "user",
        "--content", "这是测试消息内容"
    ], capture_output=True, text=True)
    
    print(f"写入记忆结果：{result.stdout}")

def test_session_hooks():
    """测试 session hooks"""
    print("\n=== 测试 session_hooks.py ===")
    
    import subprocess
    
    # hook 命令
    result = subprocess.run([
        sys.executable,
        "session_hooks.py",
        "hook",
        "--agent", "coder",
        "--channel", "qqbot",
        "--user-id", "QQ_TEST_ID_001",
        "--session-id", "test_session_001"
    ], capture_output=True, text=True)
    
    print(f"Session hook 结果：{result.stdout}")

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Cross-Channel Memory - 完整测试套件")
    print("=" * 60)
    
    try:
        test_init_mapping()
        test_lookup_user()
        test_memory_sync()
        test_session_hooks()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
