## Description: <br>
费用催缴管理 helps property and enterprise-service teams classify overdue fees, generate collection reminders and reports, and send WeCom notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property-management and enterprise-service staff use this skill to review fee collection data, calculate overdue tiers, create customer-facing reminder language, and prepare daily or monthly collection reports. When configured, it can send reminders through WeCom for routine and escalated collection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive billing and customer data may be read from the configured fee data source and included in generated reminders or reports. <br>
Mitigation: Use only approved fee data sources, restrict file access to authorized staff, and define retention or deletion rules for generated report files. <br>
Risk: Automated WeCom sends, especially escalated group or @all reminders, can notify the wrong audience or expose billing details too broadly. <br>
Mitigation: Configure only approved webhook destinations, verify group IDs before use, and require dry-run or manual approval for bulk and @all sends. <br>
Risk: Local report files can persist fee totals and overdue customer counts after the collection workflow completes. <br>
Mitigation: Store reports in an access-controlled location and apply the organization's retention, audit, and deletion policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/fee-collection) <br>
- [Reference Documentation for Fee Collection](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, API Calls, Configuration guidance] <br>
**Output Format:** [Chinese text and Markdown reminders, JSON reports, and WeCom webhook payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local report files and send configured WeCom notifications, including escalated group reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
