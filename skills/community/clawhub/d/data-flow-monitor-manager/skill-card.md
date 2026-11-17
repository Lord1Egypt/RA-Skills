## Description:

Manages cross-tenant data-flow monitoring with data-flow graphs, anomaly alerts, tiered thresholds, Prometheus security metrics, and daily leakage scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to inspect tenant data-flow events, detect anomalous or cross-tenant access, adjust monitoring thresholds, and review leakage alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-tenant monitoring and leakage scans can expose sensitive tenant access logs or data-flow metadata.

Mitigation: Install only where operators are authorized, require explicit tenant scope or documented all-tenant approval, and audit scan activity.

Risk: Threshold changes can alter security monitoring behavior or alert volume.

Mitigation: Confirm authorization, record old and new values, and make threshold updates reversible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-flow-monitor-manager)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON tool responses with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require tenant scope, PG_DSN, PROMETHEUS_URL, and config/data_flow_thresholds.yaml.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
