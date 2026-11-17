## Description:

Ding Skills lets an agent use DingTalk APIs to look up users and departments, send messages, manage approvals, schedule meetings and events, and create or search DingTalk knowledge-base documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hioneowner](https://clawhub.ai/user/hioneowner)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill through an agent to automate DingTalk workplace tasks such as directory lookup, messaging, approvals, meetings, calendars, and knowledge-base document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact DingTalk actions such as sending messages, changing approvals, deleting or cancelling calendar items, and overwriting documents.

Mitigation: Require human confirmation before executing business-changing actions and only run those workflows when the requested action is explicit.

Risk: DingTalk app credentials may grant broad enterprise automation permissions.

Mitigation: Configure the DingTalk app with the least API permissions needed and store credentials as protected environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hioneowner/skills/ding-skills)
- [DingTalk OpenAPI endpoint](https://api.dingtalk.com)
- [DingTalk TOP API endpoint](https://oapi.dingtalk.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON command output with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk app credentials and optional robot code environment variables.]

## Skill Version(s):

2.3.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
