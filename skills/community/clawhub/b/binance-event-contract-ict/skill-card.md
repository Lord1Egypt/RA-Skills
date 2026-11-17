## Description:

Automatically identifies ICT structures such as Order Blocks, Fair Value Gaps, liquidity sweeps, and inducement patterns on Binance BTC/ETH K-line data for SSS-tier event contract signal review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acwxpunh](https://clawhub.ai/user/acwxpunh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to produce structured ICT market-structure analysis for Binance BTC/ETH event contract workflows after configured K-line closes. The skill is intended for analysis review and risk-manager handoff, not direct automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes contradictory trading posture: it forbids direct trading signals while an example output includes entry, target, and stop-loss language.

Mitigation: Treat generated reports as market-structure analysis only and require human review before any trading decision or downstream execution.

Risk: The installation command uses a mutable @latest package reference.

Mitigation: Prefer a pinned, verified ClawHub installer version before installation.

Risk: Using the skill in an environment with exchange credentials or order-execution integrations could increase financial automation risk.

Mitigation: Run it without exchange credentials or automatic order execution unless those integrations have been separately reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acwxpunh/skills/binance-event-contract-ict)
- [Publisher profile](https://clawhub.ai/user/acwxpunh)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected ICT structures, score bands, confidence labels, and data-unavailable messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
