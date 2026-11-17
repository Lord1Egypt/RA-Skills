## Description:

Drafts a chart specification and source-linked reading notes from one table, while documenting limitations without rendering charts or giving investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn one table into a chart-ready specification and source-linked reading notes, while recording missing or ambiguous information for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can report incorrect numbers as verified.

Mitigation: Use the result as a drafting aid and independently check every number against its cited source cell, with the source table and file or line references available.

Risk: The optional parsing service's data handling is unverified for confidential documents.

Mitigation: Keep confidential documents offline until the service's data handling is understood and authorized.

Risk: An unsafe output path could overwrite existing work.

Mitigation: Choose an output path that is safe to overwrite.

## Reference(s):

- [Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Four-section Markdown draft with chart specifications, source-linked reading notes, limitations, and source/date details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One table per draft; numeric notes trace to source cells. Does not render charts, calculate derived values, or provide investment conclusions.]

## Skill Version(s):

0.1.7 (source: frontmatter, CHANGELOG.md, released 2026-11-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
