## Description: <br>
Runs a fleet-wide Cosmos DB for MongoDB (RU) health check through Azure Managed Grafana, scanning RU consumption, availability, latency, throttling, replication metrics, and abnormal-account logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1w2w3y](https://clawhub.ai/user/1w2w3y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators and reliability engineers use this skill to assess Cosmos DB for MongoDB (RU) account health across an Azure fleet, identify abnormal resources, and produce prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive cloud inventory, telemetry, and account health details in generated reports. <br>
Mitigation: Use the narrowest practical subscription and time range, and periodically review or delete local memory reports that contain infrastructure details. <br>
Risk: The workflow requires access to Azure Managed Grafana and may run local parsing commands for large results. <br>
Mitigation: Use a least-privileged Grafana service-account token and approve only expected local parsing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1w2w3y/amg-check-cosmosdb-mongo-ru) <br>
- [Output Format](reference/output-format.md) <br>
- [Error Handling](reference/error-handling.md) <br>
- [Analysis Patterns](reference/analysis-patterns.md) <br>
- [Phase 4 Deep Metrics](reference/phase4-deep-metrics.md) <br>
- [Phase 5 Resource Logs](reference/phase5-resource-logs.md) <br>
- [Deep-Dive Queries](reference/deep-dive-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown health report with tables, findings, action items, and optional local memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure Resource Graph queries, Azure Monitor metric and log analysis, and updates to a local known-issues report.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
