## Description:

Helps users triage unanswered email, draft replies and scheduling messages, track commitments, and prepare meeting briefs from authorized materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other authorized users use this skill to review selected email and meeting materials, prepare reply and follow-up drafts, track commitments, and assemble pre-meeting notes. External actions require separate authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive email or meeting information may be exposed through overly broad access or uploads.

Mitigation: Confirm the exact materials, recipients, tool permissions, and allowed upload scope; minimize or redact private data before sharing.

Risk: Drafts or automated actions may be sent, deleted, or written back without appropriate review.

Mitigation: Keep drafts in a review queue and obtain explicit authorization before sending, deleting, or changing business records.

Risk: Model use or tool calls may incur unapproved costs.

Mitigation: Confirm current prices, currency, and budget before paid work; test a small sample first and avoid blind retries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-fyxer-mail-followup)
- [AI-HIVE connection and authorization](references/ai-hive-connection.md)
- [Workflow and output contract](references/output-contract.md)
- [Fyxer product site (comparison context)](https://www.fyxer.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Reviewable drafts, CSV lists, meeting briefs, and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source references, unresolved items, and review status; drafts do not imply messages were sent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
