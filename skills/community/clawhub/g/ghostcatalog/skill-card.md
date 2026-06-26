## Description: <br>
Scan, tag, validate, and catalog files using the Ghost Catalog semantic file header system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SoMaCoSF](https://clawhub.ai/user/SoMaCoSF) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to organize workspace files with semantic SOM headers, maintain a local SQLite catalog, validate catalog compliance, and produce catalog status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local project files and could catalog secrets, private documents, generated files, or dependencies if ignore rules are incomplete. <br>
Mitigation: Configure .ghost_ignore or .gitignore before scanning so sensitive, generated, dependency, and private paths are excluded. <br>
Risk: The tag operation can modify multiple files by adding catalog headers. <br>
Mitigation: Review previews and source-control diffs before applying headers to batches of files. <br>
Risk: The local SQLite catalog can contain workspace file paths and metadata. <br>
Mitigation: Treat the catalog database as project metadata and exclude sensitive paths from cataloging. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SoMaCoSF/ghostcatalog) <br>
- [Ghost Catalog skill definition](artifact/SKILL.md) <br>
- [Category codes reference](artifact/category-codes.md) <br>
- [Header templates reference](artifact/header-templates.md) <br>
- [Catalog database schema](artifact/schema.sql) <br>
- [Somaco unification map](artifact/somaco-unification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Text summaries, Markdown reports, file header blocks, and SQLite catalog entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file catalog metadata and may propose or apply header changes to workspace files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
