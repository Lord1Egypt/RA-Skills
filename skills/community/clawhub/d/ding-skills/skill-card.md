## Description: <br>
Ding Skills helps agents use DingTalk APIs for organization lookup, department queries, message sending, approval workflows, meetings, calendars, and knowledge-base document operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hioneowner](https://clawhub.ai/user/Hioneowner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers in DingTalk-backed organizations use this skill to automate directory lookup, department discovery, messaging, approval, meeting, calendar, and DingTalk knowledge-base workflows. It is intended for live DingTalk organization automation when the operator has configured appropriate DingTalk app credentials and API permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing summary describes web scraping, but the reviewed package is a broad DingTalk automation skill. <br>
Mitigation: Install only when DingTalk organization automation is intended, and review the artifact behavior against the listing before deployment. <br>
Risk: The skill can change business messages, approvals, calendars, meetings, and knowledge-base documents. <br>
Mitigation: Use a least-privilege DingTalk app and require human confirmation before sending messages, approving or rejecting workflows, deleting events, canceling meetings, or overwriting documents. <br>


## Reference(s): <br>
- [ClawHub Ding Skills listing](https://clawhub.ai/Hioneowner/ding-skills) <br>
- [DingTalk OpenAPI endpoint](https://api.dingtalk.com) <br>
- [DingTalk OAPI endpoint](https://oapi.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, JSON, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk app credentials and can execute live organization, message, approval, calendar, meeting, and document operations.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
