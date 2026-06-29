## Description: <br>
Swedish double-entry bookkeeping via Accounted (app.gnubok.se), covering bank transaction categorization, invoicing, VAT, payroll, reports, and month-end close with staged human approval for writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattssonn](https://clawhub.ai/user/mattssonn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and small-business operators use this skill to connect an OpenClaw agent to Accounted/Gnubok for Swedish bookkeeping workflows such as categorizing bank transactions, creating invoices, preparing VAT reports, and closing accounting periods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Swedish bookkeeping data and may request accounting write scopes. <br>
Mitigation: Use hosted OAuth or a sandbox/test key first, grant only required scopes, and review every staged operation preview before approval. <br>
Risk: Incorrect approvals could affect invoices, VAT filings, payroll, reports, or accounting period close workflows. <br>
Mitigation: Confirm the company, period, amounts, and Swedish jurisdiction before approving operations, especially high-risk Skatteverket submissions. <br>
Risk: API keys or OAuth grants can expose financial-system access if over-scoped or mishandled. <br>
Mitigation: Prefer hosted OAuth when possible, keep grants read-only by default, and add write scopes only for the specific workflow being performed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mattssonn/accounted) <br>
- [Accounted OpenClaw homepage](https://github.com/erp-mafia/accounted-openclaw) <br>
- [Accounted](https://app.gnubok.se) <br>
- [Connect with Claude / MCP docs](https://app.gnubok.se/docs/api/connect-claude) <br>
- [gnubok-mcp package](https://www.npmjs.com/package/gnubok-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides MCP setup and staged accounting workflows; write operations require user review and approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
