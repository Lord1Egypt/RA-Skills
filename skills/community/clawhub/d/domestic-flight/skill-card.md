## Description:

国内航班实时查询，支持直飞和中转筛选，价格、时刻、航司信息一查即得，基于途牛数据直连，零配置即装即用。暑期国内航线、热门城市。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query Chinese domestic flight options by route and date, including prices, schedules, airlines, cabin classes, and direct or connecting itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search terms are sent through the skill publisher's hardcoded cloud proxy to access Tuniu data.

Mitigation: Use only when this data flow is acceptable, and avoid entering unrelated sensitive information in flight queries.

Risk: Advertised filtering and sorting features may be limited by the live data returned by the upstream service.

Mitigation: Review returned options and confirm price, inventory, and booking details on the final booking page before acting.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown-style text flight search results with prices, schedules, airline details, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live Tuniu data returned through the publisher's cloud proxy; prices and inventory can change before booking.]

## Skill Version(s):

1.1.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
