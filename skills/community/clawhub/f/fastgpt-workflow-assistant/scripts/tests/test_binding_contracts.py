"""Synthetic data-binding, HTTP contract, explicit ping and final-reply regressions."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from execution_binding_checks import check


def output(key, identifier=None, kind='dynamic'):
    return {'key': key, 'id': identifier or key, 'type': kind}


def ref(key, source, field):
    return {'key': key, 'value': [source, field], 'renderTypeList': ['reference']}


def code_node(code, inputs=None):
    return {'nodeId': 'parse', 'flowNodeType': 'code', 'inputs': [
        {'key': 'code', 'value': code}, {'key': 'codeType', 'value': 'js'}, *(inputs or [])],
        'outputs': [output('invalidTargets')]}


class BindingSchemaTests(unittest.TestCase):
    def codes(self, node, baseline=None):
        return {d['code'] for d in check([node], baseline)}

    def test_missing_input_declaration(self):
        self.assertIn('FG095', self.codes(code_node('function main({input}){return {}}')))

    def test_add_input_button_is_not_actual_parameter(self):
        n = code_node('function main({input}){return {}}', [{'key': 'system_addInputParam'}])
        self.assertIn('FG095', self.codes(n))

    def test_alias_parameter_uses_original_input_key(self):
        n = code_node('function main({input: text}){return {}}', [ref('input', 'start', 'userChatInput')])
        self.assertEqual(set(), self.codes(n))

    def test_bound_input_passes(self):
        n = code_node('async function main({input}) {return {}}', [ref('input', 'start', 'userChatInput')])
        self.assertEqual(set(), self.codes(n))

    def test_parameter_with_js_default_is_optional(self):
        self.assertEqual(set(), self.codes(code_node('function main({input = ""}){return {}}')))

    def test_declared_but_unbound_input(self):
        self.assertIn('FG096', self.codes(code_node('function main({input}){return {}}', [{'key': 'input'}])))

    def test_empty_literal_is_legitimate_binding(self):
        self.assertEqual(set(), self.codes(code_node('function main({input}){return {}}', [{'key': 'input', 'value': ''}])))

    def test_malformed_reference(self):
        self.assertIn('FG096', self.codes(code_node('function main({input}){return {}}', [ref('input', 'start', '')])))

    def test_unsupported_signature_not_guessed(self):
        self.assertEqual(set(), self.codes(code_node('function main(args){return args.input}')))

    def http_node(self, outputs):
        return {'nodeId': 'http', 'flowNodeType': 'httpRequest468', 'outputs': outputs}

    def baseline(self, outputs=None):
        return {'nodes': [self.http_node(outputs or [output('httpRawResponse', kind='static'), output('error', kind='error')])]}

    def test_fake_http_output_rejected_with_baseline(self):
        self.assertIn('FG097', self.codes(self.http_node([output('system_httpResponse')]), self.baseline()))

    def test_raw_and_custom_extracted_outputs_allowed(self):
        n = self.http_node([output('httpRawResponse', kind='static'), output('deviceName')])
        self.assertEqual(set(), self.codes(n, self.baseline()))

    def test_suspect_output_without_baseline_is_warning(self):
        d = check([self.http_node([output('system_httpResponse')])])
        self.assertEqual('warning', d[0]['severity'])

    def test_actual_alternate_baseline_respected(self):
        n = self.http_node([output('system_httpResponse')])
        self.assertEqual(set(), self.codes(n, self.baseline([output('system_httpResponse')])) )


class DataContractTests(unittest.TestCase):
    def setUp(self):
        self.workflow = {'nodes': [
            {'nodeId': 'start', 'flowNodeType': 'workflowStart', 'outputs': [output('userChatInput')]},
            code_node('function main({input}){return {invalidTargets:[{value:input,reason:"IP不是四段"}]}}', [ref('input', 'start', 'userChatInput')]),
            {'nodeId': 'reply', 'flowNodeType': 'answerNode', 'inputs': [{'key': 'text', 'value': '无法处理：{{$parse.invalidTargets$}}'}]}
        ], 'chatConfig': {'variables': [{'key': 'assetApiUrl', 'defaultValue': ''}]}}
        self.case = {'name': 'final reply preserves original and reason', 'mode': 'bound',
                     'steps': ['parse', 'reply'], 'seeds': {'start': {'userChatInput': '192.0.2.1.7'}},
                     'required_inputs': {'parse': ['input']},
                     'required_references': [['parse', 'invalidTargets']],
                     'contains_all': ['192.0.2.1.7', 'IP不是四段']}

    def execute(self, case=None):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'w.json').write_text(json.dumps(self.workflow), encoding='utf-8')
            (root / 'c.json').write_text(json.dumps({'cases': [case or self.case]}), encoding='utf-8')
            p = subprocess.run([shutil.which('node'), str(SCRIPTS / 'run_code_contract.js'), str(root/'w.json'), str(root/'c.json')], capture_output=True, text=True, encoding='utf-8', timeout=10)
            return p.returncode, json.loads(p.stdout)

    def error(self, expected):
        rc, report = self.execute()
        self.assertNotEqual(0, rc)
        self.assertIn(expected, report['cases'][0]['error'])

    def test_json_bound_pipeline_and_final_reply_pass(self):
        self.assertEqual(0, self.execute()[0])

    def test_missing_declared_binding_cannot_be_hidden_by_manual_input(self):
        self.workflow['nodes'][1]['inputs'].pop()
        self.error('input_not_declared')

    def test_unresolved_upstream_value_fails(self):
        self.case['seeds'] = {}
        self.error('reference_unresolved')

    def test_typo_in_reference_output_fails(self):
        self.workflow['nodes'][1]['inputs'][-1]['value'][1] = 'unknown'
        self.error('reference_not_declared')

    def test_input_is_not_accepted_in_bound_mode(self):
        self.case['input'] = {'input': '192.0.2.1.7'}
        self.error('bound_mode_disallows_manual_input')

    def test_http_steps_never_execute(self):
        self.workflow['nodes'][1]['flowNodeType'] = 'httpRequest468'
        self.error('unsupported_data_step')

    def test_fixed_reply_loses_reference(self):
        self.workflow['nodes'][2]['inputs'][0]['value'] = '请输入合法地址'
        self.error('required_reply_reference_missing')

    def test_reason_missing_from_data_fails_final_text(self):
        self.workflow['nodes'][1]['inputs'][0]['value'] = 'function main({input}){return {invalidTargets:[{value:input}]}}'
        self.error('reply_text_incomplete')

    def test_original_value_missing_fails_final_text(self):
        self.workflow['nodes'][1]['inputs'][0]['value'] = 'function main({input}){return {invalidTargets:[{value:"0.2.1",reason:"IP不是四段"}]}}'
        self.error('reply_text_incomplete')

    def test_seed_must_be_declared(self):
        self.case['seeds']['start']['fake'] = 'x'
        self.error('seed_output_not_declared')

    def test_executed_node_cannot_be_mocked(self):
        self.case['seeds']['parse'] = {'invalidTargets': []}
        self.error('cannot_seed_executed_step')

    def test_output_id_resolves_actual_output_key(self):
        self.workflow['nodes'][0]['outputs'][0]['id'] = 'opaque-output-id'
        self.workflow['nodes'][1]['inputs'][-1]['value'][1] = 'opaque-output-id'
        self.assertEqual(0, self.execute()[0])

    def test_global_variable_default(self):
        self.workflow['nodes'][1] = code_node('function main({assetApiUrl}){return {ready:assetApiUrl!==""}}', [ref('assetApiUrl','VARIABLE_NODE_ID','assetApiUrl')])
        self.case = {'name':'empty config gate','mode':'bound','node_id':'parse','expected':{'ready':False}}
        self.assertEqual(0, self.execute()[0])

    def test_global_variable_override(self):
        self.workflow['nodes'][1] = code_node('function main({assetApiUrl}){return {ready:assetApiUrl!==""}}', [ref('assetApiUrl','VARIABLE_NODE_ID','assetApiUrl')])
        self.case = {'name':'configured gate simulation','mode':'bound','node_id':'parse','variables':{'assetApiUrl':'https://example.invalid'},'expected':{'ready':True}}
        self.assertEqual(0, self.execute()[0])

    def test_undeclared_variable_override_fails(self):
        self.case['variables']={'fake':'x'}
        self.error('variable_override_not_declared')

    def test_no_default_unresolved_variable_fails(self):
        self.workflow['chatConfig']['variables'][0].pop('defaultValue')
        self.workflow['nodes'][1]['inputs'][-1] = ref('input','VARIABLE_NODE_ID','assetApiUrl')
        self.error('variable_unresolved')

    def ping_case(self, text, expected, correct=False):
        pattern = r'/(?:^|[^A-Za-z0-9_])ping(?:$|[^A-Za-z0-9_])/i' if correct else '/ping/i'
        self.workflow['nodes'][1] = code_node('function main({input}){return {pingIntent:' + pattern + '.test(input)}}', [ref('input','start','userChatInput')])
        self.case = {'name':'explicit ping boundary','mode':'bound','node_id':'parse','seeds':{'start':{'userChatInput':text}},'expected':{'pingIntent':expected}}
        return self.execute()[0]

    def test_mapping_substring_regression_caught(self):
        self.assertNotEqual(0,self.ping_case('mapping 192.0.2.1',False))

    def test_shopping_substring_regression_caught(self):
        self.assertNotEqual(0,self.ping_case('shopping 192.0.2.1',False))

    def test_pinging_not_explicit_ping(self):
        self.assertEqual(0,self.ping_case('pinging 192.0.2.1',False,True))

    def test_chinese_inserted_explicit_ping(self):
        self.assertEqual(0,self.ping_case('帮我 ping 一下 192.0.2.1',True,True))

    def test_uppercase_explicit_ping(self):
        self.assertEqual(0,self.ping_case('PING 192.0.2.1',True,True))


    def test_five_component_silent_drop_fails_its_own_case(self):
        self.workflow['nodes'][1] = code_node('function main({input}){return {route:"invalid",targetCount:0,invalidTargets:[]}}', [ref('input','start','userChatInput')])
        self.case = {'name':'five component original must be reported','mode':'bound','node_id':'parse','seeds':{'start':{'userChatInput':'192.0.2.1.7'}},'expected':{'route':'invalid','targetCount':0,'invalidTargets':[{'value':'192.0.2.1.7','reason':'IP不是四段'}]}}
        rc, report = self.execute()
        self.assertEqual(1,rc)
        self.assertEqual('five component original must be reported',report['cases'][0]['name'])
        self.assertEqual('expected_mismatch',report['cases'][0]['error'])

    def test_cleaning_invalid_mac_into_another_asset_fails(self):
        self.workflow['nodes'][1] = code_node('function main({input}){const v=input.replace(/[^0-9A-F]/g, "");return {targets:[v]}}', [ref('input','start','userChatInput')])
        self.case = {'name':'seven group MAC not cleaned into asset','mode':'bound','node_id':'parse','seeds':{'start':{'userChatInput':'GG:AA:BB:CC:DD:EE:FF'}},'expected':{'targets':[]}}
        self.error('expected_mismatch')

    def test_async_code_not_silently_treated_as_empty_object(self):
        self.workflow['nodes'][1]['inputs'][0]['value'] = 'async function main({input}){return {invalidTargets:[]}}'
        self.error('async_main_not_supported')

if __name__ == '__main__':
    unittest.main()
