## Description:

条件单投资助手 helps Chinese-language users identify ETF or stock types and draft conditional-order strategy parameters for China-market investing scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze China-market ETF or stock codes, compare conditional-order strategies, and produce suggested parameters for grid, fixed-price, rebound-buy, pullback-sell, stop-loss, or recurring-investment setups. The output is informational and should be reviewed before any investing action.

### Deployment Geography for Use:

Global; content is focused on Chinese-language, China-market ETF and stock scenarios.

## Known Risks and Mitigations:

Risk: Users may treat generated buy/sell parameters as personalized financial advice.

Mitigation: Present the output as reference material only and require independent review before any investing action.

Risk: Live price or cross-border ETF premium data may be unavailable or stale.

Mitigation: Verify prices and premium data independently before using generated parameters.

Risk: Users may assume the skill executes orders or manages positions.

Mitigation: Keep usage limited to analysis and guidance; use a separate reviewed trading workflow for any order placement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/conditional-order-tool)
- [Strategy matrix](artifact/references/strategy-matrix.md)
- [ETF database](artifact/references/etf-database.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown analysis reports and optional JSON report objects with suggested conditional-order parameters.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes disclaimers and prompts to verify live prices and premium data; does not place orders.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
