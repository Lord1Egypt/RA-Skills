## Description:

Use when a Polymarket market probability changes as the resolution deadline approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate Polymarket markets where time remaining before resolution is central to the trading thesis. It guides agents to inspect market deadlines, filled TradeTick history, deadline-related probability drift, exit timing, and settlement exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence financial or prediction-market trading decisions.

Mitigation: Review generated strategy logic, position sizing, deadline assumptions, and settlement-risk assumptions before acting on the output.

Risk: Deadline drift analysis can be misleading when market rules, event catalysts, or short backtest windows dominate the observed price movement.

Mitigation: Check market-resolution rules, separate gradual drift from catalyst jumps, avoid overfitting short windows, and exit before settlement unless binary exposure is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/deadline-drift)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with strategy configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading-strategy guidance and configuration suggestions; it does not execute trades or provide fair-probability forecasts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
