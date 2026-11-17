## Description:

Automatically cleans Excel spreadsheets by removing empty rows and columns, deduplicating records, sorting data, and generating summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfxia](https://clawhub.ai/user/sfxia)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to clean Excel workbooks and create a new organized file with deduplicated, sorted data and summary reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Purchased runs may fail because the package calls an Excel processing module that is not included.

Mitigation: Confirm the missing Excel handler is included and tested before purchase, installation, or deployment.

Risk: The skill advertises saving cleaned files to the desktop without evidence of an output-path confirmation step.

Mitigation: Ask the publisher to let users choose or confirm the output path before cleaned files are written.

Risk: Failure responses may expose internal error details.

Mitigation: Review error handling so user-facing messages are actionable without revealing unnecessary internal details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sfxia/skills/excel-auto-clean)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Cleaned Excel workbook plus status or payment-link message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a payment URL before processing; successful runs report that a new cleaned file was saved to the desktop.]

## Skill Version(s):

1.0.1 (source: server evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
