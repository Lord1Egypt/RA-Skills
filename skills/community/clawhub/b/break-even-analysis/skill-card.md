## Description:

Provides a break-even analysis workflow and template for US offers, with a bundled script that generates a report but does not perform the advertised calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US business owners, product managers, and finance students use the workflow and template to organize break-even assumptions for pricing or product-line decisions. Verify calculations independently before relying on them.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script does not perform break-even calculations and may silently replace missing or non-numeric inputs with zero, producing a misleading report.

Mitigation: Use an independently verified calculator for actual results, and verify every input before relying on the generated report.

Risk: The optional Windows toolkit is unsigned and was not assessed as part of this workflow.

Mitigation: The Python workflow does not require the toolkit; if obtained, verify its published SHA-256 and keep it in an isolated folder.

## Reference(s):

- [Break-even analysis for US offers](references/break-even.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Markdown report and YAML input template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script records supplied inputs and a formula but does not calculate break-even results.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
