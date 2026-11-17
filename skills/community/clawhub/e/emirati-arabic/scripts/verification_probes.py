"""Reproduce narrow checker failures and validate its CLI exit codes."""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    configure = getattr(stream, 'reconfigure', None)
    if configure is not None:
        configure(encoding='utf-8')

parser = argparse.ArgumentParser()
parser.add_argument('--project', required=True, type=Path)
args = parser.parse_args()
project = args.project.resolve()
spec = importlib.util.spec_from_file_location('checker', project / 'scripts/check_conversions.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
cases = json.loads((project / 'tests/fixtures/abu_dhabi_cases.json').read_text(encoding='utf-8'))['cases']
by_id = {c['id']: c for c in cases}
records = []
probes = [
    ('appointment', 'موعدنا مع مريم يوم الجمعة الساعة 15:30.'),
    ('quantity', 'أحتاج 13 نسخ، مب 20.'),
    ('quantity', 'أحتاج 3 نسخ، مب 2.5.'),
    ('formal', 'تنبيه: يرجى إرسال الطلب قبل يوم الاثنين.'),
    ('formal', 'يرجى إرسال الطلب قبل يوم الاثنين. EXTRA'),
]
for ident, output in probes:
    result = checker.evaluate([by_id[ident]], [{'id': ident, 'output': output}])
    records.append({'id': ident, 'output': output, 'expected_rejection': True,
                    'actual_passed': result['passed'], 'probe_passed': not result['passed']})
with tempfile.TemporaryDirectory(prefix='checker-probe-', dir=Path(__file__).resolve().parent) as directory:
    path = Path(directory) / 'responses.json'
    for name, content in [('missing-cases', '[]'), ('malformed-json', '{')]:
        path.write_text(content, encoding='utf-8')
        result = subprocess.run([sys.executable, '-B', str(project / 'scripts/check_conversions.py'),
                                 '--responses', str(path)], capture_output=True, text=True, encoding='utf-8')
        records.append({'id': name, 'expected_exit': 2, 'actual_exit': result.returncode,
                        'probe_passed': result.returncode == 2})
print(json.dumps({'passed': all(r['probe_passed'] for r in records), 'probes': records},
                 ensure_ascii=False, indent=2))
raise SystemExit(0 if all(r['probe_passed'] for r in records) else 1)
