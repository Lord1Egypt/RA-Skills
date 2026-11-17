## Description:

AI music generation via Crazyrouter API using Suno. Create songs from text descriptions with lyrics, style, and title.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate songs or instrumental audio from text prompts, optional lyrics, title, style, and model selection through the Crazyrouter API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Crazyrouter endpoint can be overridden, which may expose the API key and submitted prompts to another server.

Mitigation: Use only in environments where CRAZYROUTER_BASE_URL cannot be set by untrusted parties, and use a limited Crazyrouter API key when available.

Risk: Prompts and lyrics may contain sensitive or proprietary content that is sent to the external API provider.

Mitigation: Avoid submitting sensitive lyrics, prompts, or confidential material.

Risk: The output option writes downloaded audio to a user-selected path and may overwrite existing writable files.

Mitigation: Choose output paths carefully and run the skill in a workspace where unintended overwrites are acceptable or recoverable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xujfcn/skills/crazyrouter-music-gen)
- [Crazyrouter](https://crazyrouter.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated audio files or returned audio URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; writes the downloaded audio to the requested output path when an audio URL is returned.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
