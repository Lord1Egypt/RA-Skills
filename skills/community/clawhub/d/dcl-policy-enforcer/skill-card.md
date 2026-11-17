## Description:

DCL Policy Enforcer helps agents review LLM or agent outputs for policy, safety, jailbreak, quality, and regulatory-theme concerns using a paid DCL Trust Oracle service or a free local checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to gate risky agent actions, screen outputs for jailbreak or safety issues, and create audit evidence for policy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live policy checks can send evaluated outputs to a third-party service.

Mitigation: Redact secrets and personal data before live checks, or use the free local checklist when data should not leave the agent context.

Risk: Paid MCP calls can trigger wallet payments.

Mitigation: Configure wallet budgets, spending limits, or manual approval before enabling the live MCP server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-policy-enforcer)
- [DCL Trust Oracle MCP endpoint](https://mcp.fronesislabs.com/mcp)
- [Fronesis Labs DCL Security Suite](https://hub.fronesislabs.com)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, text]

**Output Format:** [Markdown with JSON and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct an agent to call a paid remote MCP policy-check service or use a free instruction-only checklist.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence; artifact frontmatter states 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
