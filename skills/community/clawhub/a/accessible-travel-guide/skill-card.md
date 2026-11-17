## Description:

无障碍出行助手，查询景点、酒店和交通相关无障碍设施，覆盖轮椅、视障、听障、婴儿车和老年人5类需求，提供中国热门景区和主流酒店品牌的内置数据与出行建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to look up China-focused accessibility information for attractions, hotel brands, and transport preparation across wheelchair, visual, hearing, stroller, and elderly-travel needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Built-in attraction and hotel accessibility data may be stale or incomplete, especially for temporary closures, maintenance, room availability, or local policy changes.

Mitigation: Treat outputs as planning guidance and verify critical accessibility details directly with the venue, hotel, or transport provider before travel.

Risk: Coverage is China-focused and limited to the attractions and hotel brands included by the publisher.

Mitigation: Show unavailable-result messages clearly and use exact destination, city, or brand names where possible; rely on local sources for destinations outside the covered data.

Risk: Users could mistake accessibility travel suggestions for medical or care advice.

Mitigation: Use the skill for venue and travel-planning information only, and consult medical or care professionals for health-specific travel decisions.

Risk: An optional proxy token and network helper are present but not used by the exposed tools, which may confuse reviewers or installers.

Mitigation: Review the exposed tool behavior during deployment and ask the publisher to remove or document unused network-related code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/accessible-travel-guide)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON strings containing Chinese-language accessibility details, hotel accessibility notes, travel tips, contact details, and availability messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from built-in data and may include facility routes, restroom availability, rental information, discounts, contacts, and verification reminders.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
