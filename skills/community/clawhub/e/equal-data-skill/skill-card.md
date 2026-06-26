## Description: <br>
Provides agents with API-guided access to Equal Data's China A-share stock datasets, including market data, financial indicators, company fundamentals, institutional holdings, events, announcements, and news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanjiujing](https://clawhub.ai/user/kanjiujing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent query Equal Data for China A-share market, fundamentals, event, institutional holding, fund, index, news, and announcement data. It is suited for data lookup and analysis workflows that need structured financial data rather than general web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Equal Data API key. <br>
Mitigation: Store EQUAL_DATA_API_KEY in an environment variable or approved local configuration and do not commit it to source files or prompts. <br>
Risk: Prompts may include confidential portfolio, client, or proprietary trading context that could be turned into third-party API queries. <br>
Mitigation: Avoid sending confidential trading or client context through the skill unless the Equal Data service is approved for that data. <br>
Risk: The skill depends on a third-party financial data provider. <br>
Mitigation: Install and enable it only when Equal Data is an intended and approved data source for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kanjiujing/equal-data-skill) <br>
- [Equal Data API interface index](reference/数据接口.md) <br>
- [Equal Data website](https://equal-data.com/) <br>
- [Equal Data documentation](https://equaldata.kanjiujing.cn/equal/dist/introduction) <br>
- [equal-data package](https://pypi.org/project/equal-data/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell snippets, configuration examples, and JSON-like API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EQUAL_DATA_API_KEY credential and calls a third-party financial data service.] <br>

## Skill Version(s): <br>
0.0.29 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
