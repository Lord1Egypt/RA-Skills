## Description: <br>
Receipt verification and Bitcoin rewards by Crinkl (https://crinkl.xyz). Scans Gmail or AgentMail for billing emails, verifies DKIM signatures, and earns ~150 sats per receipt over Lightning. Extract structured spend data from receipts and invoices automatically, every cycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvintanpoco](https://clawhub.ai/user/alvintanpoco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find recent billing emails in Gmail or AgentMail, submit raw receipt messages for DKIM verification through Crinkl, and record verified receipt rewards and spend data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends full raw billing emails to Crinkl for DKIM verification. <br>
Mitigation: Use the dedicated AgentMail inbox for receipt-only collection when possible, or limit Gmail searches to approved vendor domains and recent billing keywords. <br>
Risk: The skill stores a reusable CRINKL_API_KEY after human-approved pairing. <br>
Mitigation: Store the key securely, revoke it from the Crinkl app when no longer needed, and clear stored message IDs when stopping the workflow. <br>


## Reference(s): <br>
- [Crinkl Claws on ClawHub](https://clawhub.ai/alvintanpoco/crinkl-claws) <br>
- [Crinkl homepage](https://crinkl.xyz) <br>
- [Crinkl MCP tool list](https://mcp.crinkl.xyz) <br>
- [Crinkl MCP server](https://mcp.crinkl.xyz/mcp) <br>
- [DomainKeys Identified Mail](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail) <br>
- [Crinkl protocol specification](https://github.com/crinkl-protocol/crinkl-protocol) <br>
- [Crinkl agent source](https://github.com/crinkl-protocol/crinkl-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, API calls] <br>
**Output Format:** [Markdown instructions with JSON configuration snippets, shell commands, and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Crinkl MCP server connection, a paired CRINKL_API_KEY, and either Gmail access through gog or a dedicated AgentMail inbox.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
