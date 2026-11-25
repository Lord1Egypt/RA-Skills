## Description:

Searches the ElevenLabs voice library by keyword, source, and category and returns playable previews for choosing voices for TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to find ElevenLabs voices by descriptor, source, and category, then review playable previews before choosing a voice for text-to-speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and partial coverage, and flagged a possible mismatch between the ElevenLabs search purpose and dLazy authentication.

Mitigation: Review the linked CLI and package, and confirm dLazy authentication is expected before providing an API key.

## Reference(s):

- [CLI project listed in skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Voice search results with metadata and playable preview URLs, typically returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count can be adjusted with --page_size.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
