## Description: <br>
抖音公开数据智能获取工具。支持抖音关键词搜索、抖人作品抓取、获取作品评论、实时热榜跟踪，适用于短视频营销、竞品分析、舆情分析和热点监控，助力爆款内容策划与流量追踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and analysis teams use this skill to retrieve public Douyin search results, creator posts, comments, and hot-list data for content planning, competitor analysis, public-opinion analysis, and trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin search terms, profile or video URLs, request limits, and GUAIKEI_API_TOKEN are sent to the guaikei.com API. <br>
Mitigation: Use the skill only for workflows where sending those values to the third-party API is acceptable, and store the token in an environment variable rather than in prompts or files. <br>
Risk: Collected public comments, account data, and search results are saved as local JSON logs. <br>
Mitigation: Review, restrict, or delete generated log files when the collected data is sensitive for the workflow. <br>
Risk: The skill is limited to public Douyin data and does not support private or hidden content. <br>
Mitigation: Use it only for public-data retrieval tasks and avoid relying on it for private-account monitoring or complete coverage claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/douyin-search-keyword) <br>
- [Publisher profile](https://clawhub.ai/user/um-why) <br>
- [Options reference](references/options.md) <br>
- [Changelog](references/changelog.md) <br>
- [Search input schema](assets/search_cli_req.schema.json) <br>
- [Search output schema](assets/search_cli_resp.schema.json) <br>
- [Post input schema](assets/post_cli_req.schema.json) <br>
- [Post output schema](assets/post_cli_resp.schema.json) <br>
- [Comment input schema](assets/comment_cli_req.schema.json) <br>
- [Comment output schema](assets/comment_cli_resp.schema.json) <br>
- [Hot-list output schema](assets/hot_cli_resp.schema.json) <br>
- [Token and support site](https://www.guaikei.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; runtime output is structured JSON saved to local log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command outputs are constrained by the documented request and response schemas.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata, SKILL.md frontmatter, package.json, changelog released 2026-06-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
