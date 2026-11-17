## Description:

Feishu Voice Skill lets an agent turn text into NoizAI-generated speech, convert it to OPUS audio, and send it as a playable Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anightmare2](https://clawhub.ai/user/anightmare2)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to generate short voice greetings, alerts, announcements, and conversational updates, then deliver them into Feishu chats as native audio messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text is sent to NoizAI and generated audio is sent to Feishu.

Mitigation: Avoid sensitive or regulated content, confirm the intended chat ID before sending, and review message text before batch or scheduled use.

Risk: The skill requires Feishu and NoizAI credentials.

Mitigation: Use least-privilege Feishu bot permissions and keep FEISHU_APP_SECRET and NOIZ_API_KEY out of source control, logs, and command history.

Risk: Installer or scheduled usage can execute scripts or send repeated messages.

Mitigation: Pin or verify any npx installer, test with --no-send before enabling delivery, and apply rate limits for cron or batch sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anightmare2/skills/feishu-voice-skill)
- [API reference](reference.md)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [NoizAI API keys](https://developers.noiz.ai/api-keys)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; generated OPUS audio when an output path or no-send mode is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call NoizAI and Feishu APIs, send an audio message to a configured Feishu chat, and write a local OPUS file.]

## Skill Version(s):

1.2.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
