## Description:

Helps legal teams find and monitor Box-hosted contracts, extract and store metadata, and prepare cited comparisons against firm templates for attorney review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Legal teams use this skill to locate new or expiring contracts in Box, compare them with firm templates, record contract metadata, and route cited variance reports and reminders to attorneys. The attorney or firm determines materiality and risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad contract-related triggers could start a Box workflow without a clearly scoped request.

Mitigation: Confirm the target Box folder, date range, and review scope before accessing contracts.

Risk: Prerequisite Box skills are installed without a pinned version.

Mitigation: Review or pin dependency versions before installation, especially for sensitive legal work.

Risk: Metadata changes, reports, comments, and attorney collaboration can affect sensitive contracts or access.

Mitigation: Confirm the template, fields to write, report destination, and attorney sharing or comments before making changes.

## Reference(s):

- [Box skills (prerequisite)](https://github.com/box/skills)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Cited contract variance reports, structured Box metadata, and attorney-facing comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Box access and firm-confirmed review criteria; legal determinations remain with an attorney.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
