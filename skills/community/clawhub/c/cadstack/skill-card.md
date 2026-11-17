## Description:

Generate, execute, and verify CAD scripts across FreeCAD, AutoCAD, SolidWorks, and Fusion 360 using natural language commands with safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayneouyang](https://clawhub.ai/user/wayneouyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CAD engineers, and automation users use this skill pack to turn natural-language part requests into reviewed CAD scripts, backend configuration steps, exported model files, and QA reports. It is best suited for local CAD automation workflows where the user can review generated scripts and verify geometry before relying on outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local Python scripts can affect the host CAD environment or filesystem if they are unsafe or incorrect.

Mitigation: Run only in a constrained local CAD environment, keep script validation enabled, and review generated scripts before execution.

Risk: The Fusion 360 bridge exposes CAD actions over a localhost socket without documented authentication or per-request approval.

Mitigation: Avoid the Fusion 360 bridge until authentication or explicit approval is added, or run it only in a tightly controlled local session.

Risk: Generated exports may be written to unintended locations.

Mitigation: Restrict output paths to the configured CADStack output directory and verify exported files before downstream use.

Risk: Documented remote setup commands may point to unpinned or placeholder sources.

Mitigation: Install only from a verified pinned release controlled by the trusted publisher.

## Reference(s):

- [CADStack ClawHub listing](https://clawhub.ai/wayneouyang/skills/cadstack)
- [FreeCAD project](https://www.freecad.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated CAD scripts and exported CAD files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce STEP, STL, OBJ, DXF, or SVG files through local CAD backends.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
