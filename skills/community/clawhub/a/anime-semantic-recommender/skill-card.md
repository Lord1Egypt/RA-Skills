## Description:

Use for Chinese-first, source-grounded anime recommendations when the user asks for anime similar to something they watched, describes nuanced taste, wants feedback-driven refinement, or cares about story texture, romance dynamics, emotional aftertaste, pacing, relationship patterns, and avoidances rather than only genre tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamiender](https://clawhub.ai/user/kamiender)

### License/Terms of Use:

MIT-0

## Use Case:

Anime viewers and recommendation agents use this skill to turn nuanced Chinese-language taste descriptions, anchor works, and feedback into source-grounded anime recommendations. It is especially useful when relationship dynamics, emotional texture, pacing, avoidances, and post-watch feeling matter more than genre tags alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local CLI, cache, or profile features may store anime history, preference feedback, or possible Bangumi/AniList tokens on the local machine.

Mitigation: Use those optional local features only on machines where local preference data and tokens can be stored appropriately, especially on shared or backed-up systems.

Risk: Anime recommendations can become misleading when release details, adaptation status, or availability are not checked against reliable sources.

Mitigation: Follow the skill's source-grounding workflow and separate verified facts from memory or inference when high-quality sources are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kamiender/skills/anime-semantic-recommender)
- [Project homepage](https://github.com/KAMIENDER/anime-semantic-recommender)
- [Simple methodology](docs/simple-methodology.md)
- [Technical plan](docs/technical-plan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with ranked recommendation lists and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first responses with source-grounding notes when browsing or factual verification is used]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
