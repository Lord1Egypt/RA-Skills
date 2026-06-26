## Description: <br>
钉钉 OA 审批工具 helps an OpenClaw agent query pending DingTalk approval tasks, inspect approval details, approve or reject tasks, and query vacation balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whauff](https://clawhub.ai/user/whauff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workplace assistants use this skill to review DingTalk OA approval queues, inspect task details, record approve or reject decisions, and check vacation balances. Administrators configure it with a DingTalk user ID, app key, and app secret for an app that has the required OA approval permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can approve or reject live workplace approval tasks in one step. <br>
Mitigation: Require the assistant to show the exact task details and obtain explicit user confirmation before each approve or reject action. <br>
Risk: Misconfigured or overprivileged DingTalk credentials could expose or alter approval workflows beyond the intended user scope. <br>
Mitigation: Use a dedicated least-privilege DingTalk app, avoid shared or administrator user IDs, and protect the app secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whauff/dingtalk-approval) <br>
- [Publisher profile](https://clawhub.ai/user/whauff) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [DingTalk OA approval task API](https://open.dingtalk.com/document/orgapp-server/query-the-tasks-to-be-processed-by-the-user) <br>
- [DingTalk user ID documentation](https://open.dingtalk.com/document/orgapp-server/obtain-the-userid-of-a-member) <br>
- [API reference](references/api-docs.md) <br>
- [Configuration guide](references/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown-formatted text responses with task lists, approval details, status messages, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return live DingTalk approval data and can execute approve or reject actions when configured with valid credentials and permissions.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
