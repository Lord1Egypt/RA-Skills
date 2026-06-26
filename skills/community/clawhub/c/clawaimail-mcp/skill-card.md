## Description: <br>
ClawAIMail MCP Server lets AI agents create inboxes, send and receive email, search messages, manage threads, and inspect account usage through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can connect an AI agent to ClawAIMail so it can manage agent-owned email inboxes, send outbound messages, read and search received messages, and check plan usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send real email from configured inboxes. <br>
Mitigation: Require human approval for send_email and use a dedicated low-privilege API key when available. <br>
Risk: The agent can read mailbox contents and search messages. <br>
Mitigation: Avoid connecting sensitive or compliance-critical mailboxes unless this access is explicitly intended. <br>
Risk: The agent can delete inboxes and all their messages. <br>
Mitigation: Require human approval for delete_inbox before execution. <br>
Risk: A custom CLAWAIMAIL_BASE_URL can direct credentials and mail operations to an untrusted server. <br>
Mitigation: Use the default API endpoint or only set CLAWAIMAIL_BASE_URL to a server you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joansongjr/clawaimail-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/joansongjr) <br>
- [ClawAIMail website](https://clawaimail.com) <br>
- [ClawAIMail API documentation](https://clawaimail.com/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, configuration, guidance] <br>
**Output Format:** [MCP tool responses as text containing formatted JSON, plus setup configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWAIMAIL_API_KEY and uses the configured ClawAIMail API base URL.] <br>

## Skill Version(s): <br>
0.2.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
