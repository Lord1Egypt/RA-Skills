#!/usr/bin/env python3
"""文件保护集成测试"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/claw-def/src')
from file_protection import FileProtectionManager

def test_file_protection_to_log():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('skill', 'delete', '~/.ssh/id_rsa')
    assert result['allowed'] == False
    print("✅ test_file_protection_to_log 通过")

def test_restricted_file_permission_check():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('skill', 'read', '~/.aws/credentials')
    assert result['allowed'] == False
    assert result['action'] == 'ask'
    print("✅ test_restricted_file_permission_check 通过")

if __name__ == '__main__':
    test_file_protection_to_log()
    test_restricted_file_permission_check()
    print("\n✅ 集成测试通过 (2/2)")
