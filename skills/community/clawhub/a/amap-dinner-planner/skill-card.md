## Description:

Helps an agent plan group dinners by geocoding participant locations, finding a fair midpoint, recommending nearby restaurants with commute comparisons, and preparing an Amap QR map for sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to coordinate group meals by comparing participant locations, restaurant options, commute times, and shareable Amap navigation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise participant locations may be sent to Amap during geocoding, restaurant search, routing, and map generation.

Mitigation: Use approximate meeting areas or landmarks where possible, and get participant consent before entering exact home or workplace addresses.

Risk: Generated QR maps may expose participant locations and restaurant plans to anyone who receives or forwards the code.

Mitigation: Share QR codes only with intended participants and regenerate or stop using shared map links when plans change.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary)
- [Amap Web Service API Endpoint](https://restapi.amap.com)
- [ClawHub Skill Page](https://clawhub.ai/770600682-cyber/skills/amap-dinner-planner)
- [ClawHub Publisher Profile](https://clawhub.ai/user/770600682-cyber)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with restaurant recommendations, commute comparisons, and QR map details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends participant addresses or approximate locations to Amap Web Service APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
