## Description: <br>
DingTalk Bot integrates messaging, group management, approval workflows, attendance queries, and automated notifications through the DingTalk Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to let agents send DingTalk messages, manage group membership, create or query approvals, and retrieve attendance or vacation information. It is suited to workplace automation where DingTalk credentials and permissions are tightly controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send workplace messages and alter group, approval, or attendance-related workflows. <br>
Mitigation: Require explicit human approval for side-effecting actions and limit the DingTalk robot or internal app to the minimum permissions needed. <br>
Risk: Webhook URLs, app secrets, and access tokens can expose DingTalk workspace access if stored or logged improperly. <br>
Mitigation: Store credentials only in protected environment variables or a secrets manager, avoid logging secrets, and rotate credentials if exposure is suspected. <br>
Risk: Attendance and vacation queries can expose sensitive employee information. <br>
Mitigation: Restrict API scopes and user access to approved business cases, and review requests before retrieving employee attendance or leave data. <br>


## Reference(s): <br>
- [DingTalk Open Platform](https://open.dingtalk.com) <br>
- [DingTalk API Documentation](https://open.dingtalk.com/document/) <br>
- [DingTalk Robot Development](https://open.dingtalk.com/document/robot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Python snippets, shell environment settings, Markdown messages, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk webhook or internal app credentials; API calls can change messaging, groups, approvals, and attendance workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
