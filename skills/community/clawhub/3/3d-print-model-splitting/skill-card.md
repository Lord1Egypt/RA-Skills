## Description: <br>
Use when splitting a single complex STL / figurine / statue model into multiple 3D-printable and physically assemblable parts, especially with Blender face/material annotation, Bambu Studio, MeshFix, manifold Boolean, interface clearance/allowance, 3MF object validation, or assembly interference checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzyling](https://clawhub.ai/user/lzyling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and 3D-printing workflow operators use this skill to split sculpted STL figurines or statues into printable, physically assemblable parts with annotated boundaries, capped baselines, interface clearance, and validation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Blender helper script may delete the current scene before running. <br>
Mitigation: Review scripts before execution and run them only in a disposable or newly opened Blender scene, or after saving a backup of any open .blend file. <br>
Risk: Generated split parts can be printable but still fail physical assembly if interface clearance is not validated. <br>
Mitigation: Use capped split previews, boundary-edge checks, 3MF object validation, pairwise interference checks, and physical assembly testing before final handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lzyling/3d-print-model-splitting) <br>
- [Generic SOP: complex STL to printable, assemblable parts](references/sop.md) <br>
- [Clearance and Boolean lessons](references/clearance-lessons.md) <br>
- [Blender material-face annotation](references/blender-material-annotation.md) <br>
- [Versioning convention for STL splitting projects](references/versioning.md) <br>
- [Case study: validated 5-part figurine workflow](references/case-study-v13.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration notes, validation summaries, and generated STL/3MF/Blend/PNG file handoff guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project-local model, preview, and report files when the user runs the helper scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
