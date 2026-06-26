## Description: <br>
FinOne Accounting (VN Merchants) helps agents support Vietnamese merchants with FinOne / Vbill invoice CRUD, official e-invoice publication, revenue and expense statistics, VAT and product updates, and Xbill sync through the FinOne MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joy](https://clawhub.ai/user/joy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Vietnamese shop owners and micro-company operators use this skill through an agent to create, review, publish, view, and delete invoices, report revenue and expense statistics, manage VAT and product settings, and sync Xbillstore invoices in FinOne / Vbill. <br>

### Deployment Geography for Use: <br>
Vietnam <br>

## Known Risks and Mitigations: <br>
Risk: Remote accounting actions can modify real financial records through a service keyed by a remembered userId. <br>
Mitigation: Use trusted, non-shared sessions, confirm the active merchant userId before use, and verify the user binding before running sensitive actions. <br>
Risk: Publishing e-invoices, deleting invoices, syncing Xbill data, and changing product price or VAT settings can have business or compliance impact. <br>
Mitigation: Require explicit user approval before these operations, preview e-invoices before publication, and do not proceed when required invoice values are missing or zero. <br>
Risk: The FinOne MCP endpoint is header-less and each tool call relies on a numeric userId. <br>
Mitigation: Install only after trusting the FinOne/Vbill endpoint and verifying that the server enforces authorization beyond the supplied userId. <br>


## Reference(s): <br>
- [FinOne ClawHub release page](https://clawhub.ai/joy/finone) <br>
- [JOY publisher profile](https://clawhub.ai/user/joy) <br>
- [FinOne MCP server endpoint](https://api-uat.vbill.vn/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with structured tables, links, and configuration snippets; MCP tool calls use JSON-shaped arguments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FinOne userId for each tool call and explicit approval before irreversible or financially sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
