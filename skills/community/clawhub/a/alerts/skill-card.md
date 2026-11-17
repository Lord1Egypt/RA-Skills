## Description:

Smart alerting patterns for AI agents - deduplication, routing, escalation, and fatigue prevention

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and site reliability engineers use this skill to design AI-agent alerting practices for deduplication, routing, escalation, webhook reliability, status page updates, and runbook automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alerting integrations may expose operational systems if credentials or webhook endpoints are over-permissioned.

Mitigation: Use scoped integration credentials, validate webhook signatures, and check timestamps to reduce spoofing and replay risk.

Risk: Automated remediation could perform destructive actions if applied without human oversight.

Mitigation: Require explicit approval gates for destructive remediation and log all automated actions for review.

Risk: Alerting guidance can be misapplied and create noisy or misleading alerts.

Mitigation: Review alert grouping, severity, cooldown, routing, and escalation choices before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/alerts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML-style and bash-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; it does not install code or perform actions by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
