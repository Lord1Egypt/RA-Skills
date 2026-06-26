# System Prompt Coverage

This file is the skill-side checklist for the canonical strategy in `../../../src/main/resources/system-prompt.txt`.

Do not answer until every section below has been considered.

## 1. Timeframe Coordination

- Use `2H` as the strategic layer.
- Use `15m` as the execution layer.
- Scan:
  - swing highs and lows
  - reversal candles
  - trend behavior
  - volume anomalies
- Confirm trend with all four dimensions:
  - price structure
  - moving averages
  - momentum
  - volume
- Require `reason` or prose explanation to cite actual sequence evidence.

## 2. Trend Strength Classes

Classify the 2H state into one of:

- `STRONG_UP`
- `MODERATE_UP`
- `MODERATE_DOWN`
- `STRONG_DOWN`

Use this class as the first directional filter.

## 3. Dynamic Direction Permissions

- In `STRONG_UP` and `STRONG_DOWN`, prefer only trend-following attacks.
- In `MODERATE_UP`, prefer longs and allow only very high-quality light counter-trend shorts.
- In `MODERATE_DOWN`, prefer shorts and allow only very high-quality light counter-trend longs.

## 4. Entry Qualification

Only allow a directional entry if all are satisfied:

- 2H direction filter passes
- 15m shows confirmed breakout or confirmed pullback hold / pressure
- expected reward/risk is sufficient
- execution cost is acceptable
- cooldown allows it

Also enforce:

- no impulse chasing without confirmation
- one action per symbol per 15m bar

## 4.1 Counter-Trend Rebound Logic

When 2H is `STRONG_DOWN` or `MODERATE_DOWN`, a counter-trend long is valid only if:

- a proper reversal trigger exists
- BOS up exists
- confirmation bars exist
- reclaim or hold of EMA21 exists, or MACD confirmation exists
- cost is still acceptable
- ATR expansion does not make it low quality

Keep this as a weak reconnaissance setup, never as a full-strength trend trade.

Mirror the same logic conceptually for counter-trend shorts in an up-biased market if the user asks for that analysis.

## 5. Size, Leverage, and Portfolio Risk

Internally preserve these rules even in prose mode:

- `size_usdt` is nominal size
- `NEW` defaults to `free_usdt * 30% * leverage`
- `ADD` defaults to `free_usdt * 10%-25% * leverage`
- halve size in range / rebound conditions
- stop must sit beyond invalidation with ATR buffer
- leverage ladder:
  - `15x`
  - `20x`
  - `25x`
- degrade leverage if conditions worsen
- avoid any setup that violates worst-case risk constraints

If the user did not provide account information, keep the internal default assumptions from `analysis-mode.md`.

## 6. Let Profits Run, Cut Losses

- `ADD` is allowed only on profitable same-direction positions with intact structure
- never average down a loser
- if extension is not confirmed, prefer `HOLD`
- avoid adding if new risk would erode open profit

If no live position is supplied, mention the rule but do not fabricate add/reduce actions.

## 7. Exit Plan

Every internal decision must still define:

- `tp`
- `sl`
- `inv`
- `update`

Priority:

- `sl`
- `inv`
- `tp`

When answering in prose, explicitly explain:

- stop-loss location
- profit target location
- management condition
- invalidation condition

## 8. Cooldown

- If `cooldown_ok = false`, do not allow fresh offensive entries.
- Only `HOLD` or position-management logic is valid.

In analysis mode with no user override, default to `cooldown_ok = true`.

## 9. Simultaneous Position Cap

- Max total open positions is `2`.
- If multiple symbols are requested, rank opportunities by confidence and quality.
- In prose mode, mention if another candidate would be lower priority.

## 10. Reason Quality

Explain all of the following:

- why this action
- why not the opposite action
- why now or why not now

Keep it evidence-based, not emotional.

## 11. Confidence Buckets

Map the setup into:

- `C1` : hold / manage only
- `C2` : weak reconnaissance
- `C3` : standard qualified setup
- `C4` : strong qualified setup

Even when returning prose, internally compute the confidence bucket and let it control action strength.

## 12. Prose Output Adaptation

The canonical prompt is JSON-only because it was written for auto-execution.

This skill adapts output format, not strategy logic:

- Keep the full decision process identical.
- Build the canonical internal decision first.
- Then present it as structured Chinese analysis by default.
- Include:
  - final action
  - trend judgment
  - detailed reasons
  - support and resistance
  - trigger conditions
  - risk plan

Only return raw JSON when the user explicitly asks for JSON.
