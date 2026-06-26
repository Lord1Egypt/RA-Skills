from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from simmer_sdk import SimmerClient

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / 'modules'
if str(MODULES) not in sys.path:
    sys.path.insert(0, str(MODULES))

from btc_discord_alert import DiscordAlertError, send_discord_alert
from btc_heartbeat import build_heartbeat
from btc_llm_decider import (
    LLM_BLOCKER,
    MissingLLMCredentialsError,
    apply_eligible_rules,
    append_jsonl,
    build_decision_record,
    build_provider_from_env,
    load_learned_params,
    merge_learned_params,
    read_json_file,
    record_pending_rule,
    run_llm_decision,
    write_json_file,
)
from btc_position_manager import enforce_risk_limits
from btc_regime_filter import evaluate_regime
from btc_self_learn import build_learning_snapshot
from btc_sprint_executor import execute_trade
from btc_sprint_signal import SignalDecision, build_signal
from btc_trade_journal import append_journal, read_journal


DATA_DIR = ROOT / 'data'
JOURNAL_PATH = DATA_DIR / 'journal.jsonl'
LEARNING_PATH = DATA_DIR / 'learning.json'
LIVE_PARAMS_PATH = DATA_DIR / 'live_params.json'
PENDING_RULES_PATH = DATA_DIR / 'pending_rules.json'
LLM_DECISIONS_PATH = DATA_DIR / 'llm_decisions.jsonl'
DEFAULTS_PATH = ROOT / 'config' / 'defaults.json'

TUNABLE_KEYS = [
    'min_edge',
    'min_confidence',
    'max_slippage_pct',
    'cycle_interval_minutes',
    'stop_loss_pct',
    'take_profit_pct',
]


def _trace_enabled() -> bool:
    value = (os.environ.get('BTC_SPRINT_TRACE') or '').strip().lower()
    return value in {'1', 'true', 'yes', 'on'}


def trace(*parts: object) -> None:
    if _trace_enabled():
        print('[TRACE]', *parts, flush=True)


def _hard_clamp_config(config: dict) -> dict:
    config['asset'] = 'BTC'
    config['windows'] = ['5m', '15m']
    config['trading_venue'] = 'polymarket'
    config['binance_symbol'] = 'BTCUSDT'
    config.setdefault('binance_interval', '1m')
    config.setdefault('dry_run', True)
    config.setdefault('validate_real_path', True)
    config['min_edge'] = float(config.get('min_edge', 0.07))
    config['min_confidence'] = float(config.get('min_confidence', 0.65))
    config['max_slippage_pct'] = float(config.get('max_slippage_pct', 0.1))
    config['cycle_interval_minutes'] = int(config.get('cycle_interval_minutes', 15))
    config['stop_loss_pct'] = float(config.get('stop_loss_pct', 0.1))
    config['take_profit_pct'] = float(config.get('take_profit_pct', 0.12))
    return config


def load_config(defaults_path: Path = DEFAULTS_PATH, live_params_path: Path = LIVE_PARAMS_PATH) -> dict:
    config = json.loads(defaults_path.read_text())
    learned = load_learned_params(live_params_path)
    config = merge_learned_params(config, learned)
    env_map = {
        'BTC_SPRINT_DRY_RUN': ('dry_run', lambda v: v == '1'),
        'BTC_SPRINT_VALIDATE_REAL_PATH': ('validate_real_path', lambda v: v == '1'),
        'LLM_PROVIDER': ('llm_provider', str),
        'LLM_MODEL': ('llm_model', str),
        'BINANCE_SYMBOL': ('binance_symbol', str),
        'BINANCE_INTERVAL': ('binance_interval', str),
        'BTC_SPRINT_PROFILE': ('execution_profile', lambda v: v.strip().lower()),
    }
    for env_key, (cfg_key, caster) in env_map.items():
        if env_key in os.environ and os.environ[env_key]:
            config[cfg_key] = caster(os.environ[env_key])
    config = _hard_clamp_config(config)
    profile = str(config.get('execution_profile', 'balanced')).strip().lower() or 'balanced'
    config['execution_profile'] = profile
    if profile == 'aggressive':
        config['min_edge'] = min(config['min_edge'], 0.05)
        config['min_confidence'] = min(config['min_confidence'], 0.60)
        config['cycle_interval_minutes'] = min(config['cycle_interval_minutes'], 10)
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='BTC sprint bot for Simmer')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='Never submit a live trade')
    mode.add_argument('--live', action='store_true', help='Submit real trades when approved')
    parser.add_argument('--once', action='store_true', help='Run one cycle')
    parser.add_argument('--loop', action='store_true', help='Run continuously')
    parser.add_argument('--validate-real-path', action='store_true', help='Call prepare_real_trade during dry-run')
    parser.add_argument('--discord-test-alert', action='store_true', help='Send one Discord webhook test message and exit')
    return parser.parse_args()


