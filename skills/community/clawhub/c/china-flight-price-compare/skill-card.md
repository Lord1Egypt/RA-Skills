## Description: <br>
零配置即装即用｜5源实时比价一次出结果｜含预订链接和航班对比｜覆盖经济舱至头等舱 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to compare direct mainland China flight prices for a specified route and date across multiple booking platforms, then review schedules, source prices, and booking links. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Itinerary details are sent through the publisher's cloud proxy before results are returned. <br>
Mitigation: Use the skill only when sharing departure city, destination city, and travel date with the publisher's proxy is acceptable. <br>
Risk: Booking links and tie-breaking may prefer commission-linked sources when prices are equal. <br>
Mitigation: Treat booking links as convenience links and compare the final fare, taxes, fees, and terms on the booking platform before purchase. <br>
Risk: Flight prices and platform availability can change after the comparison is generated. <br>
Mitigation: Verify current price and availability on the booking page before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/china-flight-price-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown flight comparison summary with prices, schedules, source labels, warnings, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires departure city, destination city, and travel date; returns direct-flight comparisons only.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence and artifact version file) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
