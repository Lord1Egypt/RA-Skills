## Description:

Agile Workflow helps OpenClaw agents decompose, schedule, monitor, and optimize multi-agent workflows with dependency management, quality checks, and task-state tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbcs](https://clawhub.ai/user/xbcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to coordinate complex work such as content creation, software development, documentation, and analysis across multiple agents. It is intended to generate task breakdowns, dependency chains, monitoring output, quality-review guidance, configuration snippets, and operational commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background execution and cron jobs can continue outside the intended workflow scope.

Mitigation: Use an isolated OpenClaw environment and do not enable cron jobs or long-lived daemons until persistence and cleanup boundaries are reviewed.

Risk: Automatic cleanup or external execution paths may affect unrelated OpenClaw data.

Mitigation: Review cleanup commands, restrict workspace paths, and limit execution permissions before enabling automation.

Risk: Automatic report submission can disclose workflow data unexpectedly.

Mitigation: Disable automatic report submission unless the destination and data-handling expectations are approved.

Risk: An exposed dashboard can reveal operational state if it is network-accessible without controls.

Mitigation: Bind the dashboard to localhost and add authentication before exposing it beyond the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbcs/skills/agile-workflow)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [v7.0 user guide](artifact/docs/v7.0-使用指南.md)
- [v7.0 concurrency-safe architecture](artifact/docs/ADD-v7.0-并发安全架构.md)
- [v7.18 token-limit fix](artifact/docs/ADD-v7.18-Token 超限修复.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON, JavaScript, and shell command examples; workflow artifacts may be JSON, Markdown, logs, or task-state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Node.js workflow automation that creates task state, logs, reports, and cleanup actions.]

## Skill Version(s):

7.18.1 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
