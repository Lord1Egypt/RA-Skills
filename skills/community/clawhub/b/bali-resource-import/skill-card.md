## Description:

Guides agents through parsing Bali travel supplier documents and importing standardized records for hotels, vehicles, attractions, activities, SPA, clubs, restaurants, and afternoon tea into CSV resource libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[errsr](https://clawhub.ai/user/errsr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations staff use this skill to convert Bali supplier contracts and resource documents into standardized travel-resource CSV entries. It is intended for workflows that must preserve existing production CSV schemas while appending newly extracted records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite production CSV files during import.

Mitigation: Use backups, dry-run/schema validation, and operator review before allowing writes to production CSVs.

Risk: The cleanup workflow can delete broad sets of files from a target directory.

Mitigation: Run in a dedicated empty staging directory and allow cleanup only for files created during the current run.

Risk: Optional Redis or public web enrichment integrations may broaden the operational surface.

Mitigation: Enable Redis or public web enrichment only when explicitly needed and configured safely.

## Reference(s):

- [巴厘岛旅游资源标准化文档体系](references/旅游资源标准化文档体系.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV updates and an import-completion report when used by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
