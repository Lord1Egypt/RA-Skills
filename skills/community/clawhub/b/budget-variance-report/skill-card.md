## Description:

Renders a monthly budget variance report from your CSV, showing actual versus budget by category in dollars and percent with commentary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US department managers, business owners, and controllers use this skill to compare monthly actuals with budget by category, prioritize unfavorable dollar variances, and prepare review commentary from user-confirmed reasons.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Crafted CSV category names can cause the reporting script to overwrite Markdown files outside the selected output folder under certain directory layouts.

Mitigation: Use trusted CSVs with simple category names and a fresh output folder until filename sanitization and output-path containment are in place.

Risk: Report calculations may be incorrect.

Mitigation: Verify the report calculations against the source budget and actuals before relying on the results.

Risk: The optional Windows toolkit is a separate, unsigned executable and is not part of the skill workflow.

Mitigation: Assess it separately, verify the downloaded archive's published SHA-256, obtain the password from the publisher, and avoid running it as administrator without a reason.

## Reference(s):

- [Reading a US budget variance](references/budget-variance.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/budget-variance-report)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown variance-report files with category-level budget, actual, dollar and percent variance, and commentary fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided figures and confirmed reasons; not an audited or GAAP-compliant financial statement.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
