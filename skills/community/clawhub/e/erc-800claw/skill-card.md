## Description: <br>
The OpenClaw entry point for ERC-8004 agent identity and reputation. Register agents on-chain, query identities, give and receive feedback ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primer-dev](https://clawhub.ai/user/primer-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to register ERC-8004 agent identities, query on-chain identity and reputation records, and submit reputation feedback through CLI or SDK workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an Ethereum private key for mainnet on-chain registration or feedback actions. <br>
Mitigation: Use a low-value wallet, start on Sepolia/testnet, verify package sources before installation, and require explicit approval before any mainnet transaction. <br>


## Reference(s): <br>
- [ERC-8004 Protocol](https://8004.org) <br>
- [EIP-8004](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-800Claw npm package](https://npmjs.com/package/erc-800claw) <br>
- [ERC-800Claw PyPI package](https://pypi.org/project/erc-800claw) <br>
- [Skill page](https://clawhub.ai/primer-dev/erc-800claw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that read from or write to Ethereum networks and require wallet environment variables.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
