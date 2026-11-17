## Description:

Multi-source verification with confidence ratings for factual claims, examples, statistics, and research requiring cross-checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marianachow0321](https://clawhub.ai/user/marianachow0321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify factual claims across multiple sources, compare source credibility, resolve contradictions, and present confidence-rated answers with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification queries are sent through OpenClaw's configured web search provider.

Mitigation: Review generated searches before sharing sensitive wording, and install only when the configured provider's data handling is acceptable.

Risk: Broad multilingual trigger terms may activate the skill for some general discovery requests.

Mitigation: Confirm that the task requires fact verification before sending searches or fetching pages.

## Reference(s):

- [Fact Cross Check on ClawHub](https://clawhub.ai/marianachow0321/skills/fact-cross-check)
- [Query Optimization](references/query-optimization.md)
- [Research Patterns](references/research-patterns.md)
- [Source Credibility Tiers](references/source-tiers.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown answer with confidence rating, source links, verification date, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clickable source URLs for cited results and may include downgraded confidence when sources are weak, unavailable, or contradictory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
