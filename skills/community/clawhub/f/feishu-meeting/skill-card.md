## Description: <br>
Create Feishu (Lark) video meetings through the Calendar API for instant, scheduled, or recurring meetings with invitee resolution, generated video links, and attendee calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicaldd](https://clawhub.ai/user/magicaldd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and developers use this skill to create Feishu meetings, invite attendees by mobile number or email, schedule one-time or recurring calls, and place the resulting event on Feishu calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted meeting details could run unintended local code because the script handles user input unsafely. <br>
Mitigation: Use only trusted meeting details until the script passes user input to Python as data rather than executable source. <br>
Risk: The skill creates attendee-visible calendar entries. <br>
Mitigation: Confirm topic, start time, duration, recurrence, and invitees before running the command. <br>
Risk: The skill requires Feishu app credentials and calendar/contact permissions. <br>
Mitigation: Configure a least-privilege Feishu app with only the required scopes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/magicaldd/feishu-meeting) <br>
- [Feishu bot capability documentation](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-enable-bot-ability) <br>
- [Feishu Calendar API calendars endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates attendee-visible Feishu calendar events and prints meeting details including topic, link, attendees, recurrence, and unresolved invitees.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
