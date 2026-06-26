## Description: <br>
帮助 AI 从业者检索、深读和归纳机器之心 AI 行业资讯，支持按主题、公司和时间窗口追踪热点事件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiqizhixin](https://clawhub.ai/user/jiqizhixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI practitioners, analysts, developers, and industry teams use this skill to track current AI news, expand topic keywords, inspect article details, and produce traceable summaries with source article IDs or titles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and article IDs are sent to the Jiqizhixin API. <br>
Mitigation: Avoid confidential company names, research topics, or other sensitive search terms unless sharing them with that API is acceptable. <br>
Risk: The skill requires an API token for article search and detail requests. <br>
Mitigation: Store JQZX_API_TOKEN as a secret environment variable and avoid committing, logging, or printing it. <br>
Risk: Changing BASE_URL could redirect requests to an untrusted endpoint. <br>
Mitigation: Keep BASE_URL pointed at the trusted Jiqizhixin endpoint unless the replacement endpoint has been reviewed. <br>
Risk: Conclusions based only on search-result summaries may be incomplete or misleading. <br>
Mitigation: Fetch article details for representative results and clearly mark uncertainty when sample depth is limited. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiqizhixin/ai-news-radar) <br>
- [Jiqizhixin Data Service](https://www.jiqizhixin.com/data-service) <br>
- [API v1 Articles Reference](references/api-v1-articles.md) <br>
- [Keyword Reference](references/keyword_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with article IDs, titles, date-window notes, and optional shell/API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and JQZX_API_TOKEN; sends search keywords and article IDs to the Jiqizhixin API.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
