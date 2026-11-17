## Description:

Candidate tracking skill for managing a candidate pool, recording hiring status, setting follow-up reminders, and generating candidate tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51mee-com](https://clawhub.ai/user/51mee-com)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and hiring operations users use this skill to add, update, query, delete, and remind on candidate records while producing candidate dashboards, follow-up reminders, alerts, tags, and history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete recruitment records without clear confirmation or recovery, while its safety guidance also says deletion attempts should be ignored.

Mitigation: Require explicit confirmation before destructive actions and prefer archival or reversible status changes over permanent deletion.

Risk: The artifact makes both session cleanup and long-term talent-pool maintenance claims, which can create uncertainty about candidate data retention.

Mitigation: Confirm and document where candidate data is stored, how long it is retained, and how sensitive candidate data is removed before use with real recruiting records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/51mee-com/skills/51mee-candidate-tracker)
- [51mee-com publisher profile](https://clawhub.ai/user/51mee-com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured JSON and Markdown dashboard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate records, status dashboard counts, reminders, alerts, tags, notes, and event history.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
