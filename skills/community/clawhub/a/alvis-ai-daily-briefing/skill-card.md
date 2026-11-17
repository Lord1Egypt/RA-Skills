## Description:

Provides a morning briefing with overdue tasks, today's priorities, calendar overview, and context from recent meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for a concise daily or weekly planning briefing from local task, meeting, calendar, and memory context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A briefing request can aggregate sensitive workspace content such as private meeting notes, calendar details, persona memory, and user preference files.

Mitigation: Review the skill before installing and limit or remove access to sensitive memory, calendar, meeting-note, or user-profile files when that aggregation is not intended.

Risk: Broad trigger phrases may cause the agent to summarize daily-work context in situations where the user did not expect sensitive sources to be included.

Mitigation: Use the skill only in workspaces where these trigger phrases are appropriate, or narrow the trigger behavior before deployment.

## Reference(s):

- [Skill homepage](https://jeffjhunter.com)
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-ai-daily-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown daily briefing with ordered sections, task lists, calendar entries, and a focus statement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates available local context when present; skips empty sections and keeps most sections concise.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
