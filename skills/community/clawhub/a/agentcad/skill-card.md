## Description:

CAD tool for AI agents that helps users design, model, or build 3D objects and produces STEP files, PNG renders, mesh exports, and geometric metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdilla1277](https://clawhub.ai/user/jdilla1277)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers can use AI agents to create or revise 3D CAD models through an inspect, specify, build, validate, and deliver workflow, then review geometry and export model files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer version is not pinned, and scan coverage was incomplete because referenced paths were missing and an external skill was not inspected.

Mitigation: Check the install source and version, and review the referenced or external content before installing.

Risk: Optional feedback or diagnostic steps may upload text or project-related data.

Mitigation: Review the upload prompt and the exact data it describes; send feedback or diagnostics only when needed.

## Reference(s):

- [AgentCAD website and gallery](https://agentcad.dev)
- [AgentCAD on PyPI](https://pypi.org/project/agentcad/)

## Skill Output:

**Output Type(s):** [Code, 3D model files, Images, Geometric analysis]

**Output Format:** [Python build123d scripts; STEP, STL, GLB, and OBJ models; PNG renders; JSON metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Versioned geometry with validation and measurement results]

## Skill Version(s):

0.8.1 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
