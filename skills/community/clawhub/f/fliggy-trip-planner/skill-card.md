## Description:

智能行程规划师，整合航班、酒店、景点数据，一键生成完整旅行方案。当用户需要规划旅行行程、制定旅游计划、安排度假方案或询问"去哪里玩""怎么安排行程"时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunhanli7](https://clawhub.ai/user/yunhanli7)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan trips from natural-language travel requests, combining flights, hotels, attractions, restaurants, practical tips, and budget estimates into a complete itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global flyai CLI dependency.

Mitigation: Use only in environments where installing and running flyai is acceptable, and require explicit approval or a preinstalled reviewed flyai version.

Risk: Generated prices, schedules, images, and booking links may be incomplete or outdated.

Mitigation: Verify travel data with official airline, hotel, attraction, or booking sources before purchase.

Risk: User-derived travel inputs are used in shell-style flyai commands.

Mitigation: Review command arguments before execution and avoid passing sensitive personal data unless the execution environment and provider are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunhanli7/skills/fliggy-trip-planner)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel itinerary with tables, image links, booking links, budget estimates, and supporting flyai command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel prices, schedules, images, and booking links should be verified against official or booking sources before purchase.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
