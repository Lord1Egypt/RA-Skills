## Description:

Standard Operating Procedure (SOP) that bridges extraction logic to CRM append operations via atomic nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operations teams use this skill to extract CRM entities from business emails or notes and append them to a CRM spreadsheet with verification stops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically add records to a CRM spreadsheet from broadly matched business messages without a clear confirmation step.

Mitigation: Use it only where the target spreadsheet, permitted fields, deduplication rules, and approval flow are clearly configured and reviewed before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON summary of extracted CRM data and append confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes extracted entities such as name, organization, and date, plus the CRM append result.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
