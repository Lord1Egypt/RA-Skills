## Description:

Structured multi-agent collaboration for backend + frontend builds. Use when an orchestrator needs to coordinate a backend engineer and frontend engineer on the same feature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nightknight64](https://clawhub.ai/user/nightknight64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate backend and frontend agents around a shared contract, separate work areas, integration logs, verification steps, and deployment handoff guidance for full-stack feature work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment guidance may affect live services through copy, symlink, configuration, or restart actions.

Mitigation: Require explicit human approval, confirm the target environment, and prepare backups and rollback steps before executing deployment-related actions.

Risk: Symlink-based deployment can point a service at an incomplete incremental build.

Mitigation: Confirm whether a build is full or incremental, integrate changed files into the live tree when needed, and verify the deployment target before restart.

Risk: Backend and frontend agents may diverge from the shared API contract.

Mitigation: Use the SPEC.md contract as the source of truth and verify endpoint paths, request and response shapes, errors, auth flow, and UI states before release.

## Reference(s):

- [Skill release page](https://clawhub.ai/nightknight64/skills/agent-collaboration-protocol)
- [Spec template](references/spec-template.md)
- [Integration log format](references/integration-log.md)
- [Handoff message format](references/handoff-format.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces contract templates, handoff instructions, verification checklists, deployment guidance, and a setup script pattern for coordinated agent work.]

## Skill Version(s):

1.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
