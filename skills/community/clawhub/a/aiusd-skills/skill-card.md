## Description:

AIUSD trading and account management skill. Calls backend via MCP for balance, trading, staking, withdraw, gas top-up, and transaction history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to manage AIUSD balances, trading accounts, trade execution, staking, withdrawals, gas top-ups, deposits, authentication recovery, and transaction history through a conversational assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate trades, staking, unstaking, withdrawals, and gas top-ups that may move real funds.

Mitigation: Require explicit user confirmation of action, asset, amount, destination address, network, and expected fees before any funds-moving operation.

Risk: Install and authentication flows run local commands and may remove existing credential cache files.

Mitigation: Install in a dedicated directory with a low-privilege account, back up any existing aiusd-skill directory, and review local command effects before running setup or re-authentication.

Risk: The security scanner verdict is suspicious because local install/auth behavior lacks enough user confirmation for sensitive actions.

Mitigation: Inspect the embedded package before installation, avoid automatic npm lifecycle scripts when possible, and require the agent to pause for confirmation before trade, withdrawal, staking, unstaking, or gas top-up requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaunceyliu/skills/aiusd-skills)
- [AIUSD Official Website](https://aiusd.ai)
- [AIUSD OAuth Login](https://mcp.alpha.dev/oauth/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger account, trading, staking, withdrawal, gas, transaction-history, install, and authentication workflows through an agent.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact build-info reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
