## Description: <br>
Feishu Proactive Messenger lets agents send proactive Feishu text messages through Feishu OpenAPI when the normal channel only supports replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziwenwang28](https://clawhub.ai/user/ziwenwang28) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to send outbound Feishu text messages from the correct configured bot, especially in multi-agent OpenClaw workflows where a passive Feishu channel cannot initiate a conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A trusted agent could accidentally send a message to a configured default recipient. <br>
Mitigation: Review each account's defaultTo target and prefer explicit --agent and --receive-id values for sensitive sends. <br>
Risk: Message text is sent outbound to Feishu and may include confidential content if provided by the agent. <br>
Mitigation: Avoid passing secrets or confidential content as message text unless that outbound message is intended. <br>
Risk: The skill uses local OpenClaw Feishu app credentials to obtain a tenant access token and send messages. <br>
Mitigation: Limit access to the OpenClaw configuration file, scope Feishu bot permissions appropriately, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ziwenwang28/feishu-proactive-messenger) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu send message endpoint](https://open.feishu.cn/open-apis/im/v1/messages) <br>
- [Feishu bot info endpoint](https://open.feishu.cn/open-apis/bot/v3/info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI status text and markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send a Feishu message through configured credentials and returns a concise delivery result.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
