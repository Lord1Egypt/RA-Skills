## Description: <br>
Helps an agent manage DingTalk calendar workflows with curl-based API calls for primary-calendar events, free/busy lookup, video meetings, meeting rooms, sign-in and sign-out links, and recurrence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent prepare and run DingTalk calendar API workflows for scheduling, updating, deleting, checking availability, adding meeting rooms, creating video meetings, and handling sign-in or sign-out flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, and otherwise change DingTalk calendar data. <br>
Mitigation: Confirm create, update, delete, meeting-room, sign-in, and sign-out actions before execution. <br>
Risk: The skill stores DingTalk credentials and token material in a local configuration file. <br>
Mitigation: Use a least-privilege DingTalk app, restrict permissions on ~/.dingtalk-skills/config, and avoid sharing logs that contain tokens or identifiers. <br>


## Reference(s): <br>
- [DingTalk Calendar API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl commands and a local helper script for DingTalk token, identity, and configuration handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
