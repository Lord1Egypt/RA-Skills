## Description:

抖音数据查询与工具助手。覆盖视频详情、用户数据、搜索、热榜、创作者工具、星图达人、内容指数等模块。含部分交互触发和协议工具接口（已标注）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and analyze Douyin video, account, search, trending, creator, Xingtu KOL, live, and content-index data through MaxHub APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some endpoints can handle login-equivalent Douyin cookies, proxy values, or device credentials.

Mitigation: Install only if you trust MaxHub/aconfig.cn, avoid providing a primary Douyin account cookie, use a disposable test account for cookie-required endpoints, and revoke cookies after use.

Risk: API requests and queried data are transmitted to a third-party service.

Mitigation: Prefer public and read-only endpoints, avoid sending sensitive data, and review what each endpoint requires before calling it.

Risk: An unpinned installer command can change behavior if the upstream package changes.

Mitigation: Pin the installer or skill version where the deployment process allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/douyin-aggregate-scraper)
- [MaxHub API service](https://www.aconfig.cn)
- [Creator API / 创作者接口](references/api-creator.md)
- [Index & Analytics API / 指数与分析接口](references/api-index.md)
- [Search API / 搜索接口](references/api-search.md)
- [Trending & Billboard API / 热榜与趋势接口](references/api-trending.md)
- [User Data API / 用户数据接口](references/api-user.md)
- [Video & Content API / 视频与内容接口](references/api-video.md)
- [Xingtu API / 星图接口](references/api-xingtu.md)
- [Parameter Mappings / 参数映射](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON API response excerpts from MaxHub/Douyin endpoints.]

## Skill Version(s):

3.7.1 (source: evidence release, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
