## Description:

Parse employee skills CSV files, identify skill categories and individual skills, look up employee IDs from an employees table, and generate idempotent SQL INSERT statements for skill_categories, skills, and employee_skills tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inna-demidova](https://clawhub.ai/user/inna-demidova)

### License/Terms of Use:


## Use Case:

Developers and operations staff use this skill to turn employee skills CSV exports into reviewable Supabase SQL import scripts. It supports importing skill categories, skills, and employee-skill relationships while reporting missing or corrected employee matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles employee data and generates SQL that changes live database tables.

Mitigation: Review generated SQL manually, test in a staging database, and use least-privileged Supabase credentials before production execution.

Risk: Fuzzy employee-name matching can link skills to the wrong employee if an automatic correction is incorrect.

Mitigation: Require explicit review and approval for every fuzzy employee-name correction before running the employee_skills import.

Risk: CSV-derived text may create unsafe SQL if values are not escaped correctly.

Mitigation: Inspect all generated SQL and prefer safely escaped or parameterized database import paths for production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inna-demidova/skills/employee-skills-importer)

## Skill Output:

**Output Type(s):** [code, text, markdown, guidance]

**Output Format:** [Markdown summary with SQL code or generated SQL and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ordered SQL scripts for categories, skills, and employee_skills, plus a report for skipped or corrected employees when applicable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
