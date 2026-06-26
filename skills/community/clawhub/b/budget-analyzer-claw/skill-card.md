## Description: <br>
Monitors OpenClaw agent resource usage, estimates AI spend, compares it with configured budgets, detects cost anomalies, and generates cost reports with optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to review OpenClaw AI resource spending, identify high-cost agents, compare usage against daily, weekly, and monthly budgets, and receive anomaly alerts or cost optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Billing rates, budget limits, recipients, or currency assumptions may be stale or misconfigured. <br>
Mitigation: Review the billing rules, budget configuration, Feishu recipient, and currency assumptions before installing or relying on reports. <br>
Risk: Generated cost reports may expose sensitive business usage or spending data. <br>
Mitigation: Treat reports as sensitive and confirm the audience before sharing broad or cross-session summaries. <br>
Risk: Budget enforcement or agent-pausing actions could interrupt active work. <br>
Mitigation: Require explicit user confirmation before any action that would pause agents or affect running work. <br>


## Reference(s): <br>
- [billing-rules.json](references/billing-rules.json) <br>
- [budget-config.yaml](references/budget-config.yaml) <br>
- [Cost Optimization Suggestions](references/optimization-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and structured cost summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates depend on maintained billing rules and may include sensitive usage or budget information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
