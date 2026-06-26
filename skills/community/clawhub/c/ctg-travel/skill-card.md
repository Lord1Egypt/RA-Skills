## Description: <br>
中旅旅行开放平台一站式预订助手。整合机票、酒店、火车票、门票四大资源，支持查询、预订、退款全流程。下载中旅旅行APP获取 API Key。当用户表达出行住宿需求时（如"买火车票""订酒店""查询航班""购买景区门票"），提供智能引导和便捷预订服务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctg-travel](https://clawhub.ai/user/ctg-travel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search, book, review, cancel, and refund flights, hotels, train tickets, and attraction tickets through the CTG travel API after configuring CTG_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist CTG_API_KEY in config/ctgConfig.json. <br>
Mitigation: Provide CTG_API_KEY through a secure environment variable and avoid storing it in the skill configuration file. <br>
Risk: The skill sends passenger names, phone numbers, identity numbers, order details, booking requests, and refund requests to the CTG travel API. <br>
Mitigation: Use the skill only when the user accepts sharing this travel and identity data with the CTG travel API. <br>
Risk: The skill can create bookings, submit refunds, cancel orders, or save passenger identity data with inconsistent confirmation safeguards. <br>
Mitigation: Before any booking, cancellation, passenger-save, or refund action, show the exact itinerary or order, passengers, price or refund amount, and wait for explicit user confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ctg-travel/ctg-travel) <br>
- [CTG Skill Access Guide](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with shell command examples and JSON API arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CTG_API_KEY and may trigger booking, passenger-save, cancellation, or refund API calls after collecting required user details.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
