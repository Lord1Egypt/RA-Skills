## Description:

Audio and video processing toolkit for OpenClaw that helps agents convert, edit, analyze, and generate audio and video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to request common audio and video workflows such as format conversion, trimming, merging, media inspection, slideshow creation, and text-to-speech or text-to-video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL and text-to-speech handling may involve external content or services.

Mitigation: Avoid private media, private URLs, and sensitive TTS text unless external service use is acceptable.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Install in an isolated Python environment and pin and review dependencies before production use.

Risk: Media processing can create large temporary or output files.

Mitigation: Confirm output paths and available disk space before running real media-editing operations.

## Reference(s):

- [AV Skill on ClawHub](https://clawhub.ai/hgta23/skills/av)
- [Publisher profile: hgta23](https://clawhub.ai/user/hgta23)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command-oriented status messages and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files, URLs, media formats, output paths, and dependency installation steps supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
