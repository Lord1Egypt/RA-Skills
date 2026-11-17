## Description:

Convert text to speech using Volcengine TTS with preset or cloned voices and send the generated audio as a Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willsonchenservice-eng](https://clawhub.ai/user/willsonchenservice-eng)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to have an agent turn supplied text into speech and deliver it to a Feishu user or group chat. It supports Volcengine preset voices and user-provided cloned voice IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supplied text and the Volcengine API key to a TTS endpoint controlled by the environment.

Mitigation: Run it only where VOLC_TTS_URL cannot be set by untrusted parties, or remove or validate that override before use.

Risk: Generated audio is uploaded to Feishu and posted to the configured recipient.

Mitigation: Do not use the skill for secrets or regulated data, and verify the recipient chat ID before sending.

Risk: Cloned voices can be misused without permission.

Mitigation: Use cloned voice IDs only with consent from the voice owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willsonchenservice-eng/skills/feishu-voice-clone-tts)
- [Volcengine TTS console](https://console.volcengine.com/speech/new/experience/tts?projectName=default)
- [Volcengine voice clone console](https://console.volcengine.com/speech/new/experience/clone?projectName=default)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Audio messages]

**Output Format:** [Markdown guidance with inline shell commands; runtime output is a Feishu audio message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu credentials, a Volcengine API key, a voice type ID, and ffmpeg/ffprobe.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
