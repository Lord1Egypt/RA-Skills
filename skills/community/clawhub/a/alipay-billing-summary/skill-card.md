## Description:

支付宝账单汇总会为已授权用户生成周度、月度和年度账单汇总与消费分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1148260649](https://clawhub.ai/user/1148260649)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to schedule recurring Alipay bill summaries and review spending, income, categories, large transactions, payment methods, and period-over-period changes. The skill is intended for users who have authorized access to their Alipay bill data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled reports may expose sensitive financial information if the schedule, threshold, timezone, or authorization scope is not reviewed.

Mitigation: Confirm report frequency, large-transaction threshold, timezone, and Alipay authorization scope before enabling; edit or disable the cron jobs when automatic reports are not desired.

Risk: Reports depend on authorized Alipay bill data and may be incomplete if access or the dependent bill-query skill is unavailable.

Mitigation: Verify Alipay authorization and call-alipay-service availability before relying on generated summaries.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report text with OpenClaw cron shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recurring reports depend on authorized Alipay bill access and the call-alipay-service skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
