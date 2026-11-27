import argparse,copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import validate_fastgpt_workflow as v
from regression_assertions import evaluate_assertions
def codes(value,render='input'):
 w={'nodes':[{'nodeId':'s','flowNodeType':'workflowStart','inputs':[],'position':{'x':0,'y':0}},{'nodeId':'u','flowNodeType':'variableUpdate','position':{'x':200,'y':0},'inputs':[{'key':'updateList','value':[{'variable':['VARIABLE_NODE_ID','trace'],'renderType':render,'value':value}]}]}],'edges':[{'source':'s','target':'u','sourceHandle':'out','targetHandle':'in'}]}
 args=argparse.Namespace(node=None,expected_app_version=None,baseline=None,expect_preserve_layout=False,expect_preserve_models=False)
 return {d['code'] for d in v.validate(w,args)['diagnostics']}
class RuntimeContracts(unittest.TestCase):
 def test_blank_manual_rejected(self):
  for value in ['',None,'  ']:self.assertIn('FG085',codes(value))
 def test_typed_initial_values(self):
  for value in ['[]',False,0]:self.assertNotIn('FG085',codes(value))
 def test_reference_not_manual(self):self.assertNotIn('FG085',codes(['s','value'],'reference'))
 def test_error_trace_even_with_good_answer(self):
  r=evaluate_assertions({'expected_substrings':['steps'],'runtime_trace_variable':'trace'},{'answer':'steps','variables':{'trace':json.dumps([{'kind':'timeout'}])}},'unknown')
  self.assertTrue(r['runtime_anomaly']);self.assertFalse(r['assertion_failed']);self.assertEqual(r['internal_error_count'],1)
 def test_trace_empty(self):
  r=evaluate_assertions({'expected_substrings':['steps'],'runtime_trace_variable':'trace'},{'answer':'steps','variables':{'trace':'[]'}},'unknown');self.assertFalse(r['runtime_anomaly'])
 def test_trace_corrupt_or_missing(self):
  for variables in [{},{'trace':'bad'},{'trace':{}}]:
   r=evaluate_assertions({'expected_substrings':['steps'],'runtime_trace_variable':'trace'},{'answer':'steps','variables':variables},'unknown');self.assertIn('runtime_trace_invalid_or_missing',r['runtime_anomaly_flags'])
if __name__=='__main__':unittest.main()
