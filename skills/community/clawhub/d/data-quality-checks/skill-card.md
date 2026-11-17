## Description:

Designs data quality checks for tables or pipelines across completeness, validity, uniqueness, freshness, consistency, and accuracy, with rules, severity, and implementation location for each check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers, analytics engineers, and developers use this skill to plan actionable data quality checks for a table or pipeline. It helps define each check's rule, severity, execution location, and failure handling before implementation in tools such as dbt, Great Expectations, Soda, or SQL assertions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share unnecessary sensitive production data while describing tables or pipelines.

Mitigation: Provide schema, column rules, freshness expectations, and representative non-sensitive examples instead of raw private records when possible.

Risk: Incorrect severity choices could block useful pipelines or create alerts that teams ignore.

Mitigation: Review severity and failure actions with data owners before deployment, reserving blocking checks for critical integrity failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/data-quality-checks)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/data-quality-checks.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown table and notes describing data quality checks, rules, severity, implementation location, and failure handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dbt, Great Expectations, Soda, or SQL assertion recommendations when tooling is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
