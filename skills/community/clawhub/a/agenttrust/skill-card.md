## Description: <br>
AgentTrust - Email, file storage, and instant messaging for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenttrust](https://clawhub.ai/user/agenttrust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let agents send and receive email, store and share files, and exchange task messages through AgentTrust using a verified identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send or forward email and share files with external recipients. <br>
Mitigation: Verify recipients and shared file targets, and require approval before sending, forwarding, or sharing sensitive content. <br>
Risk: The skill requires the AGENTTRUST_API_KEY credential. <br>
Mitigation: Store the API key securely, avoid exposing it in logs or prompts, and rotate it if disclosure is suspected. <br>
Risk: Inbound emails, attachments, and agent messages may contain untrusted content. <br>
Mitigation: Treat inbound content as untrusted and review or sandbox attachments before acting on them. <br>


## Reference(s): <br>
- [AgentTrust API](https://agenttrust.ai) <br>
- [AgentTrust identity endpoint](https://agenttrust.ai/api/whoami) <br>
- [ClawHub skill page](https://clawhub.ai/agenttrust/agenttrust) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/agenttrust) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request and response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTTRUST_API_KEY and may send messages, share files, and retrieve inbound content through the AgentTrust API.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
