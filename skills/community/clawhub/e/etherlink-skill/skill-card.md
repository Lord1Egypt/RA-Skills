## Description: <br>
Etherlink blockchain interaction - EVM-compatible L2 on Tezos. Supports mainnet and shadownet testnet via MCP server. Use for balance checks, transactions, smart contracts, and token operations on Etherlink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efekucuk](https://clawhub.ai/user/efekucuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and web3 operators use this skill to configure an Etherlink MCP workflow and ask an agent to inspect balances, blocks, transactions, smart contracts, and token data on Etherlink mainnet or shadownet. When write access is configured, it can support transaction, token transfer, contract deployment, and state-changing contract call workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect private-key signing authority to an external MCP server that may perform real on-chain writes. <br>
Mitigation: Use read-only mode unless writes are required, verify and pin the MCP server package before installing, avoid valuable mainnet private keys, and prefer a dedicated low-balance or testnet wallet. <br>
Risk: Incorrect network, recipient, amount, gas, or calldata choices can create irreversible blockchain transactions. <br>
Mitigation: Manually confirm every transaction's network, recipient, amount, gas, and contract calldata before approving execution. <br>
Risk: Public Etherlink RPC endpoints are rate-limited and may not suit production throughput. <br>
Mitigation: Use a dedicated RPC provider or run an Etherlink node for higher-throughput production usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/efekucuk/etherlink-skill) <br>
- [Publisher profile](https://clawhub.ai/user/efekucuk) <br>
- [Etherlink](https://etherlink.com) <br>
- [Etherlink Docs](https://docs.etherlink.com/) <br>
- [Etherlink bridge docs](https://docs.etherlink.com/building-on-etherlink/bridging) <br>
- [Etherlink Network Reference](references/networks.md) <br>
- [Etherlink vs Standard Ethereum](references/differences.md) <br>
- [Etherlink MCP Server Setup](references/mcp-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and blockchain operation prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RPC endpoint checks and MCP server configuration for read-only or private-key-enabled workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
