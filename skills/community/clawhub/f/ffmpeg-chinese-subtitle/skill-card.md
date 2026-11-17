## Description:

Provides a Windows-focused Pillow and ffmpeg workflow for rendering Chinese subtitle text onto images before creating videos, avoiding ffmpeg text encoding issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media engineers use this skill to add Chinese subtitle text to image assets and create videos with ffmpeg/Pillow when Windows ffmpeg filters have encoding or path handling issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media processing commands can overwrite output files when reused paths are supplied.

Mitigation: Use dedicated working directories, review input and output paths before execution, and avoid running examples against important files.

Risk: The optional ffmpeg concat helper writes a list file and uses concat processing that can be unsafe with untrusted filenames or shared temporary directories.

Mitigation: Use trusted filenames, isolate temporary directories per run, and avoid the concat helper for untrusted media lists.

Risk: The Pillow dependency is specified with a lower bound rather than a pinned reviewed version.

Mitigation: Install Pillow through normal Python packaging with a pinned version that has been reviewed for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/systiger/skills/ffmpeg-chinese-subtitle)
- [Publisher profile](https://clawhub.ai/user/systiger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file path, font, subtitle placement, Pillow dependency, and ffmpeg command guidance.]

## Skill Version(s):

1.0.0 (source: server release, skill frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
