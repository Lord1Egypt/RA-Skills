## Description: <br>
Process Avanza CSV exports, calculate TWRR/Modified Dietz returns, and track portfolio performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to import Avanza transaction CSVs, maintain local portfolio data, calculate account-level performance, and generate TWRR or Modified Dietz investment statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio data is stored in a local SQLite database. <br>
Mitigation: Keep the database in a private workspace, control file permissions, and back it up before reset or import operations. <br>
Risk: Automatic price updates can send held asset names to Avanza. <br>
Mitigation: Use --update-prices never for offline operation or when asset-name disclosure is not acceptable. <br>
Risk: Reset operations can clear local database state. <br>
Mitigation: Review reset commands before execution and keep database backups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patello/avanza-investment-tracker) <br>
- [Workflows](references/workflows.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and tabular CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local CSV, JSON special-case, and SQLite database files; optional price updates can make network requests.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
