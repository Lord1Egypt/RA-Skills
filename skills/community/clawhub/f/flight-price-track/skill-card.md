## Description: <br>
机票降价监控与多平台比价助手，同时搜索多个旅游平台实时价格帮你比价省钱，支持按航线搜索航班、指定航班号多平台精确比价、低价日历查看最佳出发日、创建降价监控任务，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to compare flight prices across multiple travel platforms, assess current fare levels, scan flexible-date low-price calendars, and prepare price-watch requests for selected routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search parameters are sent to remote proxy services to retrieve live travel-platform prices. <br>
Mitigation: Avoid entering sensitive travel details unless the user is comfortable sending those route and date queries to the proxy service. <br>
Risk: The security guidance notes an embedded proxy token and recommends publisher-side token rotation. <br>
Mitigation: Check that the publisher has moved the token to a scoped runtime secret before deployment. <br>
Risk: Real-time flight prices can change and may differ across platforms or booking pages. <br>
Mitigation: Present results as reference information and direct users to verify final price and terms on the booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/flight-price-track) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and structured monitoring request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight searches use route, date, optional flight number, and optional target-price inputs; query results are real-time and should be treated as reference data, not guaranteed prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
