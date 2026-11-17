## Description:

Use when AudioClaw Skills, Feishu, or Lark needs to send AudioClaw voice replies with runtime-switchable voice_id, emotion preset, or speaking style, including per-message speaker overrides, voice-family emotion routing, cache reuse, and safe fallback when a requested voice is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AudioClaw operators use this skill to turn finalized assistant replies into SenseAudio TTS files, route voice and emotion choices, reuse cached audio, and deliver Feishu or Lark audio replies when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send generated audio through Feishu.

Mitigation: Install it only where direct Feishu audio sending is intended, and require explicit operator approval for deployments that send messages on behalf of users.

Risk: The Feishu sender can infer recipients from local session logs.

Mitigation: Prefer explicit chat IDs and restrict access to workspace logs that may contain routing information.

Risk: Request JSON can influence paths such as ffmpeg_exe and cache_dir.

Mitigation: Do not accept untrusted request JSON, and do not expose ffmpeg_exe or cache_dir controls to end users.

Risk: The skill uses stored credentials and sends generated voice replies to external services.

Mitigation: Review credential storage and treat synthesized reply text and audio as data sent to SenseAudio and Feishu.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/kikidouloveme79/skills/audioclaw-skills-voice-reply)
- [OpenClaw Voice Switchboard Reference](references/openclaw_voice_switchboard.md)
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Voice API](https://senseaudio.cn/docs/voice_api)
- [SenseAudio TTS endpoint](https://api.senseaudio.cn/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON request and manifest examples, inline shell commands, and generated audio files when the scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call SenseAudio and Feishu APIs, write workspace-local audio files, cache generated audio, and emit traceable JSON manifests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
