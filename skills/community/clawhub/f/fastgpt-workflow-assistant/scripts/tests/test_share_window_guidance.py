"""Share-page guidance and offline preflight tests; no external application calls."""
from pathlib import Path
import hashlib
import json
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prepare_share_window_test import inspect_target, select_test_method
S=Path(__file__).resolve().parents[1]
URL='https://example.invalid/chat/share?shareId=synthetic-share'

class PreflightTests(unittest.TestCase):
    def test_prepare_does_not_mark_runtime_pass(self):
        r=inspect_target(URL)
        self.assertEqual('synthetic-share',r['share_id'])
        self.assertIsNone(r['endpoint']);self.assertIsNone(r['app_id'])
        self.assertEqual('not_tested',r['platform_runtime']);self.assertFalse(r['importable_workflow'])
    def test_no_network(self):
        with patch.object(socket,'create_connection',side_effect=AssertionError('network forbidden')):
            self.assertEqual('not_tested',inspect_target(URL)['page_access'])
    def test_missing_id(self):
        with self.assertRaises(ValueError):inspect_target('https://example.invalid/chat/share')
    def test_empty_id(self):
        with self.assertRaises(ValueError):inspect_target('https://example.invalid/chat/share?shareId=')
    def test_duplicate_id(self):
        with self.assertRaises(ValueError):inspect_target(URL+'&shareId=other')
    def test_password_query_not_saved(self):
        with self.assertRaises(ValueError):inspect_target(URL+'&password=synthetic')
    def test_token_query_not_saved(self):
        with self.assertRaises(ValueError):inspect_target(URL+'&token=synthetic')
    def test_credentials_rejected(self):
        with self.assertRaises(ValueError):inspect_target('https://user:secret@example.invalid/chat/share?shareId=x')
    def test_non_http_rejected(self):
        with self.assertRaises(ValueError):inspect_target('file:///tmp/share?shareId=x')
    def test_whitespace_rejected(self):
        with self.assertRaises(ValueError):inspect_target(URL+' ')
    def test_bad_port(self):
        with self.assertRaises(ValueError):inspect_target('https://example.invalid:99999/chat/share?shareId=x')
    def test_workflow_hashed_without_modification(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'w.json';raw=json.dumps({'nodes':[{'nodeId':'start'}],'edges':[],'chatConfig':{}}).encode();p.write_bytes(raw)
            r=inspect_target(URL,p);self.assertEqual(hashlib.sha256(raw).hexdigest(),r['workflow']['sha256']);self.assertEqual(raw,p.read_bytes());self.assertEqual('not_verified_against_shared_channel',r['workflow']['published_version_alignment'])
    def test_validation_report_is_not_workflow(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'report.json';p.write_text(json.dumps({'workflow':'w.json','sha256':'x','results':{}}))
            with self.assertRaises(ValueError):inspect_target(URL,p)
    def test_cli_does_not_overwrite_report(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'report.json';p.write_text('preserve')
            r=subprocess.run([sys.executable,str(S/'prepare_share_window_test.py'),'--page-url',URL,'--output',str(p)],capture_output=True,text=True,timeout=15)
            self.assertEqual(1,r.returncode);self.assertEqual('preserve',p.read_text())
    def test_guidance_entry_and_boundaries_present(self):
        root=S.parent
        text=(root/'references/免登录窗口测试与引导.md').read_text(encoding='utf-8')
        for term in ['导入成功','shareId','appId','不可观察','最近7天','不能导入','发布版本','不猜','单并发']:
            self.assertIn(term,text)
        self.assertIn('免登录窗口测试与引导', (root/'SKILL.md').read_text(encoding='utf-8'))
    def test_no_real_company_link_in_new_public_guidance(self):
        text=(S.parent/'references/免登录窗口测试与引导.md').read_text(encoding='utf-8')
        self.assertNotIn('leapmotor.com',text)
        self.assertNotIn('wwY1k1pg',text)


class ApiFirstRoutingTests(unittest.TestCase):
    def test_url_testing_request_starts_http_discovery_without_user_api(self):
        r=select_test_method(True)
        self.assertEqual('http_read_page_and_public_api_evidence',r['method'])
        self.assertFalse(r['needs_chat_api_from_user'])
    def test_browser_available_does_not_override_http_priority(self):
        self.assertEqual('http_read_page_and_public_api_evidence',select_test_method(True,browser_available=True)['method'])
    def test_known_contract_goes_direct_api(self):
        self.assertEqual('direct_share_api_regression',select_test_method(True,True)['method'])
    def test_http_blocked_browser_is_fallback(self):
        self.assertEqual('browser_network_discovery_fallback',select_test_method(True,False,True,True)['method'])
    def test_no_browser_reports_tool_gap_not_permission_gate(self):
        r=select_test_method(True,False,True,False)
        self.assertEqual('report_specific_discovery_block_and_request_minimum_evidence',r['method'])
    def test_url_without_task_does_not_authorize_dialogue(self):
        self.assertEqual('clarify_test_scope',select_test_method(False)['method'])
    def test_preflight_reports_api_first_and_not_executed(self):
        r=inspect_target(URL)
        self.assertEqual('api-first',r['preferred_test_method'])
        self.assertEqual('not_tested',r['platform_runtime'])
    def test_expert_entry_routes_before_historical_notes(self):
        root=S.parents[2]
        expert=(root/'expert/agent.md').read_text(encoding='utf-8')
        self.assertLess(expert.index('分享URL直接回归'),expert.index('工作方式与交付要求'))
        text=(S.parent/'references/免登录窗口测试与引导.md').read_text(encoding='utf-8')
        self.assertIn('HTTP/API优先',text)
        self.assertNotIn('## 浏览器优先',text)

if __name__=='__main__':unittest.main()
