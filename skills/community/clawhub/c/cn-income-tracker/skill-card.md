## Description: <br>
Income Tracker records multi-source income, summarizes earnings, and produces trend, source, export, and prediction outputs for freelancers, creators, side-business operators, and small teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add income records, inspect income summaries, analyze income sources, generate text charts, and export local income data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Income amounts, sources, dates, notes, and tags are stored in a local plaintext JSON file. <br>
Mitigation: Use a private DATA_PATH, restrict filesystem permissions, avoid secrets in notes, and protect backups and exports. <br>
Risk: CSV or JSON exports can disclose sensitive income history if shared or stored insecurely. <br>
Mitigation: Review exported data before sharing and store exports only in approved private locations. <br>
Risk: Future versions that add real cloud sync or live exchange-rate network calls would change the privacy and network-risk profile. <br>
Mitigation: Review and rescan any future version before deployment, especially if network sync or live exchange-rate calls are introduced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/cn-income-tracker) <br>
- [Clawdis homepage](https://clawhub.com/skills/income-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, ASCII charts, guidance] <br>
**Output Format:** [Structured JSON responses with optional CSV export strings and ASCII chart text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local income records in a JSON file controlled by DATA_PATH.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
