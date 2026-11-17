## Description:

Wallet-based credit system for AI agents that lets agents borrow USDC on Somnia without collateral and build credit through successful repayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aroushanpurdue](https://clawhub.ai/user/aroushanpurdue)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure AI agents for wallet-based lending flows on Somnia Testnet, including bot registration, borrow permission setup, wallet credit checks, USDC borrowing, and repayment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill examples involve signing on-chain borrow, approval, and repayment transactions.

Mitigation: Verify the network, API provider, contract addresses, token amounts, decimals, and every wallet prompt before signing.

Risk: The borrow permission example uses a non-expiring permission.

Mitigation: Prefer short expirations and minimal limits, and confirm there is a way to revoke or reduce permissions after borrowing or repayment.

Risk: The security verdict is suspicious because the DeFi workflow has limited risk guidance for transaction-signing behavior.

Mitigation: Install only when the operator understands the transaction-signing requirements and has reviewed the lending flow before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aroushanpurdue/skills/ai-agent-lending)
- [Website](https://yoursite.com)
- [Agent docs](https://yoursite.com/agent)
- [Leaderboard](https://yoursite.com/leaderboard)
- [FAQ](https://yoursite.com/faq)
- [Somnia Shannon Explorer](https://shannon-explorer.somnia.network)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with JavaScript, HTTP, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENDING_API_URL and wallet-signing context for blockchain transaction examples.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
