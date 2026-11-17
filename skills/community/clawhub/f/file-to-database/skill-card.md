## Description:

Builds databases from CSV, Excel, JSON, JSONL, and TSV files, then supports natural-language database operations with safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use the skill to profile flat data files, design and validate a database, and operate it through natural-language requests. It produces schema and import deliverables and guides safe queries and data changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marked the skill suspicious for potentially unsafe database operations and broad data exports; part of the instructions was not fully inspected and some static checks were degraded.

Mitigation: Review the generated SQL and confirm the target database and export scope before execution or delivery.

Risk: Migration rehearsal and database changes may cause data loss.

Mitigation: Use a recoverable backup and rehearse migrations on a copy before applying them to important data.

Risk: Automatic delivery of the full database may expose sensitive records.

Mitigation: Check the database contents and recipients, and mask sensitive fields before sharing a delivery package.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thomaszhou22/skills/file-to-database)
- [Methodology](references/methodology.md)
- [Database operations](references/operations.md)
- [Engineering hardening](references/engineering.md)
- [Input triage](references/intake.md)
- [Output format](references/output-format.md)
- [Other database engines](references/other-engines.md)

## Skill Output:

**Output Type(s):** [Files, Code, SQL, Shell commands, Guidance]

**Output Format:** [SQL DDL, Python seed scripts, reversible migrations, Mermaid ERDs, JSON profiles, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deliverables depend on the input files and selected database engine; executing them depends on the available environment.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
