## Description:

Set price, IV, or activity-based alerts with contextual notifications for IV rank thresholds, price breaks, unusual activity, earnings, and VRP signal changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure, review, edit, and delete market alerts for tickers based on price levels, IV rank, unusual options activity, earnings timing, and VRP signal changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help create, modify, and delete persistent market alerts.

Mitigation: Use explicit ticker and alert identifiers, and confirm edit or delete actions before allowing them to proceed.

Risk: Triggered alerts may influence time-sensitive financial decisions.

Mitigation: Treat notifications as contextual information and verify current market data before acting.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-alert)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with alert configuration summaries, contextual notifications, and alert management guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ticker, condition, threshold, recurrence, and alert identifier inputs when supplied.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
