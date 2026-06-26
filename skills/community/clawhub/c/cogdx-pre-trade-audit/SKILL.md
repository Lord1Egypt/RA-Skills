---
name: cogdx-pre-trade-audit
description: Verify trading reasoning with cognitive diagnostics before executing trades. Detects logical fallacies, calibration issues, and cognitive biases in your trade thesis.
metadata:
  author: "Cerebratech"
  version: "1.0.0"
  displayName: "CogDx Pre-Trade Audit"
  difficulty: "beginner"
---

# CogDx Pre-Trade Audit

Cognitive verification layer for prediction market trades. Catches reasoning flaws before they become losses.

> **This is a template.** The default signal is your agent's trade thesis —
> the skill audits the reasoning quality before execution.
> Remix it with stricter thresholds, additional bias checks, or custom fallacy detection.
> The skill handles all the plumbing (API calls, trade execution, safeguards).
> Your agent provides the reasoning to verify.

## What it does

1. Takes your trade reasoning (thesis, confidence, market context)
2. Runs cognitive diagnostics via CogDx API
3. Returns verdict: PROCEED / REVIEW / REJECT
4. Optionally executes trade if reasoning passes

## Detects

- **Logical fallacies**: anchoring, confirmation bias, sunk cost
- **Calibration issues**: overconfidence, underconfidence
- **Reasoning gaps**: missing evidence, circular logic

## Usage

```python
from cogdx_pre_trade_audit import audit_and_trade

result = audit_and_trade(
    market_id="0x1234...",
    side="yes",
    amount=10.0,
    reasoning="BTC ETF approval likely based on SEC meeting notes...",
    confidence=0.85,
    min_validity=0.7,  # Minimum reasoning quality to proceed
    live=False  # Dry-run by default
)

if result["approved"]:
    print(f"Trade executed: {result['trade_id']}")
else:
    print(f"Trade blocked: {result['issues']}")
```

## Environment Variables

- `SIMMER_API_KEY` - Required. Your Simmer API key.
- `COGDX_WALLET` - Optional. Wallet address for CogDx credits.

## Thresholds

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_validity` | 0.7 | Minimum reasoning quality score (0-1) |
| `block_on_error` | True | Block trade if CogDx API unavailable |

## Why use this

Most trading losses come from bad reasoning, not bad data. This skill catches:
- Trades based on anchoring (first number you saw)
- Confirmation bias (only seeing supporting evidence)
- Overconfidence (betting big on weak signals)

External verification you can't do yourself.

## Credits

Built by [Cerebratech](https://api.cerebratech.ai) — cognitive diagnostics for agents.
