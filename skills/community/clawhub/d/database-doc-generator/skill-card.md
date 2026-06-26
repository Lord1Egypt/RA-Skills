## Description: <br>
Generate professional database structure documentation from PostgreSQL databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitoftom](https://clawhub.ai/user/gitoftom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and operations teams use this skill to document PostgreSQL schemas, export table and column metadata, and create data dictionaries as formatted Excel files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database credentials may be exposed through prompts, shell history, committed configuration, or command-line arguments. <br>
Mitigation: Use environment variables or a secret manager, avoid pasting real passwords into prompts or shell commands, and keep credential-bearing config files out of the skill directory. <br>
Risk: The bundled credential cleanup script can make broad repository edits. <br>
Mitigation: Review scripts/clean_credentials.py before use, run it only when repository-wide edits are intended, and keep backups or version-control checkpoints. <br>
Risk: Generated Excel files can reveal database schema details. <br>
Mitigation: Store generated workbooks in protected locations, apply restrictive file permissions, and delete sensitive output when no longer needed. <br>
Risk: Database access can exceed the documentation use case if the account is overprivileged. <br>
Mitigation: Connect with a read-only database account and use SSL/TLS or equivalent transport protection for remote PostgreSQL connections. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gitoftom/database-doc-generator) <br>
- [SQL Queries](references/SQL_QUERIES.md) <br>
- [Excel Formatting](references/EXCEL_FORMATTING.md) <br>
- [Usage Examples](references/USAGE_EXAMPLES.md) <br>
- [Security Guidelines](SECURITY.md) <br>
- [Secure Installation Guide](INSTALLATION_SECURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Excel workbook plus Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates formatted .xlsx database schema documentation from PostgreSQL metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
