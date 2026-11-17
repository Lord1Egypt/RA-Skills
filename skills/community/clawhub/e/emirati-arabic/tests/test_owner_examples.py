"""Owner consent/spelling checks and scoped context probes, not NLU certification."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'references/owner-examples.json'
CASES = ROOT / 'tests/fixtures/owner_context_cases.json'
# These are the owner's explicitly publication-authorized examples, not chat logs.
EXPECTED = {
    'meeting': ['وين اللقا في المكتاب وللا بقعه غير؟'],
    'clarify': ['مافهمت النقطة، تروم توضحها اكثر؟'],
    'decline': ['يزاك الله خير عالعزيمة، اسمحليه ما روم ايي، خلها وقت ثاني ان شاء الله'],
    'arrival': ['وصلت وللا بعدك تسوق؟', 'وين وصلت؟', 'وصلت وللا بعدك في الطريج؟'],
    'wait': ['اصبر شوي الحينه واصل', 'اتريا شوي قريب واصل'],
    'reschedule': ['هالوقت مش مناسب، خلها عقب المغرب', 'هالوقت ما يناسبنيه، خلها عقب المغرب'],
    'thanks': ['يزاك الله خير، ما قصرت'],
    'correct-order': ['هذا مب اللي طلبته، أنا طلبت شي ثاني'],
    'confirm-intent': ['يعني قصدك جي؟'],
    'late': ['وينك؟ عسى ما شر؟ من الصبح نترياك'],
    'nearer-place': ['المطعم زين لكنه بعيد، نشوفلنا بقعه قريبة'],
    'notify-outgoing': ['خلاص تمام، اذا تغير شي بخبرك', 'الامور طيبة، اذا تغير شي بخبرك', 'خلاص، هذا الجدول، اذا فيه اي تغيير بخبرك'],
    'notify-incoming': ['اذا تغير شي خبرنيه', 'اذا فيه اي تغيير خبرنيه'],
    'tomorrow': ['باجر'],
    'after-tomorrow': ['عقب باجر', 'ورا باجر'],
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def checker():
    spec = importlib.util.spec_from_file_location('owner_checker', ROOT / 'scripts/check_conversions.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OwnerExampleTests(unittest.TestCase):
    def test_exact_authorized_spelling_and_inventory(self):
        self.assertTrue(EXAMPLES.is_file(), 'Missing authorized owner examples')
        data = load(EXAMPLES)
        actual = {e['id']: [v['text'] for v in e['variants']] for e in data['entries']}
        self.assertEqual(actual, EXPECTED)
        self.assertEqual(len(data['entries']), len(EXPECTED))

    def test_attribution_context_and_readable_copy(self):
        self.assertTrue(EXAMPLES.is_file())
        data = load(EXAMPLES)
        self.assertEqual(data['attribution']['kind'], 'owner-contributed')
        self.assertEqual(data['attribution']['author'], 'Binablan')
        self.assertTrue(data['attribution']['publication_authorized'])
        self.assertFalse(data['attribution']['regional_generalization'])
        self.assertFalse(data['attribution']['historical_source_attestation'])
        text = (ROOT / 'references/owner-examples.md').read_text(encoding='utf-8')
        for entry in data['entries']:
            self.assertTrue(entry['context'])
            self.assertTrue(entry['caution'])
            for variant in entry['variants']:
                self.assertTrue(variant['context'])
                self.assertTrue(variant['meaning'])
                self.assertIn(variant['text'], text)

    def test_skill_links_and_direction_guidance(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        for name in ('references/owner-examples.md', 'references/owner-examples.json',
                     'tests/fixtures/owner_context_cases.json'):
            self.assertIn('`' + name + '`', text)
        for term in ('بخبرك', 'خبرنيه', 'مش', 'مب'):
            self.assertIn(term, text)

    def test_context_case_coverage_and_multiple_phrasings(self):
        self.assertTrue(CASES.is_file(), 'Missing context evaluation cases')
        data = load(CASES)
        covered = set()
        ids = []
        for case in data['cases']:
            covered.update(case['owner_example_ids'])
            ids.append(case['id'])
            self.assertTrue(case['input'])
            self.assertTrue(case['manual_checks'])
            self.assertEqual(case['evaluation_status'], 'authored-surface-probes-not-model-outputs')
            self.assertGreaterEqual(len(set(case['accepted_probes'])), 2)
            self.assertGreaterEqual(len(case['rejected_probes']), 2)
        self.assertEqual(covered, set(EXPECTED))
        self.assertEqual(len(ids), len(set(ids)))

    def test_positive_paraphrases_and_negative_meaning_probes(self):
        self.assertTrue(CASES.is_file())
        engine = checker()
        for case in load(CASES)['cases']:
            for wanted, field in ((True, 'accepted_probes'), (False, 'rejected_probes')):
                for output in case[field]:
                    with self.subTest(case=case['id'], output=output):
                        result = engine.evaluate([case], [{'id': case['id'], 'output': output}])
                        self.assertEqual(result['passed'], wanted, result)
                        self.assertTrue(result['human_review_required'])

    def test_notification_direction_is_not_interchangeable(self):
        self.assertTrue(CASES.is_file())
        cases = {c['id']: c for c in load(CASES)['cases']}
        engine = checker()
        for ident, opposite in (('notify-outgoing', 'notify-incoming'), ('notify-incoming', 'notify-outgoing')):
            for text in EXPECTED[opposite]:
                self.assertFalse(engine.evaluate([cases[ident]], [{'id': ident, 'output': text}])['passed'])
        for ident in ('notify-outgoing', 'notify-incoming'):
            good = cases[ident]['accepted_probes'][0]
            for negation in ('ما ', 'مب ', 'مش ', 'لن '):
                self.assertFalse(engine.evaluate([cases[ident]], [{'id': ident, 'output': negation + good}])['passed'])

    def test_relative_day_whitespace_and_both_directions(self):
        self.assertTrue(CASES.is_file())
        cases = {c['id']: c for c in load(CASES)['cases']}
        engine = checker()
        for separator in (' ', '   ', '\t', '\n', '\u00a0'):
            for modifier in ('عقب', 'ورا'):
                text = f'بكتب لك التفاصيل {modifier}{separator}باجر.'
                for ident, expected in (('tomorrow', False), ('after-tomorrow', True)):
                    with self.subTest(id=ident, text=text):
                        self.assertEqual(engine.evaluate([cases[ident]], [{'id': ident, 'output': text}])['passed'], expected)
        for day in ('باجر', 'غداً'):
            text = f'بكتب لك التفاصيل {day}.'
            self.assertFalse(engine.evaluate([cases['after-tomorrow']], [{'id': 'after-tomorrow', 'output': text}])['passed'])

    def test_owner_fixture_cli_exit_codes_and_utf8(self):
        self.assertTrue(CASES.is_file())
        cases = load(CASES)['cases']
        good = [{'id': c['id'], 'output': c['accepted_probes'][0]} for c in cases]
        bad = [{'id': c['id'], 'output': c['rejected_probes'][0]} for c in cases]
        with tempfile.TemporaryDirectory() as directory:
            response = Path(directory) / 'responses.json'
            for payload, expected in ((good, 0), (bad, 1), (good[:-1], 2)):
                response.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
                result = subprocess.run([sys.executable, '-B', '-X', 'utf8=0',
                    str(ROOT / 'scripts/check_conversions.py'), '--cases', str(CASES), '--responses', str(response)],
                    capture_output=True, env=dict(os.environ, PYTHONIOENCODING='cp1252', PYTHONUTF8='0'))
                self.assertEqual(result.returncode, expected, result.stderr.decode('utf-8', errors='replace'))
                self.assertIsInstance(json.loads(result.stdout.decode('utf-8')), dict)


if __name__ == '__main__':
    unittest.main()
