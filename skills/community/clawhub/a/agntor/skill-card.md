## Description:

Trust layer for AI agents: verify identities, guard prompts, redact PII, and manage x402 escrow payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garinmckayl](https://clawhub.ai/user/garinmckayl)

### License/Terms of Use:


## Use Case:

External developers and agent operators use Agntor to add identity checks, prompt-injection screening, PII redaction, agent trust scoring, audit tickets, and escrow payment workflows to agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes sensitive content through an external MCP service for input guarding, output redaction, trust checks, and related actions.

Mitigation: Use a narrowly scoped AGNTOR_API_KEY and avoid sending secrets or private code unless the service's data handling is understood and accepted.

Risk: Payment, audit-ticket, registration, verification probe, and kill-switch actions can affect funds or administrative state.

Mitigation: Require explicit user approval before invoking those actions.

Risk: The MCP installation is not pinned in the artifact configuration.

Mitigation: Prefer a pinned or audited package version and run the MCP server in a sandboxed environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/garinmckayl/skills/agntor)
- [Agntor GitHub Repository](https://github.com/agntor/agntor)
- [Agntor Documentation](https://docs.agntor.com)
- [Agntor Dashboard](https://app.agntor.com)
- [Agntor SDK npm Package](https://www.npmjs.com/package/@agntor/sdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call Agntor MCP tools for trust checks, input guarding, output redaction, escrow, audit ticket, registration, and administrative actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
