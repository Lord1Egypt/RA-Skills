## Description:

Generates monthly financial report text, Markdown, Word, and JSON summary files from a fixed-format finance Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiqikuaidianpao](https://clawhub.ai/user/qiqikuaidianpao)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams and agents use this skill to turn a fixed-format monthly Excel workbook into a reviewable financial report draft and a Word file for download. It is for report drafting and handoff, not audit judgment, accounting adjustments, or changing source workbook figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded workbooks or changed templates can lead to incorrect extracted figures or an incorrect report period.

Mitigation: Verify the workbook, selected sheet, report period, and generated financial figures against the source file before use.

Risk: The generated report is a draft and may contain attribution placeholders or business explanations that are not final judgments.

Mitigation: Have finance reviewers replace or approve placeholder reasoning and final operating judgments before distribution.

Risk: Dependency drift in Excel or Word libraries can change parsing or document generation behavior.

Mitigation: Use pinned, reviewed versions of openpyxl, xlrd, and python-docx for production use.

Risk: Generated report files may contain sensitive financial information in the local workspace or platform download path.

Mitigation: Run the skill in an isolated workspace when possible and handle generated files according to internal financial-data controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiqikuaidianpao/skills/crc-monthly-financial-report)

## Skill Output:

**Output Type(s):** [text, markdown, files, json, guidance]

**Output Format:** [Markdown report text plus generated .md, .docx, and .json files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Word output may include red-highlighted attribution placeholders for human review.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
