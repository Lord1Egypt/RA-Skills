## Description: <br>
DingTalk Skills helps agents look up users and departments, send messages, manage approvals, schedule meetings, query calendars, and manage DingTalk knowledge-base documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hioneowner](https://clawhub.ai/user/Hioneowner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and operations teams use this skill to let an agent operate DingTalk workflows for people lookup, department lookup, messaging, approvals, meetings, calendars, and knowledge-base documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate against a real DingTalk organization with broad messaging, approval, calendar, meeting, document, and employee-directory capabilities. <br>
Mitigation: Use a least-privilege DingTalk app and grant only the API scopes needed for the intended workflows. <br>
Risk: Send, approve, reject, delete, cancel, transfer, and overwrite actions can change real organizational state. <br>
Mitigation: Manually confirm recipients, approval IDs, event IDs, meeting IDs, workspace IDs, and document contents before executing those actions. <br>
Risk: DingTalk app secrets and robot codes could expose organization access if logged or shared. <br>
Mitigation: Keep DINGTALK_APP_KEY, DINGTALK_APP_SECRET, and DINGTALK_ROBOT_CODE in protected environment storage and avoid printing them in logs or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hioneowner/dingtalk-skills) <br>
- [DingTalk OpenAPI endpoint](https://api.dingtalk.com) <br>
- [DingTalk TOP API endpoint](https://oapi.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk app credentials and optional robot code environment variables.] <br>

## Skill Version(s): <br>
2.2.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
