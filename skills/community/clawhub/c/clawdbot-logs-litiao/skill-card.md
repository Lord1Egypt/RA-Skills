## Description:

Analyze Clawdbot logs and diagnostics. Use when the user asks about bot performance, response times, errors, session stats, token usage, API costs, or wants to debug slow responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Clawdbot response times, session statistics, token usage, API costs, gateway status, and recent errors when diagnosing slow or failing bot sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a command pattern that can print raw user conversation history from local session files.

Mitigation: Use the response-time and session-metadata scripts first, and only parse raw transcripts when a specific session is intentionally selected and its contents are acceptable to expose.

Risk: Clawdbot sessions may contain private, credential, business, or personal content.

Mitigation: Review the local data sensitivity before installing or running the skill, and redact diagnostic output before sharing it outside the trusted workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/clawdbot-logs-litiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize local log, session, token, cost, and service-status data when the user requests Clawdbot diagnostics.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
