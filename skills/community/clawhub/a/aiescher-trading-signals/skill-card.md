## Description:

Generates trading signals for stocks, indices, crypto, commodities, and forex using TradingView market data and technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiescherbot-collab](https://clawhub.ai/user/aiescherbot-collab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run technical indicator analysis across configured market assets, generate buy/sell signals, and optionally monitor for new stronger signals with email alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send trading reports to a default external Gmail recipient when Resend credentials are available.

Mitigation: Before running alerting scripts, disable alerts or change references/assets.json to an intended recipient under the user's control.

Risk: Market symbols, prices, indicators, and generated signals may leave the user's machine if email alerts send successfully.

Mitigation: Review alert configuration and recipient settings before installing or running scripts with existing Resend credentials.

## Reference(s):

- [Asset configuration](references/assets.json)
- [ClawHub skill page](https://clawhub.ai/aiescherbot-collab/skills/aiescher-trading-signals)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, console trading-signal summaries, configuration JSON, and optional HTML email reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include configured asset symbols, market prices, indicators, generated buy/sell signals, and alert status.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
