## Description:

Diagnose spreadsheet structure and recommend practical Excel/WPS-compatible formulas and workflows for cleaning, lookup and matching, summarization, text and date cleanup, and common formula troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winstonice-prog](https://clawhub.ai/user/winstonice-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and spreadsheet users use this skill to inspect Excel or WPS table structure, identify cleanup risks, and choose compatible formulas or workflows for matching, summarization, text/date cleanup, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet guidance can affect important workbook data if users apply changes directly.

Mitigation: Work on a copy for important files and require user confirmation before direct workbook changes, helper columns, or formula rewrites.

Risk: Lookup, matching, or merge recommendations can produce incorrect results when keys contain duplicates, blanks, or inconsistent formats.

Mitigation: Confirm lookup keys and duplicate records before matching sheets, and clean unstable source columns before applying formulas.

Risk: Formula compatibility can vary across Excel and WPS versions.

Mitigation: Prefer broadly compatible formulas, provide helper-column fallbacks, and verify behavior in the target spreadsheet application before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/winstonice-prog/skills/excel-wps-table-diagnosis)
- [README](artifact/README.md)
- [Spreadsheet Table Diagnosis Workflow](artifact/WORKFLOW.md)
- [Use Cases](artifact/docs/use-cases.md)
- [Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with spreadsheet formulas and step-by-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Excel/WPS compatibility notes, helper-column recommendations, cleanup order, and confirmation prompts before direct workbook changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
