## Description: <br>
Generates a city check-in itinerary by searching popular attractions, cafes, bookstores, landmarks, and food areas, then organizing the results into a shareable Amap map QR code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to turn a city name, theme, or district into a categorized check-in list with Amap points of interest and a QR code for navigation and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers may cause the skill to activate when a user casually mentions a city. <br>
Mitigation: Use the skill only when the user clearly asks for a city check-in map or itinerary, and review generated shareable artifacts before distribution. <br>
Risk: The skill requires an Amap API key. <br>
Mitigation: Store AMAP_API_KEY in the host environment and avoid exposing the key in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/770600682-cyber/amap-city-checkin) <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API documentation](https://lbs.amap.com/api/webservice/summary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown check-in list with route suggestions and an Amap QR code reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY and uses Amap Web Service APIs for live point-of-interest data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
