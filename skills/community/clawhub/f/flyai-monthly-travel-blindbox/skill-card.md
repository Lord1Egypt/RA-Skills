## Description:

基于用户当前位置，自动推荐三个周边城市作为本月周末出游目的地，筛选天气适宜的周末，并为每个目的地给出简洁的往返交通安排和预订链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[osrange](https://clawhub.ai/user/osrange)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to choose spontaneous weekend travel destinations based on their current city, remaining weekends in the month, weather suitability, transport availability, and nearby points of interest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users or agents to install the FlyAI CLI globally with an unpinned package version.

Mitigation: Pin the FlyAI CLI version and prefer a local or isolated install path before enabling the workflow.

Risk: The artifact suggests using sudo for npm global installation when permissions are insufficient.

Mitigation: Do not use sudo for this travel workflow; use a least-privilege Node environment such as nvm or a project-local dependency.

Risk: Weather forecasts, traffic availability, fares, and booking links can become stale or inaccurate.

Mitigation: Check the latest forecast and the final booking page before travel or purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osrange/skills/flyai-monthly-travel-blindbox)
- [Publisher profile](https://clawhub.ai/user/osrange)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel cards with tables, links, and inline shell commands for FlyAI lookups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs three destination cards with weather notes, round-trip train or flight options, attraction highlights, booking links, and caveats that weather and prices should be checked before travel.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
