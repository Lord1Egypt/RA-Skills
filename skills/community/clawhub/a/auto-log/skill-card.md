## Description:

Automatically creates daily log files that record AI agent events, tasks, todos, and concise activity summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socneo](https://clawhub.ai/user/socneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist local daily activity logs for AI agents, including events, task status, todos, and short summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily logs may retain sensitive prompts, events, or operational details on disk.

Mitigation: Choose a private memory_dir, avoid logging secrets or sensitive prompts, and periodically review or delete retained logs.

Risk: Agents may later read retained logs as historical data.

Mitigation: Ensure agents that read these files treat them only as historical records, not executable instructions.

## Reference(s):

- [Auto Log Skill Release Page](https://clawhub.ai/socneo/skills/auto-log)
- [README](artifact/README.md)
- [Configuration Example](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown log files, text summaries, Python API calls, CLI commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local daily log files to the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
