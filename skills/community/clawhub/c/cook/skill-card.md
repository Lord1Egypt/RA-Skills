## Description:

Recipe search skill that searches a curated recipe database from 101 Cookbooks and Omnivore's Cookbook for recipes, ingredients, cuisines, and cooking techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find recipe and cooking-guide links by ingredient, cuisine, recipe category, source, or cooking technique.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled recipe index is built from third-party recipe sites and returns links to those sites.

Mitigation: Verify attribution, reuse rights, and source-site terms before republishing, expanding, or redistributing the dataset.

Risk: Recipe and cooking-guide matches may be incomplete or stale because they come from a static bundled Markdown database.

Mitigation: Review matched source links before relying on a recipe and refresh the database when adding or updating recipe sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goog/skills/cook)
- [Publisher Profile](https://clawhub.ai/user/goog)
- [101 Cookbooks Vegetarian Recipes](https://www.101cookbooks.com/vegetarian_recipes)
- [Omnivore's Cookbook How-Tos](https://omnivorescookbook.com/category/how-tos/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown recipe and guide results with links, brief descriptions, source labels, and category groupings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows the top 8 relevant matches for large result sets and can offer additional matches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
