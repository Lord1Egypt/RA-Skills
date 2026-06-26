## Description: <br>
Enables an AI assistant to turn text into NoizAI-generated OPUS audio and send it as a playable Feishu voice message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anightmare2](https://clawhub.ai/user/Anightmare2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to generate voice greetings, announcements, reminders, stories, or chat messages from text and deliver them into Feishu chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real voice messages to a Feishu chat. <br>
Mitigation: Verify FEISHU_CHAT_ID before sending and use --no-send when testing audio generation. <br>
Risk: Feishu and NoizAI credentials are required for normal operation. <br>
Mitigation: Keep FEISHU_APP_SECRET and NOIZ_API_KEY in environment variables or a secrets manager, and avoid writing them to files or logs. <br>
Risk: Text sent to the skill is processed by external Feishu and NoizAI services. <br>
Mitigation: Avoid sensitive or regulated content unless those providers are approved for the intended data. <br>
Risk: The included cron example can create recurring automated messages. <br>
Mitigation: Use scheduled sends only when recurring messages are intended and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anightmare2/feishu-voice-skill) <br>
- [Feishu Voice Skill API reference](reference.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [NoizAI API keys](https://developers.noiz.ai/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated OPUS audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu and NoizAI credentials from environment variables; can generate audio without sending when run with --no-send.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and clawhub.yaml; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
