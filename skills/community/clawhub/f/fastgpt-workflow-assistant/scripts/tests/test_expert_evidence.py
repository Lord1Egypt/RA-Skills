"""Behavioral checks for version evidence and conservative branch contracts."""
from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from inspect_expert_versions import inspect
from check_route_contract import check


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.workflow = {'nodes': [{'nodeId': x} for x in ('router', 'asset', 'ping', 'reply')],
                         'edges': [{'source': 'router', 'sourceHandle': 'query', 'target': 'asset'},
                                   {'source': 'asset', 'target': 'reply'}]}
        self.contract = {'terminal_nodes': ['reply'], 'cases': [
            {'source': 'router', 'source_handle': 'query', 'required_nodes': ['asset', 'reply'],
             'forbidden_nodes': ['ping']}]}

    def test_good_graph_has_explicit_limits(self):
        r = check(self.workflow, self.contract)
        self.assertTrue(r['passed'])
        self.assertFalse(r['conditions_evaluated'])
        self.assertFalse(r['code_executed'])
        self.assertEqual(r['platform_runtime'], 'not_verified')

    def test_wrong_edge_rejected(self):
        self.workflow['edges'][0]['target'] = 'ping'
        self.assertFalse(check(self.workflow, self.contract)['passed'])

    def test_extra_bypass_not_ignored(self):
        self.workflow['edges'].append({'source': 'asset', 'sourceHandle': 'extra', 'target': 'ping'})
        r = check(self.workflow, self.contract)
        self.assertIn('forbidden_nodes_reachable', r['cases'][0]['errors'])

    def test_terminal_outgoing_rejected_and_traversed(self):
        self.workflow['edges'].append({'source': 'reply', 'target': 'ping'})
        errors = check(self.workflow, self.contract)['cases'][0]['errors']
        self.assertIn('terminal_has_outgoing_edges', errors)
        self.assertIn('forbidden_nodes_reachable', errors)

    def test_missing_handle_and_multiple_entries_fail(self):
        bad = copy.deepcopy(self.workflow)
        bad['edges'][0]['sourceHandle'] = 'other'
        self.assertFalse(check(bad, self.contract)['passed'])
        self.workflow['edges'].append({'source': 'router', 'sourceHandle': 'query', 'target': 'reply'})
        self.assertFalse(check(self.workflow, self.contract)['passed'])

    def test_dangling_duplicate_and_cycle_fail(self):
        for edge in ({'source': 'asset', 'target': 'missing'}, self.workflow['edges'][0],
                     {'source': 'asset', 'target': 'router'}):
            bad = copy.deepcopy(self.workflow)
            bad['edges'].append(edge)
            self.assertFalse(check(bad, self.contract)['passed'])

    def test_empty_or_unknown_contract_rejected(self):
        for contract in ({'cases': []}, {'cases': [{'source': 'router', 'source_handle': 'query',
                                                'required_nodes': ['missing']}]}):
            with self.assertRaises(ValueError):
                check(self.workflow, contract)

    def test_hidden_plugin_found_and_versions_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / '.codebuddy-plugin/plugin.json'
            plugin.parent.mkdir()
            plugin.write_text(json.dumps({'name': 'example-expert', 'version': '1.0.0',
                                          'skills': ['./skills/example']}), encoding='utf-8')
            skill = root / 'skills/example/assets/skill-version.json'
            skill.parent.mkdir(parents=True)
            skill.write_text(json.dumps({'skill_name': 'example', 'version': '2.9.3'}), encoding='utf-8')
            (root / 'skills/example/SKILL.md').write_text('example', encoding='utf-8')
            result = inspect(root)
            self.assertEqual(result['experts'][0]['expert_version'], '1.0.0')
            self.assertEqual(result['skills'][0]['skill_version'], '2.9.3')
            self.assertEqual(result['warnings'], [])
            archive = root / 'example.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                for file in (plugin, skill, root / 'skills/example/SKILL.md'):
                    z.write(file, 'outer/' + file.relative_to(root).as_posix())
            zipped = inspect(archive)
            self.assertEqual(zipped['experts'][0]['expert_version'], '1.0.0')
            self.assertTrue(zipped['archive_sha256'])

    def test_missing_plugin_is_unknown_and_missing_skill_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            r = inspect(Path(directory))
            self.assertFalse(r['experts'])
            self.assertIn('unknown, not proven absent', r['warnings'][0])
            p = Path(directory) / '.codebuddy-plugin/plugin.json'
            p.parent.mkdir()
            p.write_text(json.dumps({'version': '3.0.0', 'skills': ['./skills/missing']}))
            self.assertIn('Declared skill version evidence missing', inspect(Path(directory))['warnings'][0])

    def test_archive_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'unsafe.zip'
            with zipfile.ZipFile(p, 'w') as z:
                z.writestr('../SKILL.md', 'example')
            with self.assertRaises(ValueError):
                inspect(p)


if __name__ == '__main__':
    unittest.main()
