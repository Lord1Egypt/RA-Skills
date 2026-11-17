## Description:

全自动 AI 电话助手，帮助用户搜索中国和日本餐厅、发起 AI 电话预订、查询预订状态并获取通话记录和电子凭证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallgeding](https://clawhub.ai/user/smallgeding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to collect reservation details, search supported restaurants in China or Japan, place outbound AI phone booking requests through TripNow, and report booking results or vouchers back to the user.

### Deployment Geography for Use:

Global use; restaurant search and booking coverage is limited to supported cities in China and Japan.

## Known Risks and Mitigations:

Risk: The skill handles personal booking data such as names, phone numbers, dining times, restaurant selections, and callback URLs.

Mitigation: Confirm the booking details and callback destination before creating an outbound call, and retain personal data only as needed for the reservation workflow.

Risk: The artifact includes examples that pass an API key in a URL query parameter, which can expose credentials through logs or browser history.

Mitigation: Use Authorization headers for authentication, avoid placing real API keys in query strings, and rotate any key that has been used in a logged URL.

Risk: The skill can trigger outbound AI phone calls to restaurants.

Mitigation: Ask the user to confirm the restaurant, phone number, communication language, dining time, party size, and acceptable time changes before submitting the call task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallgeding/skills/ding-restaurant-reservation)
- [TripNow AI Open Platform](https://tripnowengine.133.cn/tripnow-ai-open-platform/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TripNow order IDs, reservation status, call-record URLs, voucher URLs, and polling or callback handling guidance.]

## Skill Version(s):

1.0.8 (source: server release evidence; artifact text also states v1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
