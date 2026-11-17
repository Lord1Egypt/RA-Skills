## Description:

Fund Advisor helps agents manage imported personal fund holdings, query fund data through qieman-mcp, and provide portfolio analysis, planning, backtesting, market news, fund search, and announcement lookup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realqiyan](https://clawhub.ai/user/realqiyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to import personal fund holdings, analyze portfolios, query current fund data, and generate investment research guidance through local tools and qieman-mcp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio import can overwrite existing local holdings records.

Mitigation: Back up the existing fund-advisor database before running CSV or Excel import commands.

Risk: Initialization can modify ~/.mcporter/mcporter.json and may persist the QIEMAN_API_KEY value in local configuration.

Mitigation: Use a scoped or disposable Qieman API key when possible and review the mcporter configuration after initialization.

Risk: Dependency installation runs before the wrapper command executes.

Mitigation: Review the artifact dependencies and wrapper behavior before running the CLI in a trusted environment.

## Reference(s):

- [Fund Advisor ClawHub release page](https://clawhub.ai/realqiyan/skills/fund-advisor)
- [Project architecture reference](references/REFERENCE.md)
- [CSV import format specification](references/csv-format.md)
- [qieman-mcp tool list](references/mcp-tools-full.md)
- [Qieman MCP tools documentation](https://qieman.com/mcp/tools)
- [Qieman MCP usage guide](https://yingmi.feishu.cn/docx/PRPRds5SBo2MITxHJL2cMPminEf)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON MCP arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses imported local portfolio data and qieman-mcp responses; outputs should be reviewed for investment risk and data freshness.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
