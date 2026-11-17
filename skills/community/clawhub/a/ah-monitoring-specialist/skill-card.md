## Description:

You are a monitoring and observability specialist expert in implementing comprehensive monitoring solutions using modern observability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to design and implement observability systems, including metrics, logs, traces, dashboards, alerting rules, synthetic checks, and SLI/SLO monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry and alerting examples may expose sensitive data through raw log messages, direct user identifiers, webhook destinations, or retained screenshots.

Mitigation: Replace placeholder endpoints, restrict webhook destinations, redact sensitive fields, avoid direct user IDs, and control screenshot retention and alert recipients before production use.

Risk: Example monitoring configurations may be copied into production without adapting alert thresholds, retention windows, or recipient policies.

Mitigation: Review alert rules, retention settings, and notification routing against the deployment environment before enabling them.

## Reference(s):

- [Monitoring Specialist Code Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown with configuration and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include YAML, JSON, Python, and JavaScript monitoring patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
