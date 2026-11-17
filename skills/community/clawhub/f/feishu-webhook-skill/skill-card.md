## Description:

Sends Feishu/Lark webhook messages, including plain text, rich text posts, interactive cards, and optional image uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaniu001](https://clawhub.ai/user/shaniu001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to let an agent compose and send Feishu/Lark group notifications, rich posts, and interactive card messages through a user-provided webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook messages may be sent to an unintended Feishu/Lark destination or include unintended content.

Mitigation: Confirm webhook URLs and message contents before sending.

Risk: Tenant access tokens can be exposed if passed directly on the command line.

Mitigation: Use FEISHU_TENANT_ACCESS_TOKEN through a protected environment or secret mechanism and avoid command-line token arguments.

Risk: Images uploaded through the helper become shared in Feishu/Lark according to the target workspace and message context.

Mitigation: Upload only images that are intended to be shared in Feishu/Lark.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/shaniu001/skills/feishu-webhook-skill)
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu image upload documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Feishu file upload documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Feishu user identity documentation](https://open.feishu.cn/document/home/user-identity-introduction/open-id)
- [VChart configuration documentation](https://www.visactor.io/vchart/option/barChart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send webhook requests or upload selected images when configured with a webhook URL and Feishu tenant access token.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
