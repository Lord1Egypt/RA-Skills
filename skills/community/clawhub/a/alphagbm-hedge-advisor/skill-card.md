## Description:

Scenario-driven hedge recommendations for an existing stock position, using ticker, cost basis, and purpose to classify the position and return Long Put, Collar, Tier-down, or position-rule guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate hedge approaches for an existing single-stock position. It returns scenario labels, hedge rationale, priced option structures, and position-sizing rules based on ticker, cost basis, and purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete options hedge ideas using live market data, which may be mistaken for personalized financial advice or an instruction to trade.

Mitigation: Confirm the ticker, cost basis, position purpose, quote timestamps, and data freshness before relying on outputs, and treat recommendations as decision-support guidance rather than trading instructions.

Risk: Hedge costs, strikes, premiums, and scenario classifications can change with market conditions and option-chain freshness.

Mitigation: Re-run analysis close to decision time and review the resolved option fields before using any hedge specification.

## Reference(s):

- [Alphagbm Hedge Advisor on ClawHub](https://clawhub.ai/clementgu/skills/alphagbm-hedge-advisor)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, configuration, guidance]

**Output Format:** [Markdown and structured JSON examples with hedge recommendations, resolved option pricing fields, and position rules.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual Chinese and English scenario labels, rationale, quote-dependent option fields, and cached API response details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
