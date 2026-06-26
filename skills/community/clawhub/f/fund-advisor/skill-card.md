## Description: <br>
Fund Advisor helps agents import and manage personal fund holdings, query and analyze local portfolio data, and use qieman-mcp tools for fund details, holdings, portfolio analysis, planning, backtesting, and financial news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realqiyan](https://clawhub.ai/user/realqiyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage fund holding records, import CSV or Excel portfolio exports, synchronize fund metadata through qieman-mcp, and generate portfolio analysis or investment-planning guidance. It is intended for workflows where financial outputs are grounded in imported holdings and qieman-mcp data rather than unsupported assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace or delete local portfolio holding records during CSV, Excel, or reset workflows. <br>
Mitigation: Back up the holdings database before imports or reset operations, and confirm the intended FUND_ADVISOR_DATA_PATH or database path before running data-changing commands. <br>
Risk: The init workflow can modify the global mcporter configuration at ~/.mcporter/mcporter.json. <br>
Mitigation: Run environment checks before initialization where practical, review the mcporter configuration after setup, and keep a backup of any existing mcporter configuration. <br>
Risk: Fund holdings and the QIEMAN_API_KEY may expose sensitive financial data if shared with external services, logs, or chat contexts. <br>
Mitigation: Limit imported and shared data to what is necessary, protect the API key as a secret, and avoid sending full account identifiers, balances, or family financial details into shared contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/realqiyan/fund-advisor) <br>
- [MCP Tools Full Reference](references/mcp-tools-full.md) <br>
- [CSV Import Format](references/csv-format.md) <br>
- [Project Reference](references/REFERENCE.md) <br>
- [qieman MCP Tools](https://qieman.com/mcp/tools) <br>
- [qieman MCP Account](https://qieman.com/mcp/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with bash command examples and JSON MCP call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update a local SQLite holdings database and may configure mcporter to call qieman-mcp.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
