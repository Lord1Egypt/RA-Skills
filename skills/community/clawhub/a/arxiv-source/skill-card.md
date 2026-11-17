## Description:

Read and analyze arXiv papers by fetching LaTeX source, listing sections, or extracting abstracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willamhou](https://clawhub.ai/user/willamhou)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and agents use this skill to retrieve public arXiv paper source, inspect paper structure, and extract abstracts for literature review or technical analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes read-only network requests to public arXiv endpoints for paper IDs supplied by the user.

Mitigation: Use it only for paper identifiers that are appropriate to disclose to public arXiv services.

Risk: Large papers or unavailable source packages may be slow or fail to fetch.

Mitigation: Start with abstract or section-list requests, then fetch full source only when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willamhou/skills/arxiv-source)
- [Publisher Profile](https://clawhub.ai/user/willamhou)
- [arXiv](https://arxiv.org)
- [arXiv Export Endpoint](https://export.arxiv.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or JSON-like tool results containing paper content, section lists, abstracts, arXiv IDs, and cache status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return in-memory cached results for repeated requests during the same session.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
