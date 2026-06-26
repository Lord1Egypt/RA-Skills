## Description: <br>
Guides users through migrating memory-lancedb-pro memory data into memos-local-openclaw-plugin by converting memory files, updating configuration, importing markdown memories, and checking the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2070super](https://clawhub.ai/user/2070super) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to move memories from memory-lancedb-pro to memos-local-openclaw-plugin, including markdown conversion, configuration cleanup, SQLite import, and migration validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration can persistently change OpenClaw plugin configuration. <br>
Mitigation: Review and replace all paths, back up the OpenClaw configuration, test changes on copies first, and remove the old plugin configuration only after confirming the new import works. <br>
Risk: The import can write memory records into a local memos SQLite database with the wrong path, schema, or duplicate data. <br>
Mitigation: Back up the memos database, confirm the expected chunks table fields, run the import on a copy first, and compare record counts before relying on the migrated data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2070super/convert-memory-files-between-systems) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local scripts that modify OpenClaw configuration and write to a memos SQLite database; users should replace hard-coded paths and test on backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
