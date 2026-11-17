## Description:

Routes lakehouse migration requests to SQL conversion, data validation, or scheduled workflow migration capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to coordinate SQL dialect conversion, compare data before and after migration, and migrate scheduled data workflows through Alibaba Cloud Lakehouse Migration Center.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initialization updates executable cloud tooling from an external plugin source.

Mitigation: Install only if you trust the plugin source and accept runtime updates; review local configuration before running.

Risk: SQL conversion sends source and converted SQL to Alibaba Cloud as audit records.

Mitigation: Confirm that sharing the SQL for audit is permitted before processing sensitive queries.

Risk: DryRun and migration actions can affect production resources when privileged credentials or dangerous SQL are used.

Mitigation: Use a least-privilege RAM role or profile, and avoid production or dangerous SQL in DryRun.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-lakehouse-migration)
- [RAM permission requirements](references/ram-policies.md)
- [SQL conversion guide](references/lhm-sql-conversion/README.md)
- [Data validation guide](references/lhm-data-validation-skill/README.md)
- [Workflow migration guide](references/lhm-bigdata-workflow-migration-skill/README.md)

## Skill Output:

**Output Type(s):** [SQL code, Markdown reports, Configuration, Guidance]

**Output Format:** [Text and Markdown, including SQL and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the routed migration task and accessible cloud services.]

## Skill Version(s):

0.0.1 (source: ClawHub release and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
