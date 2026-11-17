## Description:

Guideline for directly editing 3D-printing project files (.3mf), verified against BambuStudio specifically: cutting or otherwise modifying mesh geometry, wiring objects into the 3MF XML correctly, arranging multiple print plates in BambuStudio's shared multi-plate coordinate system, and setting print/project parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and advanced 3D-printing users use this skill to programmatically edit BambuStudio .3mf project files, including mesh cuts, object placement, multi-plate arrangement, and print setting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied 3MF archive could contain unsafe zip paths or unexpectedly large contents during extraction.

Mitigation: Use the skill only with trusted 3MF files, run it in an isolated working directory or virtual environment, and review or harden archive extraction before repeated use.

Risk: Incorrect multi-plate placement or unverified slicer assumptions can produce misleading or unusable edited project files.

Mitigation: Apply the documented BambuStudio-specific validation steps, verify plate offsets and mesh integrity before delivery, and re-derive behavior before using the guidance with other slicers.

## Reference(s):

- [3MF Structure Reference](references/3mf-structure.md)
- [Plate Coordinate System Reference](references/plate-coordinate-system.md)
- [Mesh Editing Notes](references/mesh-editing-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify 3MF project files when used by an agent; original files should not be overwritten unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
