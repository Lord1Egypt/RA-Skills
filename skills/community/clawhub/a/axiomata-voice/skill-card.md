## Description:

Axiomata Voice helps OpenClaw agents convert text messages to speech with ElevenLabs and prepare voice-message workflows for Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate speech audio from text, including long messages and accessibility-oriented voice output. The release evidence notes that advertised Telegram delivery and audio-processing behavior should be verified before operational use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the packaged code is mostly a stub and some advertised files are missing.

Mitigation: Review the artifact contents and verify required TTS, Telegram delivery, and audio-processing behavior before relying on the skill in production.

Risk: Text provided to configured ElevenLabs or Telegram workflows may be sent to external services.

Mitigation: Use approved data only, review provider data-handling requirements, and avoid sensitive text unless the deployment is authorized for those services.

Risk: The skill requires API credentials for external voice and messaging services.

Mitigation: Store credentials in a managed secrets system or environment variables, scope access narrowly, and rotate keys if exposed.

## Reference(s):

- [Axiomata Voice on ClawHub](https://clawhub.ai/kofna3369/skills/axiomata-voice)
- [Publisher profile](https://clawhub.ai/user/kofna3369)
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/<voice_id>)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions, command-line output, and audio file paths when configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external ElevenLabs credentials and, for advertised messaging workflows, Telegram configuration and working delivery scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
