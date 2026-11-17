## Description:

Creates a company patent annual report comparing yearly publications, grants, and lapses, with technology-focus and inventor summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Employees preparing year-end intellectual-property reports use this skill to compare company patent publications, grants, and lapses across years and summarize technology areas and inventor contributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent API keys can create exposure risks when connecting a paid account.

Mitigation: Keep permanent keys out of chat, use a restricted credential, require HTTPS with approved destinations and safe redirects, and set a spending limit for each task.

Risk: Company names and search details are sent to PatentMax.

Mitigation: Send only company names and search details authorized for PatentMax to receive.

## Reference(s):

- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Patent search workflow](references/search-workflow.md)
- [Query construction guide](references/query-construction.md)
- [API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV]

**Output Format:** [Markdown annual report and CSV data table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Year-over-year patent statistics, technology and inventor summaries, and reporting caveats.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
