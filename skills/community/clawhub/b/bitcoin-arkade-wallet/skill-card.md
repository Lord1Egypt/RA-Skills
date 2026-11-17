## Description:

Send and receive Bitcoin over Arkade (offchain), onchain (via onboard/offboard), and Lightning. Swap USDC/USDT stablecoins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiero](https://clawhub.ai/user/tiero)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage an Arkade Bitcoin wallet from an agent, including receiving addresses, balances, offchain and onchain Bitcoin payments, Lightning invoices and payments, and BTC-to-stablecoin swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real cryptocurrency funds through send, offboard, Lightning payment, swap, claim, and refund commands.

Mitigation: Require explicit user confirmation before any funds-moving command and display the amount and destination before execution.

Risk: Wallet keys or seed material could be exposed through unsafe CLI use or untrusted hosts.

Mitigation: Do not pass any private key or seed phrase to the CLI, protect local wallet configuration, and keep only small or test funds unless the package and host are trusted.

Risk: Unpinned npx or pnpm dlx installation examples can execute mutable package versions.

Mitigation: Pin and verify package versions before installation or execution.

Risk: The security verdict is suspicious because the skill is a real cryptocurrency wallet and some documentation patterns can expose wallet keys.

Mitigation: Review carefully before installing and scan the release before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tiero/skills/bitcoin-arkade-wallet)
- [Arkade Documentation](https://docs.arkadeos.com)
- [Arkade Default Server](https://arkade.computer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CLI output, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet addresses, balances, transaction identifiers, Lightning invoices, swap quotes, and local wallet configuration guidance.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
