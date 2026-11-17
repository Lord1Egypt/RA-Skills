## Description:

Manage substantial engineering and software projects end to end by discovering or bootstrapping a canonical project, defining scope and work breakdown, coordinating agents, maintaining requirements and traceability, controlling changes and baselines, auditing quality, and enforcing release readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aminekhettat](https://clawhub.ai/user/aminekhettat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to initialize or manage a canonical project workspace, coordinate bounded agent work, maintain requirements and traceability, control changes and baselines, record verification evidence, track risks and problems, and assess release readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating project-file operations can be redirected by project-controlled symlinks.

Mitigation: Install only for trusted project workspaces and inspect managed directories for symlinks or unexpected redirects before running mutating commands.

Risk: Bootstrap and project-management workflows can use broad local Git and remote-repository authority.

Mitigation: Review the bootstrap plan before allowing repository creation or pushes through gh, glab, or SSH.

Risk: SPICE-like checks may be mistaken for formal SPICE, Automotive SPICE, safety, or regulatory certification.

Mitigation: Treat the outputs as project-control assistance only and have qualified reviewers confirm any compliance, safety, or release claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aminekhettat/skills/engineering-project-manager)
- [Source repository homepage](https://github.com/aminekhettat/engineering-project-manager)
- [Security guidance](SECURITY.md)
- [SPICE-like scope and limitations](docs/SPICE-SCOPE.md)
- [Change and baseline management](docs/CHANGE-BASELINE-MANAGEMENT.md)
- [Requirement data model](docs/REQUIREMENT-DATA-MODEL.md)
- [Verification evidence management](docs/VERIFICATION-EVIDENCE.md)
- [Risk and problem management](docs/RISK-PROBLEM-MANAGEMENT.md)
- [Project Manager handbook](references/project-manager-handbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated project files, JSON registries, and audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, Python 3.10+, and Git; GitHub or GitLab bootstrap requires authenticated gh or glab when used.]

## Skill Version(s):

1.4.1 (source: release evidence, VERSION, publication manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