def get_client(config: dict, dry_run: bool) -> SimmerClient:
    api_key = os.environ.get('SIMMER_API_KEY')
    if not api_key:
        raise SystemExit('SIMMER_API_KEY is required')
    return SimmerClient(api_key=api_key, venue='polymarket', live=not dry_run)


def setup_external_wallet(client: SimmerClient) -> None:
    """One-time Polygon wallet linkage and USDC.e approval.

    Called on startup when WALLET_PRIVATE_KEY is present in the environment.
    Both calls are idempotent — safe to run each process start.
    Requires eth-account (pip install eth-account).
    """
    client.link_wallet()
    client.set_approvals()


def market_window_from_tags(tags: list[str]) -> str:
    if 'fast-5m' in tags:
        return '5m'
    if 'fast-15m' in tags:
        return '15m'
    return 'unknown'


def build_signal_payload(signal) -> dict:
    payload = signal.to_signal_data()
    payload['action'] = signal.action
    payload['reasoning'] = signal.reasoning
    return payload


def build_market_context(market, window: str, context: dict) -> dict:
    market_context = context.get('market', {}) if isinstance(context, dict) else {}
    slippage = context.get('slippage', {}) if isinstance(context, dict) else {}
    return {
        'market_id': getattr(market, 'id', None),
        'question': getattr(market, 'question', ''),
        'window': window,
        'asset': 'BTC',
        'venue': 'polymarket',
        'resolves_at': market_context.get('resolves_at'),
        'fee_rate_bps': market_context.get('fee_rate_bps'),
        'spread_pct': slippage.get('spread_pct'),
        'warnings': list(context.get('warnings') or []) if isinstance(context, dict) else [],
    }


def _combine_reject_reasons(*reasons: str | None) -> str | None:
    flattened = []
    for reason in reasons:
        if not reason:
            continue
        if isinstance(reason, str):
            flattened.extend(item.strip() for item in reason.split(';') if item.strip())
    if not flattened:
        return None
    deduped = list(dict.fromkeys(flattened))
    return '; '.join(deduped)


def _market_debug_label(market) -> str:
    return f"{getattr(market, 'id', None)}|{getattr(market, 'question', '')}"


def _is_btc_market(market) -> bool:
    bits = [
        getattr(market, 'asset', None),
        getattr(market, 'market_source', None),
        getattr(market, 'id', None),
        getattr(market, 'question', None),
        ' '.join(getattr(market, 'tags', []) or []),
    ]
    joined = ' '.join(str(bit).lower() for bit in bits if bit)
    return 'btc' in joined or 'bitcoin' in joined


def _synthetic_btc_market() -> SimpleNamespace:
    return SimpleNamespace(
        id='btc-fast-synthetic-debug',
        question='Synthetic BTC debug candidate for dry-run tracing',
        tags=['fast-5m'],
        asset='BTC',
    )


def _synthetic_market_context() -> dict:
    return {
        'market': {
            'resolves_at': (datetime.now(timezone.utc).replace(microsecond=0) + timedelta(minutes=90)).isoformat(),
            'fee_rate_bps': 0,
            'external_price': 0.66,
            'current_probability': 0.58,
            'divergence': 0.08,
        },
        'slippage': {'spread_pct': 0.01},
        'warnings': ['synthetic_debug'],
    }


def _synthetic_signal(window: str, min_edge: float, min_confidence: float) -> SignalDecision:
    edge = max(min_edge + 0.03, 0.10)
    confidence = max(min_confidence + 0.05, 0.72)
    return SignalDecision(
        action='yes',
        edge=edge,
        confidence=confidence,
        signal_source='synthetic_debug',
        reasoning=f'Synthetic BTC candidate injected for dry-run tracing ({window}).',
        metrics={
            'window': window,
            'synthetic': True,
            'computed_at': datetime.now(timezone.utc).isoformat(),
        },
    )


def _candidate_priority(candidate: dict) -> tuple:
    regime = candidate.get('regime') or {}
    risk_state = candidate.get('risk_state') or {}
    signal = candidate.get('signal')
    return (
        1 if regime.get('approved') else 0,
        1 if risk_state.get('allowed') else 0,
        float(getattr(signal, 'edge', 0.0) or 0.0),
        float(getattr(signal, 'confidence', 0.0) or 0.0),
        -float(regime.get('minutes_to_resolution') or 0.0),
    )


