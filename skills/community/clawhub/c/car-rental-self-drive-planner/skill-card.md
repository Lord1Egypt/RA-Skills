## Description:

租车自驾行前准备与合规路线规划助手，生成强视觉HTML卡片页面，覆盖行前清单、各国/地区租车注意事项、安全驾驶合规提醒及自驾路线推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmercy](https://clawhub.ai/user/lmercy)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to prepare rental-car self-drive trip guidance for China domestic or outbound routes, including required inputs, compliance cautions, safety reminders, and mature route suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML pages may include user-supplied trip details.

Mitigation: Escape or sanitize user-supplied values before sharing or hosting generated pages.

Risk: The skill primarily produces Chinese-language rental-car guidance.

Mitigation: Confirm language expectations when using it for non-Chinese users.

Risk: Rental rules, road access, parking, insurance, and route conditions can change by location and time.

Mitigation: Keep the skill's local-law caveats visible and verify details against official traffic rules and the rental contract before travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmercy/skills/car-rental-self-drive-planner)
- [Publisher profile](https://clawhub.ai/user/lmercy)
- [HTML template evidence](artifact/html-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Single-file HTML with inline CSS, typically delivered in Markdown as renderable code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires location and trip duration; asks follow-up questions when either is missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
