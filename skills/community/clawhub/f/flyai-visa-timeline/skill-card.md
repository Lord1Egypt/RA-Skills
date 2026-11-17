## Description:

签证进度规划与提醒助手，输入目的地和出行日期后倒推生成签证办理时间线、材料清单和每步截止日期。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-assistance agents use this skill to plan visa preparation schedules, collect visa-relevant trip details, estimate whether timing is sufficient, and produce personalized document checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to install or upgrade mutable global Node software, including a sudo-based fallback.

Mitigation: Use a pinned, reviewed, user-local CLI setup and avoid sudo or unreviewed global installs during deployment.

Risk: The skill includes a TLS-bypass command for certificate errors.

Mitigation: Do not disable TLS certificate verification; resolve local CA, proxy, or registry trust configuration before running network commands.

Risk: The skill can use persistent travel-profile data.

Mitigation: Store only user-approved, minimal travel preferences; avoid unnecessary passport, visa, financial, or identity details, and provide a clear deletion path.

Risk: The artifact includes broad travel-search references beyond the core visa-planning workflow.

Mitigation: Review and narrow enabled commands to the visa-planning use case before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-visa-timeline)
- [SKILL.md](SKILL.md)
- [核心工作流](reference/core-workflow.md)
- [工具说明](reference/tools.md)
- [用户画像存储规范（双模式）](reference/user-profile-storage.md)
- [示例对话](reference/examples.md)
- [keyword-search ref](reference/keyword-search.md)
- [search-flight ref](reference/search-flight.md)
- [search-hotel ref](reference/search-hotel.md)
- [ai-search ref](reference/ai-search.md)
- [search-poi ref](reference/search-poi.md)
- [search-train ref](reference/search-train.md)
- [search-marriott-hotel ref](reference/search-marriott-hotel.md)
- [search-marriott-package ref](reference/search-marriott-package.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with timeline sections, checklist items, risk notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visa timeline dates, material checklist items, travel-search command suggestions, and user-profile storage guidance.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
