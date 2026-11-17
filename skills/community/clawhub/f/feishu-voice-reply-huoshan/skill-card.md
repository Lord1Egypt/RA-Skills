## Description:

Generates speech with Volcengine TTS, converts the audio to Opus, uploads it to Feishu, and sends it as a voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaqzsd](https://clawhub.ai/user/kaqzsd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send short Feishu voice replies by turning provided text into speech through Volcengine TTS and delivering the converted audio with Feishu APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Volcengine and Feishu credentials that can authorize paid TTS usage and message sending.

Mitigation: Store credentials in a protected secrets mechanism, rotate them if exposed, and grant only the Feishu permissions needed for upload and message sending.

Risk: Input text and generated audio are sent to external Volcengine and Feishu services.

Mitigation: Use only non-sensitive text and confirm the intended Feishu recipient before sending.

Risk: The documented Feishu permission set includes contact-read access that may not be required for sending a voice message.

Mitigation: Remove the unused contact-read permission unless the deployment has a separate reviewed need for it.

Risk: Installation guidance and package metadata include avoidable dependency risk.

Mitigation: Avoid running npm install for this package unless dependencies are removed or pinned, and install runtime tools such as ffmpeg from trusted package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaqzsd/skills/feishu-voice-reply-huoshan)
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/195562)
- [Volcengine voice list](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [Feishu Open Platform](https://open.feishu.cn/document/home)
- [Feishu message types](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script produces temporary MP3 and Opus audio files, uploads the Opus file to Feishu, and returns status text including the Feishu message ID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
