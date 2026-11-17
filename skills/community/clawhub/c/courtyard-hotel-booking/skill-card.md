## Description:

Searches Courtyard by Marriott hotels, returns live prices and booking links, and supports hotel detail and package offer queries across connected travel platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search Courtyard by Marriott hotels, compare prices and hotel details, and obtain booking links or package offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search terms, destinations, and related query details are sent to a configured cloud proxy.

Mitigation: Install only when that data flow is acceptable, and verify PROXY_URL and PROXY_TOKEN are configured for the intended trusted proxy service.

Risk: The skill provides booking links but does not complete reservations directly.

Mitigation: Review booking page details, prices, and policies on the destination travel platform before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/courtyard-hotel-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style text with hotel results, prices, details, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the configured cloud proxy and upstream travel platform responses.]

## Skill Version(s):

1.1.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
