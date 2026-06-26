#!/usr/bin/env python3
"""测试脚本"""

import sys
from pathlib import Path

# 添加到路径
sys.path.insert(0, str(Path(__file__).parent))

from session_sync import SyncEngine, ChangeDetector, FileManager

def test_hash():
    """测试 hash 功能"""
    detector = ChangeDetector()
    content1 = "测试内容"
    content2 = "测试内容"
    content3 = "不同内容"
    
    hash1 = detector.calculate_hash(content1)
    hash2 = detector.calculate_hash(content2)
    hash3 = detector.calculate_hash(content3)
    
    assert hash1 == hash2, "相同内容 hash 应该相同"
    assert hash1 != hash3, "不同内容 hash 应该不同"
    print("✓ hash 测试通过")

def test_sanitize():
    """测试脱敏功能"""
    from session_sync import sanitize_content
    
    email = "请联系 user@example.com"
    phone = "拨打 13800138000"
    
    assert "[EMAIL]" in sanitize_content(email)
    assert "[PHONE]" in sanitize_content(phone)
    print("✓ 脱敏测试通过")

if __name__ == "__main__":
    print("运行测试...")
    test_hash()
    test_sanitize()
    print("\n所有测试通过!")
