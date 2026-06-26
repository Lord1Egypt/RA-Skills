## Description: <br>
基金量化数据分析工具，基于AkShare库获取公募基金净值、持仓、估值等数据。用于基金查询、持仓分析、业绩追踪。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[BingoBinF](https://clawhub.ai/user/BingoBinF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to query Chinese public fund information, NAV, holdings, estimates, and cross-fund holding summaries through an AkShare-backed Python CLI. It is intended for fund research and analytical workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI depends on AkShare and external financial data providers, so results can be unavailable, delayed, or affected by upstream website changes. <br>
Mitigation: Treat outputs as research data, verify important values against authoritative sources, and retry or review upstream data-provider status when calls fail. <br>
Risk: The release uses unpinned third-party Python dependencies. <br>
Mitigation: Install in an isolated environment and pin reviewed versions of akshare and pandas before routine or production-like use. <br>
Risk: Fund holdings are quarterly disclosures and can lag current positions. <br>
Mitigation: Use holding summaries as historical context and disclose the reporting lag when relying on the analysis. <br>
Risk: Embedded artifact metadata reports version 1.0.2 while server release metadata reports version 1.0.0. <br>
Mitigation: Prefer the server release version for this card and verify the package version before installing or citing the release. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Analysis] <br>
**Output Format:** [Console text and tabular output from Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language fund data summaries; values depend on AkShare and external market data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
