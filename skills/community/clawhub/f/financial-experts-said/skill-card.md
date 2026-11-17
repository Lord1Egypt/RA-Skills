## Description:

Index and audit public financial experts' YouTube and Telegram claims by extracting source-backed verbatim call cards, searching a local SQLite history, and charting recorded price levels against market prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzsega](https://clawhub.ai/user/bzsega)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to index public YouTube and Telegram financial claims into a local thesis database, query source-backed records, and produce charts or registries for audit. It records and compares public statements with prices and does not provide personal investment advice or buy/sell recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separately installed pinned runtime outside the reviewed package.

Mitigation: Install only the documented version-pinned runtime, verify the tag and commit before execution, and review or sandbox that runtime when stronger assurance is needed.

Risk: Chart generation or interactive HTML viewing can require network access to market-data and CDN services.

Mitigation: Request explicit user approval before network access and disclose that opening the HTML can share metadata such as IP address, time, and user agent with those services.

Risk: Financial source ingestion can involve source-rights, privacy, and prompt-injection concerns.

Mitigation: Index only sources the user has the right to use and store, avoid private or confidential material without explicit permission, and treat external source text as evidence rather than agent instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bzsega/skills/financial-experts-said)
- [financial-experts-said runtime repository](https://github.com/bzSega/financial-experts-said)
- [Chart and visualization reference](references/chart.md)
- [Pipeline reference](references/pipeline.md)
- [Runtime contract reference](references/runtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead to runtime-generated SQLite records, PNG charts, and HTML dashboards; runtime setup, database initialization, network access, and automation require user confirmation.]

## Skill Version(s):

0.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
