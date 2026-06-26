## Description: <br>
AI-powered personal secretary for task management and goal tracking that gives a Top 3 daily brief, captures ideas, tracks momentum, adapts to available time and energy, works with any model, and keeps data local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanglin14](https://clawhub.ai/user/yanglin14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill as a local-first personal secretary for prioritizing daily work, capturing goals and ideas, tracking completion momentum, and turning natural-language requests into task-management CLI actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores tasks, calendar-derived event details, action logs, and long-term personal preferences in a local SQLite database. <br>
Mitigation: Install only when local storage of this personal context is acceptable, set GTI_DB_DIR deliberately when needed, and use list-ltm, clear-ltm, list-calendars, and disconnect-calendar to audit or remove stored data. <br>
Risk: Connected iCal calendar URLs may contain private tokens and morning briefs may fetch connected calendars automatically. <br>
Mitigation: Connect only trusted calendar URLs or local files, avoid displaying private calendar URLs, and disconnect calendars that should no longer be synced. <br>
Risk: The skill can silently store lasting preferences, constraints, insights, or context when users disclose them. <br>
Mitigation: Review long-term memory periodically and delete entries that should not remain available to future briefings. <br>


## Reference(s): <br>
- [Publisher profile](https://clawhub.ai/user/yanglin14) <br>
- [ClawHub skill page](https://clawhub.ai/yanglin14/get-to-it) <br>
- [Project homepage](https://github.com/yanglin/get-to-it) <br>
- [Persona guide](references/persona.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style assistant responses with CLI command invocations and JSON-backed task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python CLI and local SQLite database for tasks, calendar metadata, action logs, and long-term preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
