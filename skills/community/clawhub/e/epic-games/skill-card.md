## Description:

Fetch current and upcoming free games from Epic Games Store when users ask about Epic giveaways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheerwhy](https://clawhub.ai/user/cheerwhy)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to retrieve and summarize current or upcoming Epic Games Store free-game offers, including titles, store links, and claim periods adjusted to the user's locale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent makes unauthenticated network requests to Epic's public store API.

Mitigation: Review network access expectations before installation and use only public, non-credentialed Epic Games Store requests.

Risk: Locale and country defaults may produce results that do not match the user's preferred region.

Mitigation: Ask for or provide the desired locale and country when region-specific results matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheerwhy/skills/epic-games)
- [Epic Games Store free games promotions API](https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale={locale}&country={country}&allowCountries={country})
- [Epic Games Store product link format](https://store.epicgames.com/{locale}/p/{pageSlug})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with grouped game listings and store links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes game title, claim period converted to local time, and current or upcoming free status.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
