## Description:

Quantifies whether a stock or ETF is suitable for long-term holding or requires tiered profit-taking by comparing exit strategies over roughly 10 years of daily history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate whether a ticker can be held long-term or should use a tiered take-profit strategy. It returns headline risk metrics, strategy comparisons, and suggested exit posture for stocks and ETFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can respond to broad stock sell or hold questions with concrete exit suggestions.

Mitigation: Require user confirmation and independent review before using outputs for trades, and present recommendations as scenario analysis rather than personalized financial advice.

Risk: Generated order levels may omit user-specific constraints such as taxes, liquidity, position size, and suitability.

Mitigation: Prompt users to evaluate those constraints separately and avoid placing generated orders without human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-take-profit)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with structured metrics and optional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include profile color, special flags, rollercoaster rate, max drawdown, hold CAGR, strategy comparisons, sample size, period, and computed timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
