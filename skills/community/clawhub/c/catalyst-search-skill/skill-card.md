## Description:

Catalysis literature search skill. Given a user-provided catalyst topic, reaction type, or material system, retrieve and organize relevant catalysis research papers from the open web (ScienceDirect, arXiv, OpenAlex, Google Scholar, etc.) and output structured literature-review information (literature matrix, supporting conclusions, and validation suggestions).

This skill is ready for commercial/non-commercial use.

## Publisher:

[andypeng09](https://clawhub.ai/user/andypeng09)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, engineers, and agent users use this skill to search catalysis literature for a catalyst topic, reaction type, or material system, then organize relevant papers into a structured literature matrix with supporting conclusions and validation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalysis search topics may be sent to web search or fetch providers.

Mitigation: Do not use confidential, proprietary, or export-controlled research terms unless the agent environment and search providers are approved for that data.

Risk: Search results and abstracts can be incomplete, paywalled, duplicated, or keyword-only matches.

Mitigation: Verify DOI or abstract metadata with WebFetch, deduplicate by DOI or normalized title, and mark unverified or paywalled items clearly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andypeng09/skills/catalyst-search-skill)
- [Project homepage](https://github.com/ANDYPENG09/catalyst-search-skill)
- [Capabilities and boundaries](references/capabilities.md)
- [Reaction-system search essentials](references/reaction_systems.md)
- [Literature matrix template](templates/literature_matrix.md)
- [GB/T 7714 citation template](templates/citation_gb7714.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown literature matrix with supporting conclusions and validation suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WebSearch and WebFetch results; DOI and abstract metadata should be verified and availability labeled.]

## Skill Version(s):

1.0.5 (source: server evidence, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
