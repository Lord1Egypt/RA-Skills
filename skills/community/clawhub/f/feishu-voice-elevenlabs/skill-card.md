## Description:

Sends Feishu (Lark) voice messages using ElevenLabs text-to-speech and transcribes Feishu audio messages using ElevenLabs speech-to-text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdongbear](https://clawhub.ai/user/dongdongbear)

### License/Terms of Use:


## Use Case:

Developers and Feishu workspace operators use this skill to send voice replies, transcribe received Feishu audio attachments, and support conversational reply workflows through Feishu and ElevenLabs integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu bot-send permissions can allow the skill to send messages into a workspace.

Mitigation: Use least-privileged Feishu app credentials, review the target recipient or chat before sending, and require explicit confirmation before enabling smart or automatic reply flows.

Risk: Voice and text content may be sent to ElevenLabs for speech generation or transcription.

Mitigation: Avoid routing sensitive content unless the user has approved the data flow and the deployment accepts ElevenLabs handling for that content.

Risk: Credentials and message text can be exposed on shared hosts or through unreviewed dependencies.

Mitigation: Run on trusted hosts, protect environment variables, avoid shared process visibility for sensitive invocations, and pin and verify the sag dependency.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dongdongbear/skills/feishu-voice-elevenlabs)
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
- [ElevenLabs speech-to-text API endpoint](https://api.elevenlabs.io/v1/speech-to-text)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, plain-text transcription output, and Feishu API result text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can initiate Feishu bot messages and route configured audio or text through ElevenLabs services.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
