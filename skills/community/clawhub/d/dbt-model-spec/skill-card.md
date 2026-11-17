## Description:

Dbt Model Spec helps agents design dbt models by defining grain, lineage, transformation logic, columns, tests, materialization, and starter SQL/YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics engineers use this skill to plan reviewable dbt models before implementation, including the model grain, upstream source/ref lineage, transformation logic, schema contract, dbt tests, and materialization choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or YAML may be incorrect or unsuitable for a real dbt project or production data warehouse.

Mitigation: Review the generated model spec, SQL, YAML, tests, and materialization before applying changes.

Risk: Ambiguous grain or weak tests can lead to duplicate rows, broken lineage, or incorrect metrics.

Mitigation: Confirm the stated grain and require unique, not_null, relationship, enum, and relevant custom tests before implementation.

## Reference(s):

- [Dbt Model Spec ClawHub Page](https://clawhub.ai/mohitagw15856/skills/dbt-model-spec)
- [Dbt Model Spec Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/dbt-model-spec.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with SQL and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured dbt model specification with review checks before implementation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
