## Description:

Use this skill when the user asks about invoices, e-invoices per Nghi dinh 70, revenue or expense statistics, VAT, or other accounting tasks for a Vietnamese shop or micro company.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joy](https://clawhub.ai/user/joy)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and their agents use this skill to manage FinOne / Vbill invoices, publish e-invoices, review revenue and expense statistics, update VAT or product data, and sync Xbillstore invoices for Vietnamese shops and micro companies.

### Deployment Geography for Use:

Vietnam

## Known Risks and Mitigations:

Risk: The skill performs sensitive merchant accounting actions through a header-less MCP service that relies on a user-supplied FinOne user ID.

Mitigation: Use only with independent FinOne server-side authentication and authorization, and validate the active user ID before running account-specific tools.

Risk: Shared-agent deployments can expose or reuse the wrong merchant account binding.

Mitigation: Isolate memory per user or confirm the active FinOne user ID at session start before calling FinOne tools.

Risk: Deletion, product or VAT changes, sync, and official e-invoice publication can affect financial records or create irreversible outcomes.

Mitigation: Require explicit user confirmation for these actions, preview e-invoices before publication, and avoid defaulting missing invoice or VAT values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joy/skills/finone)
- [Publisher profile](https://clawhub.ai/user/joy)
- [FinOne MCP server endpoint](https://api-uat.vbill.vn/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown responses with MCP tool calls and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FinOne user ID for every tool call and explicit user confirmation before irreversible e-invoice publication.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
