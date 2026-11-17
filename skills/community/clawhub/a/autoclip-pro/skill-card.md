## Description:

AutoClip Pro helps video creators batch process local videos with FFmpeg-based trimming, resizing, watermarking, style templates, thumbnails, and folder-level rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

External video creators, self-media operators, e-commerce sellers, and media teams can use this skill to configure and run local batch video edits across folders of source clips. It is intended for repetitive video processing workflows such as resizing, watermarking, transitions, thumbnails, and style-template application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe command execution behavior that could run unintended commands when paths or configuration values contain shell metacharacters.

Mitigation: Review carefully before installing, avoid shell metacharacters in filenames and configuration values, and update FFmpeg execution to use argument arrays with shell execution disabled.

Risk: The security scan reports cleanup behavior that could delete source videos or unintended files.

Mitigation: Run first on backed-up sample videos, verify input and output paths, and restrict deletion to files created in a dedicated temporary directory.

Risk: The security guidance flags included marketing playbooks as inappropriate unless rewritten for transparent, permission-based outreach.

Mitigation: Remove or rewrite sales and outreach material so any promotion is transparent, permission-based, and appropriate for the target community.

## Reference(s):

- [AutoClip Pro ClawHub Skill Page](https://clawhub.ai/gdp6539/skills/autoclip-pro)
- [Node.js](https://nodejs.org)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [Gyan FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
- [Sample Video Sources](artifact/examples/sample-video/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and JavaScript or shell command snippets; runtime scripts produce processed video and thumbnail files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js and FFmpeg; writes generated media to the configured output directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
