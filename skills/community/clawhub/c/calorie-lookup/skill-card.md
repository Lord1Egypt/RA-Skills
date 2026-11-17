## Description:

Spoonacular nutrition lookup and meal calorie estimation skill with USDA fallback, search optimization, cooking modifiers, optional cross-validation, and food image recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuzx886](https://clawhub.ai/user/liuzx886)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to convert natural-language meal descriptions or food photos into estimated calories and macronutrients. It supports English and non-English food descriptions by decomposing meals into queryable ingredients and returning structured nutrition results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal descriptions and food photos may be sent to external nutrition or model services.

Mitigation: Avoid submitting sensitive photos or health details, and use only approved providers for the deployment context.

Risk: Provider errors may expose API-key or service details in shared chats, logs, or production output.

Mitigation: Use dedicated low-privilege API keys and redact provider error messages before exposing results to users.

Risk: Food-query results are stored in a local SQLite cache.

Mitigation: Place the cache in a controlled location, restrict file access, and clear it when it may contain sensitive meal data.

Risk: Calorie and nutrient values are estimates that depend on ingredient matching, portion conversion, cooking modifiers, and image recognition accuracy.

Mitigation: Show assumptions and confidence notes, ask for clarification when quantities or food identity are uncertain, and avoid treating results as medical advice.

## Reference(s):

- [USDA FoodData Central Quick Reference](references/usda_fdc.md)
- [Spoonacular Food API](https://spoonacular.com/food-api)
- [USDA FoodData Central API](https://api.nal.usda.gov/fdc/v1)
- [USDA Table of Nutrient Retention Factors for Home Cooking](https://www.ars.usda.gov/ARSUserFiles/80400525/Data/retn/retn06.pdf)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON objects containing meal items, nutrient totals, notes, and clarification questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider source IDs, confidence scores, assumptions, and up to two follow-up questions.]

## Skill Version(s):

0.3.0 (source: frontmatter, pyproject.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
