## Description:

High-quality voice synthesis with 18 personas, 32 languages, sound effects, batch processing, and voice design using ElevenLabs API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to generate speech, sound effects, and voice-design previews through ElevenLabs, including multilingual and batch audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says API-key storage claims need review and generated requests send prompts, text, voice-design descriptions, preview text, and the API key to ElevenLabs over HTTPS.

Mitigation: Prefer environment variables or a secure secret manager, avoid running the setup wizard when local config storage is not acceptable, and rotate any key that may have been saved or shared.

Risk: The security review says batch file-output handling needs review before installation.

Mitigation: Process only trusted batch JSON and inspect output paths before execution until output-path validation is fixed.

Risk: The skill loads without an API key because OpenClaw cannot express that one of two environment variables is required.

Mitigation: Set ELEVEN_API_KEY or ELEVENLABS_API_KEY before use and expect the scripts to fail on first API call if neither variable is present.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robbyczgw-cla/skills/elevenlabs-voices)
- [ElevenLabs](https://elevenlabs.io)
- [ElevenLabs API Documentation](https://docs.elevenlabs.io)
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
- [ElevenLabs Sound Effects API](https://elevenlabs.io/docs/api-reference/sound-generation)
- [ElevenLabs Voice Design API](https://elevenlabs.io/docs/api-reference/voice-generation)
- [Voice Guide](references/voice-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and generated audio files from the skill scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts can write MP3 audio outputs, local usage statistics, optional config.json, and optional .env-based configuration.]

## Skill Version(s):

2.2.0 (source: frontmatter and changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
