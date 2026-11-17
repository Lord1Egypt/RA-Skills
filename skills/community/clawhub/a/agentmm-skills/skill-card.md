## Description:

AgentMM memory and log management skill gives AI agents persistent memory storage and structured logging for remembering information, recalling memories, and recording or querying logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cers-ai](https://clawhub.ai/user/cers-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory and structured logging workflows to an AI agent, including write, read, search, update, forget, sync, and stats operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory and log content is persisted to a configurable remote AgentMM endpoint, and the scanner noted that HTTPS is not enforced by the scripts.

Mitigation: Install only when the AgentMM service or self-hosted endpoint is trusted, avoid storing secrets or sensitive client data, and set AGENTMM_API_BASE to an HTTPS endpoint under the operator's control.

Risk: Autonomous memory writes can record unintended information in sensitive workspaces.

Mitigation: Require approval before autonomous memory writes where appropriate and stop the sync daemon when continuous synchronization is not needed.

Risk: Retention and deletion behavior depends on the configured AgentMM service.

Mitigation: Confirm the service's retention and deletion behavior before relying on the skill for long-term memory or log management.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cers-ai/skills/agentmm-skills)
- [AgentMM Service Home](https://agentmm.site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted API responses from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTMM_API_KEY, curl, and jq; AGENTMM_API_BASE can point to a self-hosted HTTPS endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
