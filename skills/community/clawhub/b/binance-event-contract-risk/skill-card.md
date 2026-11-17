## Description:

Continuously manages Binance BTCUSDT and ETHUSDT event contract risk by checking signals against position sizing, exposure, daily loss, and circuit-breaker rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acwxpunh](https://clawhub.ai/user/acwxpunh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-workflow operators can use this skill to review Binance event-contract signals before execution, with checks for trade size, daily loss, exposure, expiry timing, and emergency stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk calculations may approve positions larger than the skill's stated limit.

Mitigation: Correct and independently test the calculations before any approval can influence real trades.

Risk: Automated use could allow risk-check output to influence real trades without sufficient human review.

Mitigation: Require explicit user confirmation for trade approvals and prefer a pinned installer version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acwxpunh/skills/binance-event-contract-risk)
- [ClawHub publisher profile](https://clawhub.ai/user/acwxpunh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style risk assessment text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pass/fail risk checks, position sizing calculations, alerts, and circuit-breaker guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
