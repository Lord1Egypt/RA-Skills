## Description: <br>
Search flights, hotels, attractions, trains, Marriott options, and travel deals with natural-language or structured FlyAI CLI commands backed by Fliggy MCP results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yealexchen](https://clawhub.ai/user/yealexchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search and compare travel options, prices, dates, booking links, and itinerary-relevant details across flights, hotels, trains, attractions, event tickets, and travel packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches and bookings can expose sensitive itinerary, account, passport, payment, or other personal details to a third-party travel provider. <br>
Mitigation: Use the minimum necessary travel details, avoid passport or payment data in search prompts, and configure FLYAI_API_KEY only when the provider and local credential handling are trusted. <br>
Risk: Booking links, prices, availability, refund terms, visa details, and platform hints come from external travel services and may change before purchase. <br>
Mitigation: Treat results as decision support and verify final price, availability, policies, and travel requirements on the linked provider page before booking. <br>
Risk: The skill depends on a globally installed npm CLI and optional API credential configuration. <br>
Mitigation: Install the CLI only from a trusted package source, keep it updated or version-pinned for repeatable workflows, and limit API key exposure to the intended environment. <br>


## Reference(s): <br>
- [FlyAI homepage](https://open.fly.ai/) <br>
- [ClawHub skill page](https://clawhub.ai/yealexchen/flyai) <br>
- [keyword-search reference](references/keyword-search.md) <br>
- [ai-search reference](references/ai-search.md) <br>
- [search-flight reference](references/search-flight.md) <br>
- [search-hotel reference](references/search-hotel.md) <br>
- [search-train reference](references/search-train.md) <br>
- [search-poi reference](references/search-poi.md) <br>
- [search-marriott-hotel reference](references/search-marriott-hotel.md) <br>
- [search-marriott-package reference](references/search-marriott-package.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional images, booking links, tables, platform hints, and JSON-backed result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return single-line JSON; final agent responses should surface relevant images, booking links, prices, dates, constraints, and platform hints when present.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
