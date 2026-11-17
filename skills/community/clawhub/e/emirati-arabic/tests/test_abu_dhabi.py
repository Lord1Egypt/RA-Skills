"""Offline provenance/package and narrow conversion-checker regression tests.

These tests do not certify contemporary dialect fluency.
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_conversions.py'
CASES = ROOT / 'tests/fixtures/abu_dhabi_cases.json'


def load_checker():
    assert SCRIPT.is_file(), 'Conversion checker is not implemented yet'
    spec = importlib.util.spec_from_file_location('check_conversions', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AbuDhabiPackageTests(unittest.TestCase):
    def test_version_and_opt_in_profile(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('version: 0.2.1-rc.1', text.splitlines())
        self.assertIn('abu-dhabi', text)
        self.assertIn('general-emirati', text)
        self.assertIn('opt-in', text)

    def test_all_original_files_remain(self):
        for name in ('SKILL.md', 'README.md', 'LICENSE', '.gitignore',
                     'CONTRIBUTING.md', 'THIRD_PARTY_NOTICES.md',
                     'references/sources.md', 'references/examples.md',
                     'tests/test_skill_package.py'):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_lexicon_has_specific_evidence_and_original_examples(self):
        data = json.loads((ROOT / 'references/abu-dhabi-lexicon.json').read_text(encoding='utf-8'))
        sources = (ROOT / 'references/abu-dhabi-sources.md').read_text(encoding='utf-8')
        self.assertEqual(data['version'], '0.2.0')
        self.assertGreaterEqual(len(data['entries']), 10)
        ids = [entry['id'] for entry in data['entries']]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in data['entries']:
            with self.subTest(entry=entry['id']):
                for key in ('form', 'meaning_ar', 'example', 'context', 'caution', 'source_id', 'scope', 'locator'):
                    self.assertTrue(entry[key], key)
                self.assertIn(entry['scope'], ('abu-dhabi-source-attested', 'uae-shared'))
                self.assertFalse(entry['exclusive_to_abu_dhabi'])
                self.assertEqual(entry['example_status'], 'original-provisional')
                self.assertIn('### ' + entry['source_id'], sources)
                self.assertIsInstance(entry['locator']['pdf_page'], int)
                self.assertTrue(entry['locator']['printed_page'])
                self.assertEqual(entry['verification'], 'page-image-inspected')

    def test_fixture_metadata_and_references(self):
        data = json.loads(CASES.read_text(encoding='utf-8'))
        self.assertEqual(data['version'], '0.2.0')
        self.assertGreaterEqual(len(data['cases']), 16)
        ids = [case['id'] for case in data['cases']]
        self.assertEqual(len(ids), len(set(ids)))
        for case in data['cases']:
            for field in ('input', 'instruction', 'reference', 'manual_checks', 'evidence'):
                self.assertTrue(case[field], (case['id'], field))
            self.assertIn(case['profile'], ('abu-dhabi', 'general-emirati', 'preserve-register'))
            for pattern in case.get('forbidden_patterns', []):
                re.compile(pattern)
            for choices in case.get('required_any', []):
                self.assertTrue(choices)
                for pattern in choices:
                    re.compile(pattern)

    def test_skill_links_all_runtime_material(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        expected = ('references/abu-dhabi.md', 'references/abu-dhabi-sources.md',
                    'references/abu-dhabi-lexicon.json', 'references/abu-dhabi-examples.md',
                    'references/evaluation.md', 'scripts/check_conversions.py',
                    'tests/fixtures/abu_dhabi_cases.json')
        for path in expected:
            self.assertIn('`' + path + '`', text)
            self.assertTrue((ROOT / path).is_file(), path)


class ConversionCheckerTests(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker()
        self.cases = json.loads(CASES.read_text(encoding='utf-8'))['cases']
        self.responses = [{'id': c['id'], 'output': c['reference']} for c in self.cases]

    def test_authored_references_pass_narrow_checks(self):
        report = self.checker.evaluate(self.cases, self.responses)
        self.assertTrue(report['passed'], report)
        self.assertTrue(report['human_review_required'])
        self.assertEqual(report['evaluated'], len(self.cases))

    def test_missing_case_is_not_a_partial_pass(self):
        with self.assertRaises(ValueError):
            self.checker.evaluate(self.cases, self.responses[:-1])

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            self.checker.evaluate(self.cases, self.responses + [self.responses[0]])

    def test_unknown_id_rejected(self):
        with self.assertRaises(ValueError):
            self.checker.evaluate(self.cases, self.responses + [{'id': 'unknown', 'output': 'نص'}])

    def test_empty_or_wrong_typed_output_rejected(self):
        for value in ('', '   ', None, 42, ['نص']):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.checker.evaluate(self.cases, [dict(self.responses[0], output=value)] + self.responses[1:])

    def test_name_or_time_mutation_fails(self):
        changed = [dict(r, output=r['output'].replace('5:30', '6:30')) if r['id'] == 'appointment' else r for r in self.responses]
        report = self.checker.evaluate(self.cases, changed)
        self.assertFalse(report['passed'])
        self.assertIn('appointment', [r['id'] for r in report['results'] if not r['passed']])

    def test_appointment_rejects_time_substrings(self):
        case = next(c for c in self.cases if c['id'] == 'appointment')
        for time in ('15:30', '5:300', '1:5:30', '5:30:00',
                     '١5:30', '5:30٠'):
            with self.subTest(time=time):
                output = case['reference'].replace('5:30', time)
                report = self.checker.evaluate([case], [{'id': case['id'], 'output': output}])
                self.assertFalse(report['passed'], report)

    def test_quantity_rejects_numeric_substrings(self):
        case = next(c for c in self.cases if c['id'] == 'quantity')
        for wanted, rejected in (('13', '20'), ('13', '2'), ('30', '2'),
                                 ('3', '12'), ('3', '20'),
                                 ('١3', '2'), ('3', '2٠')):
            with self.subTest(wanted=wanted, rejected=rejected):
                output = f'أحتاج {wanted} نسخ، مب {rejected}.'
                report = self.checker.evaluate([case], [{'id': case['id'], 'output': output}])
                self.assertFalse(report['passed'], report)

    def test_formal_rejects_prefixed_or_appended_material(self):
        case = next(c for c in self.cases if c['id'] == 'formal')
        for prefix, suffix in (('تنبيه: ', ''), ('', ' شكراً.'),
                               ('\n', ''), ('', '\nإضافة.'),
                               (' ', ''), ('', ' '), ('', '\n')):
            with self.subTest(prefix=prefix, suffix=suffix):
                output = prefix + case['reference'] + suffix
                report = self.checker.evaluate([case], [{'id': case['id'], 'output': output}])
                self.assertFalse(report['passed'], report)

    def test_negative_fixtures_are_actually_rejected(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                bad = [{'id': case['id'], 'output': case['negative']}]
                self.assertFalse(self.checker.evaluate([case], bad)['passed'])

    def test_unrecognized_response_fields_rejected(self):
        with self.assertRaises(ValueError):
            self.checker.evaluate(self.cases, [dict(self.responses[0], typo='x')] + self.responses[1:])

    def test_cli_good_bad_and_malformed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'responses.json'
            for payload, expected in ((self.responses, 0), (self.responses[:-1], 2), (None, 2)):
                path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
                run = subprocess.run([sys.executable, '-B', str(SCRIPT), '--responses', str(path)], capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
            bad = [dict(r, output=c['negative']) for r, c in zip(self.responses, self.cases)]
            path.write_text(json.dumps(bad, ensure_ascii=False), encoding='utf-8')
            run = subprocess.run([sys.executable, '-B', str(SCRIPT), '--responses', str(path)], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)


if __name__ == '__main__':
    unittest.main()
