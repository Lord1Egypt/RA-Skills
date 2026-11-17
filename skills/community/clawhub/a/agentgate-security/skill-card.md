## Description:

Enforces regex-based, real-time authorization policies on OpenClaw agents' tool calls, blocking, allowing, or requiring approval before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiserautomation](https://clawhub.ai/user/wiserautomation)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add policy evaluation, audit logging, and approval gates around OpenClaw tool calls before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool names and full tool arguments are sent to AgentGate's hosted service for policy evaluation.

Mitigation: Review data handling, redaction controls, audit-log retention, deletion practices, and tenant isolation before using it with sensitive agents.

Risk: The release has unavailable provenance and relies on an unpinned npm package according to the security evidence.

Mitigation: Pin package versions, inspect the installed package and lockfile, and request source or provenance details before deployment.

Risk: Regex policy mistakes can allow unsafe actions or block legitimate tool calls.

Mitigation: Test policies with low-privilege agents, monitor audit logs, and require approval for high-impact tools such as shell, filesystem, payment, and outbound network actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wiserautomation/skills/agentgate-security)
- [AgentGate website](https://agent-gate-rho.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include policy examples, setup steps, and operational review guidance.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
