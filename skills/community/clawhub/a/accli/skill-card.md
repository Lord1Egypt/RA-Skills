## Description: <br>
Helps agents interact with Apple Calendar on macOS to list calendars, view events, create, update, and delete events, and check free/busy availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joargp](https://clawhub.ai/user/joargp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents assisting macOS users use this skill to inspect Apple Calendar schedules, find available time, and prepare or apply calendar changes through the accli CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Apple Calendar data through the external @joargp/accli npm package. <br>
Mitigation: Install only if the publisher and package are trusted, grant Calendar access deliberately on macOS, and review commands before execution. <br>
Risk: Create, update, and delete commands can change or remove calendar events. <br>
Mitigation: Confirm event details with the user before executing calendar writes, and use explicit calendar names or IDs with narrow date ranges. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/joargp/accli) <br>
- [@joargp/accli npm package](https://www.npmjs.com/package/@joargp/accli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for macOS Apple Calendar; recommends --json for parseable command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
