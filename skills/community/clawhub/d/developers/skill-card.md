## Description: <br>
Longbridge helps agents answer investment-analysis and developer questions using Longbridge market data, CLI workflows, SDK guidance, MCP setup, and LLM documentation references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longbridge](https://clawhub.ai/user/longbridge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and external users use this skill to work with Longbridge financial data and trading tooling, including market analysis, portfolio queries, CLI commands, Python and Rust SDK examples, MCP configuration, and documentation ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to brokerage data and trading workflows after authorization. <br>
Mitigation: Use least-privilege OAuth scopes and avoid granting trading permissions for read-only analysis. <br>
Risk: Agent-assisted order placement, replacement, or cancellation could affect real brokerage accounts. <br>
Mitigation: Require explicit user confirmation before any order placement, replacement, or cancellation. <br>
Risk: The CLI installation path includes a curl-to-shell command. <br>
Mitigation: Inspect the installer before running it and prefer trusted package-manager installation where appropriate. <br>


## Reference(s): <br>
- [Longbridge ClawHub Skill Page](https://clawhub.ai/longbridge/developers) <br>
- [Longbridge OpenAPI Documentation](https://open.longbridge.com) <br>
- [Longbridge LLMs.txt](https://open.longbridge.com/llms.txt) <br>
- [CLI Overview](references/cli/overview.md) <br>
- [MCP Server](references/mcp.md) <br>
- [Python SDK Overview](references/python-sdk/overview.md) <br>
- [Rust SDK Overview](references/rust-sdk/overview.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, command examples, configuration snippets, and explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market-analysis guidance, SDK examples, CLI commands, MCP setup steps, and Longbridge documentation references.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
