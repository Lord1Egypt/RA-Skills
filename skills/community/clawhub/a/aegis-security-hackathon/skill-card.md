## Description: <br>
Blockchain security scanner for AI agents (testnet). Pay with Base Sepolia USDC via x402 protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SwiftAdviser](https://clawhub.ai/user/SwiftAdviser) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to check token, address, and transaction risk before interacting with EVM assets. It is intended for testnet x402-paid security checks on supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction simulation sends wallet addresses and transaction payloads to an external Aegis402 service. <br>
Mitigation: Use a dedicated low-value testnet wallet and only submit wallet or transaction details you are comfortable sharing with the provider. <br>
Risk: Paid endpoints consume Base Sepolia testnet USDC through the x402 payment flow. <br>
Mitigation: Expect API requests to require testnet payment and confirm the request target before retrying with payment proof. <br>
Risk: Production or sensitive trading workflows may expose strategy or account details to the provider. <br>
Mitigation: Review the provider's privacy, logging, and retention practices before using the skill for production or sensitive workflows. <br>


## Reference(s): <br>
- [Hackathon API](https://hackathon.aegis402.xyz) <br>
- [Hackathon API base](https://hackathon.aegis402.xyz/v1) <br>
- [Skill metadata](https://hackathon.aegis402.xyz/skill.json) <br>
- [x402 Protocol documentation](https://docs.x402.org) <br>
- [Base Sepolia faucet](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet) <br>


## Skill Output: <br>
**Output Type(s):** [json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, TypeScript, and JSON examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Base Sepolia testnet USDC for paid endpoint access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
