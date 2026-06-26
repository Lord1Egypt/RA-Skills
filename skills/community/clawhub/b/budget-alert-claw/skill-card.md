## Description: <br>
Monitors budget usage, checks single or batch expense requests against configured budgets, flags overspending or anomalies, and produces advisory budget reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and budget owners use this skill to check expense requests, batch-validate spending records, detect unusual spending patterns, and generate budget execution reports from configured budget and expense data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Budget red-light results may be mistaken for actual enforced spending controls. <br>
Mitigation: Treat green, yellow, and red outcomes as recommendations unless the workflow is connected to a real approval system with human review, audit logs, and explicit fail-closed behavior. <br>
Risk: Missing budget configuration defaults can allow an expense to pass without a configured budget. <br>
Mitigation: Configure fallback rules before deployment and review any no-budget results before approving spend. <br>
Risk: Budget calculations and anomaly flags depend on the accuracy of user-provided CSV or natural-language expense data. <br>
Mitigation: Validate source budget and expense data, review generated reports, and reconcile high-impact decisions against authoritative finance systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/budget-alert-claw) <br>
- [Budget Rules](references/budget-rules.md) <br>
- [Anomaly Detection Rules](references/anomaly-detection.md) <br>
- [Notification Templates](references/notification-templates.md) <br>
- [Publisher profile](https://clawhub.ai/user/tujinsama) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON check results, CSV batch outputs, and plain-text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory unless connected to a separate approval system with human review, audit logs, and explicit fail-closed behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
