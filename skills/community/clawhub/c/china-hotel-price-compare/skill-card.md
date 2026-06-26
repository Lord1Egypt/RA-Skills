## Description: <br>
Helps users browse hotels in Chinese cities and compare a selected hotel across five travel platforms, returning current price options with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to browse hotel options by city, date, area, landmark, budget, or score, then compare a selected hotel across multiple China-focused OTA platforms before booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel searches, dates, destination details, and selected hotel names are sent through the publisher's Tencent Cloud proxy and then to travel platforms. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering sensitive travel details unless the publisher and platform data handling are suitable for the use case. <br>
Risk: When prices are tied, the skill discloses that it prefers commission-earning platforms. <br>
Mitigation: Compare the final booking page yourself before purchasing, especially when multiple platforms show the same or similar prices. <br>
Risk: Hotel prices and availability change in real time, some platforms may time out, and Meituan results may be starting prices rather than date-specific totals. <br>
Mitigation: Confirm the final date, room type, fees, cancellation terms, and total price on the booking platform before relying on a result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/china-hotel-price-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with hotel lists, prices, booking links, comparison notes, and follow-up suggestions.] <br>
**Output Parameters:** [1D; accepts a required city plus optional check-in date, check-out date, keyword, selected hotel name, maximum price, point of interest, and minimum score.] <br>
**Other Properties Related to Output:** [Outputs are based on live platform responses and may include warnings when prices differ across platforms or when fewer than five platforms return data.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
