## Description:

帮助 Agent 为微信公众号撰写 Markdown 内容、应用爆款写作方法和排版主题，并通过微信接口创建草稿或发布文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongdinghuan](https://clawhub.ai/user/gongdinghuan)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and agents managing WeChat Official Accounts use this skill to draft Chinese articles, choose WeChat-ready layouts, prepare images, create drafts, and optionally publish through WeChat APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat App Secret or access tokens could be exposed during setup or API calls.

Mitigation: Store credentials outside source files, avoid logging secrets, and rotate App Secret or access tokens if exposure is suspected.

Risk: A publish action can affect a live WeChat Official Account audience.

Mitigation: Default to draft creation, preview on mobile, and require explicit human approval before calling live publish flows.

Risk: Generated article content, links, images, or formatting may violate platform constraints or editorial requirements.

Mitigation: Review content manually before release, verify source and image rights, and check WeChat limits for title length, body length, image size, external links, and mobile rendering.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gongdinghuan/skills/clawhub-wechat-writing-pro)
- [Artifact README](artifact/README.md)
- [Markdown syntax guide](artifact/knowledge/markdown-syntax-guide.md)
- [Viral writing methodology](artifact/knowledge/viral-writing-methodology.md)
- [WeChat layout theme catalog](artifact/knowledge/theme-catalog.md)
- [WeChat publishing guide](artifact/knowledge/wechat-publishing-guide.md)
- [WeChat Official Account developer documentation](https://developers.weixin.qq.com/doc/offiaccount)
- [Renyandui Markdown theme library](https://md.axiaoxin.com)
- [Markdown reference source](https://blog.axiaoxin.com/post/markdown-guide/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples, JSON payloads, Python and curl snippets, platform constraints, and publication checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft and live publish guidance for WeChat Official Account workflows; final live publishing should require human approval.]

## Skill Version(s):

2.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
