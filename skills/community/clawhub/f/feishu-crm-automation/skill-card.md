## Description:

Automates Feishu CRM workflows for customer entry, overdue follow-up reminders, and weekly customer summary reports using Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanderen](https://clawhub.ai/user/wanderen)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to record customer details in Feishu Bitable, identify customers overdue for follow-up, and generate weekly CRM summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a specific Feishu Bitable destination that could route customer data to the wrong table.

Mitigation: Before use, replace the embedded table configuration with an approved organization-owned Feishu table or confirm the listed table belongs to the intended organization.

Risk: The skill can read and write customer contact details and sales records.

Mitigation: Require user confirmation before reading, creating, or updating CRM records, especially when processing customer contact information.

## Reference(s):

- [Follow-up Reminder Logic](references/跟进提醒逻辑.md)
- [Weekly Report Logic](references/周报生成逻辑.md)
- [ClawHub Skill Page](https://clawhub.ai/wanderen/skills/feishu-crm-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown or plain text responses with Feishu Bitable operation guidance and CRM summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer records, overdue follow-up lists, weekly CRM metrics, and Feishu Bitable field mappings.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
