## Description:

Secure email proxy for AI agents. Search, read, and draft emails via MCP with server-side credential isolation, PII redaction, prompt injection detection, and content filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanfren](https://clawhub.ai/user/ryanfren)

### License/Terms of Use:

BSL 1.1

## Use Case:

External users and developers use AgentCloak to give agents controlled email search, read, thread, label, and draft access while filtering credentials, PII, security-sensitive messages, and prompt-injection attempts before content reaches the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted AgentCloak receives email credentials and message content.

Mitigation: Review the hosted-service trust model before connecting an inbox, or self-host AgentCloak when mailbox content must stay under direct user control.

Risk: The documented self-hosting setup executes mutable third-party code from an unpinned GitHub branch.

Mitigation: Pin a reviewed release or commit before deployment and run the service with minimal privileges.

Risk: Agents may still receive sensitive or adversarial email content after filtering.

Mitigation: Use the blocklist, PII redaction, and prompt-injection warning controls, and review created drafts before sending them outside the agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanfren/skills/agentcloak-email-proxy)
- [AgentCloak hosted app](https://agentcloak.up.railway.app)
- [AgentCloak source repository](https://github.com/ryanfren/AgentCloak)
- [AgentCloak MCP endpoint](https://agentcloak.up.railway.app/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks, MCP tool call examples, and filtered email or draft results returned as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and AGENTCLOAK_API_KEY; hosted use sends credentials and email content through the AgentCloak service, while self-hosted use keeps processing local to the user's deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
