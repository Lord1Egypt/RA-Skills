## Description: <br>
Runs a fleet-wide Azure PostgreSQL Flexible Server health check across CPU, memory, storage, IOPS, disk bandwidth, connections, resource logs, and known issues using AMG MCP and Azure Monitor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1w2w3y](https://clawhub.ai/user/1w2w3y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to assess Azure PostgreSQL Flexible Server fleet health, investigate abnormal servers, correlate metrics with resource logs, and produce prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains Azure PostgreSQL operational findings across sessions in memory/amg-check-pg-flex/report.md. <br>
Mitigation: Decide before use whether persistent findings are needed, minimize retained details, and delete the report after each engagement when retention is not required. <br>
Risk: Generated shell commands may process cloud diagnostic output. <br>
Mitigation: Run generated commands only in trusted workspaces and inspect or sanitize diagnostic output before execution. <br>
Risk: The skill requires Grafana service-account access and Azure Monitor queries that can expose fleet topology and operational logs. <br>
Mitigation: Use least-privilege credentials, configure only the intended subscription IDs, and avoid sharing rendered reports outside the authorized operations context. <br>


## Reference(s): <br>
- [Analysis Patterns](reference/analysis-patterns.md) <br>
- [Deep-Dive Queries](reference/deep-dive-queries.md) <br>
- [Error Handling](reference/error-handling.md) <br>
- [Output Format](reference/output-format.md) <br>
- [Phase 3 Deep Metrics](reference/phase3-deep-dive.md) <br>
- [Phase 4 Resource Logs](reference/phase4-resource-logs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown health-check report with tables, action items, inline shell commands, and persistent Markdown configuration/report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts optional time-range and subscription arguments; writes or updates memory/amg-check-pg-flex/config.md and memory/amg-check-pg-flex/report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
