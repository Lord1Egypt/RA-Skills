## Description:

Build lightweight SDF and canvas displacement glass surfaces with Vaso for React interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodfishhhh](https://clawhub.ai/user/woodfishhhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and interface engineers use this skill to add lightweight SDF liquid-glass surfaces to React UI, especially when they need a no-WebGL fallback or many compact refractive cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Vaso dependency may change behavior or supply-chain posture if installed without version control.

Mitigation: Pin vaso to a reviewed version, keep the project lockfile, and install dependencies in a least-privileged development environment.

Risk: Readable UI content can become doubled, rainbow-fringed, or less accessible if it is placed inside the displacement layer.

Mitigation: Keep text, icons, controls, and focus rings in an unfiltered sibling overlay and verify the component on light, dark, and detailed backgrounds.

Risk: Unsupported browsers or stale canvas dimensions can make the glass surface look cropped, stretched, or unusable.

Mitigation: Keep a translucent CSS fallback under the effect, measure the host with ResizeObserver, and test resize behavior on desktop and mobile viewports.

## Reference(s):

- [SDF Tuning](references/tuning.md)
- [Vaso GitHub Repository](https://github.com/huozhi/vaso)
- [ClawHub Skill Page](https://clawhub.ai/woodfishhhh/skills/build-sdf-liquid-glass)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with React, CSS, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt bundled React and CSS assets; no external API output is produced.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
