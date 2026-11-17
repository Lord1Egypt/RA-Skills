## Description:

Elevenlabs Toolkit helps agents integrate ElevenLabs voice APIs for text-to-speech, sound effects, music-style audio generation, speech-to-text, voice isolation, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add ElevenLabs-backed voice generation, transcription, voice isolation, and streaming endpoints to voice-enabled apps and audio content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API-backed endpoints may be exposed without access controls.

Mitigation: Use the router only in a trusted, authenticated application and add caller authentication, quotas, request-size limits, and rate limits before exposing it.

Risk: The release includes an under-disclosed Mistral story-chat data flow and MISTRAL_API_KEY handling.

Mitigation: Remove that feature or explicitly disclose and review the Mistral data flow and credential handling before deployment.

Risk: API keys could be exposed through terminal output or logs.

Mitigation: Set credentials through environment variables or a secret manager and do not print API keys in terminals or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/elevenlabs-toolkit)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [ElevenLabs API base URL](https://api.elevenlabs.io/v1)
- [ElevenLabs voices endpoint](https://api.elevenlabs.io/v1/voices)
- [ElevenLabs subscription endpoint](https://api.elevenlabs.io/v1/user/subscription)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets for FastAPI and ElevenLabs API usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce FastAPI router code and workflows that handle JSON responses or MP3 audio bytes.]

## Skill Version(s):

1.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
