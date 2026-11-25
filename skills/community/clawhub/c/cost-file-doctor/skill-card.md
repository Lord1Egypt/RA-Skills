## Description:

Diagnoses construction-cost files for format, likely encryption, and local parsing feasibility, recommends next steps, and cleans repeated headers in exported Excel workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kormendierijon681-oss](https://clawhub.ai/user/kormendierijon681-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Cost engineers and project teams use this skill to identify common construction-cost file formats, assess whether local parsing is practical, and choose a next step. It can also remove repeated page headers from exported Excel workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet content may be interpreted as formulas when opened in spreadsheet software.

Mitigation: Treat workbook contents as untrusted, review the cleaned output before opening or sharing it, and keep the original file unchanged.

Risk: The suggested file search can look beyond the target file's immediate directory.

Mitigation: Limit the search to the relevant project directory and review candidate files before using them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kormendierijon681-oss/skills/cost-file-doctor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Files]

**Output Format:** [Markdown diagnostic report and cleaned Excel workbook (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports file-format and parsing guidance; the optional workbook output removes repeated page headers and applies readable formatting.]

## Skill Version(s):

1.0.3 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
