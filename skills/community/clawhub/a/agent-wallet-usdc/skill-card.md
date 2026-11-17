## Description:

Agent Wallet lets AI agents create and manage Solana, Base, and Ethereum wallets, check balances, transfer USDC or native tokens, and bridge USDC cross-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voltagemonke](https://clawhub.ai/user/voltagemonke)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to give agents wallet-management and payment capabilities across Solana, Base, and Ethereum. It is suited to creating wallets, checking funds, transferring tokens, and bridging USDC when a human has reviewed the requested transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate token transfers and cross-chain bridges that move funds.

Mitigation: Use disposable or low-value test wallets unless reviewed, and require human approval of recipient, chain, amount, and network before execution.

Risk: Seed phrases and private keys control wallet funds.

Mitigation: Do not reuse an existing funded mnemonic; store WALLET_SEED_PHRASE only in a controlled environment and do not paste seed phrases into chat.

Risk: Bundled bridge test scripts may execute transactions with the configured seed.

Mitigation: Do not run test bridge scripts with real funds or production mnemonics; inspect commands before allowing execution.

Risk: Allowance and transaction confirmation behavior requires review.

Mitigation: Review approvals, allowances, and final transaction hashes after each transfer or bridge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/voltagemonke/skills/agent-wallet-usdc)
- [Chain Reference](references/chains.md)
- [AgentWallet website](https://myagentwallet.xyz)
- [Hackathon post](https://www.moltbook.com/post/b021cdea-de86-4460-8c4b-8539842423fe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transaction status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet addresses, balances, transaction hashes, bridge status, and environment variable guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
