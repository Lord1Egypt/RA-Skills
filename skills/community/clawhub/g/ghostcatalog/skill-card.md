## Description:

Ghost Catalog scans, tags, validates, searches, and catalogs workspace files using SOM semantic headers and a local SQLite catalog database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[somacosf](https://clawhub.ai/user/somacosf)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to discover untagged project files, apply or validate SOM headers, search catalog metadata, and generate compliance reports during workspace maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tagging can prepend headers to workspace files and may break files with strict syntax or schemas.

Mitigation: Run scans first and review proposed tagging changes before applying them, especially for config files, generated files, schema-validated JSON, and files that may contain secrets.

Risk: Catalog data is stored locally and may become inaccurate if files are moved or edited outside the catalog workflow.

Mitigation: Use validation and report workflows to compare file headers against the local SQLite catalog before relying on catalog status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/somacosf/skills/ghostcatalog)
- [Ghost Catalog category codes](artifact/category-codes.md)
- [Ghost Catalog header templates](artifact/header-templates.md)
- [Ghost Catalog database schema](artifact/schema.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries, tables, generated file headers, and local SQLite catalog records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply workspace file header changes when the user invokes tagging or fixing workflows.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
