## Description: <br>
AI 每日简报 - 全球 AI 行业新闻（公司/产品/论文） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeu1688](https://clawhub.ai/user/seeu1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to generate a concise Chinese-language daily brief of major AI company news, leader statements, product launches, and selected research papers from the prior 24 hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tavily and Bocha search API credentials. <br>
Mitigation: Use dedicated, least-privilege API keys and rotate them according to the user's credential policy. <br>
Risk: The skill searches public sources and summarizes current news, which can include outdated, duplicate, or inaccurate items. <br>
Mitigation: Review generated briefs before relying on or redistributing them, and confirm important claims against the linked source material. <br>
Risk: The skill can save or post a daily brief to the configured destination. <br>
Mitigation: Confirm the Feishu or current-session delivery target before enabling scheduled delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seeu1688/ai-daily-xhs) <br>
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown brief with source links and category summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language daily brief covering company news, leader statements, product launches, selected papers, and a category count table.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
