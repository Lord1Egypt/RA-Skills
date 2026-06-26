#!/usr/bin/env python3
"""test_trust_tracker.py"""
import pytest
import sys
import os
import json
import tempfile

TEST_DIR = tempfile.mkdtemp()
TEST_DB = os.path.join(TEST_DIR, 'trust_db.json')

# 导入前设置路径
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, script_dir)

import trust_tracker
trust_tracker.TRUST_DB = TEST_DB

def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    return trust_tracker.load_trust_db()

class TestTrustUpdate:
    def test_first_update(self):
        clean_db()
        count = trust_tracker.update_trust('user:ou_123', 'send')
        assert count == 1

    def test_three_confirms(self):
        clean_db()
        for _ in range(3):
            trust_tracker.update_trust('user:ou_456', 'send')
        db = trust_tracker.load_trust_db()
        assert db['contacts']['user:ou_456']['send']['count'] >= 3

    def test_update_records_timestamp(self):
        clean_db()
        trust_tracker.update_trust('user:ou_789', 'delete')
        db = trust_tracker.load_trust_db()
        assert 'T' in db['contacts']['user:ou_789']['delete']['lastConfirm']

class TestTrustDecay:
    def test_old_entry_ignored(self):
        from datetime import datetime, timedelta
        old_time = (datetime.now() - timedelta(days=8)).isoformat()
        db = {"contacts": {"user:ou_old": {"send": {"count": 5, "lastConfirm": old_time}}}}
        trust_tracker.save_trust_db(db)
        count = trust_tracker.check_trust_count('user:ou_old', 'send')
        assert count == 0

class TestTrustReset:
    def test_reset_single(self):
        clean_db()
        trust_tracker.update_trust('user:ou_xxx', 'send')
        trust_tracker.reset_trust('user:ou_xxx')
        db = trust_tracker.load_trust_db()
        assert 'user:ou_xxx' not in db.get('contacts', {})

    def test_reset_all(self):
        clean_db()
        trust_tracker.update_trust('user:ou_a', 'send')
        trust_tracker.reset_all()
        db = trust_tracker.load_trust_db()
        assert len(db.get('contacts', {})) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
