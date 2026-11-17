## Description:

Runs a fleet-wide Azure Storage Account health check using Azure Managed Grafana MCP tools, summarizing availability, latency, transactions, error rates, capacity, ingress and egress, then deep-diving into up to seven notable accounts with metrics and resource logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1w2w3y](https://clawhub.ai/user/1w2w3y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and cloud operations teams use this skill to inspect Azure Storage Account health across one or more subscriptions, identify degraded or dormant accounts, and produce prioritized operational findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and fallback instructions can expose sensitive Grafana service-account credentials through shell commands or command history.

Mitigation: Use a least-privileged Grafana service account, prefer safer secret mechanisms over pasted bearer tokens, and rotate any token that may have been exposed.

Risk: Generated reports can contain sensitive operational data such as subscription IDs, IP addresses, user agents, URIs, and storage account details.

Mitigation: Treat generated reports and copied telemetry as sensitive operational data and restrict access to the workspace and report files.

Risk: The skill permits broader local execution than the health-check task strictly requires.

Mitigation: Review the skill before installing, run it in an appropriately scoped workspace, and use only the required MCP tools and report files during execution.

## Reference(s):

- [Analysis Patterns & Known Issue Cross-Reference](reference/analysis-patterns.md)
- [Deep-Dive Queries](reference/deep-dive-queries.md)
- [Error Handling](reference/error-handling.md)
- [ClawHub Skill Page](https://clawhub.ai/1w2w3y/skills/amg-check-storage-account)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary report with fleet inventory, pulse-check summary, deep-dive findings, resource-log findings, known-issue cross-reference, and prioritized action items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a persistent known-issues report file when sustained availability drops, throttling, high error rates, or latency degradation are found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
