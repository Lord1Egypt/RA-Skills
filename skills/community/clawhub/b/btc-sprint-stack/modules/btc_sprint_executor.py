from __future__ import annotations


def build_reasoning(signal, regime, trade_amount: float, llm_reasoning: str | None = None) -> str:
    regime_bits = ', '.join(regime['warnings']) if regime['warnings'] else 'no warnings'
    base_reasoning = llm_reasoning or signal.reasoning
    return (
        f"{base_reasoning} Edge={signal.edge:.4f}, confidence={signal.confidence:.4f}, "
        f"trade_amount=${trade_amount:.2f}, regime={regime_bits}."
    )


def execute_trade(client, market_id: str, side: str, amount: float, signal, regime: dict, *, live: bool, source: str, skill_slug: str, venue: str, validate_real_path: bool, llm_decision: dict | None = None) -> dict:
    llm_reasoning = None
    if isinstance(llm_decision, dict):
        llm_reasoning = llm_decision.get('reasoning')
    reasoning = build_reasoning(signal, regime, amount, llm_reasoning=llm_reasoning)
    signal_data = signal.to_signal_data()
    result = {
        'live': live,
        'venue': venue,
        'market_id': market_id,
        'side': side,
        'amount': amount,
        'reasoning': reasoning,
        'source': source,
        'skill_slug': skill_slug,
        'decision_source': 'llm',
        'signal_data': signal_data,
    }

    if live:
        trade = client.trade(
            market_id=market_id,
            side=side,
            amount=amount,
            venue=venue,
            reasoning=reasoning,
            source=source,
            skill_slug=skill_slug,
            signal_data=signal_data,
        )
        result['result_type'] = 'trade'
        result['trade'] = getattr(trade, '__dict__', trade)
        return result

    result['result_type'] = 'dry_run'
    if validate_real_path and venue == 'polymarket':
        preflight = client.prepare_real_trade(market_id, side, amount)
        result['preflight'] = getattr(preflight, '__dict__', preflight)
    return result
