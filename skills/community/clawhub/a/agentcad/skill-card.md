## Description:

AgentCAD helps agents design, inspect, validate, and export 3D models using build123d Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdilla1277](https://clawhub.ai/user/jdilla1277)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use AgentCAD to create or revise 3D geometry from a written specification, then inspect and validate the result. It can deliver STEP models, rendered previews, mesh exports, and geometry metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The feedback workflow may send task details and session diagnostics to the vendor without user approval.

Mitigation: Review feedback contents before sending; use `agentcad feedback --local-only` to save feedback without uploading it.

Risk: The installation instructions use an unpinned AgentCAD package version.

Mitigation: Pin a reviewed AgentCAD version in the installation environment.

Risk: The security analysis is incomplete because many local references could not be resolved.

Mitigation: Review the complete skill materials and referenced documentation before installation or execution.

## Reference(s):

- [AgentCAD documentation and project site](https://agentcad.dev)
- [AgentCAD ClawHub release](https://clawhub.ai/jdilla1277/skills/agentcad)
- [Publisher profile](https://clawhub.ai/user/jdilla1277)

## Skill Output:

**Output Type(s):** [Code, 3D model files, Images, Metrics, Guidance]

**Output Format:** [Python scripts; STEP, PNG, STL, GLB, and OBJ files; structured geometry metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Artifacts and formats depend on the requested model and selected exports.]

## Skill Version(s):

0.8.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
