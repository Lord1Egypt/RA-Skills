## Description: <br>
Access Credit Karma transaction data via MCP for transaction syncing, spending analysis, merchant and category summaries, account summaries, and local financial-data queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure an agent for Credit Karma transaction access, sync data into a local SQLite database, and answer explicit personal-finance questions about spending, merchants, categories, accounts, and transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to expose live Credit Karma session cookies. <br>
Mitigation: Treat CK_COOKIES and copied Cookie headers like passwords, avoid storing them in plain .env files when possible, and use the skill only for explicit Credit Karma requests. <br>
Risk: The skill syncs private transaction data into a local SQLite database. <br>
Mitigation: Confirm where the SQLite database is written, restrict local file access, and remove stored data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/creditkarma-mcp) <br>
- [creditkarma-mcp npm package](https://www.npmjs.com/package/creditkarma-mcp) <br>
- [creditkarma-mcp source link from skill docs](https://github.com/chrischall/creditkarma-mcp) <br>
- [fetchproxy extension](https://github.com/chrischall/fetchproxy) <br>
- [Credit Karma](https://www.creditkarma.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, SQL queries, MCP tool calls] <br>
**Output Format:** [Markdown with JSON, bash, SQL, and MCP tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing setup and usage guidance for accessing sensitive Credit Karma financial data through a registered MCP server.] <br>

## Skill Version(s): <br>
2.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
