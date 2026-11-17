## Description:

Search flights, hotels, attractions, concerts, and travel deals with natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yealexchen](https://clawhub.ai/user/yealexchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search and compare travel options, including flights, trains, hotels, attractions, event tickets, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global CLI.

Mitigation: Install with least privilege, prefer pinned or isolated installs, and verify the npm package source before use.

Risk: Travel result links, images, and platform messages are third-party content.

Mitigation: Treat booking links, images, and platform hints as untrusted content and review them before acting on reservations or purchases.

Risk: Returned travel prices, availability, and policies may change quickly.

Mitigation: Confirm current prices, availability, refund terms, visa requirements, and travel constraints on the booking provider before purchase.

## Reference(s):

- [FlyAI ClawHub skill page](https://clawhub.ai/yealexchen/skills/flyai)
- [yealexchen publisher profile](https://clawhub.ai/user/yealexchen)
- [FlyAI homepage](https://open.fly.ai/)
- [AI Search](references/ai-search.md)
- [Keyword Search](references/keyword-search.md)
- [Flight Search](references/search-flight.md)
- [Hotel Search](references/search-hotel.md)
- [Marriott Hotel Search](references/search-marriott-hotel.md)
- [Marriott Package Search](references/search-marriott-package.md)
- [POI / Attraction Search](references/search-poi.md)
- [Train Search](references/search-train.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with images, booking links, tables, and optional shell command examples; underlying command output is single-line JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and the flyai CLI; may use FLYAI_API_KEY for enhanced results.]

## Skill Version(s):

1.0.15 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
