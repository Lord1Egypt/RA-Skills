## Description: <br>
Run only when the user explicitly asks for a monthly Azure subscription cost analysis: it lists accessible subscriptions, lets the user choose targets, and queries last billing month's cost breakdown by resource type, region, and service category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1w2w3y](https://clawhub.ai/user/1w2w3y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and FinOps teams use this skill to analyze the previous full billing month's Azure subscription costs through their Azure Managed Grafana MCP endpoint. It helps compare subscription spend, identify top cost drivers, and produce a saved Markdown report for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved cost reports may contain sensitive Azure subscription spend, service, and regional usage details. <br>
Mitigation: Treat memory/amg-check-azure-spend/report.md as sensitive and delete it when the detailed report is no longer needed. <br>
Risk: The skill connects to a user-provided Azure Managed Grafana MCP endpoint using a Grafana service-account token. <br>
Mitigation: Use a least-privilege Grafana token and register only the intended Azure Managed Grafana MCP server. <br>
Risk: Approved shell or interpreter commands can affect local files or expose data during setup, waiting, or large-result parsing. <br>
Mitigation: Review each shell or interpreter command before approval and only run commands needed for the current analysis. <br>


## Reference(s): <br>
- [Error Handling](reference/error-handling.md) <br>
- [ClawHub skill page](https://clawhub.ai/1w2w3y/amg-check-azure-spend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown cost report with tables, observations, optimization suggestions, and setup or wait commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves the full report to memory/amg-check-azure-spend/report.md and processes billing queries sequentially with rate-limit waits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
