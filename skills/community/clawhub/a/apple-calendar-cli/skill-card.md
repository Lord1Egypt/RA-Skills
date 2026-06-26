## Description: <br>
Manage Apple Calendar events on macOS 14+ using apple-calendar-cli to list, get, create, update, and delete events with ISO 8601 date support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sichengchen](https://clawhub.ai/user/sichengchen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to manage Apple Calendar from a command-line workflow. It supports checking schedules and creating, updating, or deleting calendar events after Calendar access is granted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Apple Calendar events after the user grants macOS Calendar access. <br>
Mitigation: Grant Calendar permission deliberately, use narrow date ranges or calendar filters where possible, and require the agent to show the exact target event before creating, rescheduling, or deleting anything. <br>
Risk: Calendar event identifiers can become stale if events change outside the current agent workflow. <br>
Mitigation: List or get the event immediately before update or delete operations and confirm the event identifier, title, and time. <br>


## Reference(s): <br>
- [Apple Calendar CLI ClawHub Release](https://clawhub.ai/sichengchen/apple-calendar-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents are instructed to use --json for reliable parsing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
