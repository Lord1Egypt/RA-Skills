## Description: <br>
面向 AI 从业者的深度洞察解读技能，适用于周报分析、重点事件深读、主题演进复盘等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiqizhixin](https://clawhub.ai/user/jiqizhixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI industry analysts, product teams, and strategy researchers use this skill to search Jiqizhixin AI insight records, fetch full detail entries, and produce source-grounded weekly reviews, event deep dives, topic retrospectives, and business implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends AI-industry search terms and detail requests to the disclosed Jiqizhixin service. <br>
Mitigation: Avoid confidential query terms and use the skill only when that external API use is acceptable. <br>
Risk: The skill requires a JQZX_API_TOKEN for API access. <br>
Mitigation: Use a revocable token, store it in the environment, and rotate or revoke it if exposure is suspected. <br>
Risk: The scripts allow BASE_URL to be overridden. <br>
Mitigation: Verify BASE_URL is the intended provider endpoint before running the scripts. <br>


## Reference(s): <br>
- [/api/v1 洞察接口策略](references/api-v1-insights.md) <br>
- [检索关键词近义词表](references/keyword_reference.md) <br>
- [Jiqizhixin Data Service](https://www.jiqizhixin.com/data-service) <br>
- [Jiqizhixin MCP API endpoint](https://mcp.applications.jiqizhixin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with source-grounded findings and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the JQZX_API_TOKEN environment variable to query the disclosed Jiqizhixin API.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
