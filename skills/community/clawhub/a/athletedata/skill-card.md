## Description:

Read the user's own training and health data (Garmin, Oura, WHOOP, Hevy, Apple Health, Intervals.icu and 33 more apps) through the athletedata MCP server. Use when the user asks about their workouts, training load, HRV, sleep, recovery, readiness, nutrition, body composition, race predictions, or wants a structured workout pushed to their watch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athletedata](https://clawhub.ai/user/athletedata)

### License/Terms of Use:

MIT-0

## Use Case:

Athletes and their AI assistants use this skill to review connected training, recovery, sleep, nutrition, and health data, and to prepare account changes such as workouts, meals, or routines for user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This integration exposes sensitive health and fitness information through a hosted service.

Mitigation: Connect only the fitness accounts you want the AI to access, and protect the API key.

Risk: Proposed workouts, meal entries, or routines can change the user's connected accounts.

Mitigation: Review each proposed change and confirm it before execution.

## Reference(s):

- [athletedata MCP homepage](https://www.athletedata.health/mcp?utm_source=clawhub&utm_medium=mcp-directory)
- [MCP server endpoint](https://mcp.athletedata.health/mcp)
- [API key dashboard](https://www.athletedata.health/dashboard/mcp)
- [ClawHub skill page](https://clawhub.ai/athletedata/skills/athletedata)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Natural-language summaries and guidance, with Markdown or shell-command setup instructions when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized results depend on the athlete's connected accounts; changes to workouts, meals, or routines require user confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
