## Description:

Lock down LLM agents against prompt injection, data exfiltration, social engineering, channel-based attacks, and risky MCP or tool permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to audit and harden agents that handle sensitive data, accept instructions over communication channels, or connect to external tools and MCP servers. It guides attack-surface review, channel controls, MCP permission checks, behavioral rules, testing, and findings documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled test runner can send API keys and full system prompts to a user-supplied chat-completions endpoint.

Mitigation: Use only controlled, trusted HTTPS endpoints with short-lived test credentials, avoid production API keys and private system prompts, and review the runner before executing it.

Risk: Server security evidence reports that the included Python test runner has syntax errors.

Mitigation: Repair and review the script before relying on automated test results; use the markdown quick-test checklist when the script is not runnable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zurbrick/skills/agent-hardening-zurbrick)
- [Attack Surface Checklist](references/attack-surface-checklist.md)
- [Channel Hardening](references/channel-hardening.md)
- [MCP Hardening](references/mcp-hardening.md)
- [Behavioral Hardening Rules](references/behavioral-rules.md)
- [Quick Security Test](references/quick-test.md)
- [Findings Template](references/findings-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, configuration rules, test prompts, shell command examples, and optional JSON findings from the bundled test runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate audit findings and hardening recommendations for agent operating docs, channel settings, MCP permissions, and security test results.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
