## Description:

Quality-control and data-analysis toolkit for testing and inspection workflows, covering internal QC, inter-lab comparison, batch comparison, method validation, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and quality engineers use this skill to plan and run statistical QC analyses, method-validation calculations, trend monitoring, and structured report generation for testing and inspection data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can persistently modify code or templates.

Mitigation: Use a sandboxed workspace and review generated or modified files before relying on analysis results.

Risk: The security review says the skill can expose an unauthenticated configuration server.

Mitigation: Run any configuration server only on trusted local interfaces and never on shared or exposed networks.

Risk: The security review advises caution with untrusted templates, datasets, and runtime Python source generation.

Mitigation: Use trusted datasets and templates, scan inputs before execution, and disable or remove runtime source generation before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/analysis-toolkit)
- [Quickstart](references/quickstart.md)
- [Data interface](references/data-interface.md)
- [Pipeline reference](references/pipeline.md)
- [Regression and method validation](references/regression-validation.md)
- [ANOVA analysis](references/anova-analysis.md)
- [Report generation](references/report-generation.md)
- [Permissions](references/permissions.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, numeric analysis results, charts, and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce warnings for low-quality input data and may generate HTML, Word, PDF, image, or table artifacts depending on the workflow.]

## Skill Version(s):

2.0.4 (source: frontmatter, release metadata, changelog released 2026-06-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
