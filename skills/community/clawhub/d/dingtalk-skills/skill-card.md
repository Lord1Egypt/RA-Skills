## Description:

DingTalk Skills helps an agent operate DingTalk workflows for user and department lookup, messaging, meetings, approvals, calendars, and knowledge-base documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hioneowner](https://clawhub.ai/user/hioneowner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized DingTalk tenant operators use this skill to look up employees and departments, send messages, manage approvals, schedule meetings, query calendars, and work with knowledge-base documents through DingTalk scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform tenant-affecting actions such as sending messages, approving or terminating workflows, deleting schedules, canceling meetings, and overwriting documents.

Mitigation: Install only for an authorized DingTalk tenant, use a least-privilege DingTalk app, and require human confirmation before any message, approval, calendar, meeting, or document modification.

Risk: The skill can expose sensitive business data, including employee lists, resignation records, meeting links, conference passwords, host passwords, and robot codes.

Mitigation: Treat all returned employee, meeting, approval, robot, and document data as sensitive and limit access, storage, and onward sharing according to tenant policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hioneowner/skills/dingtalk-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/hioneowner)
- [DingTalk OpenAPI endpoint](https://api.dingtalk.com)
- [DingTalk legacy OpenAPI endpoint](https://oapi.dingtalk.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require DingTalk app credentials in environment variables and return structured success or error JSON.]

## Skill Version(s):

2.2.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
