from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
JOURNAL_PATH = DATA_DIR / 'journal.jsonl'
LLM_DECISIONS_PATH = DATA_DIR / 'llm_decisions.jsonl'
LIVE_PARAMS_PATH = DATA_DIR / 'live_params.json'
PENDING_RULES_PATH = DATA_DIR / 'pending_rules.json'
DEFAULTS_PATH = ROOT / 'config' / 'defaults.json'
TUNABLE_KEYS = [
    'min_edge',
    'min_confidence',
    'max_slippage_pct',
    'cycle_interval_minutes',
    'stop_loss_pct',
    'take_profit_pct',
]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def build_review_report() -> dict[str, Any]:
    journal_rows = _read_jsonl(JOURNAL_PATH)
    llm_rows = _read_jsonl(LLM_DECISIONS_PATH)
    live_params = _read_json(LIVE_PARAMS_PATH, {})
    pending_rules = _read_json(PENDING_RULES_PATH, {'rules': []})
    defaults = _read_json(DEFAULTS_PATH, {})

    btc_candidates = [
        {
            'market_id': row.get('market_id'),
            'window': row.get('window'),
            'question': row.get('market_question') or row.get('question'),
            'raw_action': (row.get('validated_decision') or {}).get('action'),
            'reject_reason': row.get('reject_reason'),
        }
        for row in llm_rows
        if row.get('btc_only')
    ]

    action_counts = Counter(
        (row.get('validated_decision') or {}).get('action')
        for row in llm_rows
        if (row.get('validated_decision') or {}).get('action')
    )
    deterministic_rejects = [
        row
        for row in llm_rows
        if row.get('reject_reason')
    ]
    reject_reasons = Counter(row.get('reject_reason') or 'unknown' for row in deterministic_rejects)
    accepted_trades = [
        {
            'market_id': row.get('market_id'),
            'window': row.get('window'),
            'side': row.get('side'),
            'amount': row.get('amount'),
            'result_type': row.get('result_type'),
        }
        for row in journal_rows
        if row.get('decision') == 'candidate' and row.get('result_type') in {'trade', 'dry_run'}
    ]
    learned_param_changes = {
        key: live_params[key]
        for key in TUNABLE_KEYS
        if key in live_params and live_params[key] != defaults.get(key)
    }
    pending_rule_list = pending_rules.get('rules') if isinstance(pending_rules, dict) else []
    pending_rule_list = pending_rule_list if isinstance(pending_rule_list, list) else []

    report = {
        'btc_only_candidates_seen': len(btc_candidates),
        'btc_candidates': btc_candidates,
        'model_actions': {
            'yes': action_counts.get('yes', 0),
            'no': action_counts.get('no', 0),
            'skip': action_counts.get('skip', 0),
        },
        'deterministic_rejects': len(deterministic_rejects),
        'accepted_trades': accepted_trades,
        'learned_param_changes': learned_param_changes,
        'pending_rules': pending_rule_list,
        'top_reject_reasons': reject_reasons.most_common(10),
        'journal_rows': len(journal_rows),
        'llm_decision_rows': len(llm_rows),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description='Summarize BTC sprint logs and LLM decisions')
    parser.add_argument('--review', action='store_true', help='Print the review report')
    args = parser.parse_args()

    report = build_review_report()
    if args.review:
        print(json.dumps(report, indent=2, sort_keys=True, default=str))
        return
    print(json.dumps(report, indent=2, sort_keys=True, default=str))


if __name__ == '__main__':
    main()
