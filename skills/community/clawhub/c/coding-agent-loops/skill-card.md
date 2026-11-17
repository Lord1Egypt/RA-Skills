## Description:

Run long-lived AI coding agents (Codex, Claude Code) in persistent tmux sessions with Ralph retry loops and completion hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luke-deltadesk](https://clawhub.ai/user/luke-deltadesk)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to run multi-step coding tasks, PRD-based workflows, and stalled agent work in persistent tmux sessions with retry loops and completion notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run long-lived autonomous coding-agent loops in repositories.

Mitigation: Install only after review, keep an active inventory of tmux sessions, monitor pane output, and kill sessions when work is complete.

Risk: The documented prerequisite installs ralphy-cli globally without a pinned version.

Mitigation: Pin and verify ralphy-cli before installation and avoid global installation where possible.

Risk: Shell templates may be unsafe if untrusted issue text, task text, or paths are pasted directly into commands.

Mitigation: Do not paste untrusted text into shell templates; quote and validate repository paths and task inputs before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tmux, Ralph, Codex, Claude Code, and OpenClaw command patterns for long-running coding-agent sessions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
