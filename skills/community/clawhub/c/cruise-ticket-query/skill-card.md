## Description: <br>
零配置即装即用，支持长江三峡游轮和城市游船船票查询含价格和预订链接、市内交通到码头查询（地铁优先）、景点门票推荐和住宿推荐，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to look up domestic river cruise tickets, dock transportation, city attractions, and hotel options before booking through linked providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User cruise searches, city names, route addresses, attraction keywords, and hotel preferences are sent to the skill author's proxy services and downstream travel providers. <br>
Mitigation: Avoid entering sensitive personal details in free-form travel queries and review the external data flow before deployment. <br>
Risk: Prices, transport times, availability, and booking terms can change after the skill returns a result. <br>
Mitigation: Verify final prices, schedules, routes, and purchase terms on the linked provider pages before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/cruise-ticket-query) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted travel lookup results with prices, routes, estimates, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on external travel and map provider responses; prices, schedules, routes, and booking availability can change.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
