## Description:

Real-time, audit-ready logging integration for ClawControl.space. Ensures deterministic, per-action observability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qasimnaqvi](https://clawhub.ai/user/qasimnaqvi)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to send per-action logs and basic metrics from an agent session to ClawControl.space for audit-oriented observability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to send broad session logs, including user messages and internal decisions, to an external service.

Mitigation: Enable it only with clear consent, limit logged data to low-sensitivity metadata, and remove internal-thought logging before deployment.

Risk: Sensitive values could be exposed through unredacted log payloads or API keys placed in URL query parameters.

Mitigation: Add redaction for sensitive fields, avoid shell interpolation, and pass API keys through safer secret-handling mechanisms instead of URL query strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qasimnaqvi/skills/clawcontrol-logger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with inline bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWCONTROL_API_KEY and sends JSON log payloads to an external ClawControl.space endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
