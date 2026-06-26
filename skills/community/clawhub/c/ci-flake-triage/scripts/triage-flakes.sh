#!/usr/bin/env bash
set -euo pipefail

JUNIT_GLOB="${JUNIT_GLOB:-test-results/**/*.xml}"
TRIAGE_TOP="${TRIAGE_TOP:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
FAIL_ON_PERSISTENT="${FAIL_ON_PERSISTENT:-0}"
FAIL_ON_FLAKE="${FAIL_ON_FLAKE:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TRIAGE_TOP" =~ ^[0-9]+$ ]] || [[ "$TRIAGE_TOP" -eq 0 ]]; then
  echo "ERROR: TRIAGE_TOP must be a positive integer (got: $TRIAGE_TOP)" >&2
  exit 1
fi

if [[ "$FAIL_ON_PERSISTENT" != "0" && "$FAIL_ON_PERSISTENT" != "1" ]]; then
  echo "ERROR: FAIL_ON_PERSISTENT must be 0 or 1 (got: $FAIL_ON_PERSISTENT)" >&2
  exit 1
fi

if [[ "$FAIL_ON_FLAKE" != "0" && "$FAIL_ON_FLAKE" != "1" ]]; then
  echo "ERROR: FAIL_ON_FLAKE must be 0 or 1 (got: $FAIL_ON_FLAKE)" >&2
  exit 1
fi

python3 - "$JUNIT_GLOB" "$TRIAGE_TOP" "$OUTPUT_FORMAT" "$FAIL_ON_PERSISTENT" "$FAIL_ON_FLAKE" <<'PY'
import glob
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

junit_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
fail_on_persistent = sys.argv[4] == '1'
fail_on_flake = sys.argv[5] == '1'

files = sorted(glob.glob(junit_glob, recursive=True))
if not files:
    print(f'ERROR: no JUnit files matched JUNIT_GLOB={junit_glob}', file=sys.stderr)
    sys.exit(1)


def status_for_case(case):
    if case.find('failure') is not None:
        return 'failed'
    if case.find('error') is not None:
        return 'error'
    if case.find('skipped') is not None:
        return 'skipped'
    return 'passed'


stats = defaultdict(lambda: {
    'statuses': [],
    'files': set(),
    'durations': [],
})

parse_errors = []
total_testcases = 0

for path in files:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    if root.tag == 'testsuite':
        cases = root.findall('.//testcase')
    else:
        cases = root.findall('.//testcase')

    for case in cases:
        name = case.attrib.get('name', '<unnamed>')
        classname = case.attrib.get('classname', '<no-classname>')
        key = f'{classname}::{name}'
        status = status_for_case(case)
        duration = case.attrib.get('time', '0')

        bucket = stats[key]
        bucket['statuses'].append(status)
        bucket['files'].add(path)
        try:
            bucket['durations'].append(float(duration))
        except ValueError:
            bucket['durations'].append(0.0)

        total_testcases += 1

records = []
for test_id, item in stats.items():
    statuses = item['statuses']
    has_fail_like = any(s in ('failed', 'error') for s in statuses)
    has_pass = any(s == 'passed' for s in statuses)
    has_skip = any(s == 'skipped' for s in statuses)

    if has_fail_like and has_pass:
        classification = 'flaky'
    elif has_fail_like:
        classification = 'persistent-failure'
    elif has_skip and not has_pass:
        classification = 'skipped-only'
    else:
        classification = 'stable-pass'

    attempts = len(statuses)
    fail_like_count = sum(1 for s in statuses if s in ('failed', 'error'))
    pass_count = sum(1 for s in statuses if s == 'passed')
    skip_count = sum(1 for s in statuses if s == 'skipped')
    avg_duration = sum(item['durations']) / len(item['durations']) if item['durations'] else 0.0

    # Higher score means higher triage priority.
    score = fail_like_count * 10 + (attempts - 1) * 3 + (1 if classification == 'persistent-failure' else 0)

    records.append({
        'test_id': test_id,
        'classification': classification,
        'attempts': attempts,
        'fail_like_count': fail_like_count,
        'pass_count': pass_count,
        'skip_count': skip_count,
        'avg_duration_seconds': round(avg_duration, 4),
        'files_seen': len(item['files']),
        'score': score,
        'statuses': statuses,
    })

records.sort(key=lambda r: (-r['score'], r['test_id']))

flake = [r for r in records if r['classification'] == 'flaky']
persistent = [r for r in records if r['classification'] == 'persistent-failure']
skipped_only = [r for r in records if r['classification'] == 'skipped-only']
stable = [r for r in records if r['classification'] == 'stable-pass']

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'total_testcase_rows': total_testcases,
    'unique_tests': len(records),
    'flaky_candidates': len(flake),
    'persistent_failures': len(persistent),
    'skipped_only': len(skipped_only),
    'stable_pass': len(stable),
    'top_n': top_n,
}

if output_format == 'json':
    out = {
        'summary': summary,
        'top_flaky': flake[:top_n],
        'persistent_failures': persistent[:top_n],
        'all_tests': records,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
else:
    print('CI FLAKE TRIAGE REPORT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} unique_tests={summary['unique_tests']} "
        f"rows={summary['total_testcase_rows']} flaky={summary['flaky_candidates']} "
        f"persistent={summary['persistent_failures']} skipped_only={summary['skipped_only']} "
        f"stable={summary['stable_pass']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    print('---')
    print(f'TOP FLAKY ({min(top_n, len(flake))})')
    if not flake:
        print('none')
    else:
        for row in flake[:top_n]:
            print(
                f"- {row['test_id']} "
                f"attempts={row['attempts']} fail_like={row['fail_like_count']} "
                f"pass={row['pass_count']} avg_s={row['avg_duration_seconds']}"
            )

    print('---')
    print(f'PERSISTENT FAILURES ({min(top_n, len(persistent))})')
    if not persistent:
        print('none')
    else:
        for row in persistent[:top_n]:
            print(
                f"- {row['test_id']} "
                f"attempts={row['attempts']} fail_like={row['fail_like_count']} "
                f"pass={row['pass_count']} avg_s={row['avg_duration_seconds']}"
            )

exit_code = 0
if fail_on_persistent and persistent:
    exit_code = 1
if fail_on_flake and flake:
    exit_code = 1

sys.exit(exit_code)
PY
