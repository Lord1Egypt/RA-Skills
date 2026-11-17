## Description:

Cross-venue trading skill for ClawHub that supports both manual candidate selection and unattended auto mode, while filtering markets by price band and trading volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users use this skill to discover prediction-market candidates across Simmer, Kalshi, or Polymarket, review ranked opportunities, and optionally execute configured trades. It is intended for users who can configure credentials, venue settings, price bands, edge thresholds, and live-trading controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place recurring unattended live trades when live mode and auto mode are deliberately enabled.

Mitigation: Keep dry-run or manual mode enabled unless live automation is intended, avoid AUTO_CONFIRM_LIVE for real-money venues, and add independent order limits before recurring execution.

Risk: Trading credentials and wallet keys may authorize real-money activity on connected venues.

Mitigation: Use isolated credentials with least privilege, keep secrets out of shared logs and files, and rotate keys if exposure is suspected.

Risk: The default strategy uses simple volume ranking and a configurable fair probability rather than a complete fair-value model.

Mitigation: Review candidates manually, tune edge and slippage thresholds, and replace the default signal with venue-specific liquidity and valuation checks before trusting live use.

## Reference(s):

- [Auto Trading Winner on ClawHub](https://clawhub.ai/skybinjf/skills/auto-trading-winner)
- [Publisher profile](https://clawhub.ai/user/skybinjf)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with configuration-driven execution and optional trade actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs ranked market candidates, selected trade details, dry-run reasoning, skip reasons, and execution status when live trading is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
