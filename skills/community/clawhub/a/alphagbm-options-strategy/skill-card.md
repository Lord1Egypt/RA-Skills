## Description:

Recommends multi-leg options strategies for a ticker and market view, ranking templates such as spreads, condors, straddles, and income plays with P&L, breakeven, Greeks, and probability-of-profit details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to choose, compare, and explain options strategies for a ticker, market view, event, or income objective. It supports trade planning and decision support, not trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Options-strategy recommendations can be incorrect, incomplete, or unsuitable for a user's financial situation.

Mitigation: Review this as financial decision support only, verify outputs independently, and do not risk capital based solely on the skill response.

Risk: Use with an AlphaGBM API key may send ticker symbols, strategy preferences, and related options-analysis inputs to AlphaGBM.

Mitigation: Confirm the API endpoint and data-sharing expectations before use, and avoid submitting sensitive trading information unless approved.

Risk: Some supported options strategies may involve substantial or uncapped loss exposure.

Mitigation: Check maximum loss, assignment risk, Greeks, and breakevens before considering any strategy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-options-strategy)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON examples and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require ALPHAGBM_API_KEY; demo tickers AAPL, NVDA, SPY, TSLA, and META are available without an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
