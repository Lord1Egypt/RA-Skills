## Description:

Cocktail Boy helps an agent look up cocktail recipes, search drinks by ingredient, and provide random cocktail recommendations from a bundled recipe database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flarecentury](https://clawhub.ai/user/flarecentury)

### License/Terms of Use:


## Use Case:

External users, bartenders, and cocktail enthusiasts can use this skill through an agent to retrieve ingredient lists, preparation guidance, glassware, and recommendations for cocktails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scene-based recommendations and the documented shortcut entrypoint appear incomplete.

Mitigation: Use the supported recipe search, ingredient search, and random recommendation commands, and verify any shortcut or scene workflow before relying on it.

Risk: Search terms containing unusual regex characters may cause errors or confusing matches.

Mitigation: Use plain cocktail or ingredient names for searches and review returned recipes before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flarecentury/skills/cocktail-boy)
- [Publisher Profile](https://clawhub.ai/user/flarecentury)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Bundled Cocktail Recipe CSV](artifact/data/rohan_cocktails.csv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text returned by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipe responses can include drink names, ingredient amounts, preparation methods, glassware, and recommendation summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
