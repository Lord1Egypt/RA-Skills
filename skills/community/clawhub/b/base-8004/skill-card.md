## Description: <br>
Register your AI agent onchain with ERC-8004 on Base. Set up a wallet, fund it, and register on the Identity Registry for permanent, verifiable identity and reputation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squirt11e](https://clawhub.ai/user/squirt11e) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create or configure a Base mainnet wallet, fund it for gas, register an agent with ERC-8004, and update the agent metadata URI after registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys may be exposed through logs, commits, screen recordings, or insecure environment handling. <br>
Mitigation: Use a fresh low-value wallet, keep the private key out of logs and source control, store it securely, and ensure `.env` is ignored before use. <br>
Risk: Transactions may be signed against the wrong chain or contract address. <br>
Mitigation: Verify Base mainnet and the documented registry contract addresses before signing or broadcasting any transaction. <br>
Risk: Agent metadata and service endpoints published onchain may be permanently public. <br>
Mitigation: Publish only names, descriptions, images, and service endpoints that are intended for public discovery. <br>


## Reference(s): <br>
- [Base 8004 on ClawHub](https://clawhub.ai/squirt11e/base-8004) <br>
- [ERC-8004 protocol homepage](https://8004.org) <br>
- [ERC-8004 registration schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>
- [Base](https://base.org) <br>
- [BaseScan Identity Registry](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) <br>
- [BaseScan Reputation Registry](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63) <br>
- [viem](https://viem.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup, funding checks, onchain transaction examples, and metadata update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
