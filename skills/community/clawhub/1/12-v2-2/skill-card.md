## Description:

An AI quantitative trading skill for stock analysis, backtesting, real-time quote analysis, eight-factor signal scoring, multi-source data fallback, and optional notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to analyze A-share stocks, screen trading signals, backtest strategies, evaluate market conditions, and configure optional notifications. Trading outputs should be treated as informational analysis rather than automated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and usage instructions may be risky or inconsistent.

Mitigation: Review shell commands and documentation before installation, and use a virtual environment with pinned dependencies.

Risk: Documentation references /tmp scripts that may not correspond to the reviewed artifact.

Mitigation: Do not run /tmp scripts unless you created and verified them yourself.

Risk: Notification and AI features can send data to external services when credentials are configured.

Mitigation: Keep notifications and AI APIs disabled unless needed, and avoid entering real SMTP or API credentials until the data flow is understood.

Risk: Trading outputs may be mistaken for financial advice.

Mitigation: Treat generated analysis and signals as informational only and review decisions independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/12-v2-2)
- [Publisher profile](https://clawhub.ai/user/nidhov01)
- [V2.2 deployment and usage guide](artifact/docs/V2.2完整部署与使用指南.md)
- [V2.2 architecture design](artifact/docs/V2.2集成架构设计.md)
- [V2.2 delivery summary](artifact/docs/V2.2完整系统交付总结.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with Python and shell command snippets plus YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local Python packages, market data access, and optional SMTP or API credentials when notification or AI features are enabled.]

## Skill Version(s):

2.2.0 (source: artifact/SKILL.md frontmatter; ClawHub release metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
