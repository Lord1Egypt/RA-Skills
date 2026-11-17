## Description:

Generates a standardized balance sheet workbook from a financial Excel source file by applying documented accounting-sheet transformation rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[courage-zen](https://clawhub.ai/user/courage-zen)

### License/Terms of Use:

MIT-0

## Use Case:

Finance staff, accountants, and agents supporting bookkeeping workflows use this skill to turn a structured Excel workbook containing balance-sheet, detail, and profit-statement sheets into a formatted balance sheet output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local financial workbooks that may contain sensitive business data.

Mitigation: Run it only on intended input files in a controlled workspace and provide explicit source and output paths.

Risk: Automatic or under-scoped file selection could process the wrong workbook.

Mitigation: Prefer command-line or scripted usage with an explicit input path and verify the selected workbook before generation.

Risk: Untrusted formulas or external links may be carried into the generated workbook.

Mitigation: Use trusted source files and review the generated workbook for unexpected formulas or external links before sharing or opening broadly.

## Reference(s):

- [Balance sheet generation rules](references/rules.md)
- [ClawHub skill page](https://clawhub.ai/courage-zen/skills/balance-sheet-cn)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an .xlsx balance sheet, defaulting to 资产负债表.xlsx when no output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
