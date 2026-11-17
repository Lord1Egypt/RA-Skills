## Description:

Automatically generate a professional Word analysis report from user-provided data files, including data overview, key metric statistics and trend analysis, key findings and conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to convert CSV, JSON, Excel, or TXT data into a professionally formatted Word analysis report with data overview, metrics, trend analysis, and findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided datasets and places derived content into a Word report.

Mitigation: Use appropriate data-handling controls for sensitive input files and review generated report content before sharing.

Risk: The report generator writes to a caller-provided output path, which could overwrite an existing file.

Mitigation: Choose an output path where replacement is acceptable or confirm that no important file already exists there.

Risk: The report generator depends on python-docx.

Mitigation: Install python-docx from a trusted package source inside an isolated Python environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and a generated .docx report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report is saved to the requested output path and the agent summarizes the report structure for review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
