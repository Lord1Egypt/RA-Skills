## Description:

Converts text to speech with MOSS-TTS, transcodes the audio, and sends it as a Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to generate spoken audio from text and send it to Feishu groups or users. It also includes chat-history retrieval behavior, so users should enable Feishu read permissions only when that broader workflow is intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes Feishu chat-history reading that is broader than the stated TTS purpose.

Mitigation: Grant message and chat read scopes only when history retrieval is needed, and otherwise limit the Feishu app to voice-message sending and file-upload permissions.

Risk: Text submitted for speech generation is sent to the external MOSS service and the resulting audio is uploaded to Feishu.

Mitigation: Avoid sending sensitive text unless the user accepts both external processing and Feishu delivery for that content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloeveryworlds/skills/feishu-voice-tts)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Audio files, Feishu messages, Guidance]

**Output Format:** [Markdown guidance with command examples; scripts produce WAV/OPUS audio and Feishu voice-message API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOSS and Feishu credentials, Feishu send/upload permissions, and ffmpeg for audio transcoding.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
