## Description:

Searches and compares Fliggy MCP hotel listings by destination, nearby POI, lodging type, dates, star rating, bed type, sort order, and CNY nightly price cap, returning structured results with images and booking/detail links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuckonit](https://clawhub.ai/user/zuckonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find, compare, and present hotel or lodging options near cities, districts, landmarks, or attractions with practical filters such as dates, room type, rating, and nightly budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed third-party npm CLI that can change outside this artifact.

Mitigation: Prefer a pinned or local CLI install when available, avoid elevated install privileges, and review the package before deployment.

Risk: The CLI may store FLYAI_API_KEY in its configuration.

Mitigation: Treat the key as a secret, avoid logging real credentials, and rotate the key if it is exposed.

Risk: Hotel images and booking/detail links are rendered from provider output without validation.

Mitigation: Verify provider domains and booking details before entering travel, account, or payment information.

## Reference(s):

- [search-hotel reference](references/search-hotel.md)
- [fly.ai homepage](https://open.fly.ai/)
- [ClawHub skill page](https://clawhub.ai/zuckonit/skills/flyai-hotel)
- [ClawHub publisher profile](https://clawhub.ai/user/zuckonit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with hotel comparison tables, image links, booking/detail links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes line-delimited JSON from the flyai search-hotel command and presents selected fields such as mainPic and detailUrl.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
