---
name: al-brooks-price-action
description: |
  Analyze charts, OHLC bars, candlestick sequences, and trading context using Al Brooks style price action.
  Use this skill when the user asks for Brooks 风格价格行为分析、Always In 偏置、趋势 vs 震荡判断、
  setup 识别（High 1/2/3/4、Low 1/2/3/4、breakout pullback、tight channel breakout pullback、
  final flag、wedge top/bottom、double top/bottom pullback、ioi）、signal bar 质量、
  scalp vs swing、entry/stop/target 规划，或明确的 no-trade 判定。
---

# Al Brooks Price Action

Use this skill for discretionary price action analysis. Prioritize context, current tradeability, and the hard right edge of the chart. Do not drift into macro or indicator-heavy analysis unless the user explicitly asks for it.

## Load References Selectively

- Read [references/core_concepts.md](references/core_concepts.md) when you need Brooks-style terminology, mental models, or a fast glossary.
- Read [references/market_context_checklist.md](references/market_context_checklist.md) when the task is mainly about market phase, Always In, magnets, breakout mode, or whether the chart is tradable at all.
- Read [references/setup_taxonomy.md](references/setup_taxonomy.md) when identifying or validating a concrete setup near the latest bars.
- Read [references/entries_and_exits.md](references/entries_and_exits.md) when the user wants entry, stop, target, scalp vs swing, or trade management detail.

## Accepted Inputs

- OHLC text or tables
- chart screenshots
- notes from another analyst or agent
- multi-timeframe summaries

If the input is incomplete, state what is missing and continue with the visible evidence instead of blocking.

## Operating Rules

1. Start with context, not the signal bar. Higher timeframe and recent structure outrank a single candle.
2. Focus on the live area. The active trade trigger should come from the latest 1-3 bars, not from an old pattern that already played out.
3. Default to `trading_range` or `no trade` when evidence is mixed.
4. Separate `actionable`, `watch`, and `none`. Do not force a trade.
5. Use Brooks-style terms, but explain the bottom line in plain language.
6. Counter-trend setups are lower quality unless the reversal evidence is unusually strong and location is excellent.
7. Do not hallucinate hidden bars or unreadable prices from screenshots. If a value is unclear, say so.

## Analysis Workflow

1. Identify instrument, timeframe, and whether the user cares about scalp, swing, or both.
2. Classify context:
   - `market_phase`: `trending`, `trading_range`, `broad_channel`, or `unknown`
   - `always_in`: `long`, `short`, or `unknown`
   - nearby magnets: prior high/low, breakout point, EMA, measured move target, range edge, gap close, session extreme
3. Decide the dominant story:
   - trend continuation
   - breakout test / breakout pullback
   - reversal attempt
   - breakout mode / two-sided range
4. Evaluate only the setup nearest the hard right edge:
   - setup name
   - direction
   - signal bar quality
   - context fit
   - whether confirmation is still needed
5. Produce one of three outcomes:
   - `actionable`
   - `watch`
   - `none`
6. If the setup is tradable, explain trigger, invalidation, first target, and whether it is better framed as scalp or swing.
7. If it is not tradable, say what would need to change to make it tradable.

## Preferred Output

Use this shape unless the user asks for a different format.

### Market Context

- `market_phase`
- `always_in`
- dominant side
- magnets / important levels

### Active Setup

- setup name
- `long`, `short`, or `none`
- why it qualifies
- why it might fail

### Tradeability

- `actionable`, `watch`, or `none`
- entry trigger
- stop logic
- target logic
- `scalp`, `swing`, or `none`
- invalidation

### Bottom Line

One short paragraph in plain language.

## Optional Machine-Readable Block

When the user wants structured output, append a JSON block using this schema:

```json
{
  "market_phase": "trending|trading_range|broad_channel|unknown",
  "always_in": "long|short|unknown",
  "setup_status": "actionable|watch|none",
  "setup_type": "string",
  "direction": "long|short|none",
  "signal_bar_quality": "high|medium|low|none",
  "entry_trigger": "string",
  "stop_logic": "string",
  "target_1": "string",
  "target_2": "string",
  "trade_style": "scalp|swing|none",
  "invalidation": "string",
  "confidence": 0.0
}
```

## Special Cases

- For screenshots: describe only what is visible, then infer cautiously.
- For multi-timeframe requests: analyze higher timeframe first, lower timeframe second.
- For post-trade reviews: separate "what the chart offered then" from "what is tradable now".
- For automation prompts: keep labels stable and concise so downstream parsers can consume them.
