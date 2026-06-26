## Description: <br>
同程程心 Skill - 基于同程旅行大模型（程心）的在线旅游搜索能力。提供更专业的机票、火车票、酒店、度假产品（自由行/跟团游）、旅游攻略、行程规划、特价机票、汽车票、长途汽车、景区、门票等的查询能力，基于同程官方数据，更加实时准确可靠，一键进入预订页面，让旅行更简单，更快乐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongcheng-ai](https://clawhub.ai/user/tongcheng-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-assistant agents use this skill to search live Tongcheng travel resources for flights, trains, hotels, bus tickets, attractions, travel products, routes, and itinerary planning, then present result details and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Chengxin API key. <br>
Mitigation: Store CHENGXIN_API_KEY in a secure environment-variable setting and avoid pasting keys into ordinary chat. <br>
Risk: Travel details in user queries are sent to Tongcheng’s API to retrieve live results. <br>
Mitigation: Tell users when live travel searches require sending trip details to Tongcheng and avoid submitting unnecessary sensitive details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tongcheng-ai/chengxin) <br>
- [Publisher profile](https://clawhub.ai/user/tongcheng-ai) <br>
- [Tongcheng homepage](https://www.ly.com) <br>
- [Configuration guide](references/config.md) <br>
- [API examples](references/api-examples.md) <br>
- [Error handling guide](references/error-handling.md) <br>
- [Output format reference](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text travel search results with booking links, plus shell command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses channel and surface options to choose table, card, Markdown-link, or plain-link output.] <br>

## Skill Version(s): <br>
0.9.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
