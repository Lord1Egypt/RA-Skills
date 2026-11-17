## Description:

Finance Reporter Publish fetches real-time Yahoo Finance market data for major stock indices, foreign exchange, commodities, and cryptocurrency, then formats the results for manual or scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfstylejf](https://clawhub.ai/user/jfstylejf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate current finance reports for monitored market symbols and to configure scheduled delivery to DingTalk or WeChat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency metadata may cause unsafe or unintended package installation.

Mitigation: Avoid running npm install for this package as written; define and pin the Python requests dependency in a Python-native dependency file before deployment.

Risk: Scheduled delivery can send finance reports to an unintended DingTalk or WeChat destination.

Mitigation: Confirm the destination, binding, and cron schedule before enabling automated delivery.

Risk: Live market data depends on Yahoo Finance availability and response quality at runtime.

Mitigation: Review generated reports before acting on them and monitor failures or retries during scheduled runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfstylejf/skills/finance-reporter-publish)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain-text finance report with command examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include symbols, currencies, current prices, prior close or 24-hour reference prices, and percentage changes.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
