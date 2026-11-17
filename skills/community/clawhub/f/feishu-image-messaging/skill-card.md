## Description:

飞书图片消息收发助手 - 通过飞书 API 发送和接收图片消息，支持本地文件、远程 URL、图文混排。解决飞书官方 API 只提供底层接口、开发者需要自行封装图片上传和消息发送流程的痛点。适用于需要自动化发送图片到飞书群聊或私聊的场景，如：每日简报配图、监控系统截图报警、报表自动推送等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitsudog](https://clawhub.ai/user/kitsudog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to send local or remote images, optionally with text, to Feishu group chats or private conversations through Feishu Open Platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote image input can cause the host to fetch arbitrary URLs and forward the result to Feishu.

Mitigation: Allow only trusted image URLs or local files, and run the skill from a restricted network environment.

Risk: Images or message text may contain sensitive screenshots, personal data, signed links, or confidential files.

Mitigation: Review content before sending and avoid transmitting sensitive or confidential material through the skill.

Risk: Feishu app credentials and short-lived bearer tokens are used by shell scripts.

Mitigation: Use a minimally permissioned Feishu app, keep FEISHU_APP_ID and FEISHU_APP_SECRET out of repositories, and avoid exposing running command environments to other local users.

## Reference(s):

- [Feishu IM API Reference](references/api.md)
- [Feishu Upload Image API](https://open.larksuite.com/document/server-docs/im-v1/image/create)
- [Feishu Download Image API](https://open.larksuite.com/document/server-docs/im-v1/image/get)
- [Feishu Send Message API](https://open.larksuite.com/document/server-docs/im-v1/message/create)
- [Feishu Tenant Access Token API](https://open.larksuite.com/document/server-docs/authentication-management/access-token/tenant_access_token_internal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts return Feishu tenant access tokens, image keys, message IDs, and command-line status or error text.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
