## Description:

Dump the current STM32 LCD framebuffer via J-Link and convert it to PNG for visual comparison with Figma.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylongw](https://clawhub.ai/user/ylongw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embedded engineers use this skill to capture on-device STM32 LCD framebuffer pixels through J-Link and convert them into PNG images for design comparison and regression snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Framebuffer captures may contain sensitive on-device screen content.

Mitigation: Use the skill only with authorization, choose output paths deliberately, and delete raw dumps and PNG files when they are no longer needed.

Risk: Unpinned image-processing dependencies can change behavior or introduce supply-chain risk.

Mitigation: Run the conversion in a dedicated Python environment and prefer a pinned Pillow version.

Risk: Incorrect framebuffer address, dimensions, or pixel format can produce corrupt or misleading images.

Mitigation: Confirm the target device settings, framebuffer size, resolution, and RGB888 format before using captures for visual comparison.

## Reference(s):

- [Framebuffer Dump Skill Page](https://clawhub.ai/ylongw/skills/framebuffer-dump)
- [SEGGER J-Link Downloads](https://www.segger.com/downloads/jlink/)
- [Pillow Python Package](https://pypi.org/project/Pillow/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local raw framebuffer dumps and PNG image files when used with authorized device access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
