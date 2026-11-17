## Description:

Automates batch Excel tasks including merging, splitting, format conversion, data cleaning, deduplication, and bulk formula filling with wildcard support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Spreadsheet users and agents use this skill to plan or carry out batch Excel workflows such as merging files, splitting workbooks, converting Excel and CSV files, cleaning data, deduplicating rows, and filling formulas across many files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch spreadsheet operations can overwrite, remove, or transform many files or rows at once.

Mitigation: Work on copies or direct outputs to a separate folder before applying wildcard, cleaning, deduplication, or fill operations.

Risk: Skipped errors may hide incomplete processing results.

Mitigation: Review skipped-error results after each batch run and confirm that expected files and rows were processed.

Risk: The command examples and operation names are Chinese-language, which may cause misuse by readers who do not understand them.

Mitigation: Use the skill only when the operator is comfortable with the command language and can confirm inputs and outputs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/excel-batch-processor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes Excel and CSV file outputs, wildcard batch processing, preservation of formulas and formatting, and skipped-error behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
