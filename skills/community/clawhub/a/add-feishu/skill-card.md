## Description: <br>
Add Feishu (Lark) as a channel. Uses WebSocket long connection -- no public URL or ngrok needed. Works alongside WhatsApp, Telegram, Slack, or as a standalone channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[will-17173](https://clawhub.ai/user/will-17173) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add a Feishu or Lark messaging channel to NanoClaw, configure bot credentials, register chats, and verify message handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration uses Feishu app credentials and persistent bot access to chats. <br>
Mitigation: Use a dedicated Feishu app, keep FEISHU_APP_ID and FEISHU_APP_SECRET out of version control, and add the bot only to trusted chats. <br>
Risk: Group registrations can allow broad chat access when trigger checks are disabled. <br>
Mitigation: Prefer trigger-required group registrations unless everyone in the chat should be able to invoke the assistant. <br>
Risk: Setup may use an incorrect chat identifier if the documented prefix differs from the implemented channel identifier. <br>
Mitigation: Verify the JID prefix during setup before registering a chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/will-17173/add-feishu) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Lark Open Platform](https://open.larksuite.com) <br>
- [Feishu bot info API](https://open.feishu.cn/open-apis/bot/v3/info) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and TypeScript snippets plus skill package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deterministic NanoClaw channel code changes and setup instructions for Feishu credentials, chat registration, validation, troubleshooting, and removal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
