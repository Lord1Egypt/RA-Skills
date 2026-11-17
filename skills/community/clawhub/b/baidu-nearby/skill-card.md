## Description:

Baidu Nearby provides Baidu web search, Baidu Map route planning, and nearby place recommendations for location-oriented queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longjf25](https://clawhub.ai/user/longjf25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Baidu, plan routes, and find nearby restaurants, attractions, hotels, shops, transportation, and other places.

### Deployment Geography for Use:

China for map and nearby-place workflows; web search usage depends on Baidu service availability.

## Known Risks and Mitigations:

Risk: Search terms, addresses, coordinates, and the Baidu API key may be sent to Baidu services.

Mitigation: Avoid highly sensitive searches or locations unless external sharing with Baidu is acceptable, and provide credentials through environment variables.

Risk: Route and place recommendations depend on external Baidu service responses and location-service limits.

Mitigation: Review returned routes and place recommendations before relying on them for travel or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longjf25/skills/baidu-nearby)
- [Baidu LBS Open Platform](https://lbsyun.baidu.com/)
- [Baidu LBS API key console](https://lbsyun.baidu.com/apiconsole/key)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Baidu LBS API key for route planning and nearby place search.]

## Skill Version(s):

1.0.4 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
