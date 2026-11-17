## Description:

Etherlink blockchain interaction - EVM-compatible L2 on Tezos. Supports mainnet and shadownet testnet via MCP server. Use for balance checks, transactions, smart contracts, and token operations on Etherlink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efekucuk](https://clawhub.ai/user/efekucuk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure an Etherlink MCP server and perform Etherlink blockchain tasks such as balance checks, transactions, contract calls, token operations, and block lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup can run unpinned external code.

Mitigation: Pin or verify the MCP server source or package before running it.

Risk: Write operations require private-key access and can move assets or deploy contracts.

Mitigation: Use read-only mode unless transactions are required, avoid primary wallet keys, and prefer a dedicated low-balance wallet.

Risk: Mainnet transactions and contract writes can have irreversible financial impact.

Mitigation: Test workflows on Etherlink Shadownet before using mainnet.

## Reference(s):

- [Etherlink Skill Page](https://clawhub.ai/efekucuk/skills/etherlink)
- [Etherlink](https://etherlink.com)
- [Etherlink Docs](https://docs.etherlink.com/)
- [Etherlink Bridging Docs](https://docs.etherlink.com/building-on-etherlink/bridging)
- [Etherlink Block Explorer](https://explorer.etherlink.com)
- [Etherlink Shadownet Explorer](https://shadownet.explorer.etherlink.com)
- [Etherlink Shadownet Faucet](https://shadownet.faucet.etherlink.com)
- [Etherlink Network Reference](references/networks.md)
- [Etherlink vs Standard Ethereum](references/differences.md)
- [Etherlink MCP Server Setup](references/mcp-setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, bash, and blockchain operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Etherlink RPC endpoints, MCP configuration, wallet environment variables, and network-specific transaction constraints.]

## Skill Version(s):

1.0.1 (source: server evidence release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
