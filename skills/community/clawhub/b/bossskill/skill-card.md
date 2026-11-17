## Description:

Startup coaching and boss secretary workflow for founders, small business owners, customer follow-up, team management, task review, business diagnosis, and operating checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanfanscoin](https://clawhub.ai/user/fanfanscoin)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, small business owners, sales leaders, and project managers use this skill to turn customer follow-up, team management, task tracking, business diagnosis, and daily review into concrete operating actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Licensed cloud features may send current command inputs, business text, license data, and device identifiers to vendor services.

Mitigation: Use the skill only when that cloud-connected posture is acceptable, and avoid entering unnecessary personal, confidential, or sensitive business data.

Risk: The skill stores local business records, exports, and a reusable license key on the user device.

Mitigation: Protect the SQLite database, generated exports, and license key with normal endpoint, backup, and access controls.

Risk: The security guidance says BOOSKILL_CORE_MODE=local should not be treated as a no-network guarantee without a code fix.

Mitigation: Do not rely on local mode for network isolation; validate network behavior before using it in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanfanscoin/skills/bossskill)
- [Checklists](references/checklists.md)
- [SQLite database reference](references/sqlite-database.md)
- [Task reminder system](references/task-reminder-system.md)
- [Team and customer schemas](references/team-customer-schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and local record/export outputs when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, query, or export a user-selected local SQLite database when the user asks for recordkeeping workflows.]

## Skill Version(s):

1.0.3 (source: ClawHub server release evidence; artifact manifests report 0.2.0-commercial-client)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
