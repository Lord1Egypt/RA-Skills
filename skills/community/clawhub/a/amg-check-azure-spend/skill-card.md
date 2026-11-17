## Description:

Run only when the user explicitly asks for a monthly Azure subscription cost analysis: it lists accessible Azure subscriptions, lets the user choose which to analyze, and queries the last full billing month's cost breakdown by resource type, region, and service category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1w2w3y](https://clawhub.ai/user/1w2w3y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operations teams, and FinOps practitioners use this skill to review monthly Azure subscription spending through Azure Managed Grafana MCP tools, compare spend across subscriptions, and produce a saved cost report with optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses Azure and Grafana billing data, which can expose sensitive subscription and cost details.

Mitigation: Use a least-privileged Grafana service account and review saved reports before sharing or retaining them.

Risk: Service-account tokens can be exposed if pasted into shell history, shared logs, or saved setup output.

Mitigation: Avoid storing live tokens in shared logs or command history, and rotate any token that may have been exposed.

Risk: The security review flagged under-disclosed token handling and an overbroad local parsing fallback.

Mitigation: Review the skill before installation, limit workspace file access where possible, and inspect generated files that may contain billing details.

## Reference(s):

- [Error Handling](reference/error-handling.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown report with tables, status notes, inline shell commands, and a saved report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries selected subscriptions sequentially, includes mandatory wait and backoff steps, and saves the report to memory/amg-check-azure-spend/report.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
