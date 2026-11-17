## Description:

Audio Tool helps agents provide FFmpeg-backed guidance for audio format conversion, clipping, compression, merging, and extraction tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and media-editing users can use this skill to ask an agent for FFmpeg-backed guidance on converting, trimming, merging, compressing, denoising, and extracting audio from media files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg-backed media operations can act on user-selected files and command options, which may produce unwanted results if the file or command is not what the user intended.

Mitigation: Review input media files and agent-proposed FFmpeg commands before execution.

Risk: The source documentation is primarily in Chinese, which can lead to misunderstanding by users who do not read it.

Mitigation: Confirm the intended audio task and command parameters in a language the user understands before running commands.

## Reference(s):

- [ClawHub Audio Tool release page](https://clawhub.ai/yang1002378395-cmyk/skills/audio-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise instructions and FFmpeg command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg to be available on the system.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
