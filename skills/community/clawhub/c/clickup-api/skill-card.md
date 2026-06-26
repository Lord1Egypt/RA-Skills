## Description: <br>
ClickUp API integration with managed OAuth for accessing tasks, lists, folders, spaces, workspaces, users, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to connect agents to ClickUp through Maton-managed OAuth, then read or manage workspaces, spaces, folders, lists, tasks, users, and webhooks. It supports project tracking and workflow automation for connected ClickUp accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Maton API key can grant access to connected ClickUp data and actions. <br>
Mitigation: Keep MATON_API_KEY private, install only when Maton is trusted to broker ClickUp OAuth/API traffic, and avoid exposing the key in logs or shared command output. <br>
Risk: Create, update, delete, connection, and webhook actions can change ClickUp resources or integrations. <br>
Mitigation: Review the target resource, connected account, and intended effect before approving any write, delete, connection, or webhook operation. <br>
Risk: Requests may target the wrong ClickUp account when multiple connections are linked. <br>
Mitigation: Specify the intended connection with the Maton-Connection header when more than one ClickUp account is available. <br>


## Reference(s): <br>
- [ClawHub ClickUp Skill Listing](https://clawhub.ai/byungkyu/clickup-api) <br>
- [Related API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [ClickUp API Overview](https://developer.clickup.com/docs/Getting%20Started.md) <br>
- [ClickUp Get Tasks](https://developer.clickup.com/reference/gettasks.md) <br>
- [ClickUp Create Task](https://developer.clickup.com/reference/createtask.md) <br>
- [ClickUp Update Task](https://developer.clickup.com/reference/updatetask.md) <br>
- [ClickUp Delete Task](https://developer.clickup.com/reference/deletetask.md) <br>
- [ClickUp Create Webhook](https://developer.clickup.com/reference/createwebhook.md) <br>
- [ClickUp Rate Limits](https://developer.clickup.com/docs/rate-limits.md) <br>
- [ClickUp LLM Reference](https://developer.clickup.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP, Python, and JavaScript examples that return JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write, delete, connection, and webhook actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
