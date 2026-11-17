## Description:

一键抄作业攻略转化助手把小红书、抖音、携程等旅行攻略内容转成可执行行程，并用飞猪/FlyAI 数据补充航班、酒店、景点和预订链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to transform inspiration posts, links, screenshots, pasted text, or rough trip descriptions into personalized itineraries with validated transportation, lodging, attractions, budget notes, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FlyAI commands are documented with TLS certificate verification disabled.

Mitigation: Remove NODE_TLS_REJECT_UNAUTHORIZED=0 and resolve certificate validation before running searches in production or trusted workflows.

Risk: The workflow recommends installing the latest global FlyAI CLI and may suggest sudo when permissions fail.

Mitigation: Review the package before use, prefer a pinned version in a managed environment, and avoid sudo or mutable global installs.

Risk: The skill processes user-provided travel links and emits booking URLs.

Mitigation: Validate source and booking URLs, restrict unsupported domains, and require user confirmation before opening links or making reservations.

Risk: Generated HTML may contain itinerary, source-post, or booking-link content derived from external pages or user input.

Mitigation: Escape dynamic HTML fields and sanitize URLs before writing or sharing generated itinerary files.

Risk: The skill can store travel preferences in memory or a local profile file.

Mitigation: Ask before saving profile data, keep stored fields minimal, and provide clear controls to update or delete the profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-copy-itinerary)
- [Publisher profile](https://clawhub.ai/user/hello-ahang)
- [Core workflow](artifact/reference/core-workflow.md)
- [Tool usage guide](artifact/reference/tools-guide.md)
- [FlyAI command reference](artifact/reference/flyai-commands.md)
- [Platform parsing guide](artifact/reference/platform-parsing.md)
- [Output templates](artifact/reference/output-templates.md)
- [HTML itinerary template](artifact/reference/html-template.md)
- [User profile storage](artifact/reference/user-profile-storage.md)
- [Flight search reference](artifact/reference/search-flight.md)
- [Hotel search reference](artifact/reference/search-hotel.md)
- [POI search reference](artifact/reference/search-poi.md)
- [Train search reference](artifact/reference/search-train.md)
- [Keyword search reference](artifact/reference/keyword-search.md)
- [AI search reference](artifact/reference/ai-search.md)
- [Marriott hotel search reference](artifact/reference/search-marriott-hotel.md)
- [Marriott package search reference](artifact/reference/search-marriott-package.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown itinerary text, FlyAI shell command suggestions, JSON-like tool inputs, and optional HTML itinerary files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking URLs, route comparisons, budget tables, validation status labels, and optional local travel-profile updates.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
