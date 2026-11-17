## Description:

多源聚合旅行助手，覆盖行程规划、酒店、机票、火车票、景点门票、品牌酒店、美食推荐和市内交通查询，并整合途牛、TourMind 和高德数据源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan trips and retrieve travel options such as hotels, flights, trains, attraction tickets, restaurants, and city transit routes. It returns search results, itinerary guidance, prices, schedules, ratings, addresses, and booking links when available.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Travel queries, itinerary details, and addresses may be sent through cloud proxy services.

Mitigation: Install only if this data handling is acceptable; avoid entering sensitive travel details and require the maintainer to disclose proxy endpoints and PROXY_TOKEN behavior.

Risk: Security evidence reports an explicit scan-evasion comment and a suspicious verdict.

Mitigation: Require maintainer review, remove the scan-evasion comment, and re-scan before routine use.

Risk: The hotel-detail tool is reported as unavailable.

Mitigation: Use hotel search for hotel information until the detail tool is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/fliggy-travel)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text travel results with prices, schedules, ratings, addresses, route summaries, and links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed results are returned through cloud proxy services; several list-style outputs cap displayed items.]

## Skill Version(s):

1.4.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
