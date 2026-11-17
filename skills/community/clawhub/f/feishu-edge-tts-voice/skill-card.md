## Description:

Sends Feishu voice messages by generating speech with Microsoft Edge TTS, converting the audio to Opus, uploading it to Feishu, and sending it as an audio message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send spoken Feishu replies when a workflow calls for voice output, TTS narration, or an audio message instead of plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text and generated audio are sent through Microsoft Edge TTS and Feishu.

Mitigation: Avoid sending sensitive text unless those services and data flows are approved for the intended use.

Risk: The skill reads Feishu app credentials from the OpenClaw configuration and can send Feishu messages on behalf of that app.

Mitigation: Use scoped Feishu credentials and review app permissions before deployment.

Risk: The security scan notes unsafe credential handling around command-line token use.

Mitigation: Replace token-in-arguments handling before production use where process arguments may be exposed.

Risk: Dependency behavior can change because the skill relies on external tools and packages such as edge-tts, ffmpeg, and curl.

Mitigation: Pin dependencies and verify the runtime environment before installing or running the skill.

## Reference(s):

- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Files]

**Output Format:** [Markdown with inline bash commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates temporary MP3 and Opus audio files, uploads the Opus file to Feishu, and sends the resulting file key as an audio message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
