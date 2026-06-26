## Description: <br>
AIUSD Core provides structured trading tools and account management for agents that buy or sell assets, check balances, stake funds, and manage positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech-FE-aiusd](https://clawhub.ai/user/tech-FE-aiusd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use AIUSD Core to manage AIUSD trading accounts, check balances, deposit or withdraw funds, trade spot assets and perpetuals, access prediction markets, stake AIUSD, and set conditional monitors through a Node-based CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad real-money trading, transfer, withdrawal, staking, auto-funding, and monitor setup authority. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit confirmation for every trade, withdrawal, staking action, transfer, auto-funding step, and monitor setup. <br>
Risk: Restoring accounts or storing authentication material can expose valuable wallet access. <br>
Mitigation: Avoid restoring valuable mnemonic backups unless necessary, verify where tokens are stored, and log out or rotate credentials when access is no longer needed. <br>
Risk: Deposits can be lost if the wrong stablecoin is sent on a chain with strict deposit rules. <br>
Mitigation: Confirm the chain, asset, minimum amount, and deposit address before transferring funds; use a small test transfer for new routes. <br>


## Reference(s): <br>
- [AIUSD website](https://aiusd.ai) <br>
- [AIUSD Core on ClawHub](https://clawhub.ai/tech-FE-aiusd/aiusd-core) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and user confirmation before trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
