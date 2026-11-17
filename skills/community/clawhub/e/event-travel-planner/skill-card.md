## Description:

Event Travel Planner helps agents plan travel for concerts, conventions, sports events, and other live events by confirming event details, gathering venue guidance from Xiaohongshu, and searching Fly.ai/Fliggy options for tickets, flights, hotels, and nearby points of interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chgufan](https://clawhub.ai/user/chgufan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan event trips end to end: confirm current event details, compare venue and attendance guidance, find bookable travel products, and produce a practical itinerary with booking links where available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can perform non-interactive dependency installation and make global or persistent CLI changes.

Mitigation: Review the setup script before running it, prefer manual installation with pinned versions, and install only in an environment where persistent CLI changes are acceptable.

Risk: The Xiaohongshu login flow uses account cookies or QR authentication for search and comment access.

Mitigation: Use QR login when possible, never expose raw cookies in chat or logs, and re-authenticate deliberately when cookies expire.

Risk: The skill may present third-party travel search results and booking links for tickets, hotels, flights, or points of interest.

Mitigation: Validate booking links, prices, dates, and provider terms before presenting them as actionable recommendations or clicking through.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chgufan/skills/event-travel-planner)
- [xhs-cli reference](references/xhs_cli.md)
- [flyai-cli reference](references/flyai_cli.md)
- [Setup guide](references/setup_guide.md)
- [xiaohongshu-cli](https://github.com/jackwener/xiaohongshu-cli)
- [Fly.ai console](https://flyai.open.fliggy.com/console)

## Skill Output:

**Output Type(s):** [text, markdown, html, shell commands, configuration, guidance]

**Output Format:** [Markdown travel plan with inline shell commands and an optional HTML itinerary file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include images and booking links from Fly.ai/Fliggy search results when available.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
