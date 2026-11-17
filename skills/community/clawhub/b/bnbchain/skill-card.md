## Description:

Interact with the BNB Chain Model Context Protocol (MCP) server for blocks, contracts, tokens, NFTs, wallet operations, Greenfield, and ERC-8004 agent tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xlucasliao](https://clawhub.ai/user/0xlucasliao)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to connect an agent to the BNB Chain MCP server for EVM chain queries, token and NFT checks, contract interaction guidance, and explicitly confirmed state-changing blockchain operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an npm package that can change over time.

Mitigation: Use a pinned and reviewed package version where possible before enabling the MCP server.

Risk: State-changing blockchain tools can use private keys and create irreversible transactions.

Mitigation: Do not provide a private key for read-only tasks; for writes, use a dedicated low-value or testnet wallet in a restricted MCP server environment.

Risk: Accidental mainnet execution can cause financial loss.

Mitigation: Require an explicit network for every write operation and confirm recipient, amount, contract, approval limit, calldata, and network before any transaction.

## Reference(s):

- [ClawHub bnbchain Skill Page](https://clawhub.ai/0xlucasliao/skills/bnbchain)
- [BNB Chain MCP Documentation](https://github.com/bnb-chain/bnbchain-mcp)
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8004 Contracts](https://github.com/erc-8004/erc-8004-contracts)
- [Agent Metadata Profile](https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html)
- [8004scan Mainnet](https://www.8004scan.io/)
- [8004scan Testnet](https://testnet.8004scan.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve MCP tool calls that require explicit network selection and optional PRIVATE_KEY configuration for state-changing operations.]

## Skill Version(s):

v1.0.2 (source: server release; artifact frontmatter: 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
