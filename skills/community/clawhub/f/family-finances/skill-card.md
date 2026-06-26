## Description: <br>
A Chinese-language household finance skill for recording assets, liabilities, cash flow, and portfolio holdings, then generating net-worth, cash-flow, portfolio, and financial health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmos180](https://clawhub.ai/user/cosmos180) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain local household finance records, inspect net worth and monthly cash flow, track portfolio allocation, and generate Chinese-language financial health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detailed household financial records are stored as local cleartext JSON files. <br>
Mitigation: Use the skill only on a trusted device, restrict local filesystem access, and back up the data directory if the records matter. <br>
Risk: Delete operations remove assets, liabilities, or holdings by record name. <br>
Mitigation: Confirm exact record names with the user before running deletion commands. <br>
Risk: Financial health scores and reports are calculated from user-entered data and may be incomplete or stale. <br>
Mitigation: Ask the user to review source records and update monthly snapshots before relying on a report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosmos180/family-finances) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cosmos180) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown or JSON-backed report summaries with inline shell commands when script execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and reads local JSON finance records under ~/.openclaw/workspace/data/family-finances/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
