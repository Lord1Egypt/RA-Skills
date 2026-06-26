#!/usr/bin/env python3
"""文件保护单元测试"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/claw-def/src')
from file_protection import FileProtectionManager

def test_critical_file_blocked():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('test', 'read', '~/.ssh/id_rsa')
    assert result['allowed'] == False
    assert result['level'] == 'critical'
    print("✅ test_critical_file_blocked 通过")

def test_restricted_file_ask():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('test', 'read', '~/.aws/credentials')
    assert result['allowed'] == False
    assert result['level'] == 'restricted'
    print("✅ test_restricted_file_ask 通过")

def test_allowed_file_pass():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('test', 'read', '~/projects/test.py')
    assert result['allowed'] == True
    print("✅ test_allowed_file_pass 通过")

if __name__ == '__main__':
    test_critical_file_blocked()
    test_restricted_file_ask()
    test_allowed_file_pass()
    print("\n✅ 单元测试全部通过 (3/3)")
