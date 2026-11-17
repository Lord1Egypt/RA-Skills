## Description:

Manage and monitor multiple OpenClaw agents, including status checks, broadcasts, logs, pause and resume commands, health checks, and workspace management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to coordinate multiple agents from a CLI, inspect agent activity, send messages, run health checks, and manage local agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful local workspace and agent controls through unsafe shell commands that can delete data or run unintended commands.

Mitigation: Review before installing, use only in a contained OpenClaw environment with trusted agent IDs and workspace names, and avoid exposing the CLI to untrusted input.

Risk: Workspace removal should be treated as permanent deletion.

Mitigation: Restrict workspace removal to trusted operators and confirm that the target workspace is disposable before running removal commands.

Risk: The shell-based implementation is not suitable for production use without hardening.

Mitigation: Add strict input validation and replace shell command construction with filesystem and process APIs before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lunaviva211-sketch/skills/colmena-manager)
- [Publisher Profile](https://clawhub.ai/user/lunaviva211-sketch)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational CLI guidance for agent monitoring, messaging, log inspection, pause/resume control, health checks, and workspace management.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
