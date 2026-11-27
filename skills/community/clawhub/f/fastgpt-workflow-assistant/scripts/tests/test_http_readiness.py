"""local-r3 offline URL, same-source, target conservation and HTTP failure regressions."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
S=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(S))
from check_http_contract import check, validate_url

class UrlTests(unittest.TestCase):
    def test_invalid_urls(self):
        for value in ['', 'TODO_CONFIGURE_API', 'abc', 'http://', 'https://???', 'https://:443', 'https://example.invalid:99999', 'https://example.invalid:', 'https://a b', 'https://-bad.invalid', 'https://bad..invalid', 'https://999.1.1.1', 'javascript:alert(1)', 'https://user:secret@example.invalid', 'https://host.invalid/#fragment', 'https://host.invalid\\other']:
            with self.subTest(url=value): self.assertFalse(validate_url(value)['valid'])
    def test_valid_syntax_not_reachability(self):
        for value in ['https://example.invalid/api', 'http://localhost:8080/query', 'http://10.1.2.3', 'http://[::1]:8080/api', 'https://api.example.invalid:443/q?a=1']:
            with self.subTest(url=value): self.assertTrue(validate_url(value)['valid'])
    def test_valid_url_is_not_automatic_readiness(self):
        self.assertIn('not_reachability_or_api_readiness',validate_url('https://example.invalid')['reason'])

class HttpContractTests(unittest.TestCase):
    def setUp(self):
        self.w={'nodes':[{'nodeId':'gate','inputs':[{'key':'url','value':['VARIABLE_NODE_ID','apiUrl']}]}, {'nodeId':'http','flowNodeType':'httpRequest468','catchError':True,'inputs':[{'key':'system_httpReqUrl','value':'{{$VARIABLE_NODE_ID.apiUrl$}}'}],'outputs':[{'key':'error','id':'error'}]}, {'nodeId':'errorReply','inputs':[{'key':'text','value':'请求失败：{{$http.error$}}'}]}], 'edges':[{'source':'http','sourceHandle':'http-source_catch-right','target':'errorReply'}], 'chatConfig':{'variables':[{'key':'apiUrl','defaultValue':''}]}}
        self.c={'cases':[{'http_node':'http','gate_node':'gate','gate_url_input':'url','source':{'reference':['VARIABLE_NODE_ID','apiUrl']},'error_targets':['errorReply'],'error_required_references':[['http','error']]}]}
    def errors(self):return check(self.w,self.c)['cases'][0]['errors']
    def test_same_source_and_catch_pass(self):self.assertEqual([],self.errors())
    def test_hidden_field_does_not_establish_capability(self):self.assertIn('no interpolation',check(self.w,self.c)['scope'])
    def test_blank_http_url_rejected(self):
        self.w['nodes'][1]['inputs'][0]['value']='';self.assertIn('HC001_gate_and_http_source_mismatch_or_missing',self.errors())
    def test_gate_and_http_diverge_rejected(self):
        self.w['nodes'][1]['inputs'][0]['value']='https://other.invalid';self.assertTrue(self.errors())
    def test_source_variable_not_declared(self):
        self.w['chatConfig']['variables']=[];self.assertIn('HC002_source_variable_not_declared',self.errors())
    def test_literal_source_equality(self):
        self.c['cases'][0]['source']={'literal':'https://example.invalid'}
        self.w['nodes'][0]['inputs'][0]['value']=self.w['nodes'][1]['inputs'][0]['value']='https://example.invalid';self.assertEqual([],self.errors())
    def test_invalid_literal_url(self):
        self.c['cases'][0]['source']={'literal':'http://'}
        self.w['nodes'][0]['inputs'][0]['value']=self.w['nodes'][1]['inputs'][0]['value']='http://';self.assertIn('HC003_invalid_literal_url',self.errors())
    def test_disabled_catch(self):
        self.w['nodes'][1]['catchError']=False;self.assertIn('HC004_http_catch_missing',self.errors())
    def test_missing_catch_edge(self):
        self.w['edges']=[];self.assertIn('HC004_http_catch_missing',self.errors())
    def test_missing_error_output(self):
        self.w['nodes'][1]['outputs']=[];self.assertIn('HC004_error_output_missing',self.errors())
    def test_wrong_catch_target(self):
        self.w['edges'][0]['target']='gate';self.assertIn('HC005_error_target_not_connected',self.errors())
    def test_error_reply_missing_reference(self):
        self.w['nodes'][2]['inputs'][0]['value']='未查询到资产';self.assertIn('HC006_error_reference_missing',self.errors())

class BehaviorRegressions(unittest.TestCase):
    def run_code(self,code,input,expected):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/'w.json').write_text(json.dumps({'nodes':[{'nodeId':'code','flowNodeType':'code','inputs':[{'key':'code','value':code}]}]}),encoding='utf-8')
            (p/'c.json').write_text(json.dumps({'cases':[{'name':'requirement','node_id':'code','input':input,'expected':expected}]}),encoding='utf-8')
            r=subprocess.run([shutil.which('node'),str(S/'run_code_contract.js'),str(p/'w.json'),str(p/'c.json')],capture_output=True,text=True,encoding='utf-8',timeout=10)
            return r.returncode,json.loads(r.stdout)
    def test_overlong_first_original_loss_detected(self):
        rc,r=self.run_code('function main({input}){return {invalidTargets:[{value:"0.2.1"}]}}',{'input':'1192.0.2.1'},{'invalidTargets':[{'value':'1192.0.2.1'}]});self.assertEqual(1,rc);self.assertEqual('expected_mismatch',r['cases'][0]['error'])
    def test_overlong_last_drop_detected(self):
        self.assertEqual(1,self.run_code('function main(){return {invalidTargets:[]}}',{'input':'192.0.2.1234'},{'invalidTargets':[{'value':'192.0.2.1234'}]})[0])
    def test_complete_digit_run_retained(self):
        code=r'function main({input}){const m=input.match(/[0-9]+(?:\.[0-9]+)+/g)||[];return {tokens:m}}'
        self.assertEqual(0,self.run_code(code,{'input':'1192.0.2.1 192.0.2.1234'},{'tokens':['1192.0.2.1','192.0.2.1234']})[0])
    def test_ping_invalid_extra_cannot_choose_first(self):
        self.assertEqual(1,self.run_code('function main(){return {route:"ping",pingIp:"192.0.2.1"}}',{'input':'ping 192.0.2.1 999.1.1.1'},{'route':'invalid','pingIp':''})[0])
    def test_ping_invalid_extra_explicit_rejection(self):
        code='function main({invalidTargets}){return {route:invalidTargets.length?"invalid":"ping",pingIp:invalidTargets.length?"":"192.0.2.1"}}'
        self.assertEqual(0,self.run_code(code,{'invalidTargets':[{'value':'999.1.1.1'}]},{'route':'invalid','pingIp':''})[0])
    def test_url_prefix_only_bug_detected(self):
        self.assertEqual(1,self.run_code('function main({url}){return {ready:/^https?:/.test(url)}}',{'url':'http://'},{'ready':False})[0])
    def formatter(self,input,expected):
        return self.run_code((S.parent/'assets/code-snippets/http-result-state.js').read_text(encoding='utf-8'),input,expected)[0]
    def test_timeout_is_error(self):self.assertEqual(0,self.formatter({'response':None,'error':'timeout','configured':True},{'state':'request_error'}))
    def test_403_is_not_asset_missing(self):self.assertEqual(0,self.formatter({'response':{'statusCode':403},'error':'','configured':True},{'state':'request_error'}))
    def test_500_is_error(self):self.assertEqual(0,self.formatter({'response':{'statusCode':500},'error':'','configured':True},{'state':'request_error'}))
    def test_empty_distinct_from_error(self):self.assertEqual(0,self.formatter({'response':[],'error':'','configured':True},{'state':'empty'}))
    def test_not_configured_distinct_from_empty(self):self.assertEqual(0,self.formatter({'response':None,'error':'','configured':False},{'state':'not_configured'}))
    def test_business_payload_received_not_proven_success(self):self.assertEqual(0,self.formatter({'response':{'data':[]},'error':'','configured':True},{'state':'received'}))


    def test_bound_http_error_reaches_failure_reply(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            code=(S.parent/'assets/code-snippets/http-result-state.js').read_text(encoding='utf-8')
            w={'nodes':[{'nodeId':'http','flowNodeType':'httpRequest468','outputs':[{'id':'httpRawResponse','key':'httpRawResponse'},{'id':'error','key':'error'}]}, {'nodeId':'format','flowNodeType':'code','inputs':[{'key':'code','value':code},{'key':'response','renderTypeList':['reference'],'value':['http','httpRawResponse']},{'key':'error','renderTypeList':['reference'],'value':['http','error']},{'key':'configured','value':True}],'outputs':[{'id':'text','key':'text'}]}, {'nodeId':'reply','flowNodeType':'answerNode','inputs':[{'key':'text','value':'{{$format.text$}}'}]}]}
            c={'cases':[{'name':'timeout final reply','mode':'bound','steps':['format','reply'],'seeds':{'http':{'httpRawResponse':None,'error':'timeout'}},'contains_all':['请求失败'],'not_contains':['未查询到资产'],'required_references':[['format','text']]}]}
            (p/'w.json').write_text(json.dumps(w),encoding='utf-8');(p/'c.json').write_text(json.dumps(c),encoding='utf-8')
            args=[shutil.which('node'),str(S/'run_code_contract.js'),str(p/'w.json'),str(p/'c.json')]
            good=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=10)
            self.assertEqual(0,good.returncode,good.stdout)
            w['nodes'][2]['inputs'][0]['value']='未查询到资产'
            (p/'w.json').write_text(json.dumps(w),encoding='utf-8')
            bad=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=10)
            self.assertEqual(1,bad.returncode)
            self.assertEqual('required_reply_reference_missing',json.loads(bad.stdout)['cases'][0]['error'])

if __name__=='__main__':unittest.main()
