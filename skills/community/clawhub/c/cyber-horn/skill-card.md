## Description: <br>
Turn text into spoken Feishu (Lark) voice messages. Use when the agent should speak in a Feishu group, send voice alerts or announcements, or reply with a playable voice note instead of text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Richerlv](https://clawhub.ai/user/Richerlv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to turn supplied text into Feishu voice messages for group announcements, alerts, or voice-note replies. It is intended for Feishu or Lark workspaces where app credentials and a target chat are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supplied text is sent to an external TTS provider and the generated audio is uploaded to Feishu. <br>
Mitigation: Use the skill only for content approved for those provider data flows, and avoid secrets or regulated content unless the workspace has approved them. <br>
Risk: Feishu and ElevenLabs credentials grant access to external services. <br>
Mitigation: Use narrowly scoped credentials and protect FEISHU_APP_SECRET and ELEVEN_API_KEY in environment storage. <br>
Risk: A default chat ID can route generated voice messages to the wrong destination. <br>
Mitigation: Verify FEISHU_DEFAULT_CHAT_ID before relying on it, or pass the intended receive ID explicitly. <br>


## Reference(s): <br>
- [Cyber Horn on ClawHub](https://clawhub.ai/Richerlv/cyber-horn) <br>
- [Richerlv ClawHub profile](https://clawhub.ai/user/Richerlv) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message create API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Audio, API Calls, Files, Text] <br>
**Output Format:** [Feishu voice message with generated Opus audio and CLI status or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, ffmpeg, and either Edge TTS or optional ElevenLabs credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
