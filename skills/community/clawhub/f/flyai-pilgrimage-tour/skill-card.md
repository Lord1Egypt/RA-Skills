## Description:

Plans film, TV, variety-show, and anime location-pilgrimage trips by finding real filming POIs and assembling routes with flight, hotel, and ticket options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to turn a film, TV show, variety program, or anime title into a bookable itinerary for visiting filming locations, including POIs, route sequencing, transportation, lodging, ticket links, and photo tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or upgrade mutable global npm software, with possible sudo use.

Mitigation: Require explicit user approval before installation, avoid sudo where possible, and verify the package source before running commands.

Risk: The skill suggests disabling TLS verification for booking-related searches.

Mitigation: Do not disable TLS by default; prefer fixing certificate or network issues and only use insecure mode temporarily with explicit user approval.

Risk: The skill can read or store persistent travel profile data, including preferences and family details.

Mitigation: Ask before saving profile data, keep stored details minimal, use protected storage, and provide a clear path to delete or skip persistence.

Risk: The skill surfaces flight, hotel, attraction, and ticket booking links.

Mitigation: Verify each booking link, provider, price, itinerary, and payment page in a trusted browser session before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-pilgrimage-tour)
- [AI Search reference](reference/ai-search.md)
- [Keyword Search reference](reference/keyword-search.md)
- [POI / Attraction Search reference](reference/search-poi.md)
- [Flight Search reference](reference/search-flight.md)
- [Train Search reference](reference/search-train.md)
- [Hotel Search reference](reference/search-hotel.md)
- [Marriott Hotel Search reference](reference/search-marriott-hotel.md)
- [Marriott Package Search reference](reference/search-marriott-package.md)
- [User Profile Storage reference](reference/user-profile-storage.md)
- [Example Dialogues](reference/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown itinerary with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FlyAI booking URLs, POI details, transport and hotel options, and optional user-profile memory updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
