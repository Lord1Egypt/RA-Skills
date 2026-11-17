## Description:

Reads Feishu documents available in the client environment and sends final Markdown content and media assets to a third-party relay for creation of WeChat Official Account drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to turn Feishu documents they can access, including embedded images and whiteboards, into WeChat Official Account draft articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu document content, embedded media, user identity metadata, subscription tokens, and WeChat AppID/AppSecret are sent to a third-party relay.

Mitigation: Use only after explicit user consent and review the relay's retention, revocation, and credential-handling practices before deployment.

Risk: The workflow can bind a Feishu open_id to a subscription token without making that identity binding visible to the user.

Mitigation: Disclose identity binding and obtain confirmation before linking a user identity to a subscription token.

Risk: A fallback local token file can persist subscription credentials in the working directory.

Mitigation: Use secure secret storage where available, keep the token file out of version control, and remove expired or invalid tokens promptly.

Risk: The image-fetching helper depends on local command-line tools and temporary-file handling while preparing base64 assets.

Mitigation: Preinstall or pin required dependencies and review the helper script's temporary-file handling before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shing19/skills/feishu-wechat-publish)
- [Publisher profile](https://clawhub.ai/user/shing19)
- [Publisher relay publish endpoint](https://feishu.shing19.cc/api/publish)
- [WeChat developer platform](https://developers.weixin.qq.com/platform)
- [WeChat platform setup image](https://image.shing19.cc/skills/feishu-wechat-publish/wechat-platform-setup.png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown responses with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces relay requests that may include Feishu document text, base64 media assets, user identity metadata, subscription tokens, and WeChat configuration values.]

## Skill Version(s):

0.5.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
