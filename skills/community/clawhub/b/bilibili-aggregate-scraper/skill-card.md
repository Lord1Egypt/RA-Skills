## Description:

B站视频、用户、评论、弹幕、直播数据查询助手，支持 App 和 Web 双端 API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and data analysts use this skill to query Bilibili creator, video, comment, danmaku, search, and live data through MaxHub APIs for content analysis and creator evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API requests and credentials to the third-party MaxHub service.

Mitigation: Install only if the service provider is trusted, use scoped credentials where possible, and avoid exposing secrets in prompts or outputs.

Risk: VIP playback flows can request a full Bilibili session cookie.

Mitigation: Avoid using a primary browser cookie; use a disposable or test account and rotate or revoke the session afterward.

Risk: Automatic degradation can route failed calls through non-Bilibili fallback paths.

Mitigation: Review fallback mappings and endpoint parameters before relying on automatic degradation for analysis workflows.

Risk: The README install example uses an unversioned npx command.

Mitigation: Prefer a pinned, trusted installer version for repeatable installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/bilibili-aggregate-scraper)
- [MaxHub API website](https://www.aconfig.cn)
- [Bilibili Data Assistant README](artifact/README.md)
- [Bilibili 数据助手 README](artifact/README_CN.md)
- [User Data API / 用户数据接口](artifact/references/api-user.md)
- [Video Data API / 视频数据接口](artifact/references/api-video.md)
- [Search & Feed API / 搜索与推荐接口](artifact/references/api-search.md)
- [Live & Comment API / 直播与评论接口](artifact/references/api-live.md)
- [Parameter Mappings / 参数映射](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with tables, bullet summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should match the user's language and keep API keys or cookies out of responses.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
