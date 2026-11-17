## Description:

Searches academic literature across Semantic Scholar, Crossref, PubMed, and arXiv with filtering, deduplication, sorting, and multiple export formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jibeilindong](https://clawhub.ai/user/jibeilindong)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and agent workflows use this skill to search scholarly databases, filter and rank papers, and return paper metadata and citations in readable or machine-processable formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and returned paper metadata are sent to third-party scholarly services.

Mitigation: Avoid sensitive queries, use your own API credentials where supported, and review the configured data destinations before use.

Risk: Saving results can overwrite local files when save_results and output_file are enabled.

Mitigation: Keep result saving disabled by default or restrict output_file to a confined directory with appropriate filesystem permissions.

Risk: arXiv queries use plaintext HTTP in the artifact.

Mitigation: Prefer changing the arXiv endpoint to HTTPS or disable arXiv searches in sensitive environments until the endpoint is updated.

Risk: Dependencies are specified as minimum versions rather than pinned versions.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jibeilindong/skills/academic-literature-search)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [PubMed API key setup](https://www.ncbi.nlm.nih.gov/account/)
- [Crossref works API endpoint](https://api.crossref.org/works)
- [arXiv API endpoint](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, bibtex, ris, html, excel]

**Output Format:** [Search results with paper metadata, statistics, citations, links, and optional formatted exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include saved result files when save_results and output_file are enabled; default output is Markdown.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
