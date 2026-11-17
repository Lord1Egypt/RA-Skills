## Description:

Creates short vertical podcast videos from provided copy by generating two-speaker podcast audio with ListenHub MCP, looping a template video with ffmpeg, and producing a brief content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyken](https://clawhub.ai/user/jackyken)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to turn written Chinese podcast or short-video copy into a vertical video with generated two-speaker audio, a selected background template, and marketing-oriented content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and configures an unpinned third-party ListenHub MCP server.

Mitigation: Pin and review the MCP package version before use, and install it only if the ListenHub publisher is trusted.

Risk: The workflow sends user-provided video copy to ListenHub for podcast generation.

Mitigation: Use the service only for content suitable for third-party processing and avoid sending confidential or sensitive copy.

Risk: The workflow requires a ListenHub API key in persistent MCP configuration.

Mitigation: Use a narrowly scoped API key, rotate it when needed, and avoid running the workflow as root.

Risk: Generated titles or filenames may be used in shell commands and output paths.

Mitigation: Sanitize generated filenames before creating or merging video files.

## Reference(s):

- [CreateVideo - Podcast to Video ClawHub page](https://clawhub.ai/jackyken/skills/create-podcast-video)
- [ListenHub MCP guide](references/listenhub-guide.md)
- [Copywriting template reference](references/copywriting-template.md)
- [Explosive dialogue copywriting structure](references/copywriting-explosive-dialogue.md)
- [ListenHub website](https://marswave.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and generated content-analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for creating task directories, generating podcast audio, combining audio with template video, and saving content analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
