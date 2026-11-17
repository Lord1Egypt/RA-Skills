## Description:

Greeks dashboard for any option contract or multi-leg position, covering first-order Greeks, second-order Greeks, individual and position-level Greeks, and scenario heatmaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading-focused agents use this skill to calculate option Greeks, inspect multi-leg position risk, and review scenario heatmaps for changes in underlying price and implied volatility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real option contract or portfolio-position details may be sent to AlphaGBM when the live API is used.

Mitigation: Use mock or non-sensitive data where appropriate, keep the API key in environment variables, and avoid sharing confidential positions.

Risk: Options-Greeks outputs can be incomplete or misleading if used as financial advice or as the sole basis for a trading decision.

Mitigation: Treat outputs as analytical support, review assumptions such as price, expiry, and implied volatility, and apply independent trading and risk controls.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API base URL](https://alphagbm.zeabur.app)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-greeks)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Markdown, Guidance]

**Output Format:** [Markdown with JSON examples and option-risk analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an AlphaGBM API key and can also rely on mock ticker data for AAPL, NVDA, SPY, TSLA, and META.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
