## Description: <br>
Accounts Payable Agent helps an agent process supplier payments, contractor invoices, and recurring bills across crypto, fiat, and stablecoin payment rails through MCP-integrated workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihangmissu](https://clawhub.ai/user/lihangmissu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators and agent builders use this skill to coordinate accounts payable workflows, including invoice checks, payment routing, audit records, and escalation for payments that exceed configured approval limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to let an agent participate in real payment workflows. <br>
Mitigation: Use sandbox credentials first, restrict API keys with hard spend limits and recipient allowlists, and require explicit human approval before live payments. <br>
Risk: Payment requests may arrive from other agents or workflows. <br>
Mitigation: Authenticate inter-agent payment requests and keep controlled audit logs for every invoice, recipient, amount, payment rail, timestamp, and status. <br>
Risk: The skill relies on an external MCP payment package for payment execution. <br>
Mitigation: Verify and pin the AgenticBTC MCP package before connecting live accounts. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/lihangmissu/accounts-payable-agent) <br>
- [AgenticBTC MCP Documentation](https://agenticbtc.io) <br>
- [agenticbtc-mcp npm Package](https://www.npmjs.com/package/agenticbtc-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash, JSON, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to call AgenticBTC payment APIs; live deployment requires external credentials, approval controls, and audit logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
