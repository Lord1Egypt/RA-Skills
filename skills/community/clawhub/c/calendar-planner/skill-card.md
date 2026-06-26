## Description: <br>
Plan work and life across Google Calendar, Outlook, Apple Calendar, and CalDAV with CLI adapters, conflict repair, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to reconcile personal and work commitments, audit calendar conflicts, choose defended time slots, and prepare safe calendar action sequences across approved calendar providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar metadata may be exposed to configured calendar providers or local calendar CLI tools during reads and writes. <br>
Mitigation: Use read-only scopes until writes are required, limit each workflow to the selected provider, and review the target calendar before approving any command. <br>
Risk: Calendar write commands could create, move, delete, or invite people to events if approved without review. <br>
Mitigation: Prefer draft plans and dry-run command sequences first, then explicitly approve only the narrow write action that matches the chosen plan. <br>
Risk: Local merged exports or planning notes can contain sensitive schedule context. <br>
Mitigation: Keep optional continuity files minimal, avoid storing attendee lists or detailed event notes unless needed, and periodically delete local exports or ~/calendar-planner/ notes. <br>


## Reference(s): <br>
- [Calendar Planner ClawHub release page](https://clawhub.ai/ivangdavila/calendar-planner) <br>
- [Calendar Planner skill homepage](https://clawic.com/skills/calendar-planner) <br>
- [Google Calendar API endpoint family](https://www.googleapis.com/calendar/v3/) <br>
- [Microsoft Graph API endpoint family](https://graph.microsoft.com/v1.0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and local script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run calendar commands, normalized calendar JSON, conflict reports, and weekly planning summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
