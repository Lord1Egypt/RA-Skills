## Description:

Orchestrates the full BMAD Method workflow across OpenClaw and Claude Code for project brainstorming, PRD, architecture, and implementation, with phases 1-3 handled interactively and phase 4 delegated to Claude Code via tmux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrikrexed](https://clawhub.ai/user/henrikrexed)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to guide BMAD project planning with the user, produce planning artifacts, and delegate implementation work to Claude Code through tmux-managed sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive a remote coding agent that changes code and commits work while normal permission prompts are bypassed.

Mitigation: Use an isolated development VM, a dedicated low-privilege account, pinned tool versions, and explicit approval checkpoints before executing or committing changes.

Risk: tmux, SSH, path, and session automation can affect the wrong environment if targets are not validated.

Mitigation: Validate host, user, project path, tmux socket, and session names before sending commands, and define a cleanup plan for monitors and sessions.

## Reference(s):

- [BMAD Claude Code Commands](references/bmad-commands.md)
- [tmux Setup & Interaction Patterns](references/tmux-setup.md)
- [ClawHub skill page](https://clawhub.ai/henrikrexed/skills/bmad-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce BMAD planning artifacts, implementation instructions, code changes, tests, commits, status updates, and review reports through coordinated agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
