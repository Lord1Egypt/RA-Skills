## Description: <br>
Give your AI agent a real email address. Send, receive, and manage emails via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Clawaimail to give agents a real email inbox, send and receive messages, search mail, inspect account usage, and manage inboxes through MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real send and delete authority over a ClawAIMail account. <br>
Mitigation: Use a dedicated limited API key and require human approval before sending email or deleting inboxes. <br>
Risk: Some ordinary-looking actions can create a remote inbox as a side effect when no inbox_id is provided. <br>
Mitigation: Pass explicit inbox IDs where possible and review tool call parameters before execution. <br>
Risk: Running the package without verifying the source can expose an email account API key to untrusted code. <br>
Mitigation: Verify the npm package and version before running it, and rotate the API key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/joansongjr/clawaimail) <br>
- [ClawAIMail API documentation](https://clawaimail.com/docs/) <br>
- [ClawAIMail website](https://clawaimail.com) <br>
- [npm package: clawaimail-mcp](https://www.npmjs.com/package/clawaimail-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration] <br>
**Output Format:** [MCP tool responses containing JSON serialized as text, plus setup configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWAIMAIL_API_KEY; tools can send email, read and search messages, delete inboxes, and may auto-create a default inbox when inbox_id is omitted.] <br>

## Skill Version(s): <br>
0.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
