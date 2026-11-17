## Description:

Searches arXiv astro-ph for recent astronomy papers and returns titles, authors, dates, abstracts, and PDF links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgeanais](https://clawhub.ai/user/jorgeanais)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to search recent astronomy literature in arXiv astro-ph and receive formatted paper metadata, full abstracts, and direct links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topics are sent to arXiv when the skill performs a literature query.

Mitigation: Avoid using sensitive or private research topics in queries unless sharing them with arXiv is acceptable.

Risk: The skill creates and runs a local Python helper to fetch and format arXiv results.

Mitigation: Review the generated helper before execution and remove it after use when local file hygiene matters.

Risk: The skill behavior is intended for astro-ph literature searches but may activate for broader literature-search requests.

Mitigation: Use it only for astronomy or astro-ph searches, and prefer more specific arXiv subcategories for recent-result queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jorgeanais/skills/astroph-arxiv-skill-repo)
- [Publisher profile](https://clawhub.ai/user/jorgeanais)
- [arXiv API endpoint](https://export.arxiv.org/api/query)
- [Atom XML namespace](http://www.w3.org/2005/Atom)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-formatted paper results with generated Python parsing code and fetch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to two papers when the user does not specify a result limit; includes highlighted scientific terms in abstracts.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
