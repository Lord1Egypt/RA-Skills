## Description: <br>
Manage Google Calendar events using `gcalcli`, including creating, listing, and deleting calendar events from the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Google Calendar events from an agent workflow through `gcalcli`, including listing agendas and creating or deleting events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and delete real calendar events. <br>
Mitigation: Confirm the calendar account, event title, date/time, and exact event match before running create or delete commands, especially when deleting by search term. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/brainz-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `gcalcli` and calendar credentials configured for the intended account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
