## Description: <br>
Private DeFi for AI agents that shields tokens into a Railgun ZK privacy pool, swaps privately, lends into Morpho vaults, and bridges cross-chain through LI.FI on Base, Arbitrum, and BSC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmchougule](https://clawhub.ai/user/mmchougule) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to b402's MCP server for private DeFi workflows, including shielded balances, swaps, lending, cross-chain transfers, and strategy execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority over real crypto funds through wallet credentials and DeFi actions. <br>
Mitigation: Use only a dedicated wallet with limited funds, never provide a main-wallet private key, and require manual confirmation for every transaction. <br>
Risk: Installation relies on an npm MCP package and can change Claude Desktop configuration. <br>
Mitigation: Inspect or pin the npm package before running it and verify Claude Desktop configuration changes after installation. <br>
Risk: Private swaps, bridge transfers, vault deposits, and destination addresses can be costly or irreversible if misconfigured. <br>
Mitigation: Manually confirm each swap, bridge route, vault deposit, amount, chain, and destination address before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mmchougule/b402-private-defi) <br>
- [b402 SDK homepage](https://github.com/b402-ai/b402-sdk) <br>
- [b402 MCP package](https://npmjs.com/package/b402-mcp) <br>
- [b402 SDK package](https://npmjs.com/package/@b402ai/sdk) <br>
- [b402 starter](https://github.com/b402-ai/b402-starter) <br>
- [b402 agent starter](https://github.com/b402-ai/b402-agent-starter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, inline shell commands, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node, npx, and a dedicated WORKER_PRIVATE_KEY; the MCP installer can update Claude Desktop configuration.] <br>

## Skill Version(s): <br>
0.4.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
