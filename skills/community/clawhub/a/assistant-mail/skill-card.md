## Description: <br>
A skill that allows AI agents to send emails using the AssistantMail API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assistantmail](https://clawhub.ai/user/assistantmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to AssistantMail mailboxes through MCP tools for sending, replying to, listing, reading, and managing mailbox data with API-key authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad mailbox authority, including reading, sending, modifying policies and recipients, and deleting mailboxes or messages. <br>
Mitigation: Use a least-privilege API key where possible and require human approval for sending email, changing policies, managing recipients, or deleting mailbox data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/assistantmail/assistant-mail) <br>
- [AssistantMail app](https://app.assistant-mail.ai) <br>
- [AssistantMail site](https://assistant-mail.ai) <br>
- [AssistantMail API base URL](https://api.assistant-mail.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, API calls] <br>
**Output Format:** [Markdown with JSON examples and MCP configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AssistantMail API key or Cognito JWT and a mailboxId for mailbox operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
