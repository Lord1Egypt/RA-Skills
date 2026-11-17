## Description:

Send local image files as native Feishu image messages via the Feishu Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonzhang2015](https://clawhub.ai/user/jasonzhang2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send generated images, charts, screenshots, or local image files to Feishu users or group chats as native image messages instead of attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials are passed as script arguments and the artifact includes a secret-looking example value.

Mitigation: Replace example values, rotate the Feishu secret if it may be real, and prefer a protected secret store or restricted configuration file over command-line arguments.

Risk: The skill uses Feishu app credentials with bot permissions to upload images and send messages.

Mitigation: Install only from a trusted publisher and use a Feishu app whose permissions and recipient scope are limited to the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jasonzhang2015/skills/feishu-bot-send-image)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu send message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path, Feishu receiver ID, app ID, app secret, and optional receiver ID type.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
