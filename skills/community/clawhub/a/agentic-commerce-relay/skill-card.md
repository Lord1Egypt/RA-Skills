## Description:

Run the CCTP relay to burn USDC on a source chain and mint on a destination chain, returning verifiable receipts for multichain agent-to-agent settlement with optional Moltbook discovery and integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nativ3ai](https://clawhub.ai/user/nativ3ai)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to prepare and run USDC CCTP relay flows for cross-chain settlement. It is intended for workflows that need machine-readable receipts for burn, message, mint, and recipient details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real blockchain transactions that can transfer value.

Mitigation: Use a dedicated low-balance wallet, start on testnets or with minimal amounts, and verify transaction details before execution.

Risk: The relay flow requires a wallet private key and RPC endpoints.

Mitigation: Keep private keys out of logs, shell history, committed files, and shared configuration; review the relay script before running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nativ3ai/skills/agentic-commerce-relay)
- [Moltbook](https://www.moltbook.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON receipt fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relay receipts include burnTx, messageHash, mintTx, and recipient when the underlying relay completes successfully.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