def run_cycle(config: dict, *, dry_run: bool, validate_real_path: bool) -> dict:
    client = get_client(config, dry_run=dry_run)

    # Redeem any winning positions before the next trade cycle.
    # Called unconditionally in live mode — works for both managed and external
    # wallets. The briefing's redeem_action field prompts this whenever positions
    # are ready.
    if not dry_run:
        try:
            client.auto_redeem()
        except Exception as exc:
            trace('auto_redeem_error', exc)

    settings = client.get_settings()
    positions = client.get_positions(venue='polymarket')
    journal_rows = read_journal(JOURNAL_PATH)
    live_params = read_json_file(LIVE_PARAMS_PATH, {})
    pending_rules = read_json_file(PENDING_RULES_PATH, {'rules': []})

    try:
        llm_provider = build_provider_from_env()
        llm_blocker = None
    except MissingLLMCredentialsError:
        llm_provider = None
        llm_blocker = LLM_BLOCKER

    fast_markets = client.get_fast_markets(asset='BTC', limit=20)
    trace('markets_fetched=', len(fast_markets))
    btc_markets = []
    for market in fast_markets:
        if _is_btc_market(market):
            btc_markets.append(market)
        else:
            trace('btc_filter_drop', _market_debug_label(market), 'reason=non_btc_market')
    trace('btc_filter_result=', {'kept': len(btc_markets), 'dropped': len(fast_markets) - len(btc_markets)})
    decisions: list[dict] = []
    llm_records: list[dict] = []
    latest_risk_state = {}
    llm_status_counts = {'validated': 0, 'blocked': 0, 'rejected': 0}

    pre_learning_snapshot = build_learning_snapshot(
        journal_rows,
        config,
        live_params=live_params,
        pending_rules=pending_rules,
    )

    llm_candidates_sent = 0

    def process_candidate(market, *, window: str, context: dict, signal, source: str) -> None:
        nonlocal latest_risk_state
        regime = evaluate_regime(context, signal, config)
        trace(
            'risk_engine',
            _market_debug_label(market),
            {
                'approved': regime['approved'],
                'reasons': regime['reasons'],
                'spread_pct': regime.get('spread_pct'),
                'fee_rate': regime.get('fee_rate'),
            },
        )
        risk_state = enforce_risk_limits(
            settings,
            positions,
            config,
            config['skill_slug'],
            journal_rows,
            execution_mode='dry_run' if dry_run else 'live',
            regime=regime,
        )
        latest_risk_state = risk_state
        trace('risk_limits', _market_debug_label(market), risk_state)

        signal_payload = build_signal_payload(signal)
        market_context = build_market_context(market, window, context)
        trace('llm_candidate', _market_debug_label(market), {'source': source, 'window': window, 'signal': signal_payload})
        nonlocal llm_candidates_sent
        llm_candidates_sent += 1

        validated_decision = None
        raw_model_output = None
        llm_reject_reason = None
        try:
            validated_decision, raw_model_output, llm_reject_reason = run_llm_decision(
                provider=llm_provider,
                market_context=market_context,
                signal_data=signal_payload,
                regime=regime,
                risk_state=risk_state,
                live_params=live_params,
                pending_rules=pending_rules,
                learning_snapshot=pre_learning_snapshot,
            )
        except Exception as exc:
            llm_reject_reason = str(exc)

        trace('llm_raw_output', _market_debug_label(market), raw_model_output)
        trace(
            'llm_validation',
            _market_debug_label(market),
            {
                'accepted': validated_decision is not None,
                'decision': validated_decision,
                'reject_reason': llm_reject_reason,
            },
        )

        if llm_reject_reason == LLM_BLOCKER:
            llm_status = 'blocked'
        elif llm_reject_reason:
            llm_status = 'rejected'
        else:
            llm_status = 'validated'
        llm_status_counts[llm_status] = llm_status_counts.get(llm_status, 0) + 1

        if validated_decision and validated_decision.get('rule_suggestion'):
            record_pending_rule(
                path=PENDING_RULES_PATH,
                suggestion=validated_decision['rule_suggestion'],
                outcome=None,
            )

        gate_reject_reason = None
        should_execute = bool(
            validated_decision
            and validated_decision.get('action') in {'yes', 'no'}
            and regime['approved']
            and risk_state['allowed']
            and not llm_reject_reason
        )

        if not should_execute:
            gate_reject_reason = _combine_reject_reasons(
                llm_reject_reason,
                '; '.join(regime['reasons']) if regime.get('reasons') else None,
                '; '.join(risk_state['reasons']) if risk_state.get('reasons') else None,
                'llm_skip' if validated_decision and validated_decision.get('action') == 'skip' else None,
            )
            trace('skip_reason', _market_debug_label(market), gate_reject_reason)

        row = {
            'ts': datetime.now(timezone.utc).isoformat(),
            'market_id': market.id,
            'question': getattr(market, 'question', ''),
            'window': window,
            'asset': 'BTC',
            'venue': 'polymarket',
            'decision': 'skipped',
            'signal_action': signal.action,
            'signal_data': signal.to_signal_data(),
            'regime': regime,
            'risk_state': risk_state,
            'llm_status': llm_status,
            'llm_provider': getattr(llm_provider, 'provider_name', None),
            'llm_model': getattr(llm_provider, 'model_name', None),
            'validated_llm_decision': validated_decision,
            'llm_reject_reason': llm_reject_reason,
            'reject_reason': gate_reject_reason,
            'result_type': 'skip',
        }

        outcome = None
        if should_execute:
            execution = execute_trade(
                client,
                market_id=market.id,
                side=validated_decision['action'],
                amount=risk_state['trade_amount_usd'],
                signal=signal,
                regime=regime,
                live=not dry_run,
                source='btc_sprint_stack.llm',
                skill_slug=config['skill_slug'],
                venue='polymarket',
                validate_real_path=validate_real_path,
                llm_decision=validated_decision,
            )
            row['decision'] = 'candidate'
            row.update(execution)
            outcome = execution.get('outcome')
            row['reject_reason'] = None
            row['execution_status'] = 'accepted'
        else:
            if llm_status == 'blocked':
                row['execution_status'] = 'blocked'
            elif validated_decision and validated_decision.get('action') == 'skip':
                row['execution_status'] = 'skipped'
            else:
                row['execution_status'] = 'rejected'

        append_journal(JOURNAL_PATH, row)
        decisions.append(row)

        llm_record = build_decision_record(
            market_id=market.id,
            window=window,
            signal_data=signal.to_signal_data(),
            regime=regime,
            risk_state=risk_state,
            provider=llm_provider,
            raw_model_output=raw_model_output,
            raw_model_payload=None,
            validated_decision=validated_decision,
            reject_reason=gate_reject_reason,
            execution_status=row.get('execution_status', 'accepted' if should_execute else 'blocked'),
            outcome=outcome,
        )
        llm_records.append(llm_record)

    candidate_queue: list[dict] = []

    for market in btc_markets:
        tags = getattr(market, 'tags', []) or []
        window = market_window_from_tags(tags)
        if window == 'unknown':
            trace('window_fallback', _market_debug_label(market), 'unknown->5m')
            window = '5m'
        if window not in config['windows']:
            trace('skip', _market_debug_label(market), f'reason=window_filter:{window}')
            continue

        context = client.get_market_context(market.id)
        signal = build_signal(
            window=window,
            context=context,
            symbol=config['binance_symbol'],
            interval=config['binance_interval'],
            min_edge=config['min_edge'],
        )
        regime = evaluate_regime(context, signal, config)
        risk_state = enforce_risk_limits(
            settings,
            positions,
            config,
            config['skill_slug'],
            journal_rows,
            execution_mode='dry_run' if dry_run else 'live',
            regime=regime,
        )
        candidate_queue.append(
            {
                'market': market,
                'window': window,
                'context': context,
                'signal': signal,
                'regime': regime,
                'risk_state': risk_state,
                'source': 'live',
            }
        )

    if not candidate_queue:
        synthetic_market = _synthetic_btc_market()
        synthetic_window = '5m'
        synthetic_context = _synthetic_market_context()
        synthetic_signal = _synthetic_signal(synthetic_window, config['min_edge'], config['min_confidence'])
        trace('synthetic_fallback', _market_debug_label(synthetic_market), {'reason': 'no real decisions'})
        synthetic_regime = evaluate_regime(synthetic_context, synthetic_signal, config)
        synthetic_risk_state = enforce_risk_limits(
            settings,
            positions,
            config,
            config['skill_slug'],
            journal_rows,
            execution_mode='dry_run' if dry_run else 'live',
            regime=synthetic_regime,
        )
        candidate_queue.append(
            {
                'market': synthetic_market,
                'window': synthetic_window,
                'context': synthetic_context,
                'signal': synthetic_signal,
                'regime': synthetic_regime,
                'risk_state': synthetic_risk_state,
                'source': 'synthetic_debug',
            }
        )

    selected_candidate = max(candidate_queue, key=_candidate_priority)
    trace('selected_candidate', _market_debug_label(selected_candidate['market']), {
        'source': selected_candidate['source'],
        'window': selected_candidate['window'],
        'edge': getattr(selected_candidate['signal'], 'edge', None),
        'confidence': getattr(selected_candidate['signal'], 'confidence', None),
    })
    process_candidate(
        selected_candidate['market'],
        window=selected_candidate['window'],
        context=selected_candidate['context'],
        signal=selected_candidate['signal'],
        source=selected_candidate['source'],
    )

    trace('llm_sent_count=', llm_candidates_sent)

    for record in llm_records:
        # Keep a separate audit trail for the model outputs.
        append_jsonl(LLM_DECISIONS_PATH, record)

    learning_snapshot = build_learning_snapshot(
        journal_rows + decisions,
        config,
        live_params=live_params,
        pending_rules=pending_rules,
    )
    live_params, pending_rules = apply_eligible_rules(
        live_params_path=LIVE_PARAMS_PATH,
        pending_rules_path=PENDING_RULES_PATH,
        learning_snapshot=learning_snapshot,
        defaults=json.loads(DEFAULTS_PATH.read_text()),
    )
    learning_snapshot = build_learning_snapshot(
        journal_rows + decisions,
        config,
        live_params=live_params,
        pending_rules=pending_rules,
    )
    write_json_file(LEARNING_PATH, learning_snapshot)

    heartbeat = build_heartbeat(client, decisions, latest_risk_state, learning_snapshot)
    heartbeat['llm'] = {
        'provider': getattr(llm_provider, 'provider_name', None),
        'model': getattr(llm_provider, 'model_name', None),
        'blocker': llm_blocker,
        'status_counts': llm_status_counts,
        'pending_rules': len(pending_rules.get('rules') or []) if isinstance(pending_rules, dict) else 0,
    }

    try:
        briefing = heartbeat.get('briefing') or {}
        opp = briefing.get('opportunities') or {}
        new_markets = opp.get('new_markets') or []
        opp['new_markets'] = [
            m for m in new_markets
            if (m.get('market_source') == config['trading_venue']) and ('bitcoin' in (m.get('question') or '').lower())
        ]
        rec = opp.get('recommended_skills') or []
        opp['recommended_skills'] = [r for r in rec if r.get('id') in {'simmer', 'polymarket-fast-loop', config['skill_slug']}]
        briefing['opportunities'] = opp
        heartbeat['briefing'] = briefing
    except Exception:
        pass

    output = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'validate_real_path': validate_real_path,
        'execution_profile': config.get('execution_profile', 'balanced'),
        'llm_provider': getattr(llm_provider, 'provider_name', None),
        'llm_model': getattr(llm_provider, 'model_name', None),
        'llm_blocker': llm_blocker,
        'decisions': decisions,
        'live_params': live_params,
        'pending_rules': pending_rules,
        'learning_snapshot': learning_snapshot,
        'heartbeat': heartbeat,
    }
    print(json.dumps(output, indent=2, default=str))
    return output


def main() -> None:
    args = parse_args()

    if args.discord_test_alert:
        try:
            result = send_discord_alert('BTC sprint bot Discord test alert')
        except DiscordAlertError as exc:
            raise SystemExit(str(exc))
        print(json.dumps({'discord_test_alert': result}, indent=2, default=str))
        return

    config = load_config()
    dry_run = True
    if args.live:
        dry_run = False
    elif args.dry_run:
        dry_run = True
    elif 'dry_run' in config:
        dry_run = bool(config['dry_run'])

    # One-time external wallet setup (link + approvals) when a private key is present.
    # Skipped in dry-run mode — no on-chain calls needed for simulation.
    if not dry_run and os.environ.get('WALLET_PRIVATE_KEY'):
        _client = get_client(config, dry_run=dry_run)
        setup_external_wallet(_client)

    validate_real_path = args.validate_real_path or bool(config.get('validate_real_path'))
    if args.loop:
        while True:
            run_cycle(config, dry_run=dry_run, validate_real_path=validate_real_path)
            time.sleep(config['cycle_interval_minutes'] * 60)
    else:
        run_cycle(config, dry_run=dry_run, validate_real_path=validate_real_path)


if __name__ == '__main__':
    main()
