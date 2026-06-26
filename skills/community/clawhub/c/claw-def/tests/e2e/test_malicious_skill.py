#!/usr/bin/env python3
"""恶意 Skill 端到端测试"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/claw-def/src')
from file_protection import FileProtectionManager

def test_malicious_skill_blocked():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('malicious-skill', 'delete', '~/.ssh/id_rsa')
    assert result['allowed'] == False
    assert result['level'] == 'critical'
    print("✅ test_malicious_skill_blocked 通过")

def test_normal_skill_allowed():
    mgr = FileProtectionManager()
    result = mgr.check_file_operation('normal-skill', 'read', '~/projects/test.py')
    assert result['allowed'] == True
    print("✅ test_normal_skill_allowed 通过")

if __name__ == '__main__':
    test_malicious_skill_blocked()
    test_normal_skill_allowed()
    print("\n✅ 端到端测试通过 (2/2)")
