## Description:

股票分析雷达专业版 helps agents analyze stocks and cryptocurrencies, compare tickers in batches, track portfolios, configure price alerts, detect market rumors, and export research outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External professional investors, research teams, and agents use this skill to analyze equities and cryptocurrencies, compare tickers in batches, monitor portfolios and alerts, and prepare exported research outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, execute, and external-notification authority could expose portfolio files, exports, API keys, callback URLs, webhook targets, or email destinations.

Mitigation: Review before installing, keep use limited to finance workflows, require explicit confirmation before exports, broker/API sync, webhook/email notifications, callback URLs, or long-running monitoring, and provide portfolio files or API keys only to trusted installations after checking where files and notifications will go.

Risk: The skill text includes unrelated security claims that may cause users to over-trust capabilities outside finance analysis.

Mitigation: Treat unrelated security wording as out of scope and rely on the skill only for finance workflows supported by the release evidence.

Risk: Rumor detection, trend scanning, and generated financial analysis may be incomplete or misleading if used as investment advice.

Mitigation: Use market-rumor and analysis outputs as decision support only, verify sources independently, and require human review before trading or portfolio changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-radar-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and exported CSV, Excel, or JSON file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local portfolio/configuration files, market-data API keys, webhook/email notification settings, and export paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
