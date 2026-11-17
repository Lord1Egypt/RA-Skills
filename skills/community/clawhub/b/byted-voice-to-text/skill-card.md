## Description:

Converts Feishu voice messages, local audio files, and audio URLs to text using Volcengine BigModel ASR Flash and Standard modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route and transcribe voice messages, local audio files, or audio URLs through Volcengine BigModel ASR, then handle the transcript as agent input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio and credentials may be sent to Volcengine/Bytedance services or environment-controlled endpoints.

Mitigation: Use only approved recordings, keep endpoint variables on trusted HTTPS defaults or vetted endpoints, and confirm organizational approval before transcription.

Risk: The skill can autonomously install ffmpeg or ffprobe through package managers.

Mitigation: Preinstall ffmpeg and ffprobe in managed environments and avoid autonomous installation unless system changes are approved.

Risk: ARK_SKILL_API_KEY can be used to manage and persist speech API keys.

Mitigation: Provide ARK_SKILL_API_KEY only when delegated key management is intended; otherwise set MODEL_SPEECH_API_KEY directly and manage secret storage externally.

Risk: The skill claims exclusive routing behavior for audio transcription.

Mitigation: Review host agent policy before enabling and treat routing language as skill guidance within the controlling agent policy.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/volcengine-skills/skills/byted-voice-to-text)
- [Audio routing strategy](references/routing_strategy.md)
- [Volcengine BigModel ASR](https://www.volcengine.com/docs/6561/1354870)
- [Volcengine ASR quickstart](https://www.volcengine.com/docs/6561/2119699)
- [Volcengine API key usage](https://www.volcengine.com/docs/6561/1816214)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcripts, JSON status or error payloads, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MODEL_SPEECH_API_KEY and supports local files, public audio URLs, and Feishu file keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
