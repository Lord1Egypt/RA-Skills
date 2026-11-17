## Description:

Executes official Arbitrum bridge tasks with a wallet found on disk, including deposits, withdrawals, claims, status checks, and stuck-bridge diagnosis across Ethereum, Arbitrum One, Arbitrum Nova, and testnets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merdikim](https://clawhub.ai/user/merdikim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare or execute official Arbitrum bridge deposits, withdrawals, claims, tracking, and stuck-bridge diagnosis. It helps enforce route checks, timing expectations, USDC versus USDC.e distinctions, and final user confirmation before transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad authority to find and use local wallet credentials for real Arbitrum bridge transactions.

Mitigation: Install only after review, restrict wallet discovery to approved credential paths, require the user to confirm the wallet address and exact transaction before signing, and never expose wallet secrets in chat.

## Reference(s):

- [Routes Reference](references/routes.md)
- [Trigger Reference](references/triggers.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status updates, transaction plans, warnings, and concise execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public wallet addresses and transaction hashes; should not include private keys, seed phrases, raw keystore contents, or secret-bearing file contents.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
