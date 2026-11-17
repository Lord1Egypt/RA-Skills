## Description:

Design, execute, and evaluate quantitative trading strategies using historical price data and Fama-French factor attribution via the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and quantitatively oriented traders use this skill to turn strategy hypotheses into historical backtests with performance metrics, drawdown analysis, factor attribution, walk-forward validation, and stress tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Finskills API queries for market data and may expose strategy details, symbols, or proprietary baskets to the provider.

Mitigation: Use it only when the user is comfortable with Finskills receiving those API queries and has reviewed the provider's privacy and retention practices.

Risk: Backtest reports can be misleading when historical results are treated as trading advice or when bias, lagged factors, slippage, or overfitting are ignored.

Mitigation: Review assumptions before acting, verify signal construction, account for execution costs and data limitations, and treat outputs as analytical support rather than a guarantee of future performance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills-backtest-expert)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Skill homepage](https://github.com/finskills/backtest-expert)
- [Finskills API](https://finskills.net)
- [Finskills registration](https://finskills.net/register)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, analysis, guidance]

**Output Format:** [Markdown report with structured strategy summary, performance metrics, factor attribution, walk-forward validation, stress tests, and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and may use Finskills market data endpoints for historical prices and Fama-French factors.]

## Skill Version(s):

1.0.2 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
