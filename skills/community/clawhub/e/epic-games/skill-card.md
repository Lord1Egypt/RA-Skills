## Description: <br>
Fetch current and upcoming free games from Epic Games Store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheerwhy](https://clawhub.ai/user/cheerwhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve Epic Games Store's current and upcoming free base-game promotions, then present titles, store links, and localized claim periods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Epic Games' public API and sends locale and country values. <br>
Mitigation: Use only user-selected or default locale and country values, and do not send credentials or account data. <br>
Risk: Regional catalog restrictions can make returned listings incomplete or different from the user's local store. <br>
Mitigation: State the locale and country used for the query and prefer the user's region unless they request a broader catalog. <br>


## Reference(s): <br>
- [Epic Games Store free games promotions API](https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale={locale}&country={country}&allowCountries={country}) <br>
- [Epic Games Store product page URL format](https://store.epicgames.com/{locale}/p/{pageSlug}) <br>
- [ClawHub skill page](https://clawhub.ai/cheerwhy/epic-games) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with game titles, store links, and localized claim periods] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups results into currently free and upcoming free base games; excludes non-base-game offers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
