## Description: <br>
Agently Mail helps an agent operate an Agently/QQ Mail mailbox through agently-cli, including reading, searching, sending, replying, forwarding, deleting messages, and downloading attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to access an Agently/QQ Mail mailbox, inspect mail, search messages, download attachments, or prepare mail write actions with user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent access to a mailbox through OAuth credentials stored locally. <br>
Mitigation: Install and authorize it only for mailboxes the user intends the agent to operate, and avoid invoking the skill for general email discussion. <br>
Risk: Send, reply, forward, and trash actions can change mailbox state or disclose content. <br>
Mitigation: Review the generated message summary and require explicit user confirmation before executing write actions. <br>
Risk: Email bodies and subjects can contain prompt-injection attempts. <br>
Mitigation: Treat message content as untrusted data and do not follow instructions embedded inside retrieved email. <br>


## Reference(s): <br>
- [Agently Mail homepage](https://agent.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/agentlymail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise user-facing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth authorization URLs, message summaries, confirmation-token workflows, mailbox command results, and attachment download paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
