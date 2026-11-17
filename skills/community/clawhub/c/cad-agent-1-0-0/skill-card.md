## Description:

Run build123d CAD code inside a container to create, render, and iteratively modify 3D models via HTTP with returned rendered images for visual feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, inspect, modify, and export parametric CAD models through an agent-driven visual iteration workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to build and run mutable remote code.

Mitigation: Install only from a trusted reviewed source and pin the repository to a specific reviewed commit when possible.

Risk: The CAD API executes modeling code and has no documented access controls in the provided evidence.

Mitigation: Bind the service to 127.0.0.1, keep port 8123 off untrusted networks, and stop or remove the container when finished.

Risk: Container execution can increase host exposure if granted broad access.

Mitigation: Avoid host mounts and Docker socket access, and run the container with minimal privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/skills/cad-agent-1-0-0)
- [CAD Agent repository](https://github.com/clawd-maf/cad-agent)
- [build123d documentation](https://build123d.readthedocs.io/)
- [VTK](https://vtk.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, HTTP examples, and build123d code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CAD export guidance for STL, STEP, and 3MF workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
