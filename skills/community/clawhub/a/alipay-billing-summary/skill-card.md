## Description: <br>
支付宝账单自动汇总服务，支持周报、月报、年报三种周期。触发词：账单汇总、每周账单、每月账单、年度账单、消费分析、账单报告、账单周报、账单月报。当用户需要定期查看账单汇总、消费分析报告时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1148260649](https://clawhub.ai/user/1148260649) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who have authorized Alipay data access use this skill to create scheduled weekly, monthly, and annual bill summary reports with spending, income, category, payment-method, large-transaction, and comparison analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Alipay financial data and produces recurring financial reports. <br>
Mitigation: Enable it deliberately, choose only the reporting periods needed, and keep generated reports private. <br>
Risk: Scheduled cron jobs may continue producing reports after the user no longer wants automated summaries. <br>
Mitigation: Track the created OpenClaw cron jobs and remove them when billing summaries should stop. <br>
Risk: The skill depends on a separate Alipay data-access skill for bill data. <br>
Mitigation: Install only when that dependency is trusted and the Alipay authorization state is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1148260649/alipay-billing-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with OpenClaw cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recurring weekly, monthly, and annual billing-summary task definitions; depends on authorized Alipay data access through call-alipay-service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
