## Description:

Assesses wind turbine gearbox health from multi-sensor and inspection data, classifies damage severity from 1 to 5, identifies likely root cause, and recommends shutdown or monitoring actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sertug17](https://clawhub.ai/user/sertug17)

### License/Terms of Use:

MIT

## Use Case:

Maintenance engineers and wind operations teams use this skill to turn gearbox inspection, oil, temperature, vibration, and acoustic observations into a structured maintenance report with severity, root cause, monitoring, escalation, and shutdown guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shutdown and monitoring recommendations may be incorrect or incomplete if treated as authoritative operational decisions.

Mitigation: Use the report as an advisory checklist and confirm Severity 4-5 results, shutdown decisions, and thresholds with qualified maintenance engineers, OEM documentation, site safety procedures, and historical trend data.

Risk: The skill depends on field observations and sensor inputs that may be subjective, missing, or affected by site conditions.

Mitigation: Cross-check multiple evidence sources before assigning the highest severity and ask for baseline-normalized values and additional trend data when available.

## Reference(s):

- [ClawHub Gearbox Skill Page](https://clawhub.ai/sertug17/skills/gearbox)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured markdown maintenance report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes root cause, severity, shutdown recommendation, monitoring strategy, and escalation triggers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
