## Description: <br>
Free habit tracking, todo, and routines for creating and tracking habits, tasks, routines, reminders, and daily briefings across chat surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phantue2002](https://clawhub.ai/user/phantue2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent integrators use this skill to manage personal habits, todos, routines, reminders, and progress summaries through the Buffy API from chat or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit, task, routine, reminder text, user IDs, and settings are sent to Buffy's external API. <br>
Mitigation: Use the skill only where that data sharing is acceptable and keep requests scoped to the user's Buffy-related intent. <br>
Risk: BUFFY_API_KEY or generated Buffy API keys could expose account access if logged or shared. <br>
Mitigation: Store keys in the agent environment or approved secret store, avoid printing them, and review generated keys before use. <br>
Risk: Optional hooks can persist conversation snippets or dispatch reminders to chat channels. <br>
Mitigation: Enable optional hooks deliberately, control log location and retention, and configure channel credentials only for approved destinations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phantue2002/buffy-agent) <br>
- [Publisher profile](https://clawhub.ai/user/phantue2002) <br>
- [Buffy CLI repository](https://github.com/phantue2002/buffy-cli) <br>
- [Buffy CLI releases](https://github.com/phantue2002/buffy-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration] <br>
**Output Format:** [Natural-language replies, Markdown guidance, JSON API payloads, and inline shell/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BUFFY_API_KEY and outbound HTTPS access to the configured Buffy API endpoint.] <br>

## Skill Version(s): <br>
1.1.7 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
