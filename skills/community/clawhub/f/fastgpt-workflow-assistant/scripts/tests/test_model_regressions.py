"""Synthetic regressions from model reviews; no private workflow/data."""
import copy,json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from node_schema_checks import check
ROOT=Path(__file__).resolve().parents[1]
class SchemaTests(unittest.TestCase):
 def codes(self,nodes,edges=[],baseline=None):return {x['code'] for x in check(nodes,edges,baseline)}
 def test_fabricated_switch(self):self.assertIn('FG090',self.codes([{'flowNodeType':'switch'}]))
 def test_target_extension_not_assumed_wrong(self):self.assertNotIn('FG090',self.codes([{'flowNodeType':'switch'}],baseline={'nodes':[{'flowNodeType':'switch'}]}))
 def test_wrong_http_key(self):self.assertIn('FG091',self.codes([{'inputs':[{'key':'system_httpReqTimeout'}]}]))
 def test_wrong_output_key(self):self.assertIn('FG091',self.codes([{'outputs':[{'key':'system_http_raw_response'}]}]))
 def test_missing_http_inputs(self):self.assertIn('FG094',self.codes([{'flowNodeType':'httpRequest468'}]))
 def test_catch_disabled(self):self.assertIn('FG093',self.codes([{'nodeId':'a'}],[{'source':'a','sourceHandle':'a-source_catch-right'}]))
 def test_wrong_condition_handle(self):self.assertIn('FG092',self.codes([{'nodeId':'a','flowNodeType':'ifElseNode','inputs':[{'key':'ifElseList','value':[{}]}]}],[{'source':'a','sourceHandle':'a-source-wrong'}]))
 def test_good_condition_handles(self):self.assertEqual(set(),self.codes([{'nodeId':'a','flowNodeType':'ifElseNode','inputs':[{'key':'ifElseList','value':[{}]}]}],[{'source':'a','sourceHandle':'a-source-IF'},{'source':'a','sourceHandle':'a-source-ELSE'}]))
 def test_unknown_type_is_warning(self):self.assertEqual('warning',check([{'flowNodeType':'custom'}],[],{'nodes':[{'flowNodeType':'code'}]})[0]['severity'])
class BehaviorTests(unittest.TestCase):
 def run_case(self,code,expected,forbidden=None):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'w.json').write_text(json.dumps({'nodes':[{'nodeId':'parse','flowNodeType':'code','inputs':[{'key':'code','value':code}]}]}),encoding='utf-8')
   case={'name':'requirement','node_id':'parse','input':{'text':'ping'},'expected':expected}
   if forbidden:case['forbidden']=forbidden
   (p/'c.json').write_text(json.dumps({'cases':[case]}),encoding='utf-8')
   r=subprocess.run([shutil.which('node'),str(ROOT/'run_code_contract.js'),str(p/'w.json'),str(p/'c.json')],capture_output=True,text=True,timeout=10)
   return r.returncode,json.loads(r.stdout)
 def test_correct_output_pass(self):self.assertEqual(0,self.run_case('function main(){return {route:"ping_missing",targets:[]}}',{'route':'ping_missing','targets':[]})[0])
 def test_missing_ping_intent_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {route:"asset"}}',{'route':'ping_missing'})[0])
 def test_truncated_target_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {targets:["192.0.2.1"]}}',{'targets':[]})[0])
 def test_discarded_target_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {invalidTargets:[]}}',{'invalidTargets':['10.1.2']})[0])
 def test_multiple_ping_first_only_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {route:"ping",pingIp:"192.0.2.1"}}',{'route':'invalid','pingIp':''})[0])
 def test_chinese_extraction_missing_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {targets:[]}}',{'targets':[{'type':'IP','value':'192.0.2.1'}]})[0])
 def test_arbitrary_cap_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {targetCount:10}}',{'targetCount':11})[0])
 def test_bad_mac_omission_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {invalidTargets:[]}}',{'invalidTargets':['GG:BB:CC:DD:EE:FF']})[0])
 def test_extra_unexpected_target_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {targets:["a","b"]}}',{'targets':['a']})[0])
 def test_empty_expectation_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {}}',{})[0])
 def test_forbidden_value_fails(self):self.assertNotEqual(0,self.run_case('function main(){return {route:"asset",pingIp:"192.0.2.1"}}',{'route':'asset'},{'pingIp':'192.0.2.1'})[0])
 def test_infinite_loop_is_bounded(self):self.assertNotEqual(0,self.run_case('function main(){while(true){}}',{'route':'asset'})[0])
 def test_module_call_fails(self):self.assertNotEqual(0,self.run_case('function main(){return require("fs")}',{'route':'asset'})[0])
if __name__=='__main__':unittest.main()
