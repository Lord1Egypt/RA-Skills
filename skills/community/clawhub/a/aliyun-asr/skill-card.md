## Description:

Pure Aliyun ASR skill for voice message transcription, supports multiple channels including Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to transcribe incoming voice messages from supported channels such as Feishu, Telegram, and WhatsApp into text for downstream AI handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice messages are uploaded to Aliyun for transcription.

Mitigation: Enable the skill only where users understand that audio will be sent to Aliyun and confirm the deployment's privacy and compliance requirements before use.

Risk: The setup recommends broad Aliyun NLS permissions.

Mitigation: Use a dedicated low-privilege Aliyun RAM user, protect and rotate the AccessKey, and avoid using primary account credentials.

Risk: Converted audio files can remain on disk after OGG-to-WAV conversion.

Mitigation: Treat local audio files as sensitive and review cleanup behavior before production deployment.

## Reference(s):

- [Aliyun NLS Console](https://nls-portal.console.aliyun.com/)
- [ClawHub skill page](https://clawhub.ai/jixsonwang/skills/aliyun-asr)
- [Publisher profile](https://clawhub.ai/user/jixsonwang)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Plain text transcription with JSON configuration guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, Aliyun NLS credentials, and access to the audio file being transcribed.]

## Skill Version(s):

1.0.10 (source: package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
