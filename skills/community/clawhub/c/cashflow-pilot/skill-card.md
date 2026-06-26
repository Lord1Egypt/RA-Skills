## Description: <br>
现金流领航 helps small and medium business owners import bills, track income and expenses, monitor receivables and payables, generate cash-flow reports, and forecast future cash flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to keep a local cash-flow ledger, import transaction files, review monthly cash-flow status, manage receivables and payables, and generate simple forecasts for planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive business finance records stored in local JSON files. <br>
Mitigation: Set CFP_DATA_DIR to a private, backed-up directory with appropriate local access controls before importing or recording financial data. <br>
Risk: Imported ledger entries, generated reminders, and cash-flow forecasts can be incomplete or inaccurate. <br>
Mitigation: Review imported classifications, reminder lists, and generated forecasts before using them for business decisions. <br>
Risk: The skill reads user-selected transaction files from disk. <br>
Mitigation: Import only files the user explicitly chooses and trusts. <br>


## Reference(s): <br>
- [Cashflow Pilot ClawHub page](https://clawhub.ai/hanjing5024064/cashflow-pilot) <br>
- [Report templates](references/report-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown reports, tables, Mermaid chart snippets, JSON-backed local records, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are tier-dependent; paid features add forecasts, expanded reminders, anomaly alerts, and chart snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
