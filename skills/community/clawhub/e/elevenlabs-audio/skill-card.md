## Description:

Create and manage voices, speech synthesis, audio projects, and conversational AI agents in ElevenLabs via the ElevenLabs API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate ElevenLabs voice workflows from an agent, including voice management, text-to-speech generation, audio projects, dubbing, pronunciation dictionaries, and conversational AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that handles authenticated ElevenLabs requests.

Mitigation: Review the ClawLink plugin source, publisher, permissions, and release provenance before installing; use a pinned or verified plugin version if supported.

Risk: Compromise or misuse of the connected integration could expose or misuse the user's ElevenLabs API access.

Mitigation: Be prepared to disable the plugin and rotate the ElevenLabs API key if compromise is suspected.

Risk: Write and destructive ElevenLabs operations can create, modify, or delete voices, projects, history items, dubbing projects, or agents.

Mitigation: Preview write operations and confirm the target resource and intended effect before execution.

## Reference(s):

- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference/overview)
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/elevenlabs-audio)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with inline bash code blocks and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or manage audio-related ElevenLabs resources through authenticated ClawLink tool calls.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
