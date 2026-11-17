## Description:

数据库健康监控 helps agents run dbskiter monitoring workflows for health checks, anomaly detection, capacity forecasting, trend analysis, baseline comparison, and degradation detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators, SREs, and operations engineers use this skill to select and run dbskiter monitoring commands for Oracle and MySQL environments. It helps agents interpret health, anomaly, capacity, trend, baseline, and degradation results from configured monitoring data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to query operational database monitoring data in environments where that access is not intended.

Mitigation: Install it only where agents are permitted to use dbskiter, and keep dbskiter permissions read-only or monitoring-scoped.

Risk: An ambiguous request could target the wrong database or monitoring check.

Mitigation: Require an explicit database name and intended check type before running generated dbskiter commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-monitor)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Analysis]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring command selections and interpretation guidance; actual database metrics depend on dbskiter access and configured data sources.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
