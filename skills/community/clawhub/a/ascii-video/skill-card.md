## Description:

Convert video to ASCII animation with multiple dithering modes, color output, and framerate control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative coders, terminal artists, and documentation authors use this skill to convert video or image inputs into ASCII terminal output or ASCII-styled GIF/MP4 files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation recommends downloading mutable remote Python code that was not the reviewed artifact.

Mitigation: Use the bundled artifact/ascii_video.py, or pin any remote download to a trusted commit and verify it before execution.

Risk: The tool reads local media files, writes local output files, and invokes ffmpeg.

Mitigation: Run it in a controlled workspace with trusted inputs and review requested input and output paths before execution.

Risk: The CI verifier can inspect and execute checks against local folders.

Mitigation: Run the verifier only on trusted folders or inside a sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/ascii-video)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated ASCII text or GIF/MP4 files when the tool is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local media inputs and writes local outputs; video conversion depends on Pillow and ffmpeg.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
