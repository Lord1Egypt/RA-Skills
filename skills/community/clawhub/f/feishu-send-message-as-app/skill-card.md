## Description: <br>
Send Feishu IM messages as a Feishu app or bot identity using an app access token, with support for text, image, post, card, and other Feishu message types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkzleond](https://clawhub.ai/user/jkzleond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send Feishu messages that appear from a configured app or bot rather than an individual user. It is intended for workflows that need app-authenticated Feishu message delivery to users or group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately send Feishu messages as the configured app or bot using app credentials. <br>
Mitigation: Use a dedicated Feishu app with minimal permissions, restrict allowed recipients where possible, and review recipient IDs, message type, and content before each send. <br>
Risk: The skill reads appId and appSecret from openclaw.json. <br>
Mitigation: Protect openclaw.json with strict file permissions and avoid exposing Feishu app credentials in chat, logs, or shared workspaces. <br>
Risk: The skill stores a reusable Feishu app token in a shared temporary cache path. <br>
Mitigation: Use the skill only on trusted hosts, lock down cache-file permissions where possible, and delete the token cache after sensitive sessions or on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkzleond/feishu-send-message-as-app) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script output is a single message_id line.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu app credentials from openclaw.json, obtains an app access token, and sends a message through Feishu's IM API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
