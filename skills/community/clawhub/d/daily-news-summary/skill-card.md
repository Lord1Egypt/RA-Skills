## Description: <br>
每日新闻总结抓取公开新闻和科技来源，生成包含国际、中国、AI 和科技巨头动态四个板块且附原文链接的中文 Markdown 日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzcnyhhd](https://clawhub.ai/user/mzcnyhhd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to create a daily Chinese briefing from public international, China, AI, and technology-company news sources. It can also help set up an optional recurring daily automation when the user explicitly requests scheduled reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches content from multiple public news sites and RSS feeds. <br>
Mitigation: Review the listed sources before use and expect partial source failures; the artifact instructs the agent to continue with successful sources and preserve original links. <br>
Risk: The skill saves a dated Markdown digest in the workspace root. <br>
Mitigation: Run it only in a workspace where this output location is acceptable, and review the generated report before sharing or relying on it. <br>
Risk: The skill can create recurring daily automation when explicitly requested. <br>
Mitigation: Create scheduled automation only when ongoing reports are desired, and review the WorkBuddy automation settings for how to edit or disable the schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzcnyhhd/daily-news-summary) <br>
- [Publisher profile](https://clawhub.ai/user/mzcnyhhd) <br>
- [News Sources Reference](references/news_sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown report saved as a dated .md file with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language daily digest; optional recurring automation only when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
