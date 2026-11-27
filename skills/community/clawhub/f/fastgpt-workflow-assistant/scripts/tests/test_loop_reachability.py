"""Native loop entry is implicit; an orphan child must still fail validation."""
import argparse
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import validate_fastgpt_workflow as validator

def fixture():
    return {'nodes':[
        {'nodeId':'start','flowNodeType':'workflowStart','position':{'x':0,'y':0},'inputs':[]},
        {'nodeId':'loop','flowNodeType':'loopRun','position':{'x':300,'y':0},'inputs':[{'key':'childrenNodeIdList','value':['entry','reply']}]},
        {'nodeId':'entry','flowNodeType':'loopRunStart','parentNodeId':'loop','position':{'x':400,'y':100},'inputs':[]},
        {'nodeId':'reply','flowNodeType':'answerNode','parentNodeId':'loop','position':{'x':600,'y':100},'inputs':[]}
    ],'edges':[
        {'source':'start','target':'loop','sourceHandle':'out','targetHandle':'in'},
        {'source':'entry','target':'reply','sourceHandle':'out','targetHandle':'in'}
    ]}

def codes(w):
    args=argparse.Namespace(node=None,expected_app_version=None,baseline=None,expect_preserve_layout=False,expect_preserve_models=False)
    return {i['code'] for i in validator.validate(w,args)['diagnostics']}

class LoopReachability(unittest.TestCase):
    def test_owned_start_is_reachable_without_canvas_edge(self):
        self.assertFalse({'FG032','FG033'} & codes(fixture()))
    def test_parent_must_be_reachable(self):
        w=fixture();w['edges']=w['edges'][1:];self.assertIn('FG032',codes(w))
    def test_parent_type_must_be_loop(self):
        w=fixture();w['nodes'][1]['flowNodeType']='answerNode';self.assertIn('FG033',codes(w))
    def test_child_must_be_listed(self):
        w=fixture();w['nodes'][1]['inputs'][0]['value']=['reply'];self.assertIn('FG033',codes(w))
    def test_parent_id_must_match(self):
        w=fixture();w['nodes'][2]['parentNodeId']='missing';self.assertIn('FG033',codes(w))
    def test_non_entry_child_is_not_blindly_exempt(self):
        w=fixture();w['edges']=w['edges'][:1];self.assertIn('FG032',codes(w))

if __name__=='__main__':unittest.main()
