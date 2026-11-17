## Description:

Boss AI Agent is an AI management advisor and team operations middleware for management advice, leadership guidance, team operations help, mentor-based decision support, C-Suite board simulation, and optional MCP-backed automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonypk](https://clawhub.ai/user/tonypk)

### License/Terms of Use:

MIT-0

## Use Case:

Managers, founders, and team leads use this skill for management decision support, 1:1 preparation, daily briefings, risk review, KPI health checks, team reporting, culture-aware feedback, and simulated executive board discussion. In Team Operations Mode, it can use MCP tools to query team context, send employee messages, schedule recurring workflows, and sync business data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Team Operations Mode can run persistent jobs, send employee messages, and sync business data.

Mitigation: Review every cron job and sync destination before enabling Team Operations Mode, disable jobs that are not needed, and preview employee-facing messages before sending.

Risk: Team Operations Mode can launch an external MCP package with an API key.

Mitigation: Pin and verify the MCP package before use and use a narrowly scoped API key for the connected organization.

Risk: Local learning fields and management context can involve sensitive workplace information.

Mitigation: Avoid storing employee personal details, health information, compensation data, performance scores, API keys, passwords, or tokens in local learning fields.

## Reference(s):

- [Boss AI Agent ClawHub Page](https://clawhub.ai/tonypk/skills/boss-ai-agent)
- [Boss AI Agent Website](https://manageaibrain.com)
- [MCP Endpoint](https://manageaibrain.com/mcp)
- [MCP Tools Reference](references/mcp-tools.md)
- [Mentor System Reference](references/mentors.md)
- [Culture Packs Reference](references/cultures.md)
- [Automated Scenarios Reference](references/scenarios.md)
- [Setup and Connection Guide](references/setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, JSON configuration snippets, and MCP tool action plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisor Mode can operate offline; Team Operations Mode may use API keys, MCP calls, cron jobs, local configuration, and employee-facing message workflows.]

## Skill Version(s):

9.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
