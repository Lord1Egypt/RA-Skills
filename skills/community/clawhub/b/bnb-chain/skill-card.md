## Description:

Basic BNB Chain operations: check balances, send BNB, and send BEP-20 tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawzai](https://clawhub.ai/user/clawzai)

### License/Terms of Use:

ISC

## Use Case:

Developers and blockchain operators use this skill to inspect BNB Chain wallet and BEP-20 token balances, submit transfers, derive wallet addresses from private keys, and inspect transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys.

Mitigation: Avoid passing private keys on the command line; prefer environment variables, secure storage, a safer signer, or a dedicated low-value wallet.

Risk: The skill can submit irreversible BNB and BEP-20 token transfers without an additional confirmation step.

Mitigation: Manually verify recipient, token contract, amount, chain, and fees before any send operation, and test first with small amounts.

Risk: The security verdict is suspicious because the behavior can move funds immediately.

Mitigation: Review the skill carefully before installing or running it, and only use it with wallets and amounts you can afford to risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawzai/skills/bnb-chain)
- [Default BNB Chain RPC endpoint](https://bsc-dataseed.binance.org/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands; helper script responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and ethers.js; can use BNB_PRIVATE_KEY and BNB_RPC_URL environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
