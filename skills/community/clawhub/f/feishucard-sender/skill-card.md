## Description:

Sends Feishu card messages with support for text and images using the message tool's card parameter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackswan-mohu](https://clawhub.ai/user/blackswan-mohu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Feishu notification cards, including text cards and cards with uploaded images, to configured users or chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret exposure through USER.md, command-line arguments, logs, shell history, or shared agent context.

Mitigation: Use a protected secret mechanism or tightly scoped environment variables, avoid placing secrets in documentation, and rotate any secret that may have been exposed.

Risk: Sensitive image or message content could be uploaded to Feishu through the helper script or sent in card payloads.

Mitigation: Upload or send only approved content and restrict the Feishu app to the minimum required permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackswan-mohu/skills/feishucard-sender)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline JSON card payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu card JSON payloads and image upload commands that require Feishu app credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
