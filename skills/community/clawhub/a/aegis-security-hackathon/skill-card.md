## Description:

Blockchain security scanner for AI agents on testnet, with payment via Base Sepolia USDC using the x402 protocol.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agent builders use this skill to scan tokens and addresses, and to simulate EVM transactions before swaps or signing actions on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, token addresses, and transaction calldata are sent to the Aegis402 service for external lookup and simulation.

Mitigation: Use a constrained testnet wallet and avoid submitting sensitive or unnecessary wallet and transaction data.

Risk: Paid endpoint calls use an x402 payment flow before results are returned.

Mitigation: Set payment limits and confirm calls are using Base Sepolia testnet USDC before integrating automated requests.

Risk: Client examples install x402 dependencies for integration.

Mitigation: Use pinned dependency versions or a reviewed lockfile for any real integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/swiftadviser/skills/aegis-security-hackathon)
- [Hackathon API](https://hackathon.aegis402.xyz)
- [Hackathon API Base](https://hackathon.aegis402.xyz/v1)
- [Published Skill Markdown](https://hackathon.aegis402.xyz/skill.md)
- [Published Skill Metadata](https://hackathon.aegis402.xyz/skill.json)
- [Production Skill](https://aegis402.xyz/skill.md)
- [x402 Protocol Documentation](https://docs.x402.org)
- [Base Sepolia Faucet](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid endpoint calls require x402 payment proof with Base Sepolia testnet USDC.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
