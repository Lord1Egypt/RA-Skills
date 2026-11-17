## Description:

CAD Agent helps AI agents create, modify, render, inspect, and export build123d CAD models through a local containerized CAD service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawd-maf](https://clawhub.ai/user/clawd-maf)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design 3D-printable parts, parametric CAD models, and mechanical components while iterating from rendered images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CAD service can execute submitted Python and may be exposed as an unauthenticated service.

Mitigation: Bind the service to 127.0.0.1, keep it off untrusted networks, and stop the container when CAD work is complete.

Risk: The setup builds mutable external code.

Mitigation: Pin or review the upstream repository commit before building the container image.

## Reference(s):

- [build123d documentation](https://build123d.readthedocs.io/)
- [VTK](https://vtk.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, HTTP examples, build123d code, and generated CAD artifacts such as rendered PNG images and exported STL, STEP, or 3MF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local containerized CAD service reachable over HTTP.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
