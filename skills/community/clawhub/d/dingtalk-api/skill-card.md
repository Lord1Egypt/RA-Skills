## Description:

Calls DingTalk Open Platform APIs for user and department lookup, bot messaging, group bot listing, resigned employee queries, and OA approval workflow operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogenes](https://clawhub.ai/user/ogenes)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to run DingTalk organization, messaging, and OA approval workflow API tasks from an agent environment. It is suited for controlled internal automation where a DingTalk app has been granted the required API permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access organization data, bot messaging, and OA approval workflow actions through a DingTalk internal app.

Mitigation: Use a least-privileged DingTalk app and grant only the API permissions needed for the intended task.

Risk: Approval create, terminate, agree/refuse, transfer, and comment operations can affect business workflows.

Mitigation: Require human review before running approval-changing commands, especially in production environments.

Risk: Testing with production credentials can expose live organization data or trigger real workflow changes.

Mitigation: Avoid production credentials until the workflow has been tested with controlled accounts and data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ogenes/skills/dingtalk-api)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ogenes)
- [DingTalk Internal App Access Token](https://open.dingtalk.com/document/orgapp/obtain-the-access_token-of-an-internal-app)
- [DingTalk Chatbot One-on-One Messages](https://open.dingtalk.com/document/orgapp/chatbots-send-one-on-one-chat-messages-in-batches)
- [DingTalk Group Robot Messages](https://open.dingtalk.com/document/orgapp/the-robot-sends-a-group-message)
- [DingTalk Approval Instance Creation](https://open.dingtalk.com/document/isvapp-server/create-an-approval-instance)
- [DingTalk Approval Operation Execution](https://open.dingtalk.com/document/isvapp-server/execute-approval-operation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DINGTALK_APP_KEY and DINGTALK_APP_SECRET and an appropriately permissioned DingTalk app.]

## Skill Version(s):

1.4.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
