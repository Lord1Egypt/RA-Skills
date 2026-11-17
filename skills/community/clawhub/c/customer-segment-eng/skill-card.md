## Description:

Analyzes bank customer data to segment and profile customers using RFM-style features, K-Means clustering, statistics, and visual reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yukirang](https://clawhub.ai/user/yukirang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to segment financial customers from uploaded bank customer data, generate cluster labels and statistics, and produce charts and a Markdown report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can duplicate sensitive banking or personally identifiable customer data into generated output files.

Mitigation: Review before use with real customer data, use a controlled output directory, export only needed fields, and mask identifiers where possible.

Risk: Generated CSV files may create spreadsheet formula execution risk when opened in spreadsheet tools.

Mitigation: Open generated CSVs with formula execution disabled and review outputs before sharing.

Risk: Customer segmentation outputs may be used in compliance-sensitive decisions such as discriminatory pricing.

Mitigation: Use outputs as decision-support only, desensitize customer data, and require compliance review before business use.

## Reference(s):

- [RFM Model Reference](references/rfm-guide.md)
- [Clustering Analysis Parameter Reference](references/clustering-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/yukirang/skills/customer-segment-eng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated CSV, PNG, and Markdown report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export customer-level rows and derived segment labels to a chosen output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
