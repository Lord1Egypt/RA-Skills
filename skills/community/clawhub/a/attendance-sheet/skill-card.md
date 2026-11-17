## Description:

Generate professional attendance sheets in xlsx format from employee work information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gykdly](https://clawhub.ai/user/gykdly)

### License/Terms of Use:


## Use Case:

HR staff, team managers, and operations users use this skill to create standardized Excel attendance sheets from employee names, date ranges, and attendance statuses for daily or monthly tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated attendance spreadsheets can contain sensitive HR records.

Mitigation: Store and share generated files under the organization's HR data handling, access control, retention, and deletion policies.

Risk: Untrusted employee names or spreadsheet text may introduce spreadsheet formula injection if formula-leading characters are not neutralized.

Mitigation: Sanitize spreadsheet-bound text by neutralizing values that begin with formula-leading characters before creating or distributing workbooks.

Risk: The generated workbook labels and command-line output are Chinese-language oriented.

Mitigation: Confirm the Chinese-language output fits the intended workflow before adopting the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gykdly/skills/attendance-sheet)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [XLSX spreadsheet file with concise command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated attendance workbooks include employee rows, date columns, status cells, summary counts, and professional formatting.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
