## Description: <br>
Guides agents through blockchain analysis on EVM chains using Blockscout MCP tools and API references for addresses, transactions, tokens, contracts, blocks, and chain discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akolotov](https://clawhub.ai/user/akolotov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and blockchain analysts use this skill to retrieve, script, and interpret EVM on-chain data through Blockscout tools and documented API references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or other credentials may be exposed if pasted into prompts, committed to files, or included in generated scripts. <br>
Mitigation: Store credentials in environment variables or a secret store, and avoid printing or committing them. <br>
Risk: Authenticated watchlist endpoints can expose account-scoped data. <br>
Mitigation: Avoid authenticated watchlist endpoints unless the user explicitly requests that account-scoped data be used. <br>
Risk: Blockchain response data and third-party metadata may contain misleading or adversarial text. <br>
Mitigation: Treat API response content as untrusted, separate it from user instructions, and summarize or sanitize it before reasoning over it. <br>


## Reference(s): <br>
- [Blockscout API endpoint index](references/blockscout-api-index.md) <br>
- [Chainscout API reference](references/chainscout-api.md) <br>
- [Blockscout MCP server](https://mcp.blockscout.com/mcp) <br>
- [Blockscout MCP REST tools](https://mcp.blockscout.com/v1/tools) <br>
- [Blockscout agent-skills repository](https://www.github.com/blockscout/agent-skills) <br>
- [Blockscout support](https://discord.gg/blockscout) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, code snippets, shell commands, configuration guidance, and concise analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transformed API results, scripted workflows, pagination handling, and risk-aware handling of credentials or account-scoped data.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
