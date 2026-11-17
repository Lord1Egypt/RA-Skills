## Description:

Exist API integration with managed OAuth. Read health and fitness tracking data, retrieve correlations and insights, manage attribute ownership, and track wellness metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an Exist account through ClawLink OAuth, read health and fitness metrics, discover correlations and insights, and manage attribute ownership or counter updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive wellness data may be exposed through the ClawLink OAuth integration.

Mitigation: Verify trust in ClawLink and the clawlink-plugin source before installing, and grant only the Exist OAuth scopes needed.

Risk: Write and ownership-release actions can alter tracked counters or stop data flow for an Exist attribute.

Mitigation: Require explicit confirmation for write and release actions, and verify the target attributes before execution.

Risk: OAuth access or plugin enablement may remain active after the user is done with the skill.

Mitigation: Know how to revoke the Exist OAuth grant and remove or disable the enabled plugin later.

## Reference(s):

- [Exist API Docs](https://developer.exist.io/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=exist)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [Exist Skill on ClawHub](https://clawhub.ai/hith3sh/skills/exist)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown instructions with bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ClawLink tool-call examples whose returned data depends on the user's Exist OAuth scopes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
