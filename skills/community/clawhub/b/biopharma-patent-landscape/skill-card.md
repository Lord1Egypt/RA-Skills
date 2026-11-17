## Description:

开展生物医药专利检索、专利族和组合布局研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP, patent, and biopharma strategy users use this skill to research patent portfolios around companies, targets, drugs, or technology themes. It supports applicant scope confirmation, patent retrieval, family mapping, legal status checks, evidence tracking, and Excel workbook delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook-writing behavior can unexpectedly restructure Excel files or alter workbook schema.

Mitigation: Use copies of workbooks, choose strict-template mode when the schema must remain unchanged, and verify sheet preservation and column mapping before delivery.

Risk: Patent and company research may send company, target, drug, or technology terms to external patent or search services.

Mitigation: Confirm that external queries are acceptable for the data before running searches, and record source URLs or retrieval identifiers for traceability.

Risk: The release uses broad shared dependencies and does not declare an isolated runtime environment.

Mitigation: Prefer pinned dependencies with runtime isolation before deployment.

## Reference(s):

- [Legacy company patent workflow](references/legacy-company-patent-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured patent research outputs, JSON company verification data, assignee lists, and Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workbook outputs may use strict-template mode or user-approved enriched mode.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
