## Description:

Master Excel/CSV data processing - cleaning, transforming, merging, and analyzing spreadsheets with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beibei030](https://clawhub.ai/user/beibei030)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, office workers, accountants, HR staff, sales teams, administrators, and students use this skill to ask an agent for Excel/CSV cleaning, transformation, merging, analysis, formatting, formula guidance, and batch-processing examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic spreadsheet cleanup can change important financial, HR, customer, or operational data through deletions, deduplication, missing-value filling, outlier filtering, or overwrites.

Mitigation: Work on copies, require explicit confirmation before applying changes, and ask the agent to show row and column change counts before saving results.

Risk: Generated formulas or transformation code can produce incorrect results when assumptions about columns, data types, outliers, or merge keys are wrong.

Mitigation: Review formulas and code, validate merge keys and unmatched rows, inspect representative samples, and compare results against expected totals before using outputs in decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with Python and Excel formula code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include spreadsheet change summaries, formulas, and pandas/openpyxl snippets; users should confirm before applying destructive data changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
