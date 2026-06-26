## Description: <br>
ERC-8004 Trustless Agents helps agents register on-chain, query ERC-8004 registries, and submit or inspect reputation feedback on Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sp0oby](https://clawhub.ai/user/sp0oby) <br>

### License/Terms of Use: <br>
CC0 - Public Domain <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare registration metadata, register or update ERC-8004 agents on Ethereum, query registry state, and submit reputation feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can sign and submit real, irreversible Ethereum transactions, including on mainnet, when a private key is configured. <br>
Mitigation: Use Sepolia and --dry-run first, verify the selected network and contract addresses, and require explicit approval before mainnet register, set-uri, or feedback commands. <br>
Risk: The skill can use a raw Ethereum private key from the environment or a local wallet file. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing private keys on the command line, and review local key material before execution. <br>


## Reference(s): <br>
- [EIP-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 Official Website](https://8004.org) <br>
- [ERC-8004 Reference Implementation](https://github.com/erc-8004/erc-8004-contracts) <br>
- [A2A Protocol](https://a2a-protocol.org/) <br>
- [Ethereum Magicians ERC-8004 Discussion](https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Ethereum network, contract address, wallet, private key, agent URI, and feedback inputs supplied by the user.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
