## Description:

Cloud memory for AI agents. Writes are free, pay only for reads. First 25 calls free, 7-day persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natmota](https://clawhub.ai/user/natmota)

### License/Terms of Use:


## Use Case:

Developers and agent operators use AgentMem to store, retrieve, delete, list, and share agent memory through a third-party cloud API. It supports session persistence, cross-device sync, team knowledge sharing, and long-term agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to upload memories, local memory files, secrets, credentials, private conversations, personal data, or business data to a third-party cloud service.

Mitigation: Use AgentMem only for deliberately selected, non-sensitive memories and require explicit user approval before any automatic or recurring upload.

Risk: Retrieved memories and public-feed content may be untrusted and could influence agent behavior.

Mitigation: Treat retrieved data as untrusted context and require review before acting on it or using it in sensitive decisions.

Risk: Public memories can expose data beyond the intended audience.

Mitigation: Require explicit confirmation before enabling public memories and avoid publishing private, personal, or business information.

## Reference(s):

- [AgentMem ClawHub listing](https://clawhub.ai/natmota/skills/agentmem)
- [AgentMem website](https://agentmem.io)
- [AgentMem API base](https://api.agentmem.io/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional API key usage and instructions for recurring memory sync.]

## Skill Version(s):

2.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
