## Description:

Mirror congressional stock trades with automated broker execution and risk management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mainfraame](https://clawhub.ai/user/mainfraame)

### License/Terms of Use:

MIT

## Use Case:

Developers and traders use this skill to configure and operate a congressional-trade mirroring bot that collects official disclosure data, produces trading recommendations, and can route orders through E*TRADE. It also provides setup, backtesting, cron automation, and notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real brokerage trades.

Mitigation: Use sandbox or paper-trading credentials first, require explicit per-order approval before live use, and enforce strict spending and position limits.

Risk: Broker and Telegram credentials may be persisted locally.

Mitigation: Store secrets outside committed files, prefer environment variables or ignored secrets files, and rotate any exposed E*TRADE keys.

Risk: Cron, systemd, or background execution can run trading workflows unattended.

Mitigation: Disable scheduled execution until the exact commands have been audited, then monitor logs and alerts during any limited rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mainfraame/skills/etrade-pelosi-bot)
- [Congressional Data documentation](docs/CONGRESSIONAL_DATA.md)
- [Senate Financial Disclosures](https://efdsearch.senate.gov/search/)
- [House Financial Disclosures](https://disclosures-clerk.house.gov/FinancialDisclosure)
- [STOCK Act information](https://www.congress.gov/bill/112th-congress/house-bill/1148)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install dependencies, configure broker credentials, authenticate E*TRADE access, run backtests, and schedule recurring execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
