## Description:

Helps an agent capture full-screen or selected-region screenshots and send screenshots or local image files to a Feishu workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andersonhjb](https://clawhub.ai/user/andersonhjb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to quickly share screenshots, selected screen regions, or local image files into Feishu during debugging, remote assistance, demonstrations, and documentation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots or selected local images may contain secrets or private information before they are sent to Feishu.

Mitigation: Use targeted region capture, review image contents before sending, and avoid full-screen capture when sensitive windows or credentials are visible.

Risk: The bundled implementation may run code from crafted image filenames.

Mitigation: Do not process untrusted filenames until the python -c interpolation issue is fixed; use controlled file paths and sanitize filenames before execution.

Risk: Compression cleanup behavior may delete an original image file.

Mitigation: Keep backups of important images and review the cleanup path logic before using the compression workflow on valuable source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andersonhjb/skills/feishu-image-sent)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Improved skill documentation](artifact/improved/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and configuration guidance for macOS screenshot capture, image compression, workspace copying, and Feishu media sending.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
