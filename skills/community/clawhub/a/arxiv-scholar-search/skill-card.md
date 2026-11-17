## Description:

Use the arXiv API for academic paper discovery, relevance screening, and structured citation-oriented Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxxxxxxxxxxxxxxxxx20gex](https://clawhub.ai/user/xxxxxxxxxxxxxxxxxxx20gex)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external users use this skill to search arXiv for papers by topic, recency, and result count, then receive structured paper summaries and citation-oriented output based on returned arXiv data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external arXiv API requests for paper searches.

Mitigation: Deploy with expected outbound access to https://export.arxiv.org/api/query and no special local permissions or credentials.

Risk: Returned papers may be incomplete, sparse, or off topic for a user's query.

Mitigation: Use the skill's quality-control loop, retry with broader or rewritten keywords when needed, and mark missing fields explicitly.

Risk: Paper summaries could become misleading if they go beyond returned source metadata or abstracts.

Mitigation: Keep output grounded in arXiv-returned metadata, abstracts, and links; do not fabricate venue, date, links, citation counts, or unsupported conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xxxxxxxxxxxxxxxxxxx20gex/skills/arxiv-scholar-search)
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown paper list with headings, paper metadata, source links, research summaries, and contribution bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is constrained to arXiv-returned metadata, abstracts, links, and explicit missing-field markers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
