## Description:

Agent 上下文管理方法论：通过分层文件体系实现跨 session 记忆延续、职责分离和高效上下文恢复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[349840432m-dev](https://clawhub.ai/user/349840432m-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up layered workspace files, startup protocols, and memory lifecycle practices for long-running agents that need cross-session context. It also provides a Python distillation helper for previewing or appending lessons from daily memory files into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist long-term agent memory and automate updates to MEMORY.md.

Mitigation: Run the distillation script with --dry-run first and review generated entries before writing them to long-term memory.

Risk: Persistent memory files may capture secrets or sensitive personal data if users store them there.

Mitigation: Avoid storing secrets or sensitive personal data in memory files and review memory content before committing or sharing a workspace.

Risk: Recurring cron execution can repeatedly modify persistent memory without direct review.

Mitigation: Do not enable the cron job until the workspace owner is comfortable with recurring persistent updates and has reviewed the script behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/349840432m-dev/skills/agent-context-memory)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [memory_distill.py](artifact/scripts/memory_distill.py)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with example files, shell commands, and a Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MEMORY.md and memory/distill-state.json when the distillation script is run without --dry-run.]

## Skill Version(s):

1.0.0 (source: server release metadata, claw.json, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
