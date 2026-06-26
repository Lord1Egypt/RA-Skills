## Description: <br>
抖音数据查询与工具助手，覆盖视频详情、用户数据、搜索、热榜、创作者工具、星图达人和内容指数等模块。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, creators, and developers use this skill to query Douyin video, user, search, trending, creator, Xingtu KOL, live, and content-index data through MaxHub APIs for data analysis and content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive MaxHub API keys and may handle Douyin session cookies that are equivalent to login credentials. <br>
Mitigation: Protect MAXHUB_API_KEY, avoid primary-account cookies, use a separate test account for cookie-required endpoints, and rotate or revoke cookies after use. <br>
Risk: Broad scraping, protocol utility, device-registration, signature, and high-quality extraction endpoints may create platform-terms or content-rights risk if misused. <br>
Mitigation: Use the skill only for authorized analysis, review applicable platform terms and content rights, and require explicit approval before using high-risk protocol or extraction endpoints. <br>
Risk: Incorrect endpoint paths or guessed parameters can cause failed requests and unreliable results. <br>
Mitigation: Use documented action tables and reference files, especially the recorded full paths and parameter mappings, before making API calls. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/new-ironman/douyin-aggregate-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Video & Content API reference](references/api-video.md) <br>
- [User Data API reference](references/api-user.md) <br>
- [Search API reference](references/api-search.md) <br>
- [Trending & Billboard API reference](references/api-trending.md) <br>
- [Creator API reference](references/api-creator.md) <br>
- [Xingtu API reference](references/api-xingtu.md) <br>
- [Index & Analytics API reference](references/api-index.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; some endpoints may require Douyin session cookies or other sensitive credentials.] <br>

## Skill Version(s): <br>
3.7.1 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
