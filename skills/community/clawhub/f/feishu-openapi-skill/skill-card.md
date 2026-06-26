## Description: <br>
Operate Feishu or Lark IM APIs through UXC with a curated OpenAPI schema, tenant-token bearer auth, and chat/message guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run Feishu or Lark IM chat lookup, message read, message send, reply, upload, user lookup, and bot event intake workflows through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read chats and messages, resolve users, send messages, reply to messages, and upload files through a Feishu or Lark bot app. <br>
Mitigation: Use least-privilege app permissions and require human confirmation before sends, replies, uploads, or other write operations. <br>
Risk: Credentials and subscription sinks can expose tenant access or captured inbound messages if handled carelessly. <br>
Mitigation: Store secrets in environment-backed credential storage, avoid inline secrets in shell commands, and protect or rotate files that capture inbound events. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/feishu-im.openapi.json) <br>
- [Feishu Open Platform docs](https://open.feishu.cn/document/) <br>
- [Lark Open Platform docs](https://open.larksuite.com/document/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide authenticated UXC calls and may lead an agent to read chats, send messages, upload files, or store inbound event records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
