## Description:

Parameterize and apply a Chinese mutual-fund buy, add, reduce, or hold strategy driven by price drawdown, recurring DCA, cash-pool management, and position limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain and apply a reusable Chinese mutual-fund strategy, including DCA, dip-buy, take-profit, cash-pool, reminder, and reporting workflows. It produces strategy suggestions and local records rather than broker-executed trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores fund strategy state, balances, holdings, and trade history in a local plaintext SQLite database.

Mitigation: Keep the database in a private user directory, avoid shared or synced locations unless protected, and limit access to the local user account.

Risk: Generated buy or sell actions could be mistaken for broker-executed trades.

Mitigation: Treat actions as local strategy records and review them before recording or acting on them outside the skill.

Risk: Market data refreshes fetch fund data from Eastmoney, so availability and data freshness depend on that external source.

Mitigation: Check source availability and skip decisions when required inputs are missing or stale.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanmwx/skills/fund-buying-decision)
- [Data Inputs](artifact/references/data_inputs.md)
- [Strategy Parameters](artifact/references/strategy_parameters.md)
- [Eastmoney Pingzhongdata Endpoint](https://fund.eastmoney.com/pingzhongdata/{fund_code}.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write strategy account state, reminders, and trade history to a local plaintext SQLite database.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
