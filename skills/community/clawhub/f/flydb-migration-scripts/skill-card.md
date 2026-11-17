## Description:

创建、修改和组织 Flydb 的 V/R/U 迁移 SQL，处理命名、版本族与目录版本、路径过滤、占位符和历史 checksum。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzxcoding](https://clawhub.ai/user/zzxcoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to create and maintain Flydb migration SQL, organize migration locations, and resolve script-related Flydb errors without directly executing database-changing commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migration SQL or configuration advice could be incorrect for the target database or project conventions.

Mitigation: Review generated SQL and run Flydb validate or dry-run checks before applying migrations to a database.

Risk: Changing an already-applied versioned migration can cause checksum mismatches and repair requirements.

Mitigation: Carry historical changes in a new versioned migration unless the user explicitly accepts the checksum and repair consequences.

Risk: A failed migration may have partially committed database changes.

Mitigation: Inspect the failure snapshot and database state before editing scripts or deciding whether repair is appropriate.

## Reference(s):

- [Flydb migration naming and version rules](references/naming-and-versions.md)
- [Flydb script error codes and modification discipline](references/errors-and-discipline.md)
- [Flydb project](https://github.com/zzxCoding/Flydb)
- [Flydb Gitee mirror](https://gitee.com/zzhenxuan/Flydb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL snippets, file names, configuration examples, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SQL migration file changes and read-only validation commands; database-changing Flydb commands are outside this skill's scope.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
