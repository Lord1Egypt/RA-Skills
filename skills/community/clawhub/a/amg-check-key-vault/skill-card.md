## Description: <br>
Runs an on-demand fleet-wide Azure Key Vault health check across availability, API latency, throttling, authentication failures, and saturation, then deep-dives into the most relevant vaults with metrics and resource logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1w2w3y](https://clawhub.ai/user/1w2w3y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers, SREs, and developers use this skill to inspect Azure Key Vault fleet health through Azure Managed Grafana telemetry, identify degraded vaults, and produce prioritized remediation actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display or persist sensitive operational telemetry such as vault names, subscription IDs, caller IPs, application IDs, or secret/key identifiers. <br>
Mitigation: Use it only for authorized Azure subscriptions, avoid sharing raw outputs externally, and review or clean memory/amg-check-key-vault/report.md and config.md when they contain sensitive details. <br>
Risk: The configured Azure Managed Grafana MCP endpoint and token grant access to operational telemetry. <br>
Mitigation: Verify the MCP endpoint before registration and use a least-privilege Grafana service-account token. <br>


## Reference(s): <br>
- [Analysis Patterns & Known Issue Cross-Reference](reference/analysis-patterns.md) <br>
- [Deep-Dive Queries](reference/deep-dive-queries.md) <br>
- [Error Handling](reference/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with metric summaries, KQL query results, action items, and persisted issue updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update memory/amg-check-key-vault/config.md and memory/amg-check-key-vault/report.md during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
