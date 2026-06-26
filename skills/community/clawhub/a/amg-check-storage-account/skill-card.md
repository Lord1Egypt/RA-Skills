## Description: <br>
Runs a fleet-wide Azure Storage Account health check with availability, latency, transaction, error-rate, metric, and resource-log analysis, then deep-dives into up to seven notable accounts and tracks known issues across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1w2w3y](https://clawhub.ai/user/1w2w3y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and developers use this skill to assess Azure Storage Account fleet health through Azure Managed Grafana MCP queries, identify accounts with availability, latency, traffic, or error anomalies, and produce prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query operational telemetry and persist diagnostic findings across sessions. <br>
Mitigation: Use a read-only Grafana or Azure token scoped to the intended subscriptions, and inspect or delete memory/amg-check-storage-account files if retained findings are not desired. <br>
Risk: The skill may ask to run local parsing commands while processing large telemetry results. <br>
Mitigation: Approve local commands only when the data being processed and the command purpose are clear. <br>


## Reference(s): <br>
- [Analysis Patterns & Known Issue Cross-Reference](reference/analysis-patterns.md) <br>
- [Deep-Dive Queries](reference/deep-dive-queries.md) <br>
- [Error Handling](reference/error-handling.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1w2w3y/amg-check-storage-account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with metric summaries, KQL query context, action items, and persistent known-issue updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write or update memory/amg-check-storage-account configuration and report files during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
