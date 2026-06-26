## Description: <br>
CreBee-新媒体多平台分发工具 helps an agent manage CreBee-connected Chinese social media accounts, publish video, image, and article content, retrieve analytics and fan profiles, and search topics, events, and music across 12 platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Scarlett](https://clawhub.ai/user/AI-Scarlett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, operators, and agent developers use this skill to automate CreBee-connected social media operations across major Chinese platforms. It supports account lookup, content publishing, scheduled task cancellation, analytics retrieval, fan-profile access, and platform-specific discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or cancel content on live social media accounts. <br>
Mitigation: Require explicit confirmation of the exact accounts, platforms, content, visibility, and timing before any publish or cancel action. <br>
Risk: Bearer tokens, account IDs, local media paths, analytics, comments, revenue, and fan-profile data are sensitive. <br>
Mitigation: Treat these values as confidential, avoid exposing them in prompts or logs, and share only the minimum data needed for the requested workflow. <br>
Risk: The connected CreBee gateway may provide broad account-data and publishing access. <br>
Mitigation: Independently review the local CreBee gateway, configured accounts, and permissions before installation or use. <br>


## Reference(s): <br>
- [CreBee Website](https://www.crebee.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Scarlett/crebee-social-media-gateway) <br>
- [Content Publishing Guide](references/publishing.md) <br>
- [Douyin API](references/platforms/douyin.md) <br>
- [Bilibili API](references/platforms/bilibili.md) <br>
- [Xiaohongshu API](references/platforms/xiaohongshu.md) <br>
- [Kuaishou API](references/platforms/kuaishou.md) <br>
- [Weibo API](references/platforms/weibo.md) <br>
- [WeChat Official Accounts API](references/platforms/gongzhonghao.md) <br>
- [Baijiahao API](references/platforms/baijiahao.md) <br>
- [Toutiaohao API](references/platforms/toutiaohao.md) <br>
- [Qiehao API](references/platforms/qiehao.md) <br>
- [Wangyihao API](references/platforms/wangyihao.md) <br>
- [Shipinhao API](references/platforms/shipinhao.md) <br>
- [Zhihu API](references/platforms/zhihu.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with HTTP examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local CreBee gateway and Bearer token; publish and cancel actions can affect live social media accounts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
