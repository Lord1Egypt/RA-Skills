## Description:

目的地PK对比助手，帮助纠结于多个目的地的用户快速做出决策。输入2-3个候选目的地、出发城市、出行日期，自动生成机票、酒店、景点的多维度对比卡片。当用户提到"选哪个目的地"、"XX还是XX"、"纠结去哪"、"对比目的地"、"PK"时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare 2-3 candidate destinations by flight, hotel, attraction, estimated cost, and preference fit before choosing where to go.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable command-line software globally and includes a sudo fallback.

Mitigation: Review before installing; prefer a pinned, verified, unprivileged FlyAI CLI installation and do not run the sudo install path unless explicitly approved.

Risk: The skill suggests disabling TLS certificate verification when certificate errors occur.

Mitigation: Do not disable TLS certificate checks; resolve local certificate or network trust issues before running travel-search commands.

Risk: The skill can read and persist travel-profile data in memory or ~/.flyai/user-profile.md.

Mitigation: Save profile data only after user confirmation, avoid sensitive details, and inspect or delete ~/.flyai/user-profile.md if persistent travel-profile data is not desired.

Risk: Travel prices, availability, and recommendations may be incomplete or time-sensitive.

Mitigation: Treat generated comparisons as decision support and verify final prices, routes, hotels, and booking terms before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-destination-pk)
- [Core workflow](reference/core-workflow.md)
- [Tools](reference/tools.md)
- [Flight search](reference/search-flight.md)
- [Hotel search](reference/search-hotel.md)
- [POI / attraction search](reference/search-poi.md)
- [Keyword search](reference/keyword-search.md)
- [User profile storage](reference/user-profile-storage.md)
- [Examples](reference/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown destination comparison card with optional FlyAI CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current FlyAI search results and may read or save travel-profile preferences when supported and confirmed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
