## Description: <br>
Helps agents send and query DingTalk daily or weekly reports and generate work-quality summaries with scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigint1](https://clawhub.ai/user/bigint1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and authorized workplace agents use this skill to create DingTalk daily or weekly reports, query report history, search for user IDs by name, and generate work-quality summaries from retrieved reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access workplace report data and employee IDs through DingTalk credentials without clear authorization boundaries. <br>
Mitigation: Install only with a least-privilege DingTalk internal app credential and use it only for users and reports the operator is authorized to access. <br>
Risk: Incorrect report text, target user IDs, recipients, date ranges, or chat notification settings could expose workplace data to the wrong audience. <br>
Mitigation: Before each action, verify the target user ID, date range, report content, recipients, and whether chat notification is enabled. <br>


## Reference(s): <br>
- [DingTalk report API specification](references/api-spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/bigint1/dingtalk-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Node.js shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk internal app credentials and user-confirmed IDs, date ranges, report content, recipients, and notification settings.] <br>

## Skill Version(s): <br>
0.9.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
