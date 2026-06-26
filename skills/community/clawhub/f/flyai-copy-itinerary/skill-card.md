## Description: <br>
一键抄作业攻略转化助手，把小红书/抖音/携程攻略链接丢进来，AI自动提取行程，调用飞猪填充真实航班、酒店、景点数据，生成可预订的个性化攻略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent skill to turn travel notes, links, screenshots, or text into personalized itineraries with current flight, hotel, attraction, and booking-link data. It is intended for travel planning assistance where users still review prices, availability, and booking choices before purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill suggests running FlyAI commands with NODE_TLS_REJECT_UNAUTHORIZED=0, which weakens HTTPS certificate validation. <br>
Mitigation: Keep normal HTTPS validation enabled unless there is an explicit, temporary, user-approved exception; prefer a pinned, user-level FlyAI CLI install. <br>
Risk: The skill may fetch external travel links and generate booking links based on third-party availability and pricing. <br>
Mitigation: Have the user review source content, prices, availability, and booking destinations before making purchases. <br>
Risk: The skill can save travel preferences such as departure city, budget, companions, and special requirements. <br>
Mitigation: Save preferences only after user confirmation and avoid storing sensitive details beyond what is needed for trip planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-copy-itinerary) <br>
- [Core workflow](reference/core-workflow.md) <br>
- [Tools guide](reference/tools-guide.md) <br>
- [FlyAI command reference](reference/flyai-commands.md) <br>
- [Output templates](reference/output-templates.md) <br>
- [Platform parsing guide](reference/platform-parsing.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Flight search reference](reference/search-flight.md) <br>
- [Hotel search reference](reference/search-hotel.md) <br>
- [POI search reference](reference/search-poi.md) <br>
- [Train search reference](reference/search-train.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown travel itinerary with embedded booking options, validation notes, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated booking links, route alternatives, budget summaries, and user preference updates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
