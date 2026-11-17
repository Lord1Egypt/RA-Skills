## Description:

CreBee Social Media Gateway helps an agent manage Chinese social media operations through a local HTTP API, including account lookup, multi-platform content publishing, analytics retrieval, audience profile access, and topic or music search across 12 supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-scarlett](https://clawhub.ai/user/ai-scarlett)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to let an agent operate CreBee's gateway for publishing video, image, and article content; checking social account data; retrieving analytics; and reading fan or audience profile information across Chinese social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, schedule, cancel, and upload content through a gateway authenticated by a long-lived bearer token.

Mitigation: Use only a trusted CreBee gateway, protect bearer tokens as account credentials, limit media paths to intended files, and require explicit user approval before publishing, scheduling, canceling, or uploading.

Risk: The skill can retrieve analytics and fan or audience profile data from connected social media accounts.

Mitigation: Require explicit user approval before retrieving profile or analytics data, avoid exposing tokens or analytics in logs and shared transcripts, and apply the account's privacy and platform policy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-scarlett/skills/crebee-social-media-gateway)
- [CreBee website](https://www.crebee.cn)
- [Content publishing guide](references/publishing.md)
- [Douyin API](references/platforms/douyin.md)
- [Bilibili API](references/platforms/bilibili.md)
- [Xiaohongshu API](references/platforms/xiaohongshu.md)
- [Kuaishou API](references/platforms/kuaishou.md)
- [Weibo API](references/platforms/weibo.md)
- [Gongzhonghao API](references/platforms/gongzhonghao.md)
- [Baijiahao API](references/platforms/baijiahao.md)
- [Toutiaohao API](references/platforms/toutiaohao.md)
- [Qiehao API](references/platforms/qiehao.md)
- [Wangyihao API](references/platforms/wangyihao.md)
- [Shipinhao API](references/platforms/shipinhao.md)
- [Zhihu API](references/platforms/zhihu.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local HTTP requests, bearer-token use, media file paths, publishing task IDs, scheduling values, analytics summaries, and platform-specific configuration parameters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
