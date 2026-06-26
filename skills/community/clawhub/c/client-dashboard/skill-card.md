## Description: <br>
Generates a client-facing executive KPI dashboard from QuickBooks Online data and produces an Excel workbook with traffic-light scoring, 6-month trend sparklines, client-specific watch items, and month-over-month KPI change tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and advisory teams use this skill after monthly close to generate a client-facing executive KPI dashboard from QuickBooks Online data for clients with an active QBO integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on authenticated QuickBooks access and a referenced local pipeline script that is not included in the reviewed package. <br>
Mitigation: Install only after inspecting and trusting the local pipeline script, and confirm the qbo-client connection targets the intended client company before running commands. <br>
Risk: Generated workbooks and CDC cache files can contain confidential client financial data. <br>
Mitigation: Store generated files and .cache/client-dashboard snapshots in approved locations, restrict access, and delete stale cache files when they are no longer needed. <br>
Risk: Using the dashboard before monthly close or for clients without QBO integration can produce incomplete or misleading executive summaries. <br>
Mitigation: Run it only after the monthly close is complete for clients with a configured QBO integration, and review the workbook against source accounting reports before sharing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated deliverable is an XLSX workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces KPI_Dashboard_{slug}_{YYYY_MM}.xlsx and stores KPI change snapshots under .cache/client-dashboard/{slug}.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
