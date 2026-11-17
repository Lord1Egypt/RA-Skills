## Description:

Generates no-code BI-style Markdown reports from CSV or JSON data snippets, including data quality checks, metric calculations, chart recommendations, and business insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and analysts use this skill to turn desensitized CSV or JSON sample rows into lightweight BI reports for sales, inventory, user growth, finance, supply chain, and marketing reviews. It is intended for exploratory reporting, chart planning, and actionable recommendation drafting rather than final automated decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided data snippets may contain personal, financial, or confidential fields.

Mitigation: Redact or replace sensitive fields before using the skill.

Risk: Generated insights may overstate conclusions from a small data sample or confuse correlation with causation.

Mitigation: Review data quality, assumptions, and recommended actions against the broader business context before acting.

Risk: The expected output is a Chinese-language BI report format, which may not fit every deployment audience.

Mitigation: Use the skill where that report language and format are acceptable, or review and translate the output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/data-insight-generator)
- [README](artifact/README.md)
- [Input schema](artifact/schema.json)

## Skill Output:

**Output Type(s):** [markdown, guidance, configuration]

**Output Format:** [Markdown report with tables, chart configuration suggestions, and business recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language report structure; expects user-provided data snippets and business context.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
