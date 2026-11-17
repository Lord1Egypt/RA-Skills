## Description:

Ccclub helps agents check a user's coding-agent leaderboard, including token usage, cost, rank among friends, and setup or join status across Claude Code, Codex, OpenCode, Amp, and pi-agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazzzystar](https://clawhub.ai/user/mazzzystar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect coding-agent usage, cost, and leaderboard rank, and to set up or join a shared ccclub group when the CLI is not initialized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an unpinned external npm package.

Mitigation: Use a pinned, verified ccclub package version and inspect the package before running setup commands.

Risk: Setup installs a background sync process that reads coding-agent usage logs and uploads summarized usage and cost counters.

Mitigation: Confirm the uploaded data with `ccclub show-data`, run setup only with user consent, and verify how to disable or uninstall background sync before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mazzzystar/skills/ccclub)
- [Ccclub API notes](https://ccclub.dev/llms.txt)
- [Ccclub read-only leaderboard API](https://ccclub.dev/api/rank/{groupCode}?period=daily&tz={utcOffsetMinutes})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or API response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the ccclub CLI or read-only HTTP API and summarize leaderboard, usage, and cost data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
