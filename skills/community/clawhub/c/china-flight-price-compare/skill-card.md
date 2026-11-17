## Description:

途牛+同程+美团+RollingGo五平台直飞航班实时比价，按航班号自动匹配同一航班跨平台报价，一次出结果含预订链接。暑期机票比价、出行省钱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare direct mainland China flight prices across several OTA platforms by departure city, destination city, and travel date. It helps identify lower displayed fares, compare the same flight across platforms, and navigate to a booking site for purchase.

### Deployment Geography for Use:

Mainland China domestic direct-flight searches

## Known Risks and Mitigations:

Risk: Flight search details such as cities and travel date are sent through the skill publisher's Tencent Cloud proxy and onward to OTA flight platforms.

Mitigation: Use the skill only when that data flow is acceptable, and avoid entering unrelated personal or sensitive information in flight-search prompts.

Risk: Displayed fares may be estimates, starting prices, stale, or missing taxes and fees.

Mitigation: Verify the final price, itinerary, and terms on the booking site before purchasing.

Risk: The artifact describes support for direct mainland China flights and excludes transfers, international flights, Hong Kong, Macau, Taiwan, booking status, and check-in.

Mitigation: Use the skill only for supported direct domestic searches and switch to an appropriate travel service for unsupported itineraries or post-booking tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/china-flight-price-compare)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted text with flight options, platform prices, caveats, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fromCity, toCity, and date; optional timePref and sortMode. Displayed prices are estimates and can change before booking.]

## Skill Version(s):

4.2.9 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
