## Description:

Score and rank options contracts by ticker using AlphaGBM's multi-factor model for liquidity, implied volatility attractiveness, Greeks balance, and risk/reward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to evaluate, compare, and explain option contracts for a ticker by score, strategy type, expiry, strike, liquidity, volatility, and risk-return factors. It supports research workflows for choosing candidate contracts, not automated trading authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols, option identifiers, expiry dates, and related query details may be sent to AlphaGBM or to a configured custom base URL.

Mitigation: Use only data appropriate for the configured service endpoint, review the endpoint before use, and avoid sending sensitive or restricted trading information.

Risk: Options scores and recommendations can be mistaken for financial advice or authorization to trade.

Mitigation: Present scores as research support, include score breakdowns and risk-return context, and require independent review before any trading decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-options-score)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown tables and concise text summaries with optional JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked contracts, score breakdowns, ATR safety notes, risk-return labels, and API-key or quota considerations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
