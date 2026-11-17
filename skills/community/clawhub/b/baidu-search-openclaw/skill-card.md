## Description:

使用百度 AI 搜索 API 进行 Web 搜索。优先使用 API 模式，配额不足时自动切换到浏览器模式。支持中文搜索、新闻搜索等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Baidu/Qianfan web searches from an agent workflow, with browser fallback when API mode is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Baidu/Qianfan and may expose sensitive personal, company, or secret data.

Mitigation: Avoid submitting secrets or sensitive data in search queries, and install only where Baidu/Qianfan data sharing is acceptable.

Risk: The skill relies on a Baidu API key stored in the execution environment.

Mitigation: Store BAIDU_API_KEY using the agent platform's secret-management mechanism and limit access to trusted execution contexts.

Risk: The script prints the parsed request body, which can reveal queries in logs.

Mitigation: Remove or suppress request-body debug output in logged or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhongm/skills/baidu-search-openclaw)
- [Baidu Qianfan API key console](https://console.bce.baidu.com/qianfan/ais/console/apiKey)
- [Baidu Qianfan AI Search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [Baidu web search URL format](https://www.baidu.com/s?wd=关键词)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [JSON search results or Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and PYTHONIOENCODING; search terms are sent to Baidu/Qianfan.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
