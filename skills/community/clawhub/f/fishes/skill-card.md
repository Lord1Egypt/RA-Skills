## Description:

Search 300 Japan fish and seafood recipes from Cookpad by fish type, cooking method, ingredient, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and recipe-focused agents use this skill to find Japanese fish and seafood recipe matches from a local Cookpad-derived dataset. It is useful for searching by English or Japanese fish names, preparation methods, flavors, or recipe categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for general fish or seafood recipe requests even when the user did not ask for Cookpad Japan results.

Mitigation: State that results are scoped to Cookpad Japan fish and seafood recipes, and clarify before relying on the dataset when the user asks for broader recipe coverage.

Risk: Recipe titles are in Japanese while tags are in English, which may make results harder for some users to interpret.

Mitigation: Summarize or translate returned recipe titles when useful, and preserve the Cookpad links for source review.

## Reference(s):

- [Cookpad Japan Fish and Seafood Category](https://cookpad.com/jp/categories/12)
- [ClawHub Skill Page](https://clawhub.ai/goog/skills/fishes)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with Japanese recipe titles, English tags, and Cookpad links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches a local JSON dataset and returns matching recipe entries; no network fetching is indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
