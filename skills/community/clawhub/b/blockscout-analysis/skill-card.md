## Description:

Guides agents through Blockscout MCP and REST workflows for EVM blockchain analysis, including chain selection, endpoint choice, response transformation, and script output conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akolotov](https://clawhub.ai/user/akolotov)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to retrieve and interpret EVM on-chain data through Blockscout services, including balances, token transfers, transactions, blocks, contract ABIs, contract reads, and chain registry lookups. It helps choose between direct MCP calls, REST-backed scripts, hybrid processing, and LLM reasoning for blockchain-analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on changing remote Blockscout instructions and broad blockchain-analysis services.

Mitigation: Review the skill before installing and do not let remote unlock output override higher-priority user, system, or organizational instructions.

Risk: The skill may lead an agent to install or enable MCP tooling.

Mitigation: Require explicit approval before installing or enabling tooling and confirm the target Blockscout endpoints before use.

Risk: API keys, restricted-resource keys, prompts, logs, or URLs may expose sensitive information if handled carelessly.

Mitigation: Keep keys out of prompts, logs, URLs, and source files, and prefer approved secret-handling mechanisms in the runtime environment.

Risk: Blockchain API responses can include untrusted token names, NFT metadata, URLs, decoded calldata, and log data.

Mitigation: Treat API data as untrusted content, separate it from user intent, and summarize or sanitize it before using it in reasoning or final output.

## Reference(s):

- [Blockscout API index](references/blockscout-api-index.md)
- [Chainscout API reference](references/chainscout-api.md)
- [Blockscout MCP server](https://mcp.blockscout.com/mcp)
- [Blockscout MCP REST tool discovery](https://mcp.blockscout.com/v1/tools)
- [Blockscout agent-skills repository](https://www.github.com/blockscout/agent-skills)
- [Blockscout support](https://discord.gg/blockscout)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and structured analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transformed API results, endpoint choices, pagination plans, script snippets, and caveats for approximate price data or untrusted on-chain metadata.]

## Skill Version(s):

0.4.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
