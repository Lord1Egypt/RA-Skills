## Description: <br>
Helps agents send Feishu messages and look up Feishu chats or members through Feishu Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Feishu messaging workflows, look up recipients or group members, and send text messages through a Feishu bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes hardcoded Feishu app credentials. <br>
Mitigation: Remove and rotate the bundled credentials before installation, then provide least-privileged Feishu credentials through environment variables. <br>
Risk: The user-search helper can expose employee directory details in terminal output. <br>
Mitigation: Run user search only for approved lookup tasks and limit access to operators who are allowed to view directory data. <br>
Risk: Message-sending helpers can send content to unintended Feishu recipients. <br>
Mitigation: Confirm the recipient identifier, receive ID type, and message content before executing send commands. <br>


## Reference(s): <br>
- [Feishu Open Platform API documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list) <br>
- [ClawHub skill page](https://clawhub.ai/make453/feishu-messaging-bak2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and Python code examples plus shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, API permissions, and recipient identifiers before real API calls are made.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
