#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / 'data' / 'runs'
OUT = ROOT / 'docs' / 'data' / 'demo-metrics.json'

RUN_INDEX = {
    'mineru-baseline': RUNS / 'sample-run' / 'summary.json',
    'mineru-t7': RUNS / 'repair-t7-run' / 'summary.json',
    'mineru-t14': RUNS / 'repair-t14-run' / 'summary.json',
    'sciverse-snapshot': RUNS / 'sciverse-sample-run' / 'summary.json',
}


def load_summary(path: Path) -> dict:
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def as_run(run_id: str, label: str, path: Path) -> dict:
    summary = load_summary(path)
    return {
        'id': run_id,
        'label': label,
        'source': str(path.relative_to(ROOT)).replace('\\', '/'),
        'created_at': summary['created_at'],
        'record_count': summary['record_count'],
        'metrics': summary['metrics'],
        'strict_rates': summary['strict_rates'],
        'by_funnel_stage': summary.get('by_funnel_stage') or [],
        'repair_candidates': summary.get('repair_candidates') or [],
    }


mineru_runs = [
    as_run('baseline', 'Baseline', RUN_INDEX['mineru-baseline']),
    as_run('t7', 'T+7', RUN_INDEX['mineru-t7']),
    as_run('t14', 'T+14', RUN_INDEX['mineru-t14']),
]
sciverse_runs = [as_run('snapshot', 'Public snapshot', RUN_INDEX['sciverse-snapshot'])]

baseline_metrics = mineru_runs[0]['metrics']
latest_metrics = mineru_runs[-1]['metrics']
mineru_deltas = {
    key: round(latest_metrics[key] - baseline_metrics[key], 2)
    for key in baseline_metrics
}

payload = {
    'brand': {
        'name': 'DevTool Answer Monitor',
        'tagline': 'Track what LLMs say before users choose your developer tool.',
    },
    'projects': [
        {
            'id': 'mineru',
            'name': 'MinerU',
            'description': 'Repair-loop sample for a developer tool with baseline, T+7, and T+14 artifacts.',
            'story': 'A version-controlled repair story that improves mention, positivity, and ecosystem clarity.',
            'runs': mineru_runs,
            'headline': {
                'title': 'Repair loop result',
                'body': 'By T+14, the public sample lifts mention rate by 10 points and ecosystem accuracy by 50 points.',
            },
            'deltas_from_baseline_to_latest': mineru_deltas,
            'links': {
                'benchmark': 'benchmark/mineru-public-benchmark.md',
                'weekly_report': 'data/runs/sample-run/weekly_report.md',
            },
        },
        {
            'id': 'sciverse',
            'name': 'Sciverse API',
            'description': 'Public snapshot for a scientific API and agent workflow product.',
            'story': 'A funnel-stage benchmark that shows strong capability understanding but weak activation confidence.',
            'runs': sciverse_runs,
            'headline': {
                'title': 'Activation gap',
                'body': 'The public sample keeps capability accuracy at 100% while activation positivity falls to 25%.',
            },
            'links': {
                'benchmark': 'benchmark/sciverse-api-public-benchmark.md',
                'weekly_report': 'data/runs/sciverse-sample-run/weekly_report.md',
            },
        },
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'wrote {OUT.relative_to(ROOT)}')
