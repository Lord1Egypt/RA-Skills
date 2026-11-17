## Description:

Hands-free voice assistant for OpenClaw on an ESP32-S3-BOX-3 with on-device wake word, switchable xAI Grok, ElevenLabs, or FishAudio STT and TTS, and no Home Assistant requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darrenjrobinson](https://clawhub.ai/user/darrenjrobinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect an ESP32-S3-BOX-3 voice assistant to OpenClaw through a Docker bridge, configure STT and TTS providers, and troubleshoot local network, API key, and device setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to build and run unpinned Docker code from an external GitHub repository while supplying API keys and device details.

Mitigation: Review the upstream repository and Docker Compose file before running it, pin to a trusted commit where practical, and provide only the credentials needed for the selected providers.

Risk: Spoken audio and transcripts may be sent to selected STT/TTS providers and the configured OpenClaw endpoint.

Mitigation: Confirm provider data handling requirements before use and avoid speaking sensitive information unless the configured endpoints are approved for that data.

## Reference(s):

- [GitHub: darrenjrobinson/voice-esp32-openclaw](https://github.com/darrenjrobinson/voice-esp32-openclaw)
- [Going Direct - ESP32 Voice for OpenClaw](https://blog.darrenjrobinson.com/going-direct-esp32-voice-for-openclaw/)
- [Hardware Voice Assistant for OpenClaw](https://blog.darrenjrobinson.com/hardware-voice-assistant-for-openclaw/)
- [ESPHome wake-word voice assistants](https://github.com/esphome/wake-word-voice-assistants)
- [ClawHub skill page](https://clawhub.ai/darrenjrobinson/skills/esp32-voice-assistant)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance references Docker, OpenClaw, ESPHome device settings, and selected STT/TTS provider credentials.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
