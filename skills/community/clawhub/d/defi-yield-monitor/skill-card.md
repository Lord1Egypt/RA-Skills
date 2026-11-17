## Description:

Monitors DeFi lending and savings positions across Aave v3, SparkLend, Spark Savings, and Kamino, including balances, APYs, health factors, and realized yield.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor DeFi lending, savings, portfolio health, APY, realized yield, and risk alerts for configured EVM and Solana wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and repeatedly runs mutable external code for sensitive DeFi portfolio monitoring without integrity controls.

Mitigation: Use a pinned, reviewed version of the monitor and verify the repository contents before setup or repeated execution.

Risk: Wallet addresses are stored locally and portfolio summaries may be sent to chat services.

Mitigation: Use dedicated wallets or channels where privacy matters, minimize configured addresses, and review delivery settings before enabling reports.

Risk: Automated cron reports can repeatedly execute the monitor before integrity checks and removal instructions are in place.

Mitigation: Avoid automated reports until integrity checks, operational ownership, and removal steps have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/defi-yield-monitor)
- [Source repository listed in skill artifact](https://github.com/reed1898/defi-yield-monitor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON reports with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include wallet-level positions, APY, health factor, realized yield, and risk alerts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
