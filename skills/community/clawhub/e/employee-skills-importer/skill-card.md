## Description: <br>
Parse employee skills CSV files, identify skill categories and individual skills, look up employee IDs from an employees table, and generate idempotent SQL INSERT statements for skill_categories, skills, and employee_skills tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inna-demidova](https://clawhub.ai/user/inna-demidova) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and database administrators use this skill to turn employee skills CSV exports into reviewed SQL scripts for a configured Supabase skills database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can update employee skills records and may affect HR data if executed without review. <br>
Mitigation: Review every generated statement, test in staging or a rollback-capable transaction, and use least-privileged database credentials. <br>
Risk: Automatic fuzzy matching can associate CSV names with the wrong employee. <br>
Mitigation: Verify every reported name correction and skipped employee before executing the employee_skills script. <br>
Risk: The skill targets a configured Supabase project that may contain employee data. <br>
Mitigation: Use the skill only when authorized to process that project's employee data and keep a current backup before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inna-demidova/employee-skills-importer) <br>
- [README.md](artifact/README.md) <br>
- [EXAMPLE_OUTPUT.md](artifact/EXAMPLE_OUTPUT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL code blocks and generated SQL file contents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces three ordered SQL scripts and may produce a report of name corrections, skipped employees, and skipped skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
