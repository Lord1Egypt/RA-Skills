## Description: <br>
Daily briefing gathers calendar events, active todos, and local weather from available companion skills, then composes a concise summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use this skill to generate a daily briefing from their available calendar, todo, and weather companion skills. It is suited for manual invocation or scheduled morning delivery when the destination channel is private and trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled or chat-channel delivery may expose sensitive schedule, task, or location-related details. <br>
Mitigation: Enable scheduled delivery only to private, trusted channels and review the companion calendar and todo skill permissions before use. <br>
Risk: Unavailable companion skills or command failures can result in an incomplete briefing. <br>
Mitigation: Treat omitted sections as unavailable data and verify companion skill setup when expected calendar, todo, or weather details are missing. <br>


## Reference(s): <br>
- [Briefing skill page](https://clawhub.ai/lstpsche/briefing) <br>
- [gcalcli-calendar companion skill](https://clawhub.ai/lstpsche/gcalcli-calendar) <br>
- [todo-management companion skill](https://clawhub.ai/lstpsche/todo-management) <br>
- [openmeteo-sh-weather-simple companion skill](https://clawhub.ai/lstpsche/openmeteo-sh-weather-simple) <br>
- [gcalcli](https://github.com/insanum/gcalcli) <br>
- [openmeteo-sh](https://github.com/lstpsche/openmeteo-sh) <br>
- [Open-Meteo](https://open-meteo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text briefing with compact sections for weather, calendar, upcoming events, and todos] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sections are omitted when companion skills are unavailable; missing data is noted rather than fabricated.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
