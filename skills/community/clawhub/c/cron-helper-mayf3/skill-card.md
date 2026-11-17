## Description:

Configure, diagnose, and fix OpenClaw cron jobs for scheduled tasks, periodic jobs, timing issues, heartbeat-versus-cron decisions, and time-based automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, inspect, validate, troubleshoot, and repair OpenClaw cron job configuration. It is most useful when scheduled jobs need self-contained prompts, durable state, appropriate timeouts, valid delivery settings, and timezone-aware schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair tools can modify persistent OpenClaw cron job configuration.

Mitigation: Run validators in read-only mode first, keep backups, review diffs, and confirm the target jobs before replacing jobs.json.

Risk: Bulk repair scripts may be unsafe for important configurations until temporary-file and validation issues are resolved.

Mitigation: Avoid bulk repair scripts on important cron configurations until the temporary-file handling and validation concerns identified by security evidence are fixed.

Risk: Incorrect timezone or delivery targets can cause jobs to run at the wrong time or notify the wrong destination.

Mitigation: Confirm schedule timezones, delivery channels, and delivery targets before enabling or updating jobs.

Risk: Stateless cron prompts can repeat work or lose progress when no durable state is written.

Mitigation: Require each cron prompt to specify checkpoint, cursor, log, or state files that the next run can read.

## Reference(s):

- [Cron Job Syntax Guide](artifact/references/syntax-guide.md)
- [Cron Job Troubleshooting Guide](artifact/references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/mayf3/skills/cron-helper-mayf3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation steps, jq filters, cron expressions, OpenClaw commands, and jobs.json configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
