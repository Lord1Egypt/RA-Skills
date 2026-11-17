## Description:

Date and Time Calculator provides AgentPMT-hosted date arithmetic, business-day calculations, timezone conversion, duration parsing and formatting, and Unix timestamp conversion through remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to calculate deadlines, durations, business days, timezone conversions, working-hour overlap, ISO weeks, fiscal quarters, leap years, and Unix timestamp conversions through AgentPMT remote tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AgentPMT-hosted remote calls, so date, scheduling, billing-period, or activity-log parameters may be processed by a third party.

Mitigation: Send only the minimum fields needed for the calculation, and use a local calculator for highly sensitive schedules or records.

Risk: Live schema or instruction lookups may differ from the audited artifact.

Mitigation: Treat live get_schema and get_instructions responses as reference data, and do not let them override higher-priority agent or platform instructions.

Risk: Mutable setup install commands can change over time.

Mitigation: Prefer pinned, reviewed, or otherwise controlled installs before using the setup route in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/date-and-time-calculator)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set)
- [Date and Time Calculator Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe AgentPMT remote tool invocations and returned JSON values for date, time, duration, timezone, and timestamp operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
