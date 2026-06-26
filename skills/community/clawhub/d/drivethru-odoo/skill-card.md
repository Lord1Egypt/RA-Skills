## Description: <br>
Talk to an Odoo ERP through its drivethru_mcp MCP server to discover tools at runtime, look up eBay products and inventory, push eBay orders and tracking, run Accounts Payable purchase-order-to-vendor-bill flows, and schedule MRP production batches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers working with a configured Odoo environment use this skill to query ERP records and, after explicit confirmation, execute eBay order, Accounts Payable, purchase order, vendor bill, and production scheduling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Odoo ERP records, including orders, vendor bills, purchase order lines, and production schedules. <br>
Mitigation: Require explicit user confirmation before any write action and state the exact records and changes before calling a write tool. <br>
Risk: ODOO_MCP_TOKEN is a sensitive ERP credential for the configured Odoo MCP server. <br>
Mitigation: Load the token from the environment, never paste it into chat, and prefer the least-privileged token available. <br>
Risk: The available MCP tools and input schemas can vary by Odoo deployment. <br>
Mitigation: Run tool discovery first, inspect the live input schema, and verify that the exposed tools match the intended workflow before making calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmtucker/drivethru-odoo) <br>
- [Odoo](https://www.odoo.com) <br>
- [Odoo agent_api endpoint surface](references/agent_api_endpoints.md) <br>
- [Production scheduling data model](references/production_scheduling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ODOO_MCP_URL and ODOO_MCP_TOKEN; live tool names and input schemas are discovered from the configured MCP server.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
