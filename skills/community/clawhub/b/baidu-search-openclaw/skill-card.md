## Description: <br>
使用百度 AI 搜索 API 进行 Web 搜索，优先使用 API 模式，配额不足时自动切换到浏览器模式，并支持中文搜索和新闻搜索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Baidu-powered web searches, especially Chinese-language and news searches, through a Baidu Qianfan API key with a browser-search fallback when API access fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu and may include sensitive or regulated information. <br>
Mitigation: Do not submit secrets, tokens, private customer data, or regulated personal information as search queries. <br>
Risk: Use of a Baidu Qianfan API key can consume quota or incur billing. <br>
Mitigation: Use a scoped API key where possible and monitor Qianfan quota and billing before broad deployment. <br>
Risk: The script disables proxy environment handling for its HTTP session. <br>
Mitigation: Review this behavior before use in environments that rely on proxy routing, inspection, or monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhongm/baidu-search-openclaw) <br>
- [Baidu Qianfan API key console](https://console.bce.baidu.com/qianfan/ais/console/apiKey) <br>
- [Baidu Qianfan AI Search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [Baidu web search fallback](https://www.baidu.com/s?wd=关键词) <br>
- [Baidu news search fallback](https://www.baidu.com/s?wd=关键词&tn=news) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON search-result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results omit snippet fields to reduce output size; API mode requires BAIDU_API_KEY and may consume Baidu Qianfan quota.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
