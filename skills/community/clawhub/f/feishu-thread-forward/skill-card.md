## Description: <br>
Forwards Feishu threads or topics to a user, group, or another topic through the Feishu Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to forward a Feishu topic or thread to another chat, user, or topic while preserving thread context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forwarding a Feishu thread can reveal thread context to the wrong recipient. <br>
Mitigation: Confirm the source thread, recipient ID, recipient type, group sensitivity, and sharing appropriateness before each use. <br>
Risk: The script uses Feishu app secrets and tenant access tokens. <br>
Mitigation: Keep credentials and tenant tokens out of chat, logs, and screenshots, and grant the bot only the permissions it needs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deadblue22/feishu-thread-forward) <br>
- [Feishu thread forward API](https://open.feishu.cn/open-apis/im/v1/threads/{thread_id}/forward?receive_id_type={type}) <br>
- [Feishu message retrieval API](https://open.feishu.cn/open-apis/im/v1/messages/{message_id}) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and a Python script that prints JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu bot credentials from local OpenClaw configuration and requires Feishu thread and recipient identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
