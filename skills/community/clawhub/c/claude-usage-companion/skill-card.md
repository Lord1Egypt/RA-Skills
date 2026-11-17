## Description:

Monitors Claude programmatic credit usage from local ccusage data, projects month-end spend, emits alerts, and reminds users to align their interactive Claude session window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decisionvex](https://clawhub.ai/user/decisionvex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill on always-on Claude Code or OpenClaw hosts to monitor programmatic credit-pool burn, project month-end usage, receive threshold alerts, and get an anchor-time reminder for hands-on interactive sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default scheduled setup can repeatedly run a mutable npm package through npx.

Mitigation: Prefer a pinned or locally installed ccusage binary and configure ccusage_cmd accordingly before scheduling.

Risk: Cron installation output and --cron-only mode can alter recurring shell execution if copied or piped without review.

Mitigation: Inspect generated cron lines before adding them, and avoid piping install --cron-only directly to crontab.

Risk: A configured alert_command runs through the shell and receives alert text on stdin.

Mitigation: Only set alert_command to a command you fully trust, and keep config.json writable only by your account.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/decisionvex/skills/claude-usage-companion)
- [Publisher profile](https://clawhub.ai/user/decisionvex)
- [Project website](https://decisionvex.github.io/claude-usage-companion/)
- [ccusage](https://github.com/ryoppippi/ccusage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local usage summaries, projections, threshold alerts, reminder text, and cron setup guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
