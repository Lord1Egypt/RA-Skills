## Description: <br>
零配置即装即用，支持汽车票班次查询含余票和预订链接、去汽车站交通方式查询（地铁优先）和目的地住宿推荐，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers planning intercity bus trips in China use this skill to query bus schedules, prices, remaining seats, station transit options, and destination hotel recommendations. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Travel search details are sent to the skill publisher's proxy services and downstream travel or map providers. <br>
Mitigation: Avoid entering sensitive home addresses or private itinerary details unless they are needed for the lookup. <br>
Risk: Ticket availability, prices, transit times, and taxi fares can change after the skill returns results. <br>
Mitigation: Confirm details on the final booking page or local transit provider before purchasing tickets or starting travel. <br>
Risk: The skill provides booking links and recommendations but does not directly purchase, refund, or manage tickets. <br>
Mitigation: Complete purchases and any after-sales requests through the linked travel provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/bus-ticket-query) <br>
- [travel-skills publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style text with ticket listings, route guidance, hotel recommendations, estimates, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns real-time or estimated travel information; prices, seat availability, routes, and fares can change.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
