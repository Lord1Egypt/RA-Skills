## Description:

帮助旅伴在出发前完成旅行风格匹配测试，识别节奏、住宿、拍照、餐饮和消费偏好差异，并基于 FlyAI 酒店、景点和交通搜索生成调和建议与预订链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare companion travel styles before a trip, surface likely conflicts, and create a concise compatibility report with compromise recommendations. It can use FlyAI search references to include hotels, attractions, flights, trains, packages, images, and booking links when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents use of a TLS certificate verification bypass.

Mitigation: Do not use the TLS-bypass command in normal operation; resolve certificate or network trust issues before running FlyAI commands.

Risk: The workflow recommends global latest-version CLI installation and may suggest sudo for permission problems.

Mitigation: Install the FlyAI CLI only from trusted sources, prefer pinned or reviewed versions, and avoid sudo/global installation unless the environment owner approves it.

Risk: Search outputs can include booking links that may affect purchases or travel plans.

Mitigation: Verify provider, price, itinerary, cancellation terms, and destination details before acting on any booking link.

Risk: Optional profile persistence may store travel preferences and family details in memory or a local plaintext file.

Mitigation: Save profile data only after explicit user consent and review stored data periodically for sensitivity and accuracy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-companion-matcher)
- [Workflow](reference/workflow.md)
- [Compromise strategies](reference/strategies.md)
- [User profile storage](reference/user-profile-storage.md)
- [AI search reference](reference/ai-search.md)
- [Keyword search reference](reference/keyword-search.md)
- [Hotel search reference](reference/search-hotel.md)
- [POI search reference](reference/search-poi.md)
- [Flight search reference](reference/search-flight.md)
- [Train search reference](reference/search-train.md)
- [Marriott hotel search reference](reference/search-marriott-hotel.md)
- [Marriott package search reference](reference/search-marriott-package.md)
- [Examples](reference/examples.md)
- [Self-growth notes](reference/self-growth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional image embeds, booking links, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FlyAI search result summaries, compatibility scores, conflict warnings, travel agreements, and booking URLs when available.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
