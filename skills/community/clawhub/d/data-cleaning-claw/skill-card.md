## Description:

Data Cleaning Claw helps agents clean CSV, Excel, and JSON datasets by removing duplicate records and HTML noise, filling missing values, standardizing common date, amount, and phone formats, and producing a cleaned file with a JSON cleaning report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data operations users can use this skill to prepare messy tabular data for review or downstream processing. It is aimed at common cleanup workflows such as deduplication, missing-value handling, format normalization, HTML noise removal, and data-quality flagging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python packages at runtime.

Mitigation: Use an isolated environment and pin or review dependencies before installation.

Risk: Cleaned CSV or Excel outputs may preserve formula-like values from untrusted input.

Mitigation: Neutralize spreadsheet formulas before opening outputs in spreadsheet software.

Risk: Deduplication and missing-value filling can change datasets in ways that may not match business rules.

Mitigation: Keep original data backups and review the generated cleaning report before relying on the cleaned dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/data-cleaning-claw)
- [Data cleaning rules](references/cleaning-rules.md)
- [Data type recognition rules](references/data-types.md)
- [Noise pattern rules](references/noise-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; generated cleaned data files and JSON cleaning reports when the script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts input and output paths, comma-separated cleaning rules, optional key fields for deduplication, and optional date, amount, and phone field lists.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
