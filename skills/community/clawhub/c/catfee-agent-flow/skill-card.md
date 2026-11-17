## Description:

AgentFlow workflow-management MCP skill for creating and managing projects, requirements, tasks, status transitions, searches, and entity file uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to synchronize requirement documents into AgentFlow, break work into tasks, track status changes, and attach files to projects, requirements, or tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project, requirement, task, and attachment data may be sent to a hard-coded plaintext HTTP AgentFlow service.

Mitigation: Use only where sending that data to the configured AgentFlow server is intended; change the endpoint to authenticated HTTPS before confidential or production use.

Risk: The skill can sync, delete, upload, and transition workflow entities with weak user control.

Mitigation: Require explicit confirmation before syncing, deleting, uploading files, or changing workflow status, and validate upload destinations before sending files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/glory904649854/skills/catfee-agent-flow)
- [AgentFlow MCP SSE endpoint](http://182.42.153.28:18900/api/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-formatted AgentFlow responses and local Markdown task files during workflows.]

## Skill Version(s):

1.9.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
