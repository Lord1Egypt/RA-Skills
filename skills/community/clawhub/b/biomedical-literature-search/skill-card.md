## Description:

Search biomedical literature from PubMed and bioRxiv for research papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and biomedical developers use this skill to find PubMed articles and bioRxiv preprints, retrieve paper metadata, and support literature reviews or topic exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and date or category filters may be sent to PubMed or bioRxiv.

Mitigation: Avoid sensitive unpublished research queries unless this network sharing is acceptable, and document the external API scope before deployment.

Risk: The example API calls do not include request timeouts or HTTP status checks.

Mitigation: Add explicit timeouts, status checks, retry handling, and bounded date ranges before using the workflow in production.

Risk: Biomedical literature results may be incomplete, unavailable, or dependent on upstream API behavior.

Mitigation: Treat results as retrieval aids, verify important findings against source publications, and surface empty or partial results clearly.

## Reference(s):

- [PubMed E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25500/)
- [bioRxiv API](https://api.biorxiv.org/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Text]

**Output Format:** [Markdown with Python code blocks and paper metadata schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paper metadata such as titles, abstracts, authors, DOIs, dates, IDs, categories, and links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
