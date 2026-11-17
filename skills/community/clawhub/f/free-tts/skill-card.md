## Description:

Dual-engine text-to-speech and voice-cloning skill for Fish Audio s2.1-pro-free and Xiaomi MiMo V2.5 TTS, including setup guidance, preset voices, voice design, persistent Fish voice IDs, and temporary audio cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darker314159](https://clawhub.ai/user/darker314159)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to configure free or limited-free cloud TTS providers, generate speech from text, clone voices with user-provided recordings, and manage reusable Fish Audio voice IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text and voice recordings are sent to Fish Audio or Xiaomi MiMo for synthesis or cloning.

Mitigation: Use the skill only with recordings and text the user has rights to submit; avoid third-party or sensitive voices unless consent and provider retention/model-improvement terms have been reviewed.

Risk: API keys are stored persistently in Windows user environment variables.

Mitigation: Use the setup helpers or manual environment-variable storage instead of hardcoding keys, rotate exposed keys, and avoid pasting secrets into shared transcripts.

Risk: Local Fish voice cache entries may retain voice IDs and source recording paths after cloning or sync.

Mitigation: Review scripts/voices_cache.json after use and remove entries or source-path metadata that should not remain on disk.

Risk: Setup checks can display proxy configuration while troubleshooting network access.

Mitigation: Avoid authenticated proxy URLs in environment variables or redact proxy credentials before sharing diagnostic output.

## Reference(s):

- [Fish Audio API reference](artifact/references/fish-api.md)
- [Xiaomi MiMo TTS API reference](artifact/references/mimo-api.md)
- [Fish Audio documentation](https://docs.fish.audio)
- [Fish Audio s2.1-pro-free API announcement](https://fish.audio/zh-CN/blog/s2-1-pro-free-api/)
- [Fish Audio OpenAPI schema](https://api.fish.audio/openapi.json)
- [Xiaomi MiMo speech synthesis V2.5 documentation](https://mimo.mi.com/docs/zh-CN/quick-start/usage-guide/audio/speech-synthesis-v2.5)
- [ClawHub skill page](https://clawhub.ai/darker314159/skills/free-tts)
- [Publisher profile](https://clawhub.ai/user/darker314159)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, audio files]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts can emit JSON status and write MP3 or WAV audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FISH_API_KEY and/or MIMO_API_KEY; network calls send text and optional voice recordings to the selected provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
