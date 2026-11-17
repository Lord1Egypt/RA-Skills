## Description:

Supports native-token and ERC20 transfers on EVM chains by constructing transactions, signing locally, and broadcasting through the OKX API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangchengming666](https://clawhub.ai/user/wangchengming666)

### License/Terms of Use:

MIT

## Use Case:

Developers and wallet operators use this skill to prepare and broadcast BSC native-token or ERC20 transfers from a locally configured wallet. It returns transaction identifiers and explorer links for follow-up after broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real funds from the configured wallet.

Mitigation: Use a dedicated low-balance wallet and inspect recipient, amount, chain, token, and gas settings before broadcasting.

Risk: Private keys and OKX credentials are required and may be exposed in shell startup files or logs.

Mitigation: Avoid storing secrets in shared shell profiles, run only in private environments, and remove or disable debug logging of signed transactions and OKX signatures before use.

Risk: On-chain transfers are irreversible once broadcast.

Mitigation: Treat each generated transaction as final and verify the resulting transaction status using the returned explorer link.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangchengming666/skills/broadcast-sign-transfer)
- [OKX Web3 API endpoint](https://web3.okx.com)
- [BSC public RPC endpoint](https://bsc-dataseed1.binance.org/)
- [BscScan transaction explorer](https://bscscan.com/tx/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with Python and bash snippets; runtime results include order_id, tx_hash, and explorer_url.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires wallet private key and OKX Web3 API credentials; broadcasts irreversible blockchain transactions.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
