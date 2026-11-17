## Description:

Per-ticker panic index (0-100) that combines VIX, IV Rank, RSI-14, volume anomaly, put/call ratio, and consecutive down days to produce a FearScore and Bull Put Spread timing signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate ticker-level market panic and identify when a Bull Put Spread entry signal is triggered. The output is intended as options research context, not as a standalone trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Options-trading signals may be treated as financial advice or used as the sole basis for trades.

Mitigation: Treat outputs as general research signals, verify market data and assumptions independently, and do not rely on the skill alone for investment decisions.

Risk: Missing or partial market inputs can reduce confidence in the composite score.

Mitigation: Review the confidence value and component fallback flags before acting on a signal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-fear-score)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Markdown guidance with JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ticker-level score components, confidence, signal status, threshold, and fallback flags for missing indicator data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
