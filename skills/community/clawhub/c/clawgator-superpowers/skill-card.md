## Description:

Framework pengembangan perangkat lunak lengkap untuk tim ClawGator. Brainstorming, planning, eksekusi sistematis, TDD, debugging, code review, dan git worktrees. Trigger otomatis sebelum memulai proyek atau perubahan kode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renggap](https://clawhub.ai/user/renggap)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to guide software development work through brainstorming, planning, test-driven development, systematic debugging, code review, verification, and git worktree workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs broad session-start instructions that can steer agent behavior before the user explicitly requests the workflow.

Mitigation: Review or disable startup hook and context-injection behavior before deployment, and install only where this development workflow is intended to actively steer sessions.

Risk: Documented setup and cleanup commands may modify or delete local skill or plugin paths.

Mitigation: Review dependency, build, installation, and cleanup commands before approving them, especially commands that target local extension directories.

## Reference(s):

- [ClawGator Superpowers ClawHub Page](https://clawhub.ai/renggap/skills/clawgator-superpowers)
- [README](README.md)
- [Testing Superpowers Skills](docs/testing.md)
- [Superpowers for Codex](docs/README.codex.md)
- [Superpowers for OpenCode](docs/README.opencode.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write development plans and design documents when the workflow calls for persistent artifacts.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
