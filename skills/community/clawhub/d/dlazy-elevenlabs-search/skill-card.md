## Description:

Search the ElevenLabs voice library by keyword, source, and category, returning playable previews to help choose a voice for text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search ElevenLabs voices by descriptor, source, and category, then review playable previews before choosing a voice for text-to-speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release scan was partial and reported unresolved local references.

Mitigation: Review the skill documentation and CLI installation details before use.

Risk: The skill requires a dLazy API key for requests.

Mitigation: Use the documented device-code login and rotate or revoke the key from the dLazy dashboard if it is exposed.

Risk: Search prompts and parameters are sent to the dLazy hosted API.

Mitigation: Avoid including confidential information in search prompts or parameters.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-search)
- [CLI homepage listed in release metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured voice search results with playable preview links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be filtered by search prompt, voice source, category, and page size.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
