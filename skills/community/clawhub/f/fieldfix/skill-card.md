## Description: <br>
Query and manage your heavy equipment fleet through FieldFix's API. Track machines, log maintenance, monitor expenses, and get AI diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueprintstudioco](https://clawhub.ai/user/blueprintstudioco) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External fleet operators and developers use this skill to let an agent query FieldFix equipment records, review service and expense history, monitor alerts, and submit maintenance, expense, or hour-meter updates through FieldFix's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a FieldFix API key to access fleet records. <br>
Mitigation: Use a dedicated least-privilege API key where possible and keep credentials out of chats, shared logs, and checked-in configuration. <br>
Risk: Write commands can log expenses, service work, or hour-meter changes. <br>
Mitigation: Manually verify any agent-proposed write action before execution, especially updates that affect cost, maintenance, or equipment history. <br>


## Reference(s): <br>
- [FieldFix API Documentation](https://www.fieldfix.ai/api) <br>
- [FieldFix App](https://app.fieldfix.ai) <br>
- [FieldFix MCP Server](https://www.npmjs.com/package/fieldfix-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the FIELDFIX_API_KEY environment variable and can perform read or user-invoked write operations against FieldFix fleet records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
