## Description:

Guides agents using ElevenLabs to generate speech and sound effects, clone voices with consent, and process audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to guide ElevenLabs speech generation, voice cloning, sound effects, audio cleanup, and transcription through their authorized account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio and text sent for processing can contain sensitive information.

Mitigation: Obtain approval before sending sensitive material and share only the minimum needed.

Risk: Generation may consume paid ElevenLabs credits.

Mitigation: Confirm the requested generation and expected cost implications before proceeding.

Risk: Voice cloning can impersonate a speaker without consent.

Mitigation: Clone a voice only after confirming the speaker explicitly consented.

Risk: Writes, deletions, and approved automations can change resources or run persistently.

Mitigation: Confirm each write or deletion and approve any function or trigger before creation.

Risk: Exposed API keys could allow unauthorized account access.

Mitigation: Prefer the CLI/OAuth login and avoid exposing MATON_API_KEY unless necessary.

## Reference(s):

- [ClawHub ElevenLabs skill](https://clawhub.ai/byungkyu/skills/elevenlabs-api)
- [ElevenLabs API documentation](https://elevenlabs.io/docs/api-reference)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with CLI and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depending on the requested API action, responses can include generated audio or transcripts.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
