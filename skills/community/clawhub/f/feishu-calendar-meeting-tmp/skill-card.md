## Description: <br>
Creates Feishu calendar events and video meetings through the Feishu Calendar API, automatically linking Feishu video meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelaner](https://clawhub.ai/user/kelaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to create Feishu calendar events with optional Feishu video meeting links after OAuth authorization. It helps agents prepare calendar API requests, token handling guidance, and event creation commands for Feishu workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Feishu user token exposed in chat, logs, or workspace files could allow unintended access to the user's Feishu calendar integration. <br>
Mitigation: Store the token in the platform secret mechanism where possible, keep scopes narrow, rotate exposed tokens, and avoid printing or persisting tokens. <br>
Risk: The skill performs calendar API actions on behalf of the user, so incorrect event details could create unwanted or inaccurate meetings. <br>
Mitigation: Review the event title, time, calendar ID, optional description, optional location, and video meeting setting before executing the API request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelaner/feishu-calendar-meeting-tmp) <br>
- [Publisher profile](https://clawhub.ai/user/kelaner) <br>
- [Feishu calendars API endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars) <br>
- [Feishu calendar events API endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars/${CALENDAR_ID}/events) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu OAuth token handling guidance, calendar ID lookup commands, event payload examples, and meeting creation response summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
