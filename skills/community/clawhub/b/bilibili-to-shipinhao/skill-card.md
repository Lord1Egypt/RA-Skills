## Description:

Converts horizontal Bilibili videos into vertical short clips for WeChat Channels, with transcription, subtitles, and cover images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editors use this skill to select highlights from horizontal knowledge videos and prepare captioned 9:16 clips and covers for manual publishing to WeChat Channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download instructions suggest disabling a host safe-delete protection when merging video streams.

Mitigation: Do not disable host safe-delete globally; run downloads in a disposable working directory and manually remove only known temporary files.

Risk: Downloading and processing external videos runs local video and transcription commands.

Mitigation: Run the workflow only if comfortable with these commands, in a dedicated working directory.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oracis/skills/bilibili-to-shipinhao)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with workflow steps and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of MP4 clips, SRT subtitles, transcript files, and cover images; publishing is manual.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
