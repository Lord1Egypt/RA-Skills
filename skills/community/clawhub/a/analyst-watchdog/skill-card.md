## Description:

Automated monitoring agent that watches an API scoreboard, detects milestones, writes findings to markdown, and alerts via file-based triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local watchdog that monitors scoreboard and health endpoints, records milestone or promotion findings, and emits file-based alerts for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted localhost API data can influence files that may be read by agents or operators.

Mitigation: Use only with a controlled localhost service, validate API response fields, and treat generated Markdown as untrusted data before downstream use.

Risk: The implementation can read JSON score files outside its intended score directory.

Mitigation: Constrain output and score directories before scheduled use, and restrict score keys to safe identifiers.

Risk: Unattended scheduled execution writes local files without interactive review.

Mitigation: Install only where scheduled writes are expected, and review file paths and alert handling before enabling cron or LaunchAgent execution.

## Reference(s):

- [Analyst Watchdog on ClawHub](https://clawhub.ai/nissan/skills/analyst-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON state, console log text, and Python code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local findings, outbox, alert, and state files; polls a localhost API and does not require external network access.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
