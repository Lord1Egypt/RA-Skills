## Description: <br>
Etherlink blockchain interaction - EVM-compatible L2 on Tezos. Supports mainnet and shadownet testnet via MCP server. Use for balance checks, transactions, smart contracts, and token operations on Etherlink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efekucuk](https://clawhub.ai/user/efekucuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Web3 operators use this skill to configure agents for Etherlink mainnet and Shadownet interactions, including balance checks, transactions, smart contract reads and writes, token operations, and RPC troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of an external MCP server that can operate with a wallet private key and perform irreversible on-chain actions. <br>
Mitigation: Review MCP server package provenance before installation, prefer read-only mode, avoid primary wallet keys, and use a dedicated low-balance wallet. <br>
Risk: Transactions and contract calls on Etherlink may move funds or change contract state. <br>
Mitigation: Test on Shadownet first and manually confirm the network, recipient, amount, contract address, and function call before signing. <br>
Risk: Public Etherlink RPC endpoints are rate-limited and some Ethereum JSON-RPC methods are unsupported. <br>
Mitigation: Use documented Etherlink network identifiers and supported methods, and run a dedicated node or provider endpoint for higher throughput. <br>


## Reference(s): <br>
- [Etherlink Skill on ClawHub](https://clawhub.ai/efekucuk/etherlink) <br>
- [Etherlink Docs](https://docs.etherlink.com/) <br>
- [Etherlink Bridging Docs](https://docs.etherlink.com/building-on-etherlink/bridging) <br>
- [Etherlink Network Reference](references/networks.md) <br>
- [Etherlink vs Standard Ethereum](references/differences.md) <br>
- [Etherlink MCP Server Setup](references/mcp-setup.md) <br>
- [Etherlink Mainnet Explorer](https://explorer.etherlink.com) <br>
- [Etherlink Shadownet Explorer](https://shadownet.explorer.etherlink.com) <br>
- [Etherlink Shadownet Faucet](https://shadownet.faucet.etherlink.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RPC endpoint selections, MCP server configuration, transaction guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
