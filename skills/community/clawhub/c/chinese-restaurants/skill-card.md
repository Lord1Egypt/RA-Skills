## Description: <br>
Find nearby Chinese restaurants for users who ask for Chinese food near them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an agent for nearby Chinese restaurant options around an authorized location, city, or neighborhood. It supports bounded restaurant lookup with filters such as open status, rating, price level, and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location may expose sensitive user information during restaurant lookup. <br>
Mitigation: Ask for location permission, prefer a city, neighborhood, or approximate location unless precise nearby results are needed, and avoid retaining exact coordinates. <br>
Risk: Restaurant lookup providers may be unavailable, rate limited, or unable to satisfy an excessive radius. <br>
Mitigation: Handle invalid location, excessive radius, provider unavailability, and rate limiting with clear bounded-result behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikeclaw007/chinese-restaurants) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Structured data, Guidance] <br>
**Output Format:** [Markdown or standardized POI list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location, radius, limit, and optional filters; maximum listed result limit is 50.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
