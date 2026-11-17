## Description:

汽车票班次查询含余票和预订链接，去汽车站交通方式查询（地铁优先）和目的地住宿推荐，多旅游平台数据直连，零配置即装即用。暑期短途汽车出行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to look up China intercity bus schedules, prices, remaining seats, route-to-station transit options, and destination hotel recommendations with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel routes, station locations, and hotel preferences are sent to external proxy and map services.

Mitigation: Use the skill only when this data sharing is acceptable, and avoid including unnecessary personal or sensitive details in travel and lodging queries.

Risk: Ticket availability, prices, traffic, transit operations, and taxi estimates can change after the skill returns results.

Mitigation: Confirm final ticket, transit, hotel, and fare details on the linked booking or map service before making travel decisions.

Risk: Setting PROXY_TOKEN can authorize requests to the proxy integration.

Mitigation: Do not set PROXY_TOKEN unless the deployment is intended to use this specific proxy integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/bus-ticket-query)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with route, ticket, transit, hotel, and booking-link results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include external booking URLs, live availability notes, estimated transit times, estimated taxi costs, and warnings that prices, seats, and transport conditions can change.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
