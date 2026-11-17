## Description:

Etherlink blockchain interaction - EVM-compatible L2 on Tezos. Supports mainnet and shadownet testnet via MCP server. Use for balance checks, transactions, smart contracts, and token operations on Etherlink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efekucuk](https://clawhub.ai/user/efekucuk)

### License/Terms of Use:


## Use Case:

Developers and web3 operators use this skill to configure Etherlink MCP access, inspect balances and blocks, send transactions, call contracts, and work with token operations on Etherlink mainnet or shadownet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned MCP package can expose the agent to unexpected package changes.

Mitigation: Pin and verify the MCP server package or source commit before installation or execution.

Risk: Wallet private keys enable irreversible asset-moving actions on Etherlink.

Mitigation: Prefer read-only mode, avoid production private keys, use a low-value testnet wallet or external signer, and require explicit confirmation for every destination, amount, contract, network, and fee before signing.

Risk: Public RPC endpoints are rate-limited and may affect reliability under higher traffic.

Mitigation: Use batching, respect the documented request limit, or configure a dedicated RPC endpoint for production workloads.

## Reference(s):

- [Etherlink Skill Page](https://clawhub.ai/efekucuk/skills/etherlink-skill)
- [Etherlink Docs](https://docs.etherlink.com/)
- [Etherlink Bridging Docs](https://docs.etherlink.com/building-on-etherlink/bridging)
- [Etherlink Explorer](https://explorer.etherlink.com)
- [Etherlink Shadownet Explorer](https://shadownet.explorer.etherlink.com)
- [Etherlink Shadownet Faucet](https://shadownet.faucet.etherlink.com)
- [Etherlink Network Reference](references/networks.md)
- [Etherlink vs Standard Ethereum](references/differences.md)
- [Etherlink MCP Server Setup](references/mcp-setup.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, markdown]

**Output Format:** [Markdown with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide read-only RPC queries or write operations that require explicit wallet private-key configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
