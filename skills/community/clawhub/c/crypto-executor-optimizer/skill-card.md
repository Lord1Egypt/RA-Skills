## Description:

Autonomous optimizer that reviews Binance trading performance every six hours and tunes crypto-executor parameters such as OBI thresholds, Kelly factor, and strategy mix with backup, validation, rollback, restart, and logging steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators who run a Binance crypto-executor bot use this skill to inspect local performance data, choose bounded trading-parameter adjustments, and apply them through supplied shell scripts. It is intended for automated optimization workflows where credential handling, downloaded code, service restarts, and recurring execution have been reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a live crypto trading bot and can restart the trading process after code changes.

Mitigation: Use tightly scoped Binance API keys with withdrawals disabled, limited capital, a dedicated unprivileged account, and human review before enabling automated optimization.

Risk: Setup downloads executor.py and optional crypto_oracle.py from mutable main-branch raw GitHub URLs.

Mitigation: Pin or verify downloaded code before setup and audit both files before execution.

Risk: Setup stores exchange credentials in /workspace/data/bot_config.env and fallback restarts source that file.

Mitigation: Keep the file chmod 600, store credentials as data rather than sourced shell where possible, and rotate keys if the workspace is shared or compromised.

Risk: The optimizer modifies executor.py through pattern replacement and installs recurring execution every six hours.

Mitigation: Confirm optimizer inputs and parameter bounds, rely on backups and syntax validation, monitor logs, and disable the cron job unless recurring changes are explicitly acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/crypto-executor-optimizer)
- [crypto-executor executor.py download](https://raw.githubusercontent.com/georges91560/crypto-executor/main/executor.py)
- [crypto-sniper-oracle download](https://raw.githubusercontent.com/georges91560/crypto-sniper-oracle/main/crypto_oracle.py)
- [crypto-sniper-oracle repository](https://github.com/georges91560/crypto-sniper-oracle)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke supplied shell scripts to apply bounded parameter updates, create backups, validate Python syntax, restart the bot, send optional Telegram notifications, and write optimization logs.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
