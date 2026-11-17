## Description:

OpenClaw API management and cost optimization. Manages multi-provider keys, monitors costs, routes tasks intelligently, and provides automated failover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT License

## Use Case:

Developers and operators use this skill to manage OpenClaw provider configuration, monitor API spending, rotate keys, validate setup, and route tasks to cost-effective models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles provider keys and OpenClaw configuration, and the security evidence flags unsafe secret-handling behavior.

Mitigation: Review before installing with real provider keys, avoid passing keys on command lines, redact key outputs, and restrict secret files to owner-only permissions.

Risk: Routing can send task text to OpenRouter when external routing is enabled.

Mitigation: Keep routing local-only for sensitive tasks unless the operator intentionally allows task text to be sent to OpenRouter.

## Reference(s):

- [ClawAPI Manager on ClawHub](https://clawhub.ai/2233admin/skills/clawapi-manager)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration guidance, and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local OpenClaw configuration, cost-monitoring, key-health, routing, and notification commands.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
