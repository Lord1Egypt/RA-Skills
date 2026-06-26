## Description: <br>
Spoonacular nutrition lookup and meal calorie estimation with USDA fallback, search optimization, cooking modifiers, cross-validation, and image recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiuZX886](https://clawhub.ai/user/LiuZX886) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to convert natural-language food descriptions or food photos into structured nutrition estimates, including calories and macronutrients. It is useful for meal logging, quick calorie lookup, and agent workflows that need Spoonacular-backed nutrition data with USDA fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal descriptions, food photos, and API keys may be processed by configured nutrition APIs and model or sub-agent workflows. <br>
Mitigation: Use only non-sensitive food descriptions and images, provide API keys only in the intended environment variables, and avoid uploading sensitive photos. <br>
Risk: Local caching can retain meal-query history in the configured SQLite cache database. <br>
Mitigation: Set CALORIE_SKILL_CACHE_DB to an approved path and clear or rotate that database when retained query history is not desired. <br>
Risk: Nutrition estimates may be affected by ambiguous inputs, portion assumptions, or uncertain image recognition. <br>
Mitigation: Review returned questions and notes, provide quantities when possible, and verify estimates before relying on them for health or dietary decisions. <br>


## Reference(s): <br>
- [Calorie Lookup on ClawHub](https://clawhub.ai/LiuZX886/calorie-lookup) <br>
- [USDA FoodData Central Quick Reference](references/usda_fdc.md) <br>
- [Spoonacular Food API](https://spoonacular.com/food-api) <br>
- [USDA FoodData Central API](https://api.nal.usda.gov/fdc/v1) <br>
- [USDA Table of Nutrient Retention Factors](https://www.ars.usda.gov/ARSUserFiles/80400525/Data/retn/retn06.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Guidance] <br>
**Output Format:** [JSON with items, totals, questions, and notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include up to two follow-up questions when quantity or unit information is missing.] <br>

## Skill Version(s): <br>
0.3.0 (source: SKILL.md frontmatter, pyproject.toml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
