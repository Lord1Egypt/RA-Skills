## Description:

Set up APort guardrails for OpenClaw with local-first policy enforcement that checks tool calls against a passport before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aporthq](https://clawhub.ai/user/aporthq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to install, configure, and verify APort guardrails that enforce local tool-call policies before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that installation runs unpinned remote source or package code and registers a persistent OpenClaw before_tool_call hook.

Mitigation: Install only from the trusted APort publisher, prefer a reviewed pinned commit or exact package version, and avoid elevated privileges during installation.

Risk: The skill writes local guardrail state under ~/.openclaw/ and changes local tool-call behavior through a hook.

Mitigation: Inspect files written under ~/.openclaw/, verify expected allow and deny behavior after setup, and confirm hook removal steps before relying on it.

Risk: Optional API mode can send tool name and action type to a configured service.

Mitigation: Keep API mode disabled unless centralized dashboards are required, and review APORT_API_URL and APORT_AGENT_ID before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aporthq/skills/aport-agent-guardrail)
- [Source code](https://github.com/aporthq/aport-agent-guardrails)
- [Security Model](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/SECURITY_MODEL.md)
- [OAP Specification](https://github.com/aporthq/aport-spec)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides prerequisite checks, interactive installation, verification commands, audit-log inspection, troubleshooting, and optional API-mode configuration.]

## Skill Version(s):

1.1.20 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
