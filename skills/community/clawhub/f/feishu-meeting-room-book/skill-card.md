## Description: <br>
Feishu Meeting Room Book learns a user's commonly used Feishu meeting rooms from calendar events and books rooms in priority order when creating or updating Feishu calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyinghanger](https://clawhub.ai/user/flyinghanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or assistants using Feishu/Lark calendar use this skill to initialize and refresh a local meeting-room preference list, create meetings, and attach an available preferred room to new or existing events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu calendar read, create, update, and free/busy permissions. <br>
Mitigation: Install only when those permissions match the intended booking workflow, and complete Feishu OAuth with the documented calendar scopes before use. <br>
Risk: The skill learns meeting-room preferences from recent calendar events and persists them in state/feishu-meeting-room-book.json. <br>
Mitigation: Review or remove the state file when saved room order, city, or preference history should not persist. <br>
Risk: The first version maintains one cached base city and does not automatically book rooms for other cities. <br>
Mitigation: For cross-city meetings, create the event without automatic room booking or manually seed and refresh the desired city before relying on the cache. <br>
Risk: Refresh depends on valid per-slice Feishu event JSON and stops on malformed or truncated event slices. <br>
Mitigation: Retry refresh after fixing the failed slice output; the helper preserves the previous state when refresh cannot complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flyinghanger/feishu-meeting-room-book) <br>
- [Publisher profile](https://clawhub.ai/user/flyinghanger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and JSON state references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu calendar events through required Feishu tools and writes renewable local room preference state.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
