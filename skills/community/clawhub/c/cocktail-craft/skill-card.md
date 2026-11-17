## Description:

Cocktail Craft helps agents answer cocktail recipe, history, technique, ingredient preparation, glassware, garnish, ice, and recipe-design questions using bundled cocktail reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makishimatouri](https://clawhub.ai/user/makishimatouri)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving legal-age cocktail enthusiasts, bartenders, and recipe developers use this skill to retrieve sourced cocktail recipes and design or validate drink concepts with precise measures, preparation steps, and presentation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install instructions may fetch a changed main-branch archive or repository state.

Mitigation: Pin and verify the exact revision before installing or deploying the skill.

Risk: Cocktail preparation guidance may involve high-proof alcohol, heat, pressure equipment, allergens, or sensitive botanicals.

Mitigation: Apply local safety checks before following preparation steps and avoid treating the skill as professional food-safety or medical advice.

Risk: Alcohol-related guidance may be inappropriate for underage users or restricted jurisdictions.

Mitigation: Limit use to legal-age users and follow applicable local alcohol laws and service policies.

Risk: Recipe content can be incomplete, dated, or unsuitable for a specific bar setup or dietary need.

Mitigation: Review sourced recipes, ingredient substitutions, batch scaling, and allergen implications before service.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/makishimatouri/skills/cocktail-craft)
- [Skill definition](SKILL.md)
- [IBA cocktail recipes JSON](references/iba-cocktails.json)
- [IBA cocktail recipes CSV](references/iba-cocktails-web.csv)
- [Cocktail classics](references/cocktail-classics.md)
- [Recipe design methodology](references/recipe-design.md)
- [Advanced techniques](references/techniques.md)
- [Homemade ingredients](references/homemade-ingredients.md)
- [Glassware, garnish, and ice](references/glassware-garnish-ice.md)
- [Brand recipe library](references/brand-recipes.md)
- [Famous bar signatures](references/famous-bar-signatures.md)
- [Competition recipes](references/competition-recipes.md)
- [Online cocktail sources](references/online-sources.md)
- [Web cocktail database](references/web-cocktail-db.md)
- [Top bars overview](references/top-bars.md)
- [Difford's Guide Bacardi Legacy winning cocktails](https://www.diffordsguide.com/competition/1082/bacardi-legacy-global/winning-cocktails)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with recipe measurements, preparation steps, source notes, and validation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No credentialed tools, MCP servers, or API calls were detected; responses should include legal-age, food-safety, allergen, and alcohol-safety caveats when relevant.]

## Skill Version(s):

1.0.0 (source: evidence release version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
