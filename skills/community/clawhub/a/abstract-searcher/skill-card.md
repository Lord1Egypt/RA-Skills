## Description:

Add abstracts to .bib file entries by searching academic databases (arXiv, Semantic Scholar, CrossRef) with browser fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to enrich BibTeX bibliographies by finding missing abstracts through academic search APIs and browser-based lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bibliography titles, authors, and related metadata may be sent to arXiv, OpenAlex, CrossRef, Semantic Scholar, Google Scholar, and publisher sites.

Mitigation: Use the skill only on bibliographies that may be shared with those services, or restrict network access for confidential, unpublished, or enterprise material.

Risk: The browser fallback can use a normal Chrome profile, including existing login sessions or institutional access.

Mitigation: Run browser fallback in a dedicated browser profile without sensitive sessions unless that access is intentional.

Risk: Fetched abstracts may belong to the wrong paper if title matching is ambiguous.

Mitigation: Review matched titles and generated BibTeX abstracts before relying on or publishing the enriched bibliography.

## Reference(s):

- [Abstract Searcher ClawHub page](https://clawhub.ai/easonc13/skills/abstract-searcher)
- [arXiv API endpoint](http://export.arxiv.org/api/query)
- [Semantic Scholar Graph API search endpoint](https://api.semanticscholar.org/graph/v1/paper/search)
- [Crossref works API endpoint](https://api.crossref.org/works)
- [OpenAlex works API endpoint](https://api.openalex.org/works)
- [Google Scholar](https://scholar.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and modified BibTeX text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces enriched BibTeX entries by adding abstract fields when matching abstracts are found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
