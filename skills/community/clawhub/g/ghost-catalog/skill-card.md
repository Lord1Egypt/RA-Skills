## Description:

Ghost Catalog scans, tags, validates, and catalogs workspace files with SOM semantic headers and a local SQLite catalog database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[somacosf](https://clawhub.ai/user/somacosf)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit local workspaces for catalog coverage, add or validate SOM file headers, search catalog metadata, and produce catalog compliance summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read many local project files while scanning and cataloging a workspace.

Mitigation: Run it only in intended workspaces and review `.ghost_ignore` and `.gitignore` coverage before scanning.

Risk: Tag operations can modify source files by inserting headers, including executable scripts.

Mitigation: Preview tag changes, preserve shebangs and first-line directives, and re-read modified files after write operations.

Risk: The package includes an unrelated improve-skill meta-skill that can inspect and modify skill files.

Mitigation: Verify the installed package contents and remove or ignore unrelated bundled skills when deploying only Ghost Catalog.

Risk: The skill may create a local SQLite catalog and Markdown report containing workspace metadata.

Mitigation: Confirm the output paths and avoid cataloging sensitive files or generated artifacts.

## Reference(s):

- [Ghost Catalog ClawHub listing](https://clawhub.ai/somacosf/skills/ghost-catalog)
- [Release changelog reference 1](https://gist.github.com/SoMaCoSF/488d6a173bff53204aa65e159085942f)
- [Release changelog reference 2](https://gist.github.com/SoMaCoSF/28df4f5af37c863515f59552ee33a2eb)
- [Ghost Catalog category codes](artifact/ghost-catalog/category-codes.md)
- [Ghost Catalog header templates](artifact/ghost-catalog/header-templates.md)
- [Ghost Catalog database schema](artifact/ghost-catalog/schema.sql)
- [.somaco unification map](artifact/ghost-catalog/somaco-unification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown summaries and reports, formatted tables, SQLite catalog records, and file header edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read many workspace files, create a local SQLite database, generate a Markdown report, and modify files by adding catalog headers]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
