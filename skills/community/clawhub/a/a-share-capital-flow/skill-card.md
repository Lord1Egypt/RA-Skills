## Description:

Provides a Chinese-language A-share capital-flow analysis framework for daily briefings, position health checks, and trading-strategy guidance based on capital flows and sector rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukai8289](https://clawhub.ai/user/wukai8289)

### License/Terms of Use:

MIT

## Use Case:

External users and market-analysis agents use this skill to generate A-share capital-flow briefings, evaluate position risk, and prepare decision-support guidance before manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated buy, sell, price, or position-sizing suggestions as professional financial advice.

Mitigation: Present outputs as decision-support analysis only and require qualified human review before making trading or allocation decisions.

Risk: Scheduled financial briefings or intraday reports may be acted on automatically without checking current market context.

Mitigation: Review scheduled reports manually before acting, especially when market data, policy signals, or holdings have changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukai8289/skills/a-share-capital-flow)
- [capital-flow-checklist.md](artifact/capital-flow-checklist.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Chinese-language Markdown-style analysis, checklists, cron task descriptions, and trading guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include buy, sell, price, position-sizing, and scheduled-report suggestions that require human review before use.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
