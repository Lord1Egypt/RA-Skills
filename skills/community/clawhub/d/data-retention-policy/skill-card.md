## Description:

Build a data retention and deletion schedule grounded in legal basis, including data categories, retention periods, legal or business basis, deletion triggers and methods, and flags for data kept with no basis or no defined period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and compliance teams use this skill to draft retention schedules that connect each data category to a retention period, justification, deletion trigger, deletion method, and affected systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated retention periods may be incorrect for regulated data, specific jurisdictions, or organization-specific obligations.

Mitigation: Review generated retention periods with legal or compliance staff before adopting them, especially for regulated data.

Risk: The artifact is markdown-only, while the skill text references optional helper commands for scripts/retention_schedule.py.

Mitigation: Do not expect the documented helper commands to work unless the helper script is supplied and reviewed separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/data-retention-policy)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/data-retention-policy.html)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a retention schedule with principles, deletion mechanics, and flags for missing retention periods or missing legal/business basis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
