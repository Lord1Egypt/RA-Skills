## Description:

Schedule and manage recurring tasks with cron and systemd timers. Use when setting up cron jobs, writing systemd timer units, handling timezone-aware scheduling, monitoring failed jobs, implementing retry patterns, or debugging why a scheduled task didn't run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill as a command-reference guide for scheduling recurring and one-off tasks, managing cron and systemd timers, handling timezone and DST behavior, and troubleshooting failed scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes destructive and privileged scheduling examples such as removing crontabs, scheduling reboots, enabling systemd timers, and writing logs under /var/log.

Mitigation: Review commands before execution, test on non-production systems first, and require explicit operator approval for destructive or privileged actions.

Risk: The security summary flags unsafe shell patterns and wrapper or lock snippets that may need hardening before production use.

Mitigation: Harden shell snippets for the target environment, including quoting, permissions, lock handling, logging paths, and failure behavior before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gitgoodordietrying/skills/cron-scheduling)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, cron, and systemd unit examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before applying destructive, privileged, or production scheduling commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
