## Description:

Clean a dataset before analysis: schema check, nulls, duplicates, outliers, and unit consistency, with every fix logged. Use before trusting any CSV, export, or scraped dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and data practitioners use this checklist before analyzing, merging, publishing, or training on a dataset. It guides repeatable checks and a cleaning log so data changes can be reviewed and reproduced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security assurance is limited because Skillspector only partially inspected the skill after a manifest parsing error.

Mitigation: Review the skill instructions and obtain a complete scan before installation if additional assurance is needed.

Risk: An incorrect cleaning rule could alter data and affect downstream analysis.

Mitigation: Keep the raw dataset unchanged and review the cleaning log, including each rule and affected-record count.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manteclaw/skills/data-cleaning-checklist)

## Skill Output:

**Output Type(s):** [Guidance, Files, Text]

**Output Format:** [Checklist guidance, a cleaned dataset in the source data's format, and a cleaning log.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve the raw dataset; record each transformation, its rule, and the number of affected records.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
