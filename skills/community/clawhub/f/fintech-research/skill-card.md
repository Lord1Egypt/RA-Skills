## Description: <br>
Fintech Research is a self-hosted equity research toolkit for Claude Code that supports US, Hong Kong, and China market workflows through analysis skills and a local MCP server using free data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredtai](https://clawhub.ai/user/fredtai) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill to perform equity research workflows such as thematic screening, single-company analysis, portfolio tracking, macro landscape review, earnings updates, and initiation-style research drafts. It is intended to support research preparation, not to replace source verification or investment judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP server exposes an unrestricted SQL tool over the cached finance database. <br>
Mitigation: Use the SQL tool only in supervised workspaces and avoid enabling it where local cached research data or file-modifying workflows are sensitive. <br>
Risk: Research outputs may include recommendations or conclusions based on cached, stale, or synthetic market data. <br>
Mitigation: Treat outputs as research drafts, verify live source data before relying on them, and check for mock:true or other fallback indicators. <br>
Risk: The skill makes outbound requests to public market-data providers and may use optional API keys. <br>
Mitigation: Install only where this network behavior is acceptable and keep optional credentials in environment variables rather than persistent files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fredtai/fintech-research) <br>
- [MCP Tools Reference](docs/tools.md) <br>
- [Data Sources](docs/data-sources.md) <br>
- [Security Policy](SECURITY.md) <br>
- [FRED](https://fred.stlouisfed.org) <br>
- [NewsAPI](https://newsapi.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research guidance with JSON tool results, shell command snippets, and optional generated report or model artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a local MCP server for market data, filings, macro data, disclosures, news, cached SQLite data, and fiscal calendar lookup.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
