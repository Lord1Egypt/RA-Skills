## Description:

Budget Analyzer Claw helps OpenClaw users estimate AI resource spend, compare usage against configured budgets, detect cost anomalies, and generate cost reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to monitor session token usage, estimate agent-level costs, identify budget overruns, and request daily, weekly, or monthly cost summaries with optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad session metadata or histories while estimating costs, exposing unrelated conversation content.

Mitigation: Limit analysis to explicitly approved sessions and time ranges, and avoid granting access to full session histories unless needed.

Risk: Generated costs may differ from actual provider invoices when billing rules are stale or a model is missing.

Mitigation: Treat reports as estimates and periodically update billing-rules.json against provider pricing before making budget decisions.

Risk: Budget and cost reports can reveal sensitive operational or business spending information.

Mitigation: Keep generated reports out of public channels and share them only with approved recipients.

## Reference(s):

- [Billing Rules](artifact/references/billing-rules.json)
- [Budget Configuration](artifact/references/budget-config.yaml)
- [Cost Optimization Tips](artifact/references/optimization-tips.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/budget-analyzer-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, status labels, cost estimates, recommendations, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost values are estimates based on maintained billing rules and should be checked against provider invoices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
