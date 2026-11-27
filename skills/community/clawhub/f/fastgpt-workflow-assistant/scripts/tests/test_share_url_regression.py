"""Local registry reuse is evidenced and same-origin; no live test requests."""
from pathlib import Path
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
S=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(S))
from run_share_url_regression import plan,command_for,registry_path,canonical_origin,main

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.file=self.root/'registry.json';self.url='https://example.invalid/chat/share?shareId=NEW_ID'
        self.profile={'origin':'https://example.invalid','endpoint_path':'/api/v2/chat/completions','protocol':'fastgpt-share-sse','mode':'share-only','evidence':{'kind':'local_success_record','verified_on':'2026-11-02','source_file':'synthetic.py','source_sha256':'synthetic'}}
        self.save();self.cases=self.root/'cases.json';self.cases.write_text(json.dumps([{'case_id':'smoke','turns':[{'question':'你好','expected_substrings':['你好']}]}]),encoding='utf-8');self.results=self.root/'result.json'
    def tearDown(self):self.tmp.cleanup()
    def save(self):self.file.write_text(json.dumps({'instances':[self.profile]}),encoding='utf-8')
    def test_known_instance_uses_saved_protocol_without_discovery(self):
        p=plan(self.url,self.file);self.assertEqual('https://example.invalid/api/v2/chat/completions',p['endpoint']);self.assertIn('no_browser_or_packet_capture',p['next_step']);self.assertFalse(p['current_protocol_verified'])
    def test_new_share_id_not_old_id(self):self.assertEqual('NEW_ID',plan(self.url,self.file)['share_id'])
    def test_different_project_directory_still_uses_user_registry(self):
        with patch.dict(os.environ,{'FASTGPT_SHARE_REGISTRY':str(self.file)}):self.assertEqual('known_protocol_smoke_required',plan(self.url)['status'])
    def test_unknown_host_not_assumed_compatible(self):self.assertEqual('unknown_instance',plan('https://other.invalid/chat/share?shareId=x',self.file)['status'])
    def test_missing_registry_does_not_guess(self):self.assertEqual('protocol_evidence_missing',plan(self.url,self.root/'missing')['status'])
    def test_explicit_registry_precedes_environment(self):
        with patch.dict(os.environ,{'FASTGPT_SHARE_REGISTRY':'other.json'}):self.assertEqual(self.file,registry_path(self.file))
    def test_protocol_must_be_supported(self):
        self.profile['protocol']='unknown';self.save()
        with self.assertRaises(ValueError):plan(self.url,self.file)
    def test_evidence_required(self):
        self.profile['evidence']={};self.save()
        with self.assertRaises(ValueError):plan(self.url,self.file)
    def test_endpoint_must_stay_same_origin(self):
        self.profile['endpoint_path']='https://other.invalid/api';self.save()
        with self.assertRaises(ValueError):plan(self.url,self.file)
    def test_network_relative_endpoint_rejected(self):
        self.profile['endpoint_path']='//other.invalid/api';self.save()
        with self.assertRaises(ValueError):plan(self.url,self.file)
    def test_duplicate_profiles_rejected(self):
        self.file.write_text(json.dumps({'instances':[self.profile,self.profile]}))
        with self.assertRaises(ValueError):plan(self.url,self.file)
    def test_default_port_canonicalized(self):self.assertEqual('https://example.invalid',canonical_origin('https://EXAMPLE.INVALID:443/chat'))
    def test_nondefault_port_not_same_instance(self):self.assertEqual('unknown_instance',plan('https://example.invalid:8443/chat/share?shareId=x',self.file)['status'])
    def test_command_uses_share_only_not_app_id(self):
        c=command_for(plan(self.url,self.file),self.cases,self.results);self.assertIn('--share-only',c);self.assertNotIn('--app-id',c)
    def test_limit_concurrency_gap(self):
        with self.assertRaises(ValueError):command_for(plan(self.url,self.file),self.cases,self.results,gap=0)
    def test_dry_run_never_executes_network_runner(self):
        argv=['run_share_url_regression.py',self.url,str(self.cases),str(self.results),'--registry',str(self.file)]
        with patch.object(sys,'argv',argv),patch('run_share_url_regression.subprocess.run',side_effect=AssertionError('must not execute')),patch('builtins.print'):
            self.assertEqual(0,main());self.assertFalse(self.results.exists())
    def test_authorized_execute_delegates_existing_runner(self):
        argv=['run_share_url_regression.py',self.url,str(self.cases),str(self.results),'--registry',str(self.file),'--execute']
        with patch.object(sys,'argv',argv),patch('run_share_url_regression.subprocess.run',return_value=subprocess.CompletedProcess([],0)) as run,patch('builtins.print'):
            self.assertEqual(0,main());self.assertIn('--share-only',run.call_args.args[0]);self.assertIn('NEW_ID',run.call_args.args[0])
    def test_existing_results_not_overwritten(self):
        self.results.write_text('preserve');argv=['x',self.url,str(self.cases),str(self.results),'--registry',str(self.file),'--execute']
        with patch.object(sys,'argv',argv),patch('run_share_url_regression.subprocess.run',side_effect=AssertionError('must not execute')),patch('builtins.print'):
            self.assertEqual(1,main());self.assertEqual('preserve',self.results.read_text())
    def test_private_profile_not_in_public_asset(self):
        text=(S.parent/'assets/share-instances.example.json').read_text(encoding='utf-8');self.assertNotIn('leapmotor.com',text);self.assertNotIn('wwY1k1',text)

if __name__=='__main__':unittest.main()
