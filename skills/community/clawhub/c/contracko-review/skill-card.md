## Description:

Reviews Contracko contracts. Use for notice dates, end dates, annual review, reminders, risk audits, comparing proposals or redlines, or portfolio priorities and gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contracko](https://clawhub.ai/user/contracko)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external business users use this skill to answer contract questions from Contracko, review portfolio deadlines and gaps, compare proposals or redlines, and manage contract reminders with appropriate permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive contract records and document text when installed with Contracko contract permissions.

Mitigation: Install only when the agent should review Contracko contract data, and grant the narrowest useful permission such as contract:read for review-only workflows.

Risk: Reminder and event updates can affect business operations when contract:write is granted.

Mitigation: Grant contract:write only for reminder or event workflows, and require user confirmation before bulk writes.

Risk: Incomplete search coverage, unindexed documents, or analysis without supporting text can lead to incorrect contract conclusions.

Mitigation: State document-search completeness, follow cursors for paginated results, and quote document evidence when the user is making a decision.

## Reference(s):

- [Contracko Review skill page](https://clawhub.ai/contracko/skills/contracko-review)
- [Contracko publisher profile](https://clawhub.ai/user/contracko)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or concise text with tables, quoted evidence, and action guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Contracko contract records and document evidence; write actions for reminders or events require appropriate permission and user confirmation for bulk changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
