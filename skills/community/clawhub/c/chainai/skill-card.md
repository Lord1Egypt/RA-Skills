## Description:

Ethereum and EVM blockchain CLI skill for signing messages, sending tokens, swapping via 1inch Fusion, checking balances, broadcasting transactions, and managing wallets across Ethereum and BNB Smart Chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kvhnuke](https://clawhub.ai/user/kvhnuke)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use ChainAI to run Ethereum and EVM wallet operations from a non-interactive CLI, including balance checks, signing, transfers, swaps, transaction broadcast, and transaction status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent raw private-key access.

Mitigation: Use only an empty or low-value test wallet, prefer CHAINAI_PRIVATE_KEY over command-line private-key flags, and prevent keys from appearing in logs, chat output, files, URLs, or diagnostics.

Risk: Send, broadcast, and swap commands can trigger irreversible financial transactions.

Mitigation: Require explicit human approval for the exact network, recipient, token, amount, transaction, and swap order before running any broadcast, send, or swap submission path.

Risk: The npm package executes third-party blockchain tooling that may handle funds.

Mitigation: Audit or pin the chainai package before trusting it with funded wallets, and test with low-value accounts before production use.

## Reference(s):

- [ChainAI ClawHub Skill Page](https://clawhub.ai/kvhnuke/skills/chainai)
- [ChainAI Homepage](https://github.com/kvhnuke/chainai)
- [kvhnuke Publisher Profile](https://clawhub.ai/user/kvhnuke)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, and CHAINAI_PRIVATE_KEY for wallet operations; commands may create signatures, transactions, broadcasts, or swap orders.]

## Skill Version(s):

0.0.12 (source: server release metadata; artifact frontmatter and command examples report 0.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
