## Description:

AgentPMT Audit Logs lets an agent read this account's activity history, including past chat sessions, chat transcripts with tool calls, tool-call history, workflow runs, workflow schedules, and authorized agent groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review AgentPMT account activity, summarize agent work, investigate failed workflow runs, and audit read-only chat, tool-call, workflow, and schedule history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit-log responses can expose sensitive account history, chat transcripts, tool-call details, workflow runs, and schedule information.

Mitigation: Use the narrowest available AgentPMT scope, prefer current-agent-group access unless broader review is necessary, and avoid placing secrets or payment headers in prompts or logs.

Risk: Setup examples include unpinned npx installation commands.

Mitigation: Prefer reviewed OpenClaw or ClawHub setup paths, or pin versions before using command-line installation in production environments.

## Reference(s):

- [AgentPMT Audit Logs marketplace page](https://www.agentpmt.com/marketplace/agentpmt-audit-logs)
- [AgentPMT Audit Logs on ClawHub](https://clawhub.ai/agentpmt/skills/agentpmt-audit-logs)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only AgentPMT audit-log outputs may include sensitive account activity; use the narrowest available scope.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
