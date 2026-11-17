## Description:

在公众号后台创建文章合集。触发场景：创建公众号合集、新建文章合集、在公众号创建一个合集、创建合集。

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External users with access to a WeChat Official Account backend use this skill to guide an agent through creating a new article collection in an authenticated OpenClaw browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates an authenticated WeChat Official Account browser session and can create a real article collection.

Mitigation: Confirm the account context and desired collection name before invocation, and use the documented OpenClaw browser profile.

Risk: Stale account tokens or page references can cause the workflow to fail or act on the wrong browser state.

Mitigation: Retrieve the current token from the WeChat backend home page and use fresh page snapshots before clicking or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/create-wechat-oa-article-collection-infinite)
- [WeChat Official Account backend](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown instructions with ordered workflow steps and operational cautions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated WeChat Official Account browser session; uses the current account token and dynamic page references.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
