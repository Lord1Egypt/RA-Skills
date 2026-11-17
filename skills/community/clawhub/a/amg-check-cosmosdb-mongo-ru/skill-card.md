## Description:

Runs a fleet-wide Azure Managed Grafana health check for Cosmos DB for MongoDB (RU) accounts, scanning RU consumption, availability, latency, throttling, and replication metrics before deep-diving abnormal accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1w2w3y](https://clawhub.ai/user/1w2w3y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Azure Cosmos DB for MongoDB (RU) fleets through Azure Managed Grafana, identify abnormal resource health signals, and produce prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can expose a Grafana bearer token and grants access to Azure monitoring data for selected subscriptions.

Mitigation: Use a narrowly scoped, revocable Grafana service-account token and avoid storing or pasting the token in shell history.

Risk: The workflow can persist cloud inventory, telemetry summaries, and known-issue reports in local workspace files.

Mitigation: Review or disable local memory/report writes when the workspace is shared, and treat generated reports as potentially sensitive operational data.

Risk: Fleet-wide scans may query every matching Cosmos DB for MongoDB (RU) account through the configured AMG MCP server.

Mitigation: Limit configured subscriptions to the intended scope and review the generated findings before acting on remediation guidance.

## Reference(s):

- [Analysis Patterns & Known Issue Cross-Reference](reference/analysis-patterns.md)
- [Deep-Dive Queries](reference/deep-dive-queries.md)
- [Error Handling](reference/error-handling.md)
- [Output Format](reference/output-format.md)
- [Phase 4: Tier 2 - Deep Metrics for Abnormal Accounts](reference/phase4-deep-metrics.md)
- [Phase 5: Resource Logs for Abnormal Accounts](reference/phase5-resource-logs.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health-check report with tables, command snippets, findings, action items, and local configuration/report updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-supplied time range and subscription selection; may persist configuration and known-issue reports in workspace memory files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
