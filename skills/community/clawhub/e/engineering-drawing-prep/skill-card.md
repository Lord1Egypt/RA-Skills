## Description:

Automated pre-design document preparation for engineering projects. Standardize client DWGs, audit deliverables, extract data tables, and generate RFIs before real design begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mclyang](https://clawhub.ai/user/mclyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering document-control teams use this skill to prepare client-supplied engineering deliverables before design work begins. It inventories and hashes files, standardizes DWG packages, audits CAD quality issues, extracts schedule/register data, and drafts RFIs for missing project information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The intake audit can delete ._*, .DS_Store, .dwl, and .dwl2 files from the supplied client folder in place.

Mitigation: Run the workflow only on a copied working directory and preserve the original client deliverables as read-only source records.

Risk: Generated RFIs, audit reports, and extracted registers may be incomplete or incorrect for engineering decisions.

Mitigation: Treat generated outputs as advisory drafts and require review by the responsible engineering or document-control team before use.

Risk: Optional package installation guidance is unpinned.

Mitigation: Install dependencies only in an approved virtual environment or through the organization's approved package process.

## Reference(s):

- [Industry Standards and Field Lessons](references/industry_standards.md)
- [Title Block Template](templates/title_block.md)
- [Register Schema](schemas/register_schema.json)
- [ClawHub skill page](https://clawhub.ai/mclyang/skills/engineering-drawing-prep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON, CSV, DWG/PDF package, report, and RFI file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow artifacts such as manifests, hash logs, QA reports, register files, and RFI summaries; generated engineering outputs require professional review.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
