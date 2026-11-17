## Description:

P&L simulation engine for single-leg and multi-leg option positions that generates payoff diagrams, time-based P&L, price, IV, and time scenarios, breakeven analysis, and probability distributions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, developers, and agents use this skill to simulate option-position P&L, stress-test price, IV, and time scenarios, and review breakeven, probability, and risk/reward outputs before acting on trade ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio positions, trade ideas, and API keys can be sensitive when sent for options P&L analysis.

Mitigation: Ask the user to confirm before sending ambiguous or private trading details to AlphaGBM, and avoid exposing API keys in prompts or logs.

Risk: P&L diagrams, probability distributions, and risk/reward statistics depend on the position and scenario inputs supplied to the simulator.

Mitigation: Review the position legs, spot price, IV, dates, and scenario assumptions before relying on simulator output.

## Reference(s):

- [AlphaGBM P&L Simulator Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-pnl-simulator)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON simulation results with concise Markdown explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require ALPHAGBM_API_KEY; demo tickers are described as available without an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
