## Description:

在微信视频号后台创建视频合集。

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External users and account operators use this skill to guide an agent through creating a video collection in the logged-in WeChat Channels backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs an account-changing action in a logged-in WeChat Channels backend.

Mitigation: Provide the exact collection title and confirm the final Create action before execution to avoid unwanted account clutter.

Risk: The WeChat Channels backend may have multiple tabs or SPA state that makes the active target ambiguous.

Mitigation: Check available tabs and confirm the active WeChat Channels page before entering the title or creating the collection.

## Reference(s):

- [WeChat Channels backend](https://channels.weixin.qq.com/)
- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/create-wechat-channel-collection-infinite)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser-operation guidance for navigating WeChat Channels, managing tabs, filling the collection title, and confirming creation.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter lists 1.0.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
