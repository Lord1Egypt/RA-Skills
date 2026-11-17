## Description:

Pre-defined business workflows combining multiple MCP tools for CRM, sales, purchase, inventory, project, payments, and utility tasks in ERPNext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravana-indus](https://clawhub.ai/user/ravana-indus)

### License/Terms of Use:

MIT

## Use Case:

ERPNext teams and agent developers use this skill to trigger repeatable business workflows for CRM, sales, purchase, inventory, project, payment, search, and bulk record operations. It requires a Frappe/ERPNext environment and the bc_mcp module.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, submit, cancel, delete, export, and run custom methods on ERP business records with broad authority.

Mitigation: Install it only for tightly controlled ERPNext accounts with least-privilege roles and require human review before record-changing, payment, stock, export, and custom-method operations.

Risk: The generic_task and bulk_operation workflows can operate across DocTypes with weak scoping.

Mitigation: Enable those workflows only when the runtime enforces DocType allowlists, field and method allowlists, non-empty filters, dry runs, audit logs, and confirmation gates.

## Reference(s):

- [Artifact skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/ravana-indus/skills/erpnext-frappe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command examples, plus ERPNext workflow output templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow definitions and execution guidance for ERPNext/Frappe MCP operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
