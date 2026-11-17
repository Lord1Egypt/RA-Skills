"""Review regressions; surface guards, not native-language certification."""
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('review_checker', ROOT / 'scripts/check_conversions.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
CASES = json.loads((ROOT / 'tests/fixtures/abu_dhabi_cases.json').read_text(encoding='utf-8'))['cases']
BY_ID = {case['id']: case for case in CASES}


def passes(ident, output):
    return checker.evaluate([BY_ID[ident]], [{'id': ident, 'output': output}])['passed']


class ReviewRegressionTests(unittest.TestCase):
    def test_verification_probes_emit_utf8_under_cp1252(self):
        env = dict(os.environ, PYTHONUTF8='0', PYTHONIOENCODING='cp1252')
        result = subprocess.run(
            [sys.executable, '-B', '-X', 'utf8=0',
             str(ROOT / 'scripts/verification_probes.py'), '--project', str(ROOT)],
            capture_output=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', errors='replace'))
        decoded = result.stdout.decode('utf-8')
        self.assertIn('موعدنا', decoded)
        self.assertTrue(json.loads(decoded)['passed'])

    def test_quantity_rejects_decimal_or_extended_numbers(self):
        for wanted, rejected in (('3', '2.5'), ('3', '2٫5'), ('3', '2,5'),
                                 ('3', '2٫٥'), ('3', '2e3'), ('3', '2/5'),
                                 ('3', '2%'), ('2.3', '2'), ('٠.3', '2'),
                                 ('1,3', '2'), ('١٫3', '2'), ('3', '2.0')):
            with self.subTest(wanted=wanted, rejected=rejected):
                self.assertFalse(passes('quantity', f'أحتاج {wanted} نسخ، مب {rejected}.'))

    def test_quantity_allows_sentence_punctuation(self):
        for output in ('أحتاج 3 نسخ، مب 2.', 'أحتاج 3 نسخ، ليس 2.',
                       'أحتاج 3 نسخ، مب 2، شكراً.'):
            with self.subTest(output=output):
                self.assertTrue(passes('quantity', output))

    def test_future_accepts_both_tomorrow_forms(self):
        for output in ('بكتب لك التفاصيل باجر.', 'بكتب لك التفاصيل غداً.',
                       'سأكتب لك التفاصيل باجر.', 'سأكتب لك التفاصيل غداً.'):
            with self.subTest(output=output):
                self.assertTrue(passes('future', output))

    def test_future_rejects_changed_tense_or_day(self):
        for output in ('كتبت لك التفاصيل باجر.', 'أكتب لك التفاصيل باجر.',
                       'بكتب لك التفاصيل أمس.', 'بكتب لك التفاصيل.',
                       'بكتب لك التفاصيل عقب أسبوع.'):
            with self.subTest(output=output):
                self.assertFalse(passes('future', output))

    def test_future_rejects_aqab_tomorrow_with_whitespace(self):
        for separator in (' ', '   ', '\t', '\n', '\u00a0'):
            output = f'بكتب لك التفاصيل عقب{separator}باجر.'
            with self.subTest(separator=repr(separator)):
                self.assertFalse(passes('future', output))

    def test_future_rejects_wara_tomorrow_with_whitespace(self):
        for separator in (' ', '   ', '\t', '\n', '\u00a0'):
            output = f'بكتب لك التفاصيل ورا{separator}باجر.'
            with self.subTest(separator=repr(separator)):
                self.assertFalse(passes('future', output))

    def test_future_rejects_negation(self):
        for output in ('ما بكتب لك التفاصيل غداً.', 'مب بكتب لك التفاصيل باجر.',
                       'لن أكتب لك التفاصيل باجر.', 'بكتب لك التفاصيل مو باجر.'):
            with self.subTest(output=output):
                self.assertFalse(passes('future', output))


if __name__ == '__main__':
    unittest.main()
