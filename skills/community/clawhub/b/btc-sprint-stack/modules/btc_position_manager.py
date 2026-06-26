from __future__ import annotations

from datetime import datetime, timezone


def _safe_get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def active_positions_for_skill(positions, skill_slug: str) -> list:
    scoped = []
    for position in positions:
        source = _safe_get(position, 'source')
        if source and source != skill_slug:
            continue
        if (_safe_get(position, 'shares', 0.0) or 0.0) <= 0:
            continue
        scoped.append(position)
    return scoped


def enforce_risk_limits(
    settings: dict,
    positions,
    config: dict,
    skill_slug: str,
    journal_rows: list[dict],
    *,
    execution_mode: str = 'dry_run',
    regime: dict | None = None,
) -> dict:
    reasons = []
    settings = settings or {}
    scoped_positions = active_positions_for_skill(positions, skill_slug)
    if execution_mode not in {'dry_run', 'live'}:
        reasons.append(f'unknown_execution_mode:{execution_mode}')

    if len(scoped_positions) >= config['max_open_positions']:
        reasons.append('max_open_positions_reached')

    if settings.get('trading_paused'):
        reasons.append('trading_paused')

    daily_spent = float(settings.get('sdk_daily_spent') or 0.0)
    if daily_spent >= config['max_daily_loss_usd']:
        reasons.append('max_daily_loss_reached')

    today = datetime.now(timezone.utc).date().isoformat()
    today_trades = [row for row in journal_rows if row.get('ts', '').startswith(today) and row.get('result_type') == 'trade']
    if len(today_trades) >= config['max_trades_per_day']:
        reasons.append('max_trades_per_day_reached')

    recent_losses = [row for row in today_trades if row.get('pnl_usd', 0) < 0]
    if recent_losses:
        latest_loss = recent_losses[-1].get('ts')
        if latest_loss:
            loss_time = datetime.fromisoformat(latest_loss.replace('Z', '+00:00'))
            cooldown = (datetime.now(timezone.utc) - loss_time).total_seconds() / 60
            if cooldown < config['cooldown_after_loss_minutes']:
                reasons.append(f'cooldown_active:{cooldown:.1f}m')

    if regime is not None:
        spread_pct = regime.get('spread_pct')
        if spread_pct is not None and spread_pct > config['max_slippage_pct']:
            reasons.append(f'max_slippage_pct_exceeded:{spread_pct:.4f}')

    amount = min(
        config['max_trade_usd'],
        config['max_single_market_exposure_usd'],
        config['bankroll_usd'],
    )
    amount = round(max(amount, 0.0), 2)
    if amount <= 0:
        reasons.append('non_positive_trade_amount')

    return {
        'allowed': not reasons,
        'reasons': reasons,
        'trade_amount_usd': amount,
        'open_positions': len(scoped_positions),
        'daily_spent': daily_spent,
        'execution_mode': execution_mode,
    }
