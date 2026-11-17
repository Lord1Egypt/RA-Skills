## Description:

Generates daily portfolio analysis reports by merging brokerage holdings, fetching current prices and exchange rates, and summarizing allocation, daily movement, country, and industry exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengbinxu](https://clawhub.ai/user/shengbinxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance operators use this skill to consolidate brokerage account holdings and generate a scheduled or conversational portfolio report. The report includes current prices, exchange rates, allocation percentages, daily gains or losses, and country and industry breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive holdings reports to Feishu without clear per-run consent or visible destination controls.

Mitigation: Verify the Feishu destination before use, redact brokerage screenshots and account identifiers, and add a local-only or confirmation step before push delivery.

Risk: Real portfolio data is stored under the OpenClaw workspace and may include sensitive holdings information.

Mitigation: Keep portfolio configuration files private, avoid uploading them to public repositories, and limit workspace access to trusted users.

## Reference(s):

- [Futu OpenD command documentation](https://openapi.futunn.com/futu-api-doc/opend/opend-cmd.html)
- [ClawHub skill page](https://clawhub.ai/shengbinxu/skills/daily-portfolio-analysis)
- [Publisher profile](https://clawhub.ai/user/shengbinxu)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown-style text report with tabular portfolio summaries and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send complete reports through the configured Feishu notifier and uses local portfolio configuration data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
