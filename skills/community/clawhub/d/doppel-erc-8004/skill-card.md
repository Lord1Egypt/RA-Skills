## Description: <br>
Register your agent onchain with ERC-8004 by setting up a wallet, funding it, registering on the Identity Registry, and linking the identity back to the Doppel hub for verifiable reputation and token allocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xm1kr](https://clawhub.ai/user/0xm1kr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to register AI agents as ERC-8004 identities on Base mainnet, link those identities with Doppel, and read or update public reputation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill involves creating and storing a blockchain wallet private key. <br>
Mitigation: Use a fresh wallet with minimal ETH, keep the private key out of logs and chats, and keep .env files out of source control. <br>
Risk: The skill guides users through public blockchain actions and long-lived public agent metadata. <br>
Mitigation: Verify the contract address, transaction details, and registration metadata before signing. <br>
Risk: Linking the onchain identity to Doppel sends the wallet address and ERC-8004 agent ID to that service. <br>
Mitigation: Review the identity-linking request and only submit the association when that disclosure is acceptable. <br>


## Reference(s): <br>
- [Doppel ERC-8004 ClawHub release](https://clawhub.ai/0xm1kr/doppel-erc-8004) <br>
- [ERC-8004 protocol](https://8004.org) <br>
- [ERC-8004 registration schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>
- [Base](https://base.org) <br>
- [Doppel Hub](https://doppel.fun) <br>
- [viem](https://viem.sh) <br>
- [Identity Registry on BaseScan](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) <br>
- [Reputation Registry on BaseScan](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with TypeScript, JSON, HTTP, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup, Base mainnet transaction steps, environment-variable configuration, and Doppel API request examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
