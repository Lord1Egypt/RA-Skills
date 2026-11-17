## Description:

机票降价监控与多平台比价助手，搜索多平台实时价格对比，支持航线搜索、指定航班精确比价、低价日历、降价监控，帮你把握最佳购票时机。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to compare flight prices across sources, evaluate whether current fares are attractive, scan flexible travel dates, and prepare price-watch requests for follow-up checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search details such as cities, dates, flight numbers, and target prices are sent to fixed proxy APIs.

Mitigation: Install only when that data flow is acceptable, and scope PROXY_TOKEN to this flight proxy when possible.

Risk: Price-watch output could be mistaken for a locally installed background monitor.

Mitigation: Treat monitor results as a request for the host agent to schedule and review future checks.

Risk: Flight prices and booking links can change after the skill returns results.

Mitigation: Review live booking pages and final prices before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/flight-price-track)
- [travel-skills publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON objects with human-readable flight price analysis, comparison results, calendar summaries, and suggested follow-up commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitor output is a structured request for the host agent to schedule future checks; it is not a local background service installed by the skill.]

## Skill Version(s):

2.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
