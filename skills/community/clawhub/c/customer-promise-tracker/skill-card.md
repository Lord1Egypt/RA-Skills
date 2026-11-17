## Description:

Extracts customer commitments from calls and messages, tracks their status, and produces an overdue list with links to original evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, account managers, and agencies use this skill to capture customer promises, record fulfillment, and review open or overdue commitments with links to their sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer promise records sent to BlueColumn may contain sensitive business information, personal details, or internal links.

Mitigation: Use only if BlueColumn is approved for the data; omit secrets, regulated data, unnecessary personal details, and internal-only links, using minimal summaries or opaque record IDs where possible.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/customer-promise-tracker)
- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown list with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists promise owners, commitments, due dates, and fulfillment status when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
