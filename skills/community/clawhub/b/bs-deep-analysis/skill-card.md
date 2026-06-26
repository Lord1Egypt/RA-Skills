## Description: <br>
Controller-level Balance Sheet deep analysis from QuickBooks Online that pulls current and prior period balance sheets, runs rolling averages and GL drill-downs, and generates a 7-tab Excel workbook with actionable findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and accounting teams use this skill for monthly close balance sheet review, working capital health checks, equity rollforward reconciliation, and material balance-change explanations from QuickBooks Online data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Excel reports and cache files may contain sensitive financial, vendor, payee, and transaction-level details. <br>
Mitigation: Use secure output directories and delete or protect generated Excel and cache files after use. <br>
Risk: Running the skill with the wrong QuickBooks company access could analyze or expose unintended company data. <br>
Mitigation: Install and run it only where the agent is expected to access that QuickBooks company, and confirm the company slug and authorization before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/bs-deep-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with bash examples; the referenced pipeline produces an Excel workbook.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected QuickBooks Online company slug; generated reports and cache files may contain sensitive financial and transaction-level details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
