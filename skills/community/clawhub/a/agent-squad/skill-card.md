## Description:

Agent Squad manages persistent AI coding squads in tmux sessions with task queues, progress reports, automatic health monitoring, and support for Claude Code, Codex, Gemini CLI, OpenCode, Kimi, Trae, Aider, and Goose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xtimi](https://clawhub.ai/user/0xtimi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, assign work to, monitor, nudge, stop, restart, configure, and archive persistent AI coding squads for software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start unattended agents in full-auto or approval-bypass modes with broad ability to read, write, and execute within the selected project directory.

Mitigation: Use isolated repositories or worktrees, keep credentials and sensitive files out of project directories, and review generated changes before merging or deployment.

Risk: Persistent watchdog behavior can restart agents automatically after crashes and continue work without additional approval.

Mitigation: Disable the watchdog for sensitive work, stop squads when unattended execution is no longer needed, and monitor logs and status reports.

Risk: Status and peek operations may expose raw terminal output, reports, logs, or project details.

Mitigation: Avoid placing secrets in squad-accessible directories and review terminal or report content before sharing it outside the trusted environment.

Risk: The skill initializes git repositories in new project directories and can create task, report, log, and configuration files as part of normal operation.

Mitigation: Run it in disposable or clearly scoped workspaces, keep important work under version control, and inspect generated files and commits regularly.

## Reference(s):

- [Agent Squad on ClawHub](https://clawhub.ai/0xtimi/skills/agent-squad)
- [Publisher profile](https://clawhub.ai/user/0xtimi)
- [Agent Squad homepage](https://github.com/0xTimi/agent-squad)
- [Agent Squad support](https://github.com/0xTimi/agent-squad/issues)
- [OpenClaw](https://openclaw.ai)
- [tmux](https://github.com/tmux/tmux)
- [Full guide](docs/guide.md)
- [Supported AI engines](references/engines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text and markdown status summaries, with shell command results and generated task, report, log, and configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update files in configured squad coordination directories and project directories through the selected unattended agent engine.]

## Skill Version(s):

0.9.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
