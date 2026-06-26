#!/usr/bin/env python3
"""
test_interceptor.py - interceptor.py测试用例
"""
import pytest
import sys
import os
import json
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)

# 临时trust_db用于测试
TEST_DB = tempfile.mktemp(suffix='.json')

# mock路径
import interceptor
interceptor.SCRIPT_DIR = SCRIPT_DIR
interceptor.TRUST_DB = TEST_DB
interceptor.TRUST_TRACKER = os.path.join(SCRIPT_DIR, 'trust_tracker.py')

def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def write_db(data):
    os.makedirs(os.path.dirname(TEST_DB), exist_ok=True)
    with open(TEST_DB, 'w') as f:
        json.dump(data, f)

class TestDetectIntimateSignals:
    def test_short_message(self):
        """短回复应该触发亲密信号"""
        is_intimate, reason = interceptor.detect_intimate_signals("好的")
        assert is_intimate == True

    def test_laugh_pattern(self):
        """哈哈应该触发亲密信号"""
        is_intimate, reason = interceptor.detect_intimate_signals("哈哈哈哈哈")
        assert is_intimate == True

    def test_long_formal_message(self):
        """正式长消息不应该触发亲密信号"""
        is_intimate, reason = interceptor.detect_intimate_signals("请先确认一下这个操作的影响范围，谢谢")
        assert is_intimate == False

    def test_ok_pattern(self):
        """ok应该触发亲密信号"""
        is_intimate, reason = interceptor.detect_intimate_signals("ok")
        assert is_intimate == True

class TestDetectDowngradeSignals:
    def test_wait_signal(self):
        """等等应该触发降级信号"""
        is_down, reason = interceptor.detect_downgrade_signals("等等，先别发")
        assert is_down == True

    def test_confirm_signal(self):
        """确认应该触发降级信号"""
        is_down, reason = interceptor.detect_downgrade_signals("我先确认一下")
        assert is_down == True

    def test_casual_message(self):
        """日常消息不应该触发降级"""
        is_down, reason = interceptor.detect_downgrade_signals("感觉没问题")
        assert is_down == False

class TestDynamicRecipientRisk:
    def test_local_is_neutral(self):
        """local上下文应该是neutral"""
        is_high, reason = interceptor.is_high_risk_recipient_dynamic('local')
        assert is_high == False

    def test_group_is_high(self):
        """group应该是高风险"""
        is_high, reason = interceptor.is_high_risk_recipient_dynamic('group:xxx')
        assert is_high == True

    def test_intimate_signal_reduces_risk(self):
        """有亲密信号时，普通ID应该是低风险"""
        is_high, reason = interceptor.is_high_risk_recipient_dynamic(
            'user:ou_123', context_message='好的收到！'
        )
        assert is_high == False

    def test_downgrade_signal_increases_risk(self):
        """有降级信号时，普通ID应该提高风险"""
        is_high, reason = interceptor.is_high_risk_recipient_dynamic(
            'user:ou_123', context_message='等等，先确认一下'
        )
        assert is_high == True

class TestShouldIntercept:
    def test_local_delete_tmp(self):
        """本地/tmp删除应该放行"""
        intercept, reason = interceptor.should_intercept('delete', 'local', ['/tmp/test.txt'])
        assert intercept == False

    def test_group_send_blocked(self):
        """群聊发消息应该拦截"""
        intercept, reason = interceptor.should_intercept('send', 'group:xxx', [])
        assert intercept == True

    def test_low_trust_needs_confirm(self):
        """低信任应该需要确认"""
        intercept, reason = interceptor.should_intercept('send', 'user:ou_123', [])
        assert intercept == True

    def test_high_risk_operation_needs_confirm(self):
        """高风险操作应该需要确认"""
        write_db({"contacts": {"user:ou_123": {"send": {"count": 5, "lastConfirm": "2026-04-07T10:00:00"}}}})
        intercept, reason = interceptor.should_intercept('exec', 'user:ou_123', ['rm -rf /'])
        assert intercept == True

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
