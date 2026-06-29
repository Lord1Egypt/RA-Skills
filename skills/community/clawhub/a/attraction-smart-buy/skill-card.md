## Description: <br>
美团、飞猪、途牛三平台景点门票比价，帮用户找到最低价门票和最优购票方案 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search attraction ticket options and compare current prices across Meituan, Fliggy, and Tuniu before choosing a booking link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Attraction names, cities, and related search terms are sent to the skill's proxy service and travel platforms. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering private itinerary details. <br>
Risk: Live platform results, ticket availability, matching, and prices may be incomplete or change after retrieval. <br>
Mitigation: Review booking links and platform details before purchasing tickets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/attraction-smart-buy) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured ticket search results, price comparisons, images, booking links, and notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on live proxy and travel-platform responses for user-supplied city and attraction queries.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
