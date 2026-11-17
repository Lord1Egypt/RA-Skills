## Description:

Generates guidance and code for OKX DEX Aggregator swap flows that get swap calldata, handle token approvals, support transaction signing, and broadcast signed transactions on supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronllee](https://clawhub.ai/user/aaronllee)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate OKX DEX swap and broadcast flows into applications, bots, scripts, or agent workflows. It is intended for users who need code or operational guidance for swap calldata retrieval, ERC-20 approvals, transaction signing, MEV protection options, Solana Jito tips, and transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers irreversible approval, signing, and broadcast flows for on-chain transactions.

Mitigation: Require a separate user confirmation before each approval and before each swap broadcast, and only use wallets and amounts the user is prepared to risk.

Risk: Approval calldata can authorize token spending by a router or spender address.

Mitigation: Prefer exact-amount approvals, avoid unlimited approvals, and independently verify the spender address and decoded calldata before signing.

Risk: Raw private keys or signed transactions could expose funds if mishandled.

Mitigation: Use hardware wallets, keystore-backed signers, or policy-enforcing signing services instead of raw private keys, and never log private keys, API secrets, or signed transactions.

Risk: Incorrect token addresses, slippage, nonce handling, or retries can cause loss, failed swaps, or duplicate transaction attempts.

Mitigation: Validate token addresses, amounts, price impact, honeypot flags, slippage settings, and current nonce before signing; do not automatically retry failed broadcasts without checking transaction state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronllee/skills/easy-swap)
- [OKX DEX Aggregator Swap API](https://web3.okx.com/api/v6/dex/aggregator/swap)
- [OKX DEX Broadcast Transaction API](https://web3.okx.com/api/v6/dex/pre-transaction/broadcast-transaction)
- [OKX Web3 API host](https://web3.okx.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JavaScript code examples plus configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API call examples, transaction field mappings, wallet signing guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
