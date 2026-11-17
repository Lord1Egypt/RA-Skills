## Description:

Background daemon that monitors QuantConnect backtests with adaptive polling, real-time equity tracking, drawdown early-stop, auto-download, and auto-diagnosis while surviving terminal disconnection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to register, monitor, and review QuantConnect backtests without keeping a terminal session open. It is intended for workflows that need status checks, logs, downloaded results, and diagnosis summaries from long-running backtests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The background poller can permanently delete QuantConnect backtests when drawdown thresholds are crossed.

Mitigation: Require explicit opt-in or confirmation for early-stop deletion and review drawdown thresholds before enabling the poller.

Risk: Shell-based macOS notifications can run shell commands.

Mitigation: Remove shell-based notifications or replace them with an argument-safe notification API before deployment.

Risk: Result paths can write outside the intended results folder.

Mitigation: Sanitize result names and constrain output paths to a trusted results directory.

Risk: Auto-diagnosis can load unverified code from importable forensics modules.

Mitigation: Disable auto-diagnosis unless the module source is trusted, reviewed, and pinned.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin dependencies and review them before installation in a production environment.

## Reference(s):

- [Backtest Poller on ClawHub](https://clawhub.ai/tltby12341/skills/backtest-poller)
- [Publisher profile](https://clawhub.ai/user/tltby12341)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, CLI status text, logs, JSON, CSV, and diagnosis text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses QuantConnect credentials from environment variables and may create state, log, result JSON, order CSV, and diagnosis text files.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
