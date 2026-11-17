## Description:

Classifies field names, field lists, and SQL DDL into general data classification grades and financial dual labels based on GB/T 43697-2024 and JR/T 0197-2020 guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangzaiz666](https://clawhub.ai/user/liangzaiz666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data stewards, and compliance reviewers use this skill to classify schema metadata into general data grades and financial labels before business-owner review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schema metadata and generated classification files can contain sensitive business or personal-data signals.

Mitigation: Review what schema metadata is shared with the skill, restrict access to generated CSVs, and handle exports as sensitive files.

Risk: Generated CSV output may carry spreadsheet-related risk when input field names or comments are untrusted.

Mitigation: Avoid opening exported CSVs in spreadsheet software unless the source schema text is trusted or has been sanitized.

Risk: Classification suggestions may be mistaken for final regulatory determinations.

Mitigation: Require business-owner or compliance review for uncertain items and before relying on labels for policy decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangzaiz666/skills/data-classification)
- [GB/T 43697-2024 general classification rules](artifact/references/general-rules.md)
- [Financial dual-label workflow](artifact/references/financial-dual-label.md)
- [JR/T 0197-2020 Appendix A compact table](artifact/references/jrt0197-appendix-a-compact.md)
- [JR/T 0197-2020 Appendix A full CSV](artifact/references/jrt0197-appendix-a-full.csv)

## Skill Output:

**Output Type(s):** [text, markdown, csv, json, guidance]

**Output Format:** [Markdown tables for concise results, CSV files for larger classifications, and JSON or CSV from the helper script when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-field classifications, confidence, review notes, candidate financial labels when applicable, and a coverage check.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
