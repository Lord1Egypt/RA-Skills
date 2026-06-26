## Description: <br>
Manage Feishu (Lark) group chats using natural language, including adding or removing group members, listing groups or members, sending messages, renaming groups, and creating new groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinzeny](https://clawhub.ai/user/vinzeny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and Feishu administrators use this skill to manage Feishu group chats through natural language requests while the agent resolves groups, users, permissions, and required confirmations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill exposes a raw Feishu tenant access token. <br>
Mitigation: Treat token output as a secret, avoid sharing it with the user or logs, and refresh or discard it after the current operation. <br>
Risk: The security review reports broad tenant-level authority for Feishu group operations. <br>
Mitigation: Install only for trusted Feishu administrators, use a tightly scoped Feishu app, and verify required permissions before use. <br>
Risk: Write operations can add or remove members, send messages, rename groups, or create groups. <br>
Mitigation: Confirm the exact user, group, message, or group name with the requester before executing any write action. <br>
Risk: Write actions use SkillPay billing and may share billing identifiers with that service. <br>
Mitigation: Explain billing before retrying payment-required actions and wait for the user to top up or approve continuation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vinzeny/feishu-group-ops) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions require explicit user confirmation and may return payment-required JSON before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
