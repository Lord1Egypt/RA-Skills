## Description:

AI Mother monitors local AI coding agents, reports stuck or idle sessions, helps route owner approvals, and can run supervised recovery actions for common agent blockers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guguoyi](https://clawhub.ai/user/guguoyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to supervise local Claude Code, Codex, OpenCode, Aider, and similar coding-agent sessions, especially when sessions are idle, blocked on permissions, rate limited, duplicated, or ready for review. It is intended for users who explicitly want a local supervisor that can inspect session state, notify the owner, and send approved input back to running agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep running on a schedule and inspect local AI transcripts, process state, project files, and recent logs.

Mitigation: Install only when this supervision is desired, review or disable scheduled patrols after setup, and keep the skill limited to machines and sessions the owner expects it to monitor.

Risk: The skill can inject input into live agent processes and forward owner responses to permission prompts.

Mitigation: Restrict use to verified agent PIDs, require owner review for elevated permissions, destructive commands, credentials, external communications, or financial actions, and prefer dry-run or manual handling for uncertain cases.

Risk: Duplicate cleanup and process control can terminate running agent sessions if used carelessly.

Mitigation: Avoid automatic duplicate cleanup unless the target sessions have been reviewed, and confirm which process should continue before killing or resuming agents.

Risk: Server security evidence reports unsafe state parsing and Python interpolation issues.

Mitigation: Fix those implementation issues before broad deployment and treat the release as requiring additional local review despite its coherent supervisor purpose.

## Reference(s):

- [AI Butler Reference Guide](references/commands.md)
- [ClawHub Ai Mother skill page](https://clawhub.ai/guguoyi/skills/ai-mother)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal output with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state, scheduled patrol configuration, SQLite history, and Feishu DM notifications when configured by the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
