## Description: <br>
DB Smart Import helps agents analyze CSV, SQL dump, and database schemas, suggest column mappings, and prepare or run imports into MySQL, MariaDB, or SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarbcs1-prog](https://clawhub.ai/user/jarbcs1-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to inspect source and destination schemas, map columns, import CSV data, and execute SQL dumps during database migration or ingestion work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL dumps can execute statements that permanently change or delete data in a live database. <br>
Mitigation: Inspect SQL dumps as executable code, test first on staging or a fresh restore, back up the target database, and use least-privilege database users. <br>
Risk: Automated column mappings can be incorrect and import values into the wrong destination fields. <br>
Mitigation: Review suggested mappings and verify column types before running any bulk import. <br>
Risk: Database passwords passed directly on the command line can be exposed through shell history or process listings. <br>
Mitigation: Use safer credential handling where available and avoid passing real production passwords directly as command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jarbcs1-prog/db-smart-importer) <br>
- [Publisher profile](https://clawhub.ai/user/jarbcs1-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON mapping objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use bundled Python scripts to inspect schemas, suggest mappings, import CSV rows, or execute SQL dump statements.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
