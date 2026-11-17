## Description:

Agent Wallet CLI helps agents manage self-custodial crypto wallets for balances, transfers, signing, approvals, transaction history, x402 payments, and wallet lifecycle workflows across Ethereum, Solana, Polygon, Arbitrum, and Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donald-jackson](https://clawhub.ai/user/donald-jackson)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use this skill to automate wallet setup, balance checks, token transfers, signing, approvals, transaction history, and x402 payment workflows through agent-wallet-cli. It is intended for self-custodial wallet operations where fund access and session-token handling require human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant agents real fund-control authority through wallet session tokens and transaction commands.

Mitigation: Unlock manually where possible, provide only short-lived session tokens, test with small amounts, and dry-run before transactions involving meaningful value.

Risk: Password, mnemonic, and session-token examples can expose sensitive wallet material if copied into shell history, logs, or agent context.

Mitigation: Avoid giving agents WALLET_PASSWORD or mnemonics, prefer secure prompts or stdin, and never log or share session tokens or recovery phrases.

Risk: The documented global npm install is not pinned, so the installed CLI may differ from the reviewed version.

Mitigation: Review the package source and npm provenance, then pin or otherwise verify the CLI version before using real funds.

Risk: Confirmation-skipping flags and x402 payments can authorize spending without a final human prompt.

Mitigation: Avoid --yes for meaningful value, use dry-run first, and set tight x402 maximums.

## Reference(s):

- [Agent Wallet CLI ClawHub page](https://clawhub.ai/donald-jackson/skills/agent-wallet-cli)
- [agent-wallet-cli repository](https://github.com/donald-jackson/agent-wallet-cli)
- [agent-wallet-cli npm package](https://www.npmjs.com/package/agent-wallet-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command guidance may involve sensitive wallet operations and should favor dry-run checks, manual unlock, short-lived tokens, and explicit spending limits.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
