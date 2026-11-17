## Description:

Connects an agent to an Odoo ERP through the drivethru_mcp MCP server for inventory and order lookup, Accounts Payable workflows, document-backed PO pricing review, production scheduling, replenishment purchasing, and permission-scoped Knowledge base retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations agents use this skill to read from and write to Odoo during Odoo Discuss support, order management, purchasing, Accounts Payable, production scheduling, replenishment, document review, and internal SOP lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad live ERP access can read or change orders, bills, production schedules, purchasing, inventory, documents, and internal knowledge.

Mitigation: Install only for agents and users that should have broad Odoo authority; prefer least-privilege or read-only credentials where possible.

Risk: The security evidence says business-changing safeguards rely mostly on agent instructions rather than technical locks.

Mitigation: Require explicit dry-run behavior or user approval before live writes, and verify the attached drivethru_mcp server and any vendor checkout skills separately.

Risk: ERP, customer, vendor, or internal knowledge data may be sensitive.

Mitigation: Avoid echoing customer PII or sensitive ERP data into chat unless necessary for the task.

## Reference(s):

- [Odoo](https://www.odoo.com)
- [Odoo agent_api endpoint surface](references/agent_api_endpoints.md)
- [Document-driven PO pricing review](references/po_pricing_review.md)
- [Production scheduling data model](references/production_scheduling.md)
- [Replenishment vendor purchasing](references/replenishment_purchasing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON examples and shell commands; helper scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ODOO_MCP_URL and ODOO_MCP_TOKEN for MCP access; several workflows can perform live Odoo writes after confirmation.]

## Skill Version(s):

0.9.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
