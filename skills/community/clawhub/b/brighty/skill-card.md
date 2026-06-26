## Description: <br>
Banking interface for AI bots and automation. Get a bank account, issue a Mastercard, buy and sell crypto, send payments and invoices via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maay](https://clawhub.ai/user/Maay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, automation builders, and Brighty business or freelance account owners use this skill to connect an agent to Brighty banking workflows, including account lookup, card operations, crypto exchange, payouts, invoices, and team management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an unpinned remote MCP server from the Maay/brighty_mcp repository. <br>
Mitigation: Install only from a trusted Brighty publisher and repository, and prefer a pinned, reviewed MCP server version before use. <br>
Risk: The Brighty API key can enable money movement and account management. <br>
Mitigation: Use the least-privileged API token available, keep it in environment configuration only, keep it out of chat and memory, and monitor account activity. <br>
Risk: Payments, transfers, card changes, account termination, and team-management actions can have direct financial or access-control impact. <br>
Mitigation: Require explicit user confirmation before every payment, transfer, card, account, or team-management action, with amounts and recipients shown clearly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Maay/brighty) <br>
- [Brighty MCP Server Repository](https://github.com/Maay/brighty_mcp) <br>
- [Brighty API Documentation](https://apidocs.brighty.app/docs/api/brighty-api) <br>
- [Brighty Business Portal](https://business.brighty.app/auth?signup=true) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and BRIGHTY_API_KEY; banking, payment, card, account, and team-management actions should be confirmed explicitly before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
