## Description:

Query and manage a heavy equipment fleet through FieldFix's API, including machines, maintenance, expenses, alerts, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueprintstudioco](https://clawhub.ai/user/blueprintstudioco)

### License/Terms of Use:

MIT

## Use Case:

External fleet operators and their agents use FieldFix to inspect machine records, review service history, monitor expenses and alerts, and submit maintenance, expense, or hour-meter updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A FieldFix API key can let an agent access fleet data and perform actions against the connected FieldFix account.

Mitigation: Use a limited-scope API key if FieldFix supports one and provide it only through FIELDFIX_API_KEY.

Risk: Write commands can create or update service, expense, and hour-meter records.

Mitigation: Require the agent to preview and get explicit confirmation before running log-service, log-expense, or update-hours.

## Reference(s):

- [FieldFix API Documentation](https://www.fieldfix.ai/api)
- [FieldFix App](https://app.fieldfix.ai)
- [FieldFix MCP Server](https://www.npmjs.com/package/fieldfix-mcp-server)
- [FieldFix ClawHub Skill Page](https://clawhub.ai/blueprintstudioco/skills/fieldfix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIELDFIX_API_KEY and network access to the FieldFix API; write commands can change service, expense, and hour-meter records.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
