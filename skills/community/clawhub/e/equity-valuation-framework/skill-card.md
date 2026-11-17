## Description:

Provides a decision-grade equity valuation playbook and report standard for multiples, DCF, quality assessment, scenarios, and margin-of-safety analysis when users request valuation, stock comparison, investment thesis explanation, or structured risk review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to turn structured equity, market, peer, macro, and news inputs into a professional valuation memo with multiples, DCF scenarios, sensitivity tables, risk register, fair-value range, and margin-of-safety framing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake valuation output for personalized investment advice or an order to trade.

Mitigation: Keep outputs educational, avoid absolute buy or sell commands, include the skill's disclaimer, and frame conclusions as conditional valuation views.

Risk: Stale, incomplete, or inconsistent financial and market inputs can produce misleading fair-value ranges.

Mitigation: Require freshness, completeness, and consistency checks before valuation; disclose missing inputs and downgrade confidence when data quality is weak.

Risk: DCF and multiples assumptions can create false precision when cash-flow visibility or peer comparability is limited.

Mitigation: Use scenario ranges, sensitivity tables, explicit assumptions, and directional conclusions when robust triangulation is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/equity-valuation-framework)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown valuation report with tables, scenarios, risk register, fair-value range, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current structured financial, price, peer, macro, and news inputs; does not fetch data directly.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
