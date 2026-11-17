## Description:

Use when splitting a single complex STL / figurine / statue model into multiple 3D-printable and physically assemblable parts, especially with Blender face/material annotation, Bambu Studio, MeshFix, manifold Boolean, interface clearance/allowance, 3MF object validation, or assembly interference checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzyling](https://clawhub.ai/user/lzyling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, makers, and 3D-print workflow operators use this skill to turn complex sculpted STL models into split, capped, clearance-adjusted, slicer-ready parts with validation reports for physical assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path-like part names or filenames may cause helper scripts to write outside the intended project folders.

Mitigation: Review all helper script arguments before execution, use simple slug-style part names, and reject absolute paths or path separators in part and output filenames.

Risk: Generated model, preview, and report files may overwrite existing project artifacts when reused in the same output directory.

Mitigation: Run the workflow in a disposable project folder with versioned output directories and keep accepted baselines read-only or copied forward before experimentation.

Risk: Automated mesh repair or slicer acceptance can make parts printable without proving they physically assemble.

Mitigation: Require capped split previews, boundary-edge reporting, 3MF validation, pairwise interference checks, and a physical assembly test before final acceptance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lzyling/skills/3d-print-model-splitting)
- [Generic SOP: complex STL to printable, assemblable parts](references/sop.md)
- [Blender material-face annotation](references/blender-material-annotation.md)
- [Clearance and Boolean lessons](references/clearance-lessons.md)
- [Versioning and status conventions](references/versioning.md)
- [Validated 5-part figurine case study](references/case-study-v13.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, project-local helper scripts, and validation report formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of STL, 3MF, Blend, PNG preview, and JSON/text validation artifacts in a project workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
