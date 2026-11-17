## Description:

Skill that restores conversation context when users want to continue where they left off by reading compressed context files, extracting recent operations, projects, and tasks, and producing structured work-state summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexunitario-sketch](https://clawhub.ai/user/alexunitario-sketch)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to resume interrupted or newly started sessions by restoring project status, pending tasks, recent operations, and timeline context from compressed session files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background cron monitoring and auto-restore behavior can create persistence and execution risk.

Mitigation: Review and disable cron and auto-restore paths unless background monitoring is explicitly required.

Risk: Restored conversation context may contain sensitive project or task information.

Mitigation: Treat restored context as sensitive and limit use of notification or forwarding hooks to audited destinations under the user's control.

Risk: The documented crontab pipeline can overwrite existing scheduled jobs if used carelessly.

Mitigation: Preserve and review existing crontab entries before installing any generated monitoring schedule.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexunitario-sketch/skills/context-restore)
- [Usage Guide](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Design Decisions](references/design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text reports, optional JSON summaries, Python API results, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports minimal, normal, and detailed report levels; optional timeline, filtering, diff, auto-monitoring, confirmation, file output, and Telegram chunking modes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
