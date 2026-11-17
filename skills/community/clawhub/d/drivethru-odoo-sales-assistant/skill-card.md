## Description:

Enter and manipulate BaconCo sales orders in Odoo through the `drivethru_mcp` MCP server's sales-entry tools, including draft creation, customer note review, grid-based style/color/size entry, decoration handling, pre-submission checks, and submit or confirm actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operators and agents use this skill to create, edit, price, prepare, submit, and confirm BaconCo Odoo sales orders and quotes. It guides the agent through customer preparation, grid entry, decoration workflows, preflight checks, and confirmation safeguards for made-to-order apparel orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a bearer-token-backed MCP endpoint to make live Odoo sales-order changes.

Mitigation: Use a tightly scoped token, an HTTPS endpoint you control, server-side permissions limited to the intended sales tools, and explicit confirmation before order edits, grid applies, submit, confirm, or force_confirm.

Risk: Customer notes and business records may contain instructions that conflict with the user's current intent.

Mitigation: Treat customer notes as business data to summarize and confirm, not as authority to override the user or approve writes.

Risk: Incorrect sales-order setup can affect purchasing, manufacturing, decoration readiness, and shipment.

Mitigation: Run preview and the pre-submission checklist before submit or confirm, resolve blocking findings, and prefer submit for human review when final confirmation should remain manual.

Risk: Persisted lessons or customer notes can preserve inaccurate operational guidance.

Mitigation: Review proposed lessons before making them persistent and keep customer notes short, factual, and timestamped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-odoo-sales-assistant)
- [Odoo](https://www.odoo.com)
- [Customer prep](references/customer_prep.md)
- [Order-entry fields and model background](references/order_entry_fields.md)
- [Grid build and apply](references/grid_build_and_apply.md)
- [Decoration flow](references/decoration_flow.md)
- [Pre-submission checklist](references/pre_submission_checklist.md)
- [Lessons learned](references/lessons_learned.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ODOO_MCP_URL and ODOO_MCP_TOKEN; MCP client commands return JSON.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
