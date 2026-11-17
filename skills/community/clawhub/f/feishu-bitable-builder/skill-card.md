## Description:

Helps agents design, build, automate, and hand off Feishu Bitable systems from business requirements, including table schemas, fields, views, workflows, dashboards, permissions, and supporting documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[664624249](https://clawhub.ai/user/664624249)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and business system builders use this skill to turn CRM, project management, inventory, task tracking, and data-collection requirements into Feishu Bitable app structures, automations, dashboards, and handoff materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to build or modify Feishu Bitable systems with tenant, app, user, and permission changes.

Mitigation: Confirm the target Feishu tenant, app, users, and exact permission changes before execution.

Risk: The source asks the bot to retain edit access after handoff.

Mitigation: Remove bot edit access after delivery unless time-limited support access is explicitly approved.

Risk: Automations may delete data, approve purchases, send customer messages, or export data outside Feishu.

Mitigation: Review high-impact automations before activation and limit payloads to the necessary fields.

Risk: Bitable systems may contain sensitive business, customer, or operational data.

Mitigation: Use least-privilege access, field-level permissions, backups, audit logs, and export review for sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/664624249/skills/feishu-bitable-builder)
- [Feishu Bitable field type reference](references/field-types.md)
- [Feishu Bitable view type guide](references/view-types.md)
- [Feishu Bitable automation and workflow guide](references/automation.md)
- [Feishu Bitable dashboard design guide](references/dashboard.md)
- [Feishu Bitable function guide](references/functions.md)
- [Feishu Bitable best practices](references/best-practices.md)
- [Feishu Bitable application scenarios](references/scenarios.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Markdown, Code]

**Output Format:** [Markdown with structured checklists, API/tool call examples, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu app, table, field, view, automation, permission, dashboard, and handoff specifications.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
