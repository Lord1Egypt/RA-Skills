## Description:

Guide for deploying 3DGS from research to production: 10 industry verticals, engineering stack, GIS toolchain solutions, cross-platform deployment, and common pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaccen](https://clawhub.ai/user/jaccen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose 3D Gaussian Splatting pipelines, toolchains, deployment targets, and risk-aware next steps for production-oriented applications such as digital twins, autonomous driving simulation, robotics, GIS, AR/VR, and e-commerce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-run package commands in the guidance may install or execute unpinned dependencies.

Mitigation: Pin exact package versions, prefer project-local dependencies with lockfiles, avoid global installs or ad hoc npx execution, and run conversion tooling with minimal privileges.

Risk: 3DGS deployment guidance may be incomplete for a specific regulated, safety-critical, or high-fidelity production domain.

Mitigation: Review recommendations against domain constraints, validate outputs against real data and quality gates, and require human engineering review before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaccen/skills/3dgs-engineering-guide)
- [SuperSplat Editor](https://superspl.at/editor)
- [PlayCanvas Gaussian Splat Blog](https://playcanvas.com/blog/turning-a-gaussian-splat-into-a-videogame)
- [Awesome-Gaussian-Skills](https://github.com/jaccen/Awesome-Gaussian-Skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with decision tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic execution; guidance may include user-run package commands.]

## Skill Version(s):

1.0.6 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
