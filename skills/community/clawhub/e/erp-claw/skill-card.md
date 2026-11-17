## Description:

ERP Claw is an AI-native ERP agent skill for local accounting, invoicing, inventory, purchasing, tax, billing, HR, payroll, advanced accounting, financial reporting, and module management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

MIT

## Use Case:

Business operators, finance teams, HR/payroll staff, and developers use this skill to manage a local ERP database, run accounting and operational workflows, generate reports, and configure industry or regional modules through agent-invoked commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad authority over local ERP, accounting, payroll, HR, and related business data.

Mitigation: Install only in environments where that level of local data access is acceptable, restrict filesystem and database access, and review high-impact accounting, payroll, HR, restore, schema, cron, and deployment actions before execution.

Risk: Module and dashboard setup can run mutable remote code without strong integrity controls.

Mitigation: Avoid production module updates and dashboard setup until the remote repositories have been reviewed and pinned, and keep verified backups before enabling those workflows.

## Reference(s):

- [ERP Claw ClawHub listing](https://clawhub.ai/mailnike/skills/erp-claw)
- [OpenClaw](https://openclaw.org)
- [ERPClaw website](https://www.erpclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on a local SQLite ERP database and may create business records, reports, backups, schedules, or installed modules.]

## Skill Version(s):

3.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
