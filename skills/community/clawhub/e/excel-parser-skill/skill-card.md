## Description:

Excel Parser extracts structured and text content from .xls, .xlsx, .xlsm, .xltx, and .xltm spreadsheet files using python-calamine with fallback Excel readers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to parse Excel workbooks, extract sheet rows and counts, and convert spreadsheet contents into text for downstream analysis, reporting, review, or automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Python packages during normal use, which may affect the active environment or introduce unreviewed dependency versions.

Mitigation: Install and run the skill in an isolated environment, or preinstall pinned and reviewed versions of python-calamine, xlrd, openpyxl, and python-dotenv before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yejinlei/skills/excel-parser-skill)
- [python-calamine](https://github.com/dimastbk/python-calamine)
- [xlrd](https://github.com/python-excel/xlrd)
- [openpyxl documentation](https://openpyxl.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python examples, shell commands, environment configuration, and JSON-like structured parse results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parse results can include per-sheet rows, row and column counts, total cell count, selected parser engine, and formatted text.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence; artifact setup.py and CHANGELOG.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
