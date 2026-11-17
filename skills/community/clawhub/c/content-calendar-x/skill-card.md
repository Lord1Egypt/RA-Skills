## Description:

Content Calendar helps businesses and creators plan content strategy, generate post ideas, schedule platform-specific posts, and repurpose existing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v3ads](https://clawhub.ai/user/v3ads)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and teams use this skill to turn business context, audience goals, platform choices, cadence, and existing content into content pillars, post ideas, calendars, and repurposing plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated post copy, hashtags, CTAs, or scheduling guidance may be inaccurate, off-brand, or misleading if published without review.

Mitigation: Review and edit generated content and calendar timing before scheduling or publishing.

Risk: The bundled script can write generated calendar output to a local file when an output path is provided.

Mitigation: Choose the destination path explicitly and inspect the generated file before using it.

## Reference(s):

- [Post Formats by Platform](references/post-formats.md)
- [Content Calendar Template](assets/calendar-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown content calendars, optional JSON calendar entries, and concise planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local calendar file when the agent is given an output path; generated copy should be reviewed before publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
