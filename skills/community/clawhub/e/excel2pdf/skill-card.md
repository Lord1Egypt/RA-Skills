## Description:

Convert Excel (.xlsx) sign-in sheets and rosters to print-ready A4 PDFs with Chinese font support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncepuee](https://clawhub.ai/user/ncepuee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrative users can use this skill to convert Excel rosters, sign-in sheets, and tabular spreadsheets into printable A4 PDFs while preserving Chinese column text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter creates or overwrites a PDF at the default or user-specified output path.

Mitigation: Review the output path before running the script, especially when using --out.

Risk: Dependency versions are not pinned in the artifact instructions.

Mitigation: Install dependencies in a virtual environment and pin openpyxl and reportlab versions for reproducible deployments.

Risk: The converter requires a Chinese-capable system font or an explicit font path.

Mitigation: Confirm an appropriate font is installed or pass --font with a known .ttf or .ttc file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncepuee/skills/excel2pdf)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown guidance with command examples; generated output is a PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads a selected .xlsx workbook and writes a formatted A4 PDF to the default or specified output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
