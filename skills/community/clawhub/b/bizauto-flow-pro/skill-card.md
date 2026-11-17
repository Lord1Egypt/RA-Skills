## Description:

业务自动化师(专业版) helps agents audit, design, implement, monitor, and optimize enterprise business automations with event-driven workflows, human approval gates, multi-system synchronization, fault-tolerance planning, and ROI reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations teams, automation engineers, and developers use this skill to identify high-value workflows, design approval-aware automations, plan integrations across business systems, and generate implementation guidance such as cron schedules, workflow configuration, monitoring plans, and remediation checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward broad execution and write actions for business automation workflows.

Mitigation: Require explicit user confirmation before creating cron jobs, writing files, calling APIs, sending messages, updating business systems, or touching payments and production data.

Risk: Loose or mismatched trigger text may cause the skill to activate outside business automation tasks.

Mitigation: Remove the unrelated UI/design trigger language before use and limit activation to business automation planning and implementation requests.

Risk: Automation workflows may involve credentials or external system access.

Mitigation: Keep credentials in scoped environment variables or approved secret storage and review proposed integrations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bizauto-flow-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline text, YAML, bash, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron schedules, API calls, approval workflows, monitoring metrics, troubleshooting steps, and ROI summaries for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
