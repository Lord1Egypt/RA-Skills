## Description:

AgentMFA requests human approval before sensitive actions using MCP tools for registration, identity, and approval flows across MCP-compatible clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leiarenee](https://clawhub.ai/user/leiarenee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentMFA to require explicit human approval before destructive, financial, production, messaging, infrastructure, or other sensitive actions performed by an MCP-compatible agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs an unpinned external CLI, which can change between reviews.

Mitigation: Review the CLI source and install provenance, and pin or mirror a reviewed CLI version for sensitive environments.

Risk: Approval codes or one-time proof tokens could be exposed if they are logged or pasted into chat.

Mitigation: Treat approval codes and tokens as transient secrets; do not log, persist, or echo them in user-visible transcripts.

Risk: AgentMFA is opt-in, so sensitive actions are not protected unless the agent explicitly requests approval.

Mitigation: Require the agent workflow to request approval before sensitive actions and to abort when approval is rejected, expired, or missing.

## Reference(s):

- [AgentMFA homepage](https://agentmfa.ai)
- [AgentMFA privacy and security policy](https://agentmfa.ai/privacy)
- [AgentMFA MCP Examples](references/examples.md)
- [AgentMFA Error Handling](references/errors.md)
- [ClawHub skill page](https://clawhub.ai/leiarenee/skills/agentmfa)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the agentmfa CLI and an MCP-compatible client; approval checks are opt-in and must be invoked by the agent.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
