## Description:

Converts text to speech with Volcengine Doubao TTS, including voice, emotion, speed, volume, and pitch options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shandingdonren](https://clawhub.ai/user/shandingdonren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure Volcengine credentials, send text to Doubao TTS, and receive playable or saved speech audio with selectable voices and emotion handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to an external Volcengine/ByteDance text-to-speech service.

Mitigation: Use the skill only with text that is appropriate to send to the external provider.

Risk: The access token configuration file can expose service credentials if it is broadly readable.

Mitigation: Store credentials with restrictive file permissions or in a secret manager.

Risk: The documented global install flow is unpinned.

Mitigation: Install from a trusted, pinned release and review the artifact hashes before deployment.

Risk: Unsafe save-path and PowerShell playback handling can become command execution.

Mitigation: Avoid arbitrary save paths and Windows PowerShell playback until temporary-file and playback handling are fixed.

## Reference(s):

- [Volcengine](https://www.volcengine.com/)
- [Volcengine Speech Synthesis Documentation](https://www.volcengine.com/docs/6561/97465)
- [ByteDance TTS API Endpoint](https://openspeech.bytedance.com/api/v1/tts)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Files]

**Output Format:** [Markdown guidance with JSON configuration, bash command examples, HTTP requests, and MP3 audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local credentials, jq, curl, base64, and an available audio playback command for automatic playback.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
