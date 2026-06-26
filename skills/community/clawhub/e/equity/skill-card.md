## Description: <br>
Model cap tables, dilution scenarios, and vesting schedules for startups. Use when planning fundraising, pricing options, or tracking equity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and startup operators can invoke this command-line skill when planning or recording equity-related scenarios, exports, and activity. Security evidence indicates the release should be reviewed before use for real cap table, financing, valuation, grant, or fundraising work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review found that the script is advertised for startup equity modeling but mainly stores arbitrary command inputs in local plaintext logs instead of performing equity calculations. <br>
Mitigation: Review the script before installation and do not rely on it for real cap table, financing, valuation, grant, or fundraising decisions unless the publisher provides verified equity-modeling logic. <br>
Risk: Entered founder, employee, investor, valuation, grant, or fundraising details may be written to local plaintext logs under ~/.local/share/equity. <br>
Mitigation: Avoid entering confidential equity data unless local plaintext storage is acceptable; manage access to the data directory and delete logs or exports when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/equity) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain1) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/equity by default.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
