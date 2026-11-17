## Description:

Automated failure detection, diagnosis, and auto-repair system for cron jobs. Monitors task health, fixes common issues automatically, and requests human confirmation when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users who run OpenClaw cron jobs use this skill to monitor task failures, diagnose common error classes, apply routine repairs, and produce notifications or reports when manual intervention is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended repair actions may edit cron jobs or change file permissions from unsafe inputs.

Mitigation: Run under a least-privileged account, restrict write access to cron metadata, validate job IDs and script paths, and require explicit confirmation for chmod or other high-impact repairs.

Risk: Shell-string command execution can amplify malformed or attacker-controlled job metadata.

Mitigation: Prefer a revised implementation that uses argument-array process execution and rejects unexpected characters in job IDs, delivery targets, and script paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/failure-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and Markdown notification messages with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a JSON repair log and may issue OpenClaw cron edit or chmod commands when configured to auto-repair.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
