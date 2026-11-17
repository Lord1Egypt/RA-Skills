## Description:

The drivethru-operations skill helps an agent query, analyze, and run controlled purchasing, manufacturing, inventory, replenishment, receiving, shipping, and accounts-payable workflows in Odoo through the drivethru_mcp MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Internal operations employees use this skill to answer Odoo purchasing, manufacturing, inventory, replenishment, receiving, shipping, and scheduled routine-sweep questions. It can also prepare or execute approved operational workflows such as replenishment-to-PO, transfer correction, and PO-to-vendor-bill matching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live ERP data, including purchase orders, stock transfers, and vendor bills.

Mitigation: Require explicit human approval before write workflows and state the exact records, actions, and expected effect before calling write-capable tools.

Risk: The Odoo MCP token can expose operational ERP access if it is broad, leaked, or pointed at an untrusted endpoint.

Mitigation: Use a narrowly scoped token, configure the endpoint only through administrator-controlled environment variables, require HTTPS, and never paste the token into chat.

Risk: Incorrect field choices or paginated result handling can produce misleading operational counts or totals.

Mitigation: Use the documented field dictionary or field-list tools before filtering, take counts from total_matched or server-side aggregates, and report the query method with each number.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-operations)
- [Odoo](https://www.odoo.com)
- [Operations field reference](references/field_reference.md)
- [Operations query patterns](references/query_patterns.md)
- [Drive Thru routines](references/routines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or concise text with optional shell commands and JSON tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query methods, exception summaries, operational recommendations, and approval prompts before write actions.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
