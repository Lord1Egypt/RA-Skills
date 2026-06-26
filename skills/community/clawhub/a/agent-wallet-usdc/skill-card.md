## Description: <br>
Multi-chain wallet management for AI agents. Create wallets, check balances, transfer tokens (USDC/native), and bridge cross-chain. Use when agents need to send/receive payments, check funds, or manage crypto wallets. Supports Solana, Base, and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voltagemonke](https://clawhub.ai/user/voltagemonke) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to create or import wallets, inspect balances, send USDC or native tokens, and bridge USDC across Solana, Base, and Ethereum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real crypto funds and gives an agent direct authority to transfer or bridge assets. <br>
Mitigation: Use fresh, low-value wallets and require explicit human approval before every transfer or bridge. <br>
Risk: Seed phrase exposure or reuse can compromise all funds controlled by the wallet. <br>
Mitigation: Do not reuse existing mainnet seeds; keep seed phrases out of chat, logs, and shared files. <br>
Risk: Transfers and bridges can be sent on the wrong chain, to the wrong recipient, or with unexpected fees. <br>
Mitigation: Verify chain, token, amount, recipient address, and fee details before execution. <br>
Risk: Bundled bridge test and debug scripts may execute real transactions when configured with funded wallets. <br>
Mitigation: Avoid running test or debug scripts with production funds or production wallet seeds. <br>


## Reference(s): <br>
- [Agent Wallet ClawHub page](https://clawhub.ai/voltagemonke/agent-wallet-usdc) <br>
- [Chain Reference](references/chains.md) <br>
- [Agent Wallet website](https://myagentwallet.xyz) <br>
- [Hackathon project page](https://www.moltbook.com/post/b021cdea-de86-4460-8c4b-8539842423fe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and transaction status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet addresses, balances, transaction hashes, bridge state identifiers, and chain-specific status messages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
