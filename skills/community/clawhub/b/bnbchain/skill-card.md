## Description: <br>
Interact with the BNB Chain MCP server for blocks, contracts, tokens, NFTs, wallet, Greenfield, and ERC-8004 agent tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xlucasliao](https://clawhub.ai/user/0xlucasliao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to query BNB Chain and EVM-compatible network data, inspect contracts and tokens, and run BNB Chain MCP workflows. When a private key is configured, it can also support transfers, contract writes, Greenfield actions, and ERC-8004 agent registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Providing PRIVATE_KEY enables state-changing blockchain actions such as transfers, approvals, contract writes, Greenfield writes, and ERC-8004 registration. <br>
Mitigation: For read-only use, do not provide PRIVATE_KEY. For writes, use a testnet or low-value wallet and confirm the network, recipient or contract, amount, approvals, and fees before any transaction. <br>
Risk: Write actions on the wrong network can cause irreversible financial loss. <br>
Mitigation: Require an explicit network for every write action. If the network is missing, ask before calling the tool and use get_supported_networks to discover valid options. <br>
Risk: Using npx @bnb-chain/mcp@latest fetches the MCP package from npm at runtime. <br>
Mitigation: Review or install the package locally and verify or pin a package version before granting wallet credentials where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xlucasliao/bnbchain) <br>
- [BNB Chain MCP](https://github.com/bnb-chain/bnbchain-mcp) <br>
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 contracts](https://github.com/erc-8004/erc-8004-contracts) <br>
- [Agent Metadata Profile](https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, configuration snippets, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain addresses, transaction hashes, balances, contract data, network names, and safety confirmations.] <br>

## Skill Version(s): <br>
v1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
