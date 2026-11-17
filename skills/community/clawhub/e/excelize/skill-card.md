## Description:

Use when you need to reading and writing Microsoft Excel™ (XLAM / XLSM / XLSX / XLTM / XLTX) spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuri](https://clawhub.ai/user/xuri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install excelize-py and generate, read, and modify spreadsheet files, including charts and images, from agent-authored Python examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command does not pin the excelize package version, which can reduce reproducibility and supply-chain review confidence.

Mitigation: Install in a virtual environment and pin a reviewed excelize version for reproducible or higher-assurance use.

Risk: The examples can read, create, save, or overwrite spreadsheet files at user-provided paths.

Mitigation: Review target file paths and run examples on copies or disposable files before using them with important spreadsheets.

## Reference(s):

- [Excelize-py API docs](https://xuri.me/excelize-py/)
- [Excelize-py source code](https://github.com/xuri/excelize-py)
- [Excelize-py docs repository](https://github.com/xuri/excelize-py-docs)
- [Excelize package on PyPI](https://pypi.org/project/excelize)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may create, read, modify, or overwrite spreadsheet files at paths chosen by the user.]

## Skill Version(s):

0.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
