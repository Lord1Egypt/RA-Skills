## Description:

Capture screenshots and screen recordings when users need to capture full screens, windows, regions, or tutorial material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture screenshots, windows, screen regions, or short screen-recording workflows for documentation, tutorials, debugging, and visual reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen capture can expose sensitive visible information.

Mitigation: Use only when the visible screen contents are appropriate to capture, and close or mask sensitive windows before running it.

Risk: Windows output-path handling can run unintended PowerShell commands when untrusted paths are supplied.

Mitigation: Do not pass untrusted or externally supplied output paths on Windows until the path handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/dinghaibin-screenshot-tool)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown with shell commands and generated screenshot or recording files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG, JPG, or MP4 files depending on the requested capture mode and platform support.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
