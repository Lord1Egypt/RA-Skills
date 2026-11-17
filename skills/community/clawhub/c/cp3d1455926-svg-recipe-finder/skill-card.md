## Description:

Recommends recipes from available ingredients and returns Chinese-language recipe details, cooking tips, nutrition information, favorites, and shopping-list responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language cooking queries, recommend dishes from available ingredients, and generate recipe details, nutrition notes, favorites, or shopping lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Favorites and shopping-list items are saved locally in JSON files and may expose low-sensitivity personal food preferences on shared machines.

Mitigation: Avoid storing sensitive dietary or personal notes in the lists, and clear or protect the local files on shared systems.

Risk: Nutrition and recipe suggestions come from bundled recipe data and may be incomplete or unsuitable for specific dietary restrictions.

Mitigation: Review ingredients and nutrition notes before relying on them for health, allergy, or dietary decisions.

## Reference(s):

- [Recipe Finder ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/cp3d1455926-svg-recipe-finder)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Chinese-language Markdown responses with optional local JSON files for favorites and shopping lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled recipe data and may save favorites.json or shopping_list.json beside the script when persistence functions are used.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
