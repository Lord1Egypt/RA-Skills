from __future__ import annotations

from statistics import mean


TUNABLE_KEYS = [
    'min_edge',
    'min_confidence',
    'max_slippage_pct',
    'cycle_interval_minutes',
    'stop_loss_pct',
    'take_profit_pct',
]


def build_learning_snapshot(journal_rows: list[dict], config: dict, live_params: dict | None = None, pending_rules: dict | None = None) -> dict:
    executed = [row for row in journal_rows if row.get('result_type') in {'trade', 'dry_run'} and row.get('decision') == 'candidate']
    edges = [row.get('signal_data', {}).get('edge') for row in executed if row.get('signal_data', {}).get('edge') is not None]
    confidences = [row.get('signal_data', {}).get('confidence') for row in executed if row.get('signal_data', {}).get('confidence') is not None]
    live_params = live_params or {}
    pending_rules = pending_rules or {}
    live_param_deltas = {
        key: live_params[key]
        for key in TUNABLE_KEYS
        if key in live_params and live_params[key] != config[key]
    }
    pending_rule_count = len((pending_rules.get('rules') or []) if isinstance(pending_rules, dict) else [])
    snapshot = {
        'experiments_enabled': True,
        'tunable_keys': TUNABLE_KEYS,
        'candidate_count': len(executed),
        'avg_edge': mean(edges) if edges else None,
        'avg_confidence': mean(confidences) if confidences else None,
        'current_defaults': {key: config[key] for key in TUNABLE_KEYS},
        'live_param_deltas': live_param_deltas,
        'pending_rule_count': pending_rule_count,
    }
    suggestions = []
    if snapshot['avg_edge'] is not None and snapshot['avg_edge'] < config['min_edge']:
        suggestions.append('raise signal quality or narrow market selection before lowering min_edge')
    if snapshot['avg_confidence'] is not None and snapshot['avg_confidence'] < config['min_confidence']:
        suggestions.append('confidence is below threshold; autoresearch should tune signal thresholds before live enablement')
    snapshot['suggestions'] = suggestions
    return snapshot
