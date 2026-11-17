## Description:

Api Cost Optimizer helps OpenClaw operators estimate LLM API spend, diagnose heartbeat-driven waste, and generate cost-saving recommendations from local agent configuration and usage assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to estimate daily, weekly, monthly, and yearly LLM API costs, identify inefficient heartbeat settings, and prioritize model or configuration changes that may reduce spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts handle user-controlled inputs and environment values in ways the security evidence flags as unsafe for untrusted use.

Mitigation: Review or patch the scripts before installation and run them only as a trusted local operator with normal numeric inputs.

Risk: Cost reports are estimates based on configuration analysis and assumed usage patterns rather than actual provider billing records.

Mitigation: Treat generated reports as planning guidance and compare them with provider billing logs before making financial decisions.

Risk: Hostile environment or path values may affect script behavior.

Mitigation: Avoid exposing the skill to untrusted parameters or hostile local environment/path values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/api-cost-optimizer-kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and terminal text with cost estimates, heartbeat diagnostics, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates are based on configuration and assumed usage patterns, not live provider billing data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
