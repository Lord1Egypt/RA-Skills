## Description:

Enhances memory search by combining co-occurrence graph analysis and semantic similarity for improved contextual relevance and ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system integrators use this skill to add context-aware ranking to memory search workflows by combining text matches, co-occurrence relationships, and semantic similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parts of search queries may be stored in the co-occurrence system.

Mitigation: Review before installing in environments with sensitive memory contents, and require query redaction and retention limits where sensitive data may be searched.

Risk: Adapter code is loaded from a hard-coded local workspace path outside the reviewed package.

Mitigation: Install only when the adapter directory is trusted and controlled, or require packaged or integrity-checked dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/enhanced-search-service)
- [Publisher profile](https://clawhub.ai/user/whoisme007)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown and Python examples with configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces enhanced search result fields such as enhanced score, component scores, memory ID, and explanation when used in code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
