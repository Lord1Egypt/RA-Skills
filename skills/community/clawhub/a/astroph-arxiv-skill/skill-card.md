## Description:

Queries arXiv filtering by astro-ph, extracting full abstracts, authors, and PDF links. Embeds the Python script directly into the skill for robust and reproducible XML parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgeanais](https://clawhub.ai/user/jorgeanais)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external users use this skill to search recent astro-ph arXiv papers for a specific topic and return titles, authors, publication dates, full abstracts, and abstract/PDF links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadly worded literature-search requests may trigger an astro-ph arXiv lookup when that was not intended.

Mitigation: Phrase requests clearly when an astro-ph arXiv lookup is or is not desired.

Risk: Using a broad astro-ph category with submitted-date sorting can return older papers instead of recent results.

Mitigation: Use a specific astro-ph subcategory or omit the category filter when the query is already specific.

## Reference(s):

- [arXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with generated paper entries and inline links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to two papers when the user does not specify a result count.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
