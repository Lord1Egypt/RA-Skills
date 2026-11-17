## Description:

Delegate coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-backed bash sessions, including background monitoring and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate complex coding, review, refactoring, and feature-building work to external coding agents while monitoring interactive PTY sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to launch other coding agents with broad local authority, including unsandboxed or auto-approved modes.

Mitigation: Prefer sandboxed runs, isolated worktrees or containers, pinned dependencies, and manual review before commits, pushes, PR comments, or PR creation.

Risk: The skill includes workflows involving package installs and remote GitHub changes.

Mitigation: Avoid `--yolo` examples on sensitive or untrusted repositories and require review before dependency installation or remote repository writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/coding-agent-cp3d)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose launching background PTY sessions and local coding-agent commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
