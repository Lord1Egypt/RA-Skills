## Description: <br>
飞猪旅行 helps agents search Fliggy and Amap-powered travel information for itineraries, hotels, flights, train tickets, attraction tickets, food, local transport, and Marriott hotel options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search travel options, compare prices and schedules, build trip plans, and receive booking links for review outside the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches are sent to external flyai/Fliggy services and may include itinerary details. <br>
Mitigation: Avoid entering highly sensitive travel details unless necessary and install only if this data flow is acceptable. <br>
Risk: Returned booking links lead to external sites where prices, availability, and purchase terms can change. <br>
Mitigation: Review booking pages directly before purchasing and treat returned prices and availability as informational. <br>
Risk: The skill depends on an external CLI and remote travel APIs. <br>
Mitigation: Approve installation deliberately and review results before using them for travel decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/fliggy-travel) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style travel search results with prices, schedules, images, booking links, and trip guidance when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational; booking and payment are completed on external Fliggy app or web pages.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
