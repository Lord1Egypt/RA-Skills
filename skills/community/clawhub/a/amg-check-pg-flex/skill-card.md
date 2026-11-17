## Description:

Runs a fleet-wide Azure PostgreSQL Flexible Server health check, scanning CPU, memory, storage, IOPS, disk bandwidth, and connection metrics before investigating abnormal servers with Azure Monitor metrics, PostgreSQL resource logs, and known-issue tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1w2w3y](https://clawhub.ai/user/1w2w3y)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators, SREs, and database engineers use this skill to run an on-demand health check across Azure PostgreSQL Flexible Server fleets. It helps triage fleet-level resource pressure, deep-dive abnormal servers, correlate logs and metrics, and maintain a persistent known-issues report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live Grafana bearer token can be exposed through shell history, logs, screenshots, or support transcripts if pasted directly into setup commands.

Mitigation: Use a least-privilege dedicated Grafana service-account token, prefer secret management over inline command entry, and rotate the token if exposure is suspected.

Risk: The skill accesses Azure Managed Grafana and PostgreSQL monitoring data during health checks.

Mitigation: Install and run it only in environments where that monitoring-data access is approved, and scope credentials to the minimum required permissions.

Risk: Large-result recovery may involve local parsing commands over saved telemetry files.

Mitigation: Review the generated file path and contents before approving local parsing commands, and avoid broad command approval unless the result file is trusted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/1w2w3y/skills/amg-check-pg-flex)
- [Output Format](reference/output-format.md)
- [Error Handling](reference/error-handling.md)
- [Phase 3 Deep Metrics](reference/phase3-deep-dive.md)
- [Phase 4 Resource Logs](reference/phase4-resource-logs.md)
- [Analysis Patterns](reference/analysis-patterns.md)
- [Deep-Dive Queries](reference/deep-dive-queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, action items, inline commands, and persistent known-issue updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fleet inventory, pulse-check results, abnormal-server deep dives, resource-log findings, known-issue cross-reference, prioritized actions, and an updated memory report.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
