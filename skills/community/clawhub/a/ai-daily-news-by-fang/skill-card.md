## Description: <br>
AI 技术进展追踪工具：在用户询问近期 AI 动态时，多源检索模型发布、AI 工具迭代、重要技术公告、社区热门项目、论文和新实践，并输出按热度排序、附原文链接的中文摘要列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fangziyang0910](https://clawhub.ai/user/Fangziyang0910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect recent AI technical news into a Chinese daily digest, focused on models, tools, research ideas, and notable community projects while excluding finance, business, and policy items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports are archived locally and sent through Feishu after completion. <br>
Mitigation: Confirm the archive location and replace the placeholder Feishu open_id with the intended recipient before use. <br>
Risk: The workflow depends on a referenced smart-web-fetch helper for web retrieval. <br>
Mitigation: Verify that the helper path resolves to a trusted local tool before running the workflow. <br>
Risk: News collection may include stale, low-signal, or off-scope items if source results are not reviewed. <br>
Mitigation: Apply the documented three-day limit, neutral-title filter, and exclusion of finance, business, and policy items before publishing or sending the digest. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Fangziyang0910/ai-daily-news-by-fang) <br>
- [AI News Sources](references/sources.md) <br>
- [QbitAI](https://www.qbitai.com) <br>
- [Jiqizhixin](https://www.jiqizhixin.com) <br>
- [Hacker News](https://news.ycombinator.com/) <br>
- [OpenAI Blog](https://openai.com/index) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [Claude Code Changelog](https://code.claude.com/docs/en/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown digest with source links, local archive path, and Feishu-ready message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese summaries for items from the last three days and records the write round, item count, and update time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
