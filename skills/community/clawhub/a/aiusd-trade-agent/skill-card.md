## Description:

Trade AIUSD tokens, manage balances, stake, withdraw to wallets, top up gas, view transaction history, and handle authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:

MIT

## Use Case:

External users and bot operators use this skill to manage AIUSD accounts through chat, including balance checks, trades, staking, withdrawals, gas top-ups, deposits, and transaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate trades, staking, withdrawals, and gas top-ups that move crypto assets.

Mitigation: Use it only when asset-moving actions require explicit user approval and the user has confirmed the operation.

Risk: The skill uses local credentials, and re-authentication can delete shared auth state and open a browser login flow.

Mitigation: Treat re-authentication as sensitive and perform it only after a clear auth failure or explicit user request.

Risk: The self-extracting installers remove an existing aiusd-skill directory before installing.

Mitigation: Avoid running the installers over a local installation with uncommitted or user-modified files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaunceyliu/skills/aiusd-trade-agent)
- [AIUSD official website](https://aiusd.ai)
- [MCP Alpha OAuth login](https://mcp.alpha.dev/oauth/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with command and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live tool schemas for account, trading, staking, withdrawal, gas, and transaction operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
