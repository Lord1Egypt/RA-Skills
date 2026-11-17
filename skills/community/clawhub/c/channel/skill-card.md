## Description:

WeChat Official Account Draft Box management tool. Create and manage graphic draft articles via WeChat API, supporting text and images. Automatically extracts the first paragraph as summary. Supports draft creation, listing, publishing, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to create, list, publish, and delete WeChat Official Account draft articles through the WeChat API. It supports text, image upload, automatic cover generation, and summary extraction for draft workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat Official Account credentials and caches access tokens locally.

Mitigation: Use a dedicated secret manager or tightly permissioned environment file, avoid storing AppSecret in shell startup files, and harden or disable local token caching where possible.

Risk: Publish and delete commands can cause irreversible account actions.

Mitigation: Confirm the target media_id and account context before running publish or delete commands, and restrict credentials to accounts where that level of access is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manifoldor/skills/channel)
- [WeChat Official Account API Reference](references/wechat_api.md)
- [WeChat Official Account Overview](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [WeChat Official Platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WECHAT_APPID and WECHAT_APPSECRET environment variables and performs WeChat Official Account API operations against draft, media, publish, and delete endpoints.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
