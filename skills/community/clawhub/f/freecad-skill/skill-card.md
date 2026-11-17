## Description:

Create, edit, verify and export parametric FreeCAD models (STEP, STL, 3MF) and DXF drawings from JSON; STL import; mass and stress checks; parts from GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninja7v](https://clawhub.ai/user/ninja7v)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mechanical engineers use this skill to create and revise parametric FreeCAD models from JSON requests, inspect and check geometry, run mass and linear static stress analyses, and export CAD models and drawings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence, but coverage was partial (53 of 54 components scanned) and some instruction-text checks were incomplete; its guidance also notes broad detected capabilities without a declared tool scope.

Mitigation: Review the skill behavior and host permissions before enabling it. Set FCSKILL_OFFLINE=1 when optional library downloads are not needed.

Risk: Generated geometry and linear static stress results can be misleading when dimensions, constraints, loads, or material assumptions are wrong; the documented FEM analysis is a linear estimate and is not certified.

Mitigation: Review geometry warnings and export checks, inspect FEM equilibrium and convergence, and have safety-critical designs independently validated by a qualified engineer.

## Reference(s):

- [FreeCAD skill release](https://clawhub.ai/ninja7v/skills/freecad-skill)
- [Publisher profile](https://clawhub.ai/user/ninja7v)

## Skill Output:

**Output Type(s):** [Files, JSON, Analysis, Guidance]

**Output Format:** [Native FreeCAD documents and CAD/drawing exports, with JSON operation results and optional analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model dimensions use millimetres and degrees. Geometry checks, export verification, and linear static analysis are reported when requested; FEM results are estimates, not certified calculations.]

## Skill Version(s):

3.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
