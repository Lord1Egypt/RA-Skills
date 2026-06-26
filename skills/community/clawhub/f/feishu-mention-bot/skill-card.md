## Description: <br>
飞书群聊中 @机器人并发送消息。当用户需要在飞书群里艾特机器人、通知其他机器人、或让机器人之间互相通信时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcjinglang](https://clawhub.ai/user/pcjinglang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
开发者和自动化运维人员使用该技能在飞书群聊中按正确格式 @机器人并发送消息，支持机器人通知、机器人间通信和相关 API 调用准备。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app secrets and tenant access tokens can be exposed through logs, shell history, or shared files. <br>
Mitigation: Use a least-privilege Feishu app and keep app_secret and tenant tokens out of logs and shared files. <br>
Risk: Message-history queries can expose sensitive chat content or mention metadata. <br>
Mitigation: Query message history only in chats where the operator has authorization and limit use to the bot open_id lookup task. <br>
Risk: Incorrect CHAT_ID or open_id values can send messages to the wrong chat or mention the wrong bot. <br>
Mitigation: Confirm CHAT_ID and open_id values before sending any Feishu message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcjinglang/feishu-mention-bot) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message history API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=CHAT_ID&page_size=50) <br>
- [Feishu send message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and API JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; examples require caller-supplied Feishu app credentials, chat IDs, and bot open_ids.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
