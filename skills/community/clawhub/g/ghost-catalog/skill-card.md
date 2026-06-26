## Description: <br>
Scan, tag, validate, and catalog workspace files using the Ghost Catalog semantic file header system and a local SQLite catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SoMaCoSF](https://clawhub.ai/user/SoMaCoSF) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to inventory project files, apply or validate SOM semantic file headers, search catalog metadata, and generate catalog compliance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package bundles a separate improve-skill meta-skill with broader behavior than Ghost Catalog's file cataloging purpose. <br>
Mitigation: Review whether both bundled skills are desired before installation or use, and invoke only the skill needed for the task. <br>
Risk: Cataloging operations can inspect workspace files and may modify headers, reports, or the local SQLite catalog. <br>
Mitigation: Use the skill in a version-controlled workspace, configure .ghost_ignore before scanning, and require explicit review before tag, report, database update, or skill-file modification operations. <br>
Risk: Workspace scans may include sensitive or private files if ignore rules are incomplete. <br>
Mitigation: Keep secrets and private data out of scan scope by configuring .ghost_ignore and .gitignore before running catalog operations. <br>


## Reference(s): <br>
- [Ghost Catalog Skill Page](https://clawhub.ai/SoMaCoSF/ghost-catalog) <br>
- [Publisher Profile](https://clawhub.ai/user/SoMaCoSF) <br>
- [Release Changelog 1](https://gist.github.com/SoMaCoSF/488d6a173bff53204aa65e159085942f) <br>
- [Release Changelog 2](https://gist.github.com/SoMaCoSF/28df4f5af37c863515f59552ee33a2eb) <br>
- [Category Codes](ghost-catalog/category-codes.md) <br>
- [Header Templates](ghost-catalog/header-templates.md) <br>
- [SQLite Catalog Schema](ghost-catalog/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, formatted tables, SQL schema guidance, file header templates, and local file modification instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SOM file headers, a SQLite catalog database, and docs/ghost-catalog-report.md when the user approves write operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
