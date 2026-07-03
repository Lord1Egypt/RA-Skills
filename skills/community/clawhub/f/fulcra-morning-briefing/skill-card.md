## Description: <br>
Compose a personalized morning briefing using Fulcra sleep, biometric, calendar, activity, and optional weather context, with tone and detail calibrated to how the user slept. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to collect recent Fulcra sleep, biometric, activity, calendar, and optional weather context, then compose a personalized morning briefing calibrated to sleep quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Morning briefings can expose sensitive sleep, biometric, steps, location, and calendar details. <br>
Mitigation: Deliver detailed briefings only to the intended user or an explicitly approved channel; keep group-chat summaries qualitative and minimal. <br>
Risk: The optional cron workflow can write sensitive briefing JSON to /tmp. <br>
Mitigation: Store scheduled output in a user-private path with restrictive permissions and a retention policy. <br>
Risk: A briefing may be based on stale or incomplete Fulcra data. <br>
Mitigation: Use freshness checks as signals and fetch the specific sleep, biometric, activity, calendar, and weather records before summarizing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arc-claw-bot/skills/fulcra-morning-briefing) <br>
- [Fulcra Platform](https://fulcradynamics.com) <br>
- [Fulcra Developer Docs](https://fulcradynamics.github.io/developer-docs/) <br>
- [Context iOS App](https://apps.apple.com/app/id1633037434) <br>
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python) <br>
- [Fulcra Context MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing prose with optional JSON collection output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Fulcra workflow; briefing length, tone, and detail vary with sleep quality.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
