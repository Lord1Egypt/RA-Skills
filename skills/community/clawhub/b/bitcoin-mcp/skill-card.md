## Description: <br>
47 Bitcoin tools for AI agents, including fee intelligence, mempool analysis, address lookups, transaction decoding, and related Bitcoin MCP workflows backed by the Satoshi API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bortlesboat](https://clawhub.ai/user/Bortlesboat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and use a Bitcoin MCP server for fee estimates, mempool and block inspection, address lookups, transaction analysis, PSBT checks, Lightning invoice decoding, mining data, and market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches the upstream bitcoin-mcp package through uvx, so users depend on that package and its distribution channel. <br>
Mitigation: Install only if you trust the upstream bitcoin-mcp package, review the referenced package and repository, and monitor package updates before use in sensitive environments. <br>
Risk: Bitcoin queries may be sent to the Satoshi API and could include wallet-linked data. <br>
Mitigation: Avoid submitting wallet addresses, raw transactions, PSBTs, invoices, or other private wallet-linked data unless that privacy tradeoff is acceptable. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/Bortlesboat/bitcoin-mcp) <br>
- [PyPI package: bitcoin-mcp](https://pypi.org/project/bitcoin-mcp/) <br>
- [GitHub repository: Bortlesboat/bitcoin-mcp](https://github.com/Bortlesboat/bitcoin-mcp) <br>
- [Satoshi API](https://bitcoinsapi.com) <br>
- [uv package manager](https://github.com/astral-sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup status text, MCP configuration snippets, and connection-test guidance for uvx-based bitcoin-mcp use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
