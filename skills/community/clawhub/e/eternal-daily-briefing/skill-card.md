## Description:

Generates a consolidated daily briefing with weather, calendar events, tasks, news, and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agent workflows use this skill to assemble a daily update from weather, news, market, task, and event sources. It supports full, compact, JSON, and section-focused briefing modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Section-only commands may still contact all configured external services and read local briefing files before unused sections are hidden.

Mitigation: Review configuration before use, avoid narrow modes when privacy or offline behavior is required, or modify the script so each section fetches only the data it displays.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-daily-briefing)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Formatted console text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full, short, and section-focused daily briefing output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
