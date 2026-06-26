## Description: <br>
Pre-defined business workflows combine MCP tools for CRM, sales, purchase, inventory, project, payments, and utility tasks in ERPNext. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ravana-indus](https://clawhub.ai/user/Ravana-indus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
ERPNext operators, developers, and business teams use this skill to execute repeatable ERP workflows such as creating customers, quotations, sales orders, purchase orders, stock entries, payments, projects, and bulk record operations through an MCP-enabled Frappe environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad, high-impact ERP record changes, including create, update, delete, import, export, submit, cancel, and payment actions. <br>
Mitigation: Install only with a trusted ERPNext/MCP server and a least-privileged ERP account; require previews and explicit confirmation for update, delete, export, import, submit, cancel, and payment actions. <br>
Risk: The generic_task and bulk_operation workflows have limited scoping and can target many DocTypes. <br>
Mitigation: Restrict or disable generic_task and bulk_operation before production use, and add DocType and method allowlists. <br>
Risk: Incorrect workflow inputs could create or submit inaccurate financial, inventory, sales, purchase, or project records. <br>
Mitigation: Verify backups and audit logging are enabled, and keep business guardrails such as credit checks, stock validation, amount limits, and batch-size limits active. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Ravana-indus/erpnext-frappe) <br>
- [Publisher profile](https://clawhub.ai/user/Ravana-indus) <br>
- [Business Claw Skills documentation](artifact/SKILL.md) <br>
- [Skill definitions](artifact/definitions/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Structured workflow results and formatted status messages from ERPNext/Frappe MCP actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted Frappe/ERPNext environment and the bc_mcp module for tool routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact definition versions) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
