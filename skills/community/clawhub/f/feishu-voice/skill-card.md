## Description:

Feishu Voice converts text to speech with coze-tts, converts the audio to Feishu-compatible opus format, uploads it, and sends it as a playable Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate sending generated voice messages into Feishu chats from text input, with optional voice, speed, and receiver parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user text and generated audio through external Feishu and Coze services while using local credentials.

Mitigation: Use minimally scoped Feishu and Coze credentials, restrict the Feishu app permissions to the needed chat workflow, and avoid sensitive text unless the data path is approved.

Risk: The skill executes a local coze-tts dependency that may inherit environment secrets.

Mitigation: Install coze-tts only from a trusted local path and review that dependency before running this skill with production credentials.

Risk: Temporary audio files are created on the local machine during conversion.

Mitigation: Run the skill in a trusted or isolated workspace and avoid shared machines for sensitive voice content until temporary-file handling is hardened.

## Reference(s):

- [ClawHub Feishu Voice skill page](https://clawhub.ai/franklu0819-lang/skills/feishu-voice)
- [Feishu voice API reference](artifact/references/feishu_voice_api.md)
- [Feishu message create documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Files, Text]

**Output Format:** [Markdown guidance with bash command examples; runtime output is terminal status text and a Feishu voice message side effect.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, ffprobe, jq, Feishu credentials, a Coze API key, and the coze-tts dependency; generates temporary local audio files during execution.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
