## Description:

AgentPulse tracks LLM API costs, token usage, latency, errors, and rate-limit signals for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sru4ka](https://clawhub.ai/user/sru4ka)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect OpenClaw usage telemetry to AgentPulse, then answer questions about spend, token volume, errors, latency, model usage, and alert setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently send detailed metadata for every LLM call to AgentPulse, including model names, token counts, latency, status, and costs.

Mitigation: Install and configure it only where that telemetry flow is approved, and ensure users understand that reporting can occur in the background.

Risk: Raw error messages may contain sensitive context and can be forwarded to the AgentPulse service.

Mitigation: Avoid including sensitive data in error messages where possible, and control or disable telemetry in OpenClaw environments that handle restricted information.

## Reference(s):

- [ClawHub AgentPulse skill page](https://clawhub.ai/sru4ka/skills/agentpulse)
- [AgentPulse service](https://agentpulse.dev)
- [AgentPulse dashboard](https://agentpulse.dev/dashboard)
- [AgentPulse alerts dashboard](https://agentpulse.dev/dashboard/alerts)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with shell commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTPULSE_API_KEY and curl; may send LLM usage metadata and raw error messages to agentpulse.dev.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
